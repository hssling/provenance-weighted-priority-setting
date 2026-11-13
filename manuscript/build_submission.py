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
    text = re.sub(r"^\|.*$", "", text, flags=re.M)        # tables
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
    # self-citations that name the author
    text = re.sub(r"Siddalingaiah HS?\.?", "[Author]", text)
    # The deposit identifiers de-anonymise the submission: the repository URL
    # carries the author's username, and resolving the DOI shows the author
    # record. A journal reviewing blind expects these to be withheld and given
    # to the editor instead. The unblinded source keeps them in full.
    text = re.sub(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
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
    print(f"{'paper':<9}{'abstract':>10}{'body':>8}{'refs':>6}{'tables':>8}  blinded to")
    for key, (fname, intro) in PAPERS.items():
        src = (HERE / fname).read_text(encoding="utf-8")
        abstract = count_words(section(src, "## Abstract", "**Keywords")
                               if "**Keywords" in src else
                               section(src, "## Abstract", "\n---"))
        body = count_words(section(src, intro, "## References"))
        reflist = src.split('## References')[1]
        nxt = reflist.find(chr(10) + '## ')
        if nxt != -1:
            reflist = reflist[:nxt]
        refs = len(re.findall(r'^\d+\. ', reflist, flags=re.M))
        tables = len(re.findall(r"^\*\*Table \d+\.", src, flags=re.M))

        text, _ = blind(src)
        d = OUT / key
        d.mkdir(exist_ok=True)
        dest = d / "03_manuscript_blinded.md"
        dest.write_text(text, encoding="utf-8")
        for leak in ("Siddalingaiah", "hssling", "ORCID", "Shridevi", "0000-0002",
                     "github.com", "zenodo."):
            assert leak not in text, f"{key}: blinded copy still contains {leak!r}"
        print(f"{key:<9}{abstract:>10}{body:>8}{refs:>6}{tables:>8}  {dest.relative_to(HERE)}")

        # The unblinded source goes in too: a single-blind journal wants that
        # one, and having both means the choice is made at upload, not here.
        (d / "04_manuscript_unblinded.md").write_text(src, encoding="utf-8")

    print("\nState these counts on the title pages. Do not retype them from memory.")
    print(f"\n{to_docx()}")
    return 0


def to_docx() -> str:
    """Convert every .md under submission/ to .docx. Optional by design."""
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
             "--standalone", "--wrap=none"],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        (made if proc.returncode == 0 and docx.exists() else failed).append(
            md.relative_to(OUT).as_posix())
    msg = f"pandoc: wrote {len(made)} .docx beside the Markdown"
    if failed:
        msg += f"; FAILED on {failed}"
    return msg


if __name__ == "__main__":
    sys.exit(main())
