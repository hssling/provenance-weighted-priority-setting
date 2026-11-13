"""Build the per-journal submission set from the two manuscript sources.

Everything here is derived, never hand-maintained, so a correction to a
manuscript cannot leave a stale blinded copy or a wrong word count behind.
That failure mode has already cost this project once: a cover letter claimed
400 dpi for 600 dpi figures because the number was typed, not derived.

Writes manuscript/submission/paper_{a,b}/03_manuscript_blinded.md and prints
the counts the title pages must state.

If pandoc is on PATH it also writes a .docx beside every .md in the
submission folders, because neither target journal accepts Markdown. Without
pandoc it says so and writes the Markdown only; the build still succeeds, so
the counts and the blinding never depend on a tool being installed.

Usage: python -I manuscript/build_submission.py
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from submission_layout import LAYOUT  # noqa: E402
OUT = HERE / "submission"

PAPERS = {
    "paper_a": ("manuscript_draft_v1.md", "## 1. Introduction"),
    "paper_b": ("manuscript_b_draft_v1.md", "## 1. Background"),
}

# Lines identifying the author. Removed from the blinded copy; each must be
# found, or the blinding is silently incomplete.
IDENTIFYING = [
    r"^\*\*Author:\*\*.*$",
    r"^Department of Community Medicine.*$",
    r"^Correspondence:.*$",
    r"^\*\*Target journal:\*\*.*$",
]


def count_words(text: str) -> int:
    """Main-text words as both journals define them: tables are excluded, and
    a table's caption and the note beneath it are part of the table. Section
    headings are kept, which errs on the side of over-counting."""
    text = re.sub(r"^\|.*$", "", text, flags=re.M)                  # table rows
    text = re.sub(r"^\*\*Table \d+\..*$", "", text, flags=re.M)     # captions
    text = re.sub(r"^\[Table \d+ about here\]$", "", text, flags=re.M)
    text = re.sub(r"\*\*|`|#", "", text)
    return len(text.split())


def section(text: str, start: str, end: str) -> str:
    i, j = text.index(start), text.index(end)
    return text[i + len(start):j]


def blind(text: str) -> tuple[str, int]:
    removed = 0
    for pat in IDENTIFYING:
        text, n = re.subn(pat, "", text, flags=re.M)
        if n == 0:
            raise SystemExit(f"blinding pattern never matched: {pat}")
        removed += n
    # the author's own working notes never go to a journal
    i = text.find("## Notes for the author")
    if i != -1:
        text = text[:i].rstrip() + "\n"
    # Self-citations that name the author. Paper A uses Health Policy and
    # Planning's author-date style, so the surname also appears bare, as in
    # "(Siddalingaiah 2026a)" and "Siddalingaiah (2026a, under review)". Both
    # journals reviewing these papers are double-anonymized, so the surname
    # must go in every form it takes.
    text = re.sub(r"Siddalingaiah(?: HS?)?\.?", "[Author]", text)
    # The deposit identifiers de-anonymise the submission: the repository URL
    # carries the author's username, and resolving the DOI shows the author
    # record. A journal reviewing blind expects these to be withheld and given
    # to the editor instead. The unblinded source keeps them in full.
    # Only the author's own repository: WHO's data collection form is also on
    # GitHub (GTB-TME/gtbreport2026), and a pattern matching any github.com
    # URL blanked that reference in the blinded copy.
    text = re.sub(r"https://github\.com/hssling/[A-Za-z0-9_.-]+",
                  "[repository URL withheld for blind review]", text)
    text = re.sub(r"doi:10\.5281/zenodo\.[0-9]+",
                  "[archive DOI withheld for blind review]", text)
    # tidy what those substitutions leave behind
    text = text.replace("[repository URL withheld for blind review] and archived at Zenodo, "
                        "[archive DOI withheld for blind review]",
                        "[repository and archive DOI withheld for blind review]")
    text = re.sub(r" \(release v[0-9.]+; the concept DOI "
                  r"\[archive DOI withheld for blind review\][^)]*\)", "", text)
    text = re.sub(r" +([.,;])", r"\1", text)      # space left before punctuation
    return re.sub(r"\n{3,}", "\n\n", text), removed


def main() -> int:
    OUT.mkdir(exist_ok=True)
    print(f"{'paper':<9}{'abstract':>10}{'body':>8}{'refs':>6}{'tables':>8}  journal")
    for key, (fname, intro) in PAPERS.items():
        lay = LAYOUT[key]
        src = (HERE / fname).read_text(encoding="utf-8")
        abstract = count_words(section(src, "## Abstract", "**Keywords")
                               if "**Keywords" in src else
                               section(src, "## Abstract", "\n---"))
        # IJTB counts Introduction through Conclusions; the declarations its
        # house style places before the references are outside the limit.
        body = count_words(section(src, intro, lay["body_end"]))
        reflist = src.split('## References')[1]
        nxt = reflist.find(chr(10) + '## ')
        if nxt != -1:
            reflist = reflist[:nxt]
        refs = (len(re.findall(r'^\d+\. ', reflist, flags=re.M))
                or len(re.findall(r'^[A-Z][^\n|]*?\.\s\d{4}[a-z]?\.', reflist, flags=re.M)))
        assert refs, f"{key}: counted no references; the list style may have changed"
        tables = len(re.findall(r"^\*\*Table \d+\.", src, flags=re.M))
        # Figures were the one count the title page carried by hand. It read
        # "0" for both papers, typed before any figure existed, long after
        # each paper had two. Counted from the captions now, like the rest.
        figures = len(re.findall(r"^\*\*Figure \d+\.", src, flags=re.M))

        text, _ = blind(src)
        d = OUT / key
        d.mkdir(exist_ok=True)
        for leak in ("Siddalingaiah", "hssling", "ORCID", "Shridevi", "0000-0002",
                     "zenodo.", "8941087719"):
            assert leak not in text, f"{key}: blinded copy still contains {leak!r}"

        basis = lay["word_count_basis"]
        blinded_body, table_blocks = split_tables(add_word_count(text, body, basis))
        unblinded_body, unblinded_tables = split_tables(
            add_word_count(for_submission(src), body, basis))
        assert len(table_blocks) == tables == len(unblinded_tables), (
            f"{key}: {tables} table captions but {len(table_blocks)} tables split out")
        if lay["tables_in_manuscript"]:
            # IJTB house set: highlights travel as their own file, and tables
            # sit after the reference list, each marked where it belongs.
            blinded_body = tables_after_references(
                drop_section(blinded_body, "## Highlights"), table_blocks)
            unblinded_body = tables_after_references(
                drop_section(unblinded_body, "## Highlights"), unblinded_tables)
            write_ijtb_extras(d, lay, src)
        else:
            # Tables are written from the blinded text: they carry no author
            # identity, and the blinded form is safe for either review model.
            (d / lay["tables_file"]).write_text(
                "# Tables\n\n" + "\n\n---\n\n".join(table_blocks) + "\n", encoding="utf-8")
        bracket = lay["tables_in_manuscript"]          # IJTB prints "[1]"
        blinded_body = literal_reference_numbers(blinded_body, bracket)
        unblinded_body = literal_reference_numbers(unblinded_body, bracket)
        (d / lay["blinded"]).write_text(blinded_body, encoding="utf-8")
        # The unblinded source goes in too: a single-anonymized journal wants
        # that one, and having both means the choice is made at upload, not here.
        (d / lay["manuscript"]).write_text(unblinded_body, encoding="utf-8")
        print(f"{key:<9}{abstract:>10}{body:>8}{refs:>6}{tables:>8}  {lay['journal']}")

        stamp_counts(d / lay["title_page"], abstract, body, tables, refs, figures)
        copy_figures(key, d, lay, figures)
        supp = HERE / f"supplementary_paper_{key[-1]}.md"
        if supp.exists():
            (d / lay["supplement"]).write_text(supp.read_text(encoding="utf-8"),
                                               encoding="utf-8")

    print("\nThese counts are written into the title pages by this script. Type them "
          "into the portal from here, not from memory.")
    print(f"\n{to_docx()}")
    return 0


def copy_figures(key: str, d: Path, lay: dict, figures: int) -> None:
    """Each folder is the complete upload for its journal, named by the
    figure number the text cites. Paper A takes the 600 dpi TIFF masters,
    with PNG previews as the author's IJTB uploads carried; paper B takes PNG."""
    letter = key[-1]
    figdir = HERE.parent / "figures"
    ext = ".tif" if lay["figure"].endswith(".tif") else ".png"
    figs = sorted(figdir.glob(f"figure_{letter}*{ext}"))
    assert len(figs) == figures, (
        f"{key}: {figures} figure captions but {len(figs)} {ext} files in "
        f"{figdir}; run figures/make_figures.py")
    for old in list(d.glob("*_Figure_*.tif")) + list(d.glob("*_Figure_*.png")):
        old.unlink()
    for fig in figs:
        k = int(re.match(rf"figure_{letter}(\d+)_", fig.name).group(1))
        shutil.copyfile(fig, d / lay["figure"].format(n=10 + k, k=k))
        if "preview" in lay:
            shutil.copyfile(fig.with_suffix(".png"),
                            d / lay["preview"].format(n=91 + k, k=k))


