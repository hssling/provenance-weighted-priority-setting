"""Check paper B's Journal of Clinical Epidemiology set against the journal's own rules.

The journal's Guide for Authors sets, for Original Research: at most 3,000 words of
main text, 100 references, 5 figures and 5 tables; a structured abstract of at most
350 words; 1 to 7 keywords; 3 to 5 highlights of at most 85 characters each, in a
separate file with "highlights" in its name; a "What is new?" box of 3 to 5 points
below the abstract and before the Introduction; references numbered in square
brackets in order of first citation; and the generative-AI declaration as its own
section before the reference list. This check reads the source and the built upload
set and fails on any breach. It also requires that:

  * tables, figures and supplementary notes and tables are numbered in order of first
    citation in the running text, are all cited, and are presented in that order;
  * the counts written into the title page and the cover letter are the derived ones;
  * the paper states associations and computations, not causes: no causal wording in
    the manuscript, its highlights, its supplement or its cover letter;
  * the uploaded Word files carry no underline or strikethrough.

The source is kept local, so on a machine without it the check says so and passes.

Usage: python -I verification/check_jce_profile.py
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
M = ROOT / "manuscript"
sys.path.insert(0, str(M))
sys.path.insert(0, str(ROOT / "verification"))
from submission_layout import LAYOUT  # noqa: E402

KEY = "paper_b_jce"
LAY = LAYOUT[KEY]
SRC = M / LAY["source"]
SUPP = M / LAY["supplement_source"]
OUT = M / "submission" / KEY

ABSTRACT_HEADINGS = ["Background and Objective", "Methods", "Results", "Discussion and Conclusion"]
AI_HEADING = ("## Declaration of generative AI and AI-assisted technologies in the manuscript "
              "preparation process")
# Wording that asserts a cause. The paper measures where values came from and computes
# what an estimate would be under stated assumptions; it does not identify causes.
CAUSAL = re.compile(
    r"\b(?:caus(?:e|es|ed|ing|al|ally|ation)|because|due to|owing to|led to|"
    r"lead(?:s|ing)? to|result(?:s|ed|ing)? in|as a result|driv(?:e|es|en|ing)|"
    r"effects? of|impact(?:s|ed)?|attributable to|consequen(?:ce|ces|tly))\b", re.I)


def between(text: str, start: str, end: str) -> str:
    i = text.find(start)
    if i == -1:
        return ""
    i += len(start)
    j = text.find(end, i)
    return text[i:j if j != -1 else len(text)]


def running_text(src: str) -> str:
    """Introduction to the end of the main text, without captions or table rows: where
    first citations of exhibits and supplementary items are counted."""
    body = src[src.index(LAY["body_start"]):src.index("## References")]
    body = re.sub(r"(?m)^\*\*(?:Supplementary )?(?:Table|Figure) S?\d+\..*$", "", body)
    return re.sub(r"(?m)^\|.*$", "", body)


def check_limits(c: dict, lim: dict) -> list[str]:
    errs = []
    for key, name in (("body", "words of main text"), ("abstract", "abstract words"),
                      ("references", "references"), ("figures", "figures"), ("tables", "tables")):
        limit = lim["words" if key == "body" else key]
        if c[key] > limit:
            errs.append(f"  {c[key]:,} {name}, over the limit of {limit:,}")
    lo, hi = lim["keywords"]
    if not lo <= c["keywords"] <= hi:
        errs.append(f"  {c['keywords']} keywords; the journal wants {lo} to {hi}")
    return errs


def check_abstract(src: str) -> list[str]:
    ab = between(src, "## Abstract", "**Keywords")
    found = re.findall(r"(?m)^\*\*([^*]+?)\.\*\*", ab)
    if found != ABSTRACT_HEADINGS:
        return [f"  abstract headings are {found}; expected {ABSTRACT_HEADINGS}"]
    if re.search(r"\[\d", ab):
        return ["  the abstract cites a reference by number; the journal asks for none"]
    return []


def check_what_is_new(src: str, lim: tuple[int, int]) -> list[str]:
    i, k = src.find("## What is new?"), src.find(LAY["body_start"])
    a = src.find("## Abstract")
    if i == -1:
        return ["  no 'What is new?' box"]
    errs = []
    if not a < i < k:
        errs.append("  the 'What is new?' box is not between the abstract and the Introduction")
    box = src[i:k]
    points = re.findall(r"(?m)^- ", box)
    if not lim[0] <= len(points) <= lim[1]:
        errs.append(f"  the 'What is new?' box has {len(points)} points; the journal wants "
                    f"{lim[0]} to {lim[1]}")
    for need in ("Key findings", "What this adds", "implication"):
        if need not in box:
            errs.append(f"  the 'What is new?' box lacks the part {need!r}")
    return errs


def check_highlights(bullets: list[str], filename: str, lim: tuple[int, int],
                     chars: int) -> list[str]:
    errs = []
    if "highlights" not in filename.lower():
        errs.append(f"  highlights file {filename!r} lacks 'highlights' in its name")
    if not lim[0] <= len(bullets) <= lim[1]:
        errs.append(f"  {len(bullets)} highlights; the journal wants {lim[0]} to {lim[1]}")
    for b in bullets:
        if len(b) > chars:
            errs.append(f"  highlight of {len(b)} characters (limit {chars}): {b}")
    return errs


def check_ai_declaration(src: str) -> list[str]:
    i, r = src.find(AI_HEADING), src.find("## References")
    c = src.find("## 6. Conclusions")
    if i == -1:
        return ["  no section headed as Elsevier's generative-AI declaration"]
    if not c < i < r:
        return ["  the generative-AI declaration is not between the Conclusions and the references"]
    return []


def first_order(text: str, pattern: str) -> list[str]:
    seen: list[str] = []
    for m in re.finditer(pattern, text):
        for item in expand(m):
            if item not in seen:
                seen.append(item)
    return seen


def expand(m: re.Match) -> list[str]:
    """'Supplementary Notes 3 and 4', 'Notes 1-5', 'Tables S1-S4' -> each item."""
    kind = "Note" if m.group(1).startswith("Note") else "Table S"
    nums = [int(x) for x in re.findall(r"\d+", m.group(2))]
    if re.search(r"[–-]", m.group(2)) and len(nums) == 2:
        nums = list(range(nums[0], nums[1] + 1))
    return [f"{kind}{n}" for n in nums]


SUPP_CITE = (r"Supplementary (Notes?|Tables?) ((?:S?\d+)(?:(?:\s*[,–-]\s*|\s+and\s+)S?\d+)*)")


def check_supplementary_order(src: str, supp: str) -> list[str]:
    """Supplementary notes and tables, each numbered in order of first citation in the
    running text, all cited, none cited that does not exist, presented in that order."""
    errs = []
    cited = first_order(running_text(src), SUPP_CITE)
    presented = ([f"Note{n}" for n in re.findall(r"(?m)^## Supplementary Note (\d+)\.", supp)]
                 + [f"Table S{n}" for n in re.findall(r"(?m)^\*\*Supplementary Table S(\d+)\.", supp)])
    for kind in ("Note", "Table S"):
        c = [x for x in cited if x.startswith(kind)]
        p = [x for x in presented if x.startswith(kind)]
        nums = [int(x[len(kind):]) for x in c]
        if nums != sorted(nums):
            errs.append(f"  supplementary {kind.strip()} items first cited out of order: {c}")
        if sorted(nums) != list(range(1, len(nums) + 1)):
            errs.append(f"  supplementary {kind.strip()} items cited are {c}; numbering has a gap")
        pres = [int(x[len(kind):]) for x in p]
        if pres != sorted(pres):
            errs.append(f"  the supplement presents {kind.strip()} items out of order: {p}")
        if set(c) != set(p):
            errs.append(f"  supplementary {kind.strip()} items cited {sorted(set(c))} but "
                        f"present {sorted(set(p))}")
    return errs


def check_causal(texts: dict[str, str]) -> list[str]:
    errs = []
    for where, t in texts.items():
        for m in CAUSAL.finditer(t):
            ctx = t[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
            errs.append(f"  causal wording in {where}: ...{ctx}...")
    return errs


def check_stamped(page: str, rows: list[tuple[str, int]], name: str) -> list[str]:
    errs = []
    for pat, want in rows:
        m = re.search(pat, page)
        got = int(m.group(1).replace(",", "")) if m else None
        if got != want:
            errs.append(f"  {name}: states {got} where the derived count is {want} ({pat})")
    return errs


def check_docx_format(folder: Path) -> list[str]:
    errs = []
    for docx in sorted(folder.glob("*.docx")):
        if docx.name.startswith("~$"):
            continue
        x = zipfile.ZipFile(docx).read("word/document.xml").decode("utf-8", "ignore")
        if re.search(r"<w:u\s+w:val=\"(?!none)", x) or "<w:strike" in x or "<w:dstrike" in x:
            errs.append(f"  {docx.name}: underline or strikethrough formatting")
    return errs


def main() -> int:
    if not SRC.exists():
        print(f"PASSED: {SRC.name} is kept local and is not on this machine; "
              "the Journal of Clinical Epidemiology profile was not checked here")
        return 0
    import build_submission as bs
    import check_exhibit_order as ceo
    import check_references as cr
    src = SRC.read_text(encoding="utf-8")
    supp = SUPP.read_text(encoding="utf-8") if SUPP.exists() else ""
    lim = LAY["limits"]
    c = bs.jce_counts(src, LAY)
    errs: list[str] = []
    errs += check_limits(c, lim)
    errs += check_abstract(src)
    errs += check_what_is_new(src, lim["what_is_new"])
    hfile = OUT / LAY["highlights"]
    built = ([ln[2:].strip() for ln in hfile.read_text(encoding="utf-8").splitlines()
              if ln.startswith("- ")] if hfile.exists() else [])
    if built != bs.highlights_of(src):
        errs.append(f"  {hfile.name} differs from the source's highlights; rebuild")
    errs += check_highlights(built, hfile.name, lim["highlights"], lim["highlight_chars"])
    errs += check_ai_declaration(src)
    # order of first citation: references, then tables and figures, then supplementary items
    errs += [e.replace("paper B (JCE)", "references") for e in cr.check_numbered(src, "paper B (JCE)")]
    errs += ceo.check("paper B (JCE)", SRC)
    errs += check_supplementary_order(src, supp)
    # counts written into the uploads
    tp = (OUT / LAY["title_page"]).read_text(encoding="utf-8")
    errs += check_stamped(tp, [
        (r"\| Abstract \(structured\) \| ([\d,]+) words", c["abstract"]),
        (r"\| Main text, Introduction[^|]*\| ([\d,]+) words", c["body"]),
        (r"\| Main text with the declarations[^|]*\| ([\d,]+) words", c["with_declarations"]),
        (r"\| Tables \| (\d+) \|", c["tables"]), (r"\| Figures \| (\d+) \|", c["figures"]),
        (r"\| References \| (\d+) \|", c["references"])], "title page")
    cover = (OUT / LAY["cover"]).read_text(encoding="utf-8")
    errs += check_stamped(cover, [
        (r"The main text has ([\d,]+) words", c["body"]),
        (r"\(([\d,]+) words with the declarations", c["with_declarations"]),
        (r"with (\d+) tables, ", c["tables"]), (r" tables, (\d+) figures and ", c["figures"]),
        (r" figures and (\d+) references", c["references"])], "cover letter")
    for name in (LAY["manuscript"], LAY["blinded"]):
        up = (OUT / name).read_text(encoding="utf-8") if (OUT / name).exists() else ""
        if f"**Word count:** {c['body']:,} words" not in up:
            errs.append(f"  {name}: does not state the derived word count {c['body']:,}")
    # figures: one TIFF and one PNG preview per caption
    tifs = sorted(OUT.glob(LAY["figure_glob"]))
    pngs = sorted(OUT.glob("9[2-9]_Figure_*_preview.png"))
    if len(tifs) != c["figures"] or len(pngs) != c["figures"]:
        errs.append(f"  {len(tifs)} TIFF and {len(pngs)} preview files for {c['figures']} figures")
    # wording
    main_text = src[src.index("## Abstract"):src.index("## References")]
    captions = between(src, "## Figure captions", "\n## Supplementary material")
    cover_body = between(cover, "Dear Editors,", "Yours sincerely")
    errs += check_causal({"the manuscript": main_text, "the figure captions": captions,
                          "the supplement": supp, "the cover letter": cover_body})
    errs += check_docx_format(OUT)
    if errs:
        print(f"FAILED: {len(errs)} breach(es) of the Journal of Clinical Epidemiology profile")
        print("\n".join(errs))
        return 1
    print(f"PASSED: paper B (JCE) is within the journal's limits ({c['body']:,} of {lim['words']:,} "
          f"words, abstract {c['abstract']} of {lim['abstract']}, {c['references']} references, "
          f"{c['tables']} tables, {c['figures']} figures, {c['keywords']} keywords); the What is "
          f"new? box has {c['what_is_new_points']} points; {len(built)} highlights within "
          f"{lim['highlight_chars']} characters; references, tables, figures and supplementary "
          f"items are in order of first citation; the stamped counts are the derived ones; no "
          f"causal wording; no underline or strikethrough")
    return 0


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if __name__ == "__main__":
    sys.exit(main())