def literal_reference_numbers(text: str, bracket: bool) -> str:
    """Write each reference number as text, one paragraph per reference.

    Pandoc turns the source's "1." lines into one Word list, and the .docx
    holds a single numbering instance -- yet Word, rendering paper A, restarted
    the count at 1 on the third reference, so references 3-22 printed as 1-20
    and every citation after [2] pointed at the wrong source. Nothing in the
    file was wrong; only a render showed it. Literal numbers cannot be
    renumbered. IJTB prints them as "[1]", as the author's IJTB-S-26-01305
    manuscript did; IJE keeps "1." (escaped so pandoc does not make a list)."""
    i = text.find("## References")
    if i == -1:
        return text
    j = text.find("\n## ", i + 5)
    j = j if j != -1 else len(text)
    out = []
    for ln in text[i:j].split("\n"):
        m = re.match(r"^(\d+)\. (.*)$", ln)
        if m:
            num = f"[{m.group(1)}]" if bracket else f"{m.group(1)}\\."
            out += [f"{num} {m.group(2)}", ""]
        elif ln.strip():
            out += [ln, ""]
    block = "\n".join(out).rstrip() + "\n"
    return text[:i] + block + text[j:]


def drop_section(text: str, heading: str) -> str:
    """Remove one '## ' section, up to the next heading or rule."""
    i = text.find(heading)
    if i == -1:
        return text
    stops = [x for x in (text.find("\n## ", i + len(heading)),
                         text.find("\n---", i + len(heading))) if x != -1]
    return text[:i] + (text[min(stops) + 1:] if stops else "")


def tables_after_references(text: str, blocks: list[str]) -> str:
    """Place every table after the reference list and before the figure
    legends, as in the author's IJTB-S-26-01305 manuscript."""
    tables = "## Tables\n\n" + "\n\n".join(blocks) + "\n\n"
    i = text.find("## Figure captions")
    return text[:i] + tables + text[i:] if i != -1 else text.rstrip() + "\n\n" + tables


def write_ijtb_extras(d: Path, lay: dict, src: str) -> None:
    """Highlights and figure captions are separate uploads at IJTB. Both are
    cut from the manuscript source, so they cannot disagree with it."""
    title = re.search(r"(?m)^# (.+)$", src).group(1).strip()
    hi = section(src, "## Highlights", "## 1. Introduction")
    bullets = [ln for ln in hi.splitlines() if ln.startswith("- ")]
    assert 3 <= len(bullets) <= 5, f"IJTB house set wants 3-5 highlights, found {len(bullets)}"
    for b in bullets:
        assert len(b[2:]) <= 85, f"highlight over 85 characters: {b[2:]}"
    (d / lay["highlights"]).write_text(
        "# Highlights\n\n" + "\n".join(bullets) + "\n", encoding="utf-8")
    caps = src[src.index("## Figure captions") + len("## Figure captions"):]
    if "\n---" in caps:
        caps = caps[:caps.index("\n---")]
    # Each figure gets its own heading, its preview embedded, then its caption,
    # as in the author's IJTB-S-26-01305 captions file: an editor or reviewer
    # sees figure and caption together without opening the TIFF masters.
    blocks = []
    for m in re.finditer(r"(?ms)^\*\*Figure (\d+)\..*?(?=^\*\*Figure \d+\.|\Z)", caps):
        k = int(m.group(1))
        preview = lay["preview"].format(n=91 + k, k=k)
        blocks.append(f"## Figure {k}\n\n![]({preview}){{width=6.3in}}\n\n"
                      + m.group(0).strip())
    figures = len(re.findall(r"(?m)^\*\*Figure \d+\.", src))
    assert len(blocks) == figures, f"{len(blocks)} caption blocks for {figures} figures"
    (d / lay["captions"]).write_text(
        f"# Figures\n\n**Manuscript.** {title}\n\n"
        "Figures are supplied separately as 600 dpi TIFF files for production; PNG "
        "previews are embedded below.\n\n" + "\n\n".join(blocks) + "\n", encoding="utf-8")


def for_submission(text: str) -> str:
    """Remove what is for the author only, keeping the author's identity.

    The blinded copy has always lost these, inside blind(). The unblinded copy
    was written straight from the source, so paper B's upload to IJE carried a
    "Target journal" line naming the alternative journals considered -- one
    "held as a fallback" -- and the whole "Notes for the author -- not for
    submission" section. Both are now removed from every upload."""
    text = re.sub(r"(?m)^\*\*Target journal:\*\*.*\n?", "", text)
    i = text.find("## Notes for the author")
    if i != -1:
        text = text[:i].rstrip() + "\n"
    return re.sub(r"\n{3,}", "\n\n", text)


def add_word_count(text: str, body: int, basis: str) -> str:
    """IJE: "The main document should include a title page with author names
    and affiliations. The word count should be included on the title page."
    The count is the one the build derived, never typed."""
    line = f"**Word count:** {body:,} {basis}"
    m = re.search(r"(?m)^\*\*Running title:\*\*.*$", text)
    assert m, "no running title to anchor the word count"
    return text[:m.end()] + "\n\n" + line + text[m.end():]


def split_tables(text: str) -> tuple[str, list[str]]:
    """Lift each table -- caption, rows and the italic note under it -- out
    of the text, leaving '[Table N about here]' where it stood."""
    lines = text.split("\n")
    out: list[str] = []
    tables: list[str] = []
    i = 0
    while i < len(lines):
        m = re.match(r"^\*\*Table (\d+)\.", lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        block = [lines[i]]
        i += 1
        seen_rows = False
        while i < len(lines):
            ln = lines[i]
            if ln.startswith("|"):
                seen_rows = True
            elif ln.strip() == "":
                pass
            elif seen_rows and ln.startswith("*") and not ln.startswith("**"):
                pass                                    # the table's own note
            else:
                break
            block.append(ln)
            i += 1
        while block and not block[-1].strip():
            block.pop()
        assert any(b.startswith("|") for b in block), f"Table {m.group(1)} has no rows"
        tables.append("\n".join(block))
        out += [f"[Table {m.group(1)} about here]", ""]
    return "\n".join(out), tables


def stamp_counts(page: Path, abstract: int, body: int, tables: int,
                 refs: int, figures: int) -> None:
    """Write the derived counts into the title page's count table.

    These were hand-maintained and went stale three times in one afternoon,
    each time because an edit elsewhere moved a number. Each row must match,
    or the title page has been restructured and the build should say so
    rather than quietly leave the old figure in place.
    """
    if not page.exists():
        return
    s = page.read_text(encoding="utf-8")
    rows = [(r"(\| Abstract \(structured\) \| )[\d,]+( words \|)", abstract),
            (r"(\| Main text,[^|]*\| )[\d,]+( words \|)", body),
            (r"(\| Tables \| )\d+( \|)", tables),
            (r"(\| Figures \| )\d+( \|)", figures),
            (r"(\| References \| )\d+( \|)", refs)]
    for pat, value in rows:
        s, n = re.subn(pat, lambda m: f"{m.group(1)}{value:,}{m.group(2)}", s)
        if n != 1:
            raise SystemExit(f"{page.name}: expected one row for {pat!r}, found {n}")
    page.write_text(s, encoding="utf-8")


def to_docx() -> str:
    """Convert every .md under submission/ to .docx. Optional by design."""
    import style_docx_tables as style_tables
    pandoc = shutil.which("pandoc")
    if not pandoc:
        return ("pandoc not on PATH: wrote Markdown only. Neither journal accepts "
                "Markdown, so convert before uploading.")
    made, failed = [], []
    for md in sorted(OUT.rglob("*.md")):
        if md.name == "README.md" or md.name == "SUBMISSION_STEPS.md":
            continue                      # working documents, not uploads
        docx = md.with_suffix(".docx")
        proc = subprocess.run(
            [pandoc, str(md), "-f", "markdown+pipe_tables", "-o", str(docx),
             "--standalone", "--wrap=none",
             # images are named relative to their own folder, not the cwd
             f"--resource-path={md.parent}"],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        ok = proc.returncode == 0 and docx.exists()
        if ok:
            # Pandoc's tables arrive in Word with no borders; the author's IJTB
            # tooling writes journal (booktabs) rules into each table.
            style_tables.process(docx)
        (made if ok else failed).append(md.relative_to(OUT).as_posix())
    msg = f"pandoc: wrote {len(made)} .docx beside the Markdown"
    if failed:
        msg += f"; FAILED on {failed}"
    return msg + "\n" + check_docx_metadata()


def check_docx_metadata() -> str:
    """A blinded .docx can name its author in document properties even when
    the text does not. Pandoc leaves those empty, but opening and re-saving
    in Word stamps the account name into dc:creator and cp:lastModifiedBy,
    and a reviewer sees it in File > Properties. Checked, not assumed.
    """
    import zipfile
    leaks = []
    blinded = [OUT / k / Path(v["blinded"]).with_suffix(".docx").name
               for k, v in LAYOUT.items()]
    for docx in sorted(p for p in blinded if p.exists()):
        try:
            z = zipfile.ZipFile(docx)
            meta = " ".join(z.read(n).decode("utf-8", "ignore")
                            for n in ("docProps/core.xml", "docProps/app.xml")
                            if n in z.namelist())
        except Exception as exc:                       # noqa: BLE001
            leaks.append(f"{docx.name}: unreadable ({exc})")
            continue
        for term in ("Siddalingaiah", "hssling", "Shridevi", "0000-0002"):
            if term in meta:
                leaks.append(f"{docx.relative_to(OUT).as_posix()}: "
                             f"document properties contain {term!r}")
    if leaks:
        raise SystemExit("blinded .docx metadata leak:\n  " + "\n  ".join(leaks))
    return "blinded .docx document properties: no author metadata"


if __name__ == "__main__":
    sys.exit(main())
