"""Build paper A's Health Empirics upload set from its local Markdown sources.

Health Empirics wants one Word document: title page, abstract and keywords, numbered text,
references (APA 7), appendices, tables (title above, no vertical rules) and figures (legend
below), on A4 with 2.5 cm margins, Times New Roman 12 pt and 1.5 line spacing. The layout
follows the author's earlier Health Empirics package; no text is shared with it.

Sources (git-ignored, kept on the author's machine; this script carries no manuscript text):
  manuscript/manuscript_a_he.md               the paper
  manuscript/manuscript_a_he_cover_letter.md  the letter to the Editor
  manuscript/manuscript_a_he_email.md         the covering e-mail
Figures: figures/figure_a1_*.png|tif and figures/figure_a2_*.png|tif (made by figures/make_figures.py).

Writes manuscript/submission/paper_a_he/: HE_manuscript_fiscal_invisibility.docx,
HE_cover_letter.docx, Figure_1.tif, Figure_2.tif (RGB, 600 dpi) and submission_email.txt.

Before writing, it checks: the abstract (200-250 words) and keyword rules (4-8, alphabetical);
the short title (at most 20 words); that every in-text citation has a reference and every
reference is cited, with the list in alphabetical order; that tables, figures and appendices
are each cited and first cited in numerical order; and the word count on both readings.

Usage: python -I manuscript/build_paper_a_he.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = HERE / "manuscript_a_he.md"
LETTER = HERE / "manuscript_a_he_cover_letter.md"
EMAIL = HERE / "manuscript_a_he_email.md"
OUT = HERE / "submission" / "paper_a_he"
FROZEN = {"paper_a", "paper_b", "paper_b_tmih", "paper_b_jce", "paper_a_he"}
FIGURES = [ROOT / "figures" / "figure_a1_two_accounts_of_the_same_shortfall",
           ROOT / "figures" / "figure_a2_interventions_to_budget_lines"]
DOCX_NAME = "HE_manuscript_fiscal_invisibility.docx"
TEXT_WIDTH_CM = 16.0
WORD_RANGE = (4000, 8000)
AUTHOR = "Siddalingaiah H S"


# ------------------------------------------------------------------ parsing
def sections(text: str) -> list[tuple[int, str, list[str]]]:
    """[(level, heading, lines)] for '#', '##' and '###' headings, in order."""
    out: list[tuple[int, str, list[str]]] = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip(), []))
        elif out:
            out[-1][2].append(line.rstrip())
    return out


def blocks(lines: list[str]) -> list[tuple[str, object]]:
    """Paragraphs and pipe tables from a section's lines: [('p', text) | ('t', rows)]."""
    out: list[tuple[str, object]] = []
    table: list[list[str]] = []
    for line in lines + [""]:
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not set("".join(cells)) <= set("-: "):
                table.append(cells)
            continue
        if table:
            out.append(("t", table))
            table = []
        if line.strip():
            out.append(("p", line.strip()))
    return out


def plain(text: str) -> str:
    return re.sub(r"[*`]", "", text)


def nwords(text: str) -> int:
    return sum(1 for tok in plain(text).split() if re.search(r"[^\W_]", tok))


# ------------------------------------------------------------------ docx helpers
def new_doc() -> Document:
    d = Document()
    s = d.sections[0]
    s.page_width, s.page_height = Cm(21.0), Cm(29.7)
    for attr in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(s, attr, Cm(2.5))
    n = d.styles["Normal"]
    n.font.name = "Times New Roman"
    n.font.size = Pt(12)
    n.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Times New Roman")
    n.paragraph_format.line_spacing = 1.5
    n.paragraph_format.space_after = Pt(6)
    d.core_properties.author = AUTHOR
    d.core_properties.last_modified_by = AUTHOR
    d.core_properties.title = ""
    d.core_properties.comments = ""
    return d


def runs(p, text: str, bold=False, italic=False, size=None):
    pos = 0
    for m in re.finditer(r"\*\*(.+?)\*\*|(?<![*\w])\*(?!\*)(.+?)(?<!\*)\*(?![*\w])|`(.+?)`", text):
        if m.start() > pos:
            _run(p, text[pos:m.start()], bold, italic, size)
        if m.group(1) is not None:
            _run(p, m.group(1), True, italic, size)
        elif m.group(2) is not None:
            _run(p, m.group(2), bold, True, size)
        else:
            _run(p, m.group(3), bold, italic, size)
        pos = m.end()
    if pos < len(text):
        _run(p, text[pos:], bold, italic, size)
    return p


def _run(p, s, bold, italic, size):
    r = p.add_run(s)
    r.bold, r.italic = bold, italic
    if size:
        r.font.size = Pt(size)


def para(doc, text="", bold=False, size=None, align=None, before=None, keep=False, spacing=None):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    if before is not None:
        p.paragraph_format.space_before = Pt(before)
    if keep:
        p.paragraph_format.keep_with_next = True
    if spacing:
        p.paragraph_format.line_spacing = spacing
    if text:
        runs(p, text, bold=bold, size=size)
    return p


def _borders(cell, top=False, bottom=False):
    tcPr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        on = (edge == "top" and top) or (edge == "bottom" and bottom)
        el.set(qn("w:val"), "single" if on else "nil")
        if on:
            el.set(qn("w:sz"), "8")
            el.set(qn("w:color"), "000000")
        b.append(el)
    tcPr.append(b)


def table(doc, rows: list[list[str]], size=9.5):
    header, body = rows[0], rows[1:]
    t = doc.add_table(rows=1, cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = OxmlElement("w:tblHeader")
    hdr.set(qn("w:val"), "true")
    t.rows[0]._tr.get_or_add_trPr().append(hdr)
    for j, h in enumerate(header):
        c = t.rows[0].cells[j]
        c.paragraphs[0].paragraph_format.line_spacing = 1.0
        runs(c.paragraphs[0], h, bold=True, size=size)
        _borders(c, top=True, bottom=True)
    for i, row in enumerate(body):
        cells = t.add_row().cells
        for j, v in enumerate(row):
            cells[j].paragraphs[0].paragraph_format.line_spacing = 1.0
            runs(cells[j].paragraphs[0], v, size=size)
            _borders(cells[j], bottom=i == len(body) - 1)
    return t


# ------------------------------------------------------------------ checks
def check_abstract(abstract: list[str], problems: list[str]) -> int:
    body = [b for b in abstract if not b.startswith("**Keywords:**")]
    n = sum(nwords(b) for b in body)
    if not 200 <= n <= 250:
        problems.append(f"abstract has {n} words; Health Empirics asks for 200-250")
    heads = [re.match(r"\*\*(.+?)\.\*\*", b).group(1) for b in body if re.match(r"\*\*(.+?)\.\*\*", b)]
    if heads != ["Background", "Methods", "Results", "Conclusion"]:
        problems.append(f"abstract headings {heads}")
    kw = next((b for b in abstract if b.startswith("**Keywords:**")), "")
    words = [k.strip().rstrip(".") for k in kw.replace("**Keywords:**", "").split(";") if k.strip()]
    if not 4 <= len(words) <= 8:
        problems.append(f"{len(words)} keywords; 4-8 required")
    if words != sorted(words, key=str.casefold):
        problems.append(f"keywords not alphabetical: {words}")
    return n


def reference_keys(refs: list[str]) -> dict[tuple[str, str], str]:
    """(citation form, year) for each reference, as APA 7 cites it in text."""
    keys = {}
    for r in refs:
        m = re.match(r"^(.*?)\s\((\d{4}[a-z]?)\)\.", r)
        if not m:
            raise SystemExit(f"cannot read author/year of reference: {r[:80]}")
        authors, year = m.group(1), m.group(2)
        group = re.match(r"^(World Health Organization|Central TB Division|Global Fund to Fight AIDS, "
                         r"Tuberculosis and Malaria)\.?$", authors)
        if group:
            keys[(group.group(1), year)] = r
            continue
        if authors.startswith("OECD"):
            keys[("OECD et al.", year)] = r
            continue
        surnames = re.findall(r"(?:^|, |& |\. \. \. )([A-Z][\w'\- ]+?), (?:[A-Z]\.)", authors)
        if not surnames:
            raise SystemExit(f"no surnames parsed: {authors[:80]}")
        if "&" not in authors and len(surnames) == 1 and "RECORD" not in authors:
            form = surnames[0]
        elif re.search(r"^[^,]+, [A-Z. -]+, & [^,]+, [A-Z. -]+$", authors):
            form = f"{surnames[0]} & {surnames[1]}"
        else:
            form = f"{surnames[0]} et al."
        keys[(form, year)] = r
    return keys


ALIASES = {"WHO": "World Health Organization"}


def cited_keys(text: str) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    text = re.sub(r"\[WHO\]", "", text)
    # parenthetical: (A, 2020; B et al., 2019, 2021)
    for grp in re.findall(r"\(([^()]*\d{4}[a-z]?)\)", text):
        for part in grp.split(";"):
            part = part.strip()
            m = re.match(r"^(?:e\.g\., )?(.+?), ((?:\d{4}[a-z]?)(?:, \d{4}[a-z]?)*)$", part)
            if not m:
                continue
            who = ALIASES.get(m.group(1).strip(), m.group(1).strip())
            for y in m.group(2).split(", "):
                out.add((who, y))
    # narrative: Smith et al. (2020), WHO (2026a)
    for who, years in re.findall(r"((?:[A-Z][\w'\-]+(?: [A-Z][\w'\-]+)*)(?: et al\.| & [A-Z][\w'\-]+)?) "
                                 r"\((\d{4}[a-z]?(?:, \d{4}[a-z]?)*)\)", text):
        for y in years.split(", "):
            out.add((ALIASES.get(who, who), y))
    return out


def check_citations(cite_text: str, refs: list[str], problems: list[str]) -> None:
    keys = reference_keys(refs)
    cited = cited_keys(cite_text)
    missing = sorted(cited - set(keys))
    uncited = sorted(set(keys) - cited)
    if missing:
        problems.append(f"cited but not in the reference list: {missing}")
    if uncited:
        problems.append(f"in the reference list but never cited: {uncited}")
    order = [re.sub(r"[^\w ]", "", r).casefold() for r in refs]
    if order != sorted(order):
        problems.append("reference list is not in alphabetical order")
    for r in refs:
        if "doi.org" not in r and not re.search(r"https?://", r) and "Central TB Division. (2017)" not in r:
            problems.append(f"reference without DOI or URL: {r[:70]}")


def check_exhibit_order(body: str, n_tables: int, n_figures: int, appendices: list[str],
                        problems: list[str]) -> None:
    for kind, labels in (("Table", [str(i) for i in range(1, n_tables + 1)]),
                         ("Figure", [str(i) for i in range(1, n_figures + 1)]),
                         ("Appendix", appendices)):
        first = {}
        for m in re.finditer(rf"\b{kind}s?\s+([0-9A-Z])\b", body):
            first.setdefault(m.group(1), m.start())
        missing = [lab for lab in labels if lab not in first]
        if missing:
            problems.append(f"{kind} {missing} never cited in the text")
        cited = [lab for lab in labels if lab in first]
        if [first[lab] for lab in cited] != sorted(first[lab] for lab in cited):
            problems.append(f"{kind}s first cited out of order: {sorted(cited, key=first.get)}")


# ------------------------------------------------------------------ build
def build() -> int:
    if OUT.name in FROZEN:
        raise SystemExit(f"{OUT.name} is a submitted set and is never rebuilt")
    text = SRC.read_text(encoding="utf-8")
    secs = sections(text)
    title = next(h for lvl, h, _ in secs if lvl == 1)
    get = {h: ls for lvl, h, ls in secs if lvl == 2}
    title_page = [b for k, b in blocks(get["Title page"]) if k == "p"]
    abstract = [b for k, b in blocks(get["Abstract"]) if k == "p"]
    refs = [b for k, b in blocks(get["References"]) if k == "p"]
    appendix_heads = [h for lvl, h, _ in secs if lvl == 2 and h.startswith("Appendix ")]
    i_body = next(i for i, (lvl, h, _) in enumerate(secs) if lvl == 2 and h.startswith("1. "))
    i_decl = next(i for i, (lvl, h, _) in enumerate(secs) if h == "Declarations")
    body_secs = secs[i_body:i_decl]
    decl = blocks(get["Declarations"])
    tables_src = blocks(get["Tables"])
    legends = [b for k, b in blocks(get["Figure legends"]) if k == "p"]

    problems: list[str] = []
    short = next((b for b in title_page if b.startswith("**Short title:**")), "")
    n_short = nwords(short.replace("**Short title:**", ""))
    if not short or n_short > 20:
        problems.append(f"short title missing or {n_short} words (at most 20)")
    n_abs = check_abstract(abstract, problems)
    body_text = "\n".join(line for _, _, ls in body_secs for line in ls)
    appendix_text = "\n".join(line for lvl, h, ls in secs if h.startswith("Appendix ") for line in ls)
    cite_text = "\n".join([body_text, appendix_text, "\n".join(get["Declarations"]),
                           "\n".join(get["Tables"]), "\n".join(legends)])
    check_citations(cite_text, refs, problems)
    n_tables = sum(1 for k, b in tables_src if k == "p" and re.match(r"\*\*Table \d+\.\*\*", b))
    check_exhibit_order(body_text, n_tables, len(legends),
                        [h.split()[1].rstrip(".") for h in appendix_heads], problems)
    if problems:
        print("FAILED:\n  - " + "\n  - ".join(problems))
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    doc = new_doc()
    # title page
    para(doc, title, bold=True, size=14)
    for b in title_page:
        para(doc, b)
    wc = para(doc, "Word count: (computed below)", bold=True)
    doc.add_page_break()
    # abstract
    para(doc, "Abstract", bold=True, size=13, keep=True)
    for b in abstract:
        para(doc, b, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    doc.add_page_break()
    # main text
    for lvl, h, ls in body_secs:
        para(doc, h, bold=True, size=13 if lvl == 2 else 12, before=12 if lvl == 2 else 8, keep=True)
        for k, b in blocks(ls):
            para(doc, b, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    # declarations
    para(doc, "Declarations", bold=True, size=13, before=12, keep=True)
    for k, b in decl:
        para(doc, b, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    # references, hanging indent
    para(doc, "References", bold=True, size=13, before=12, keep=True)
    for r in refs:
        p = para(doc, r, align=WD_ALIGN_PARAGRAPH.LEFT)
        p.paragraph_format.left_indent = Cm(1.27)
        p.paragraph_format.first_line_indent = Cm(-1.27)
    # appendices
    for h in appendix_heads:
        doc.add_page_break()
        para(doc, h, bold=True, size=13, keep=True)
        for k, b in blocks(get[h]):
            if k == "t":
                table(doc, b, size=9)
            else:
                para(doc, b, align=WD_ALIGN_PARAGRAPH.JUSTIFY, keep=b.startswith("**Table"))
    # tables: title above, note below
    first = True
    for k, b in tables_src:
        if k == "p" and re.match(r"\*\*Table \d+\.\*\*", b):
            doc.add_page_break()
            if first:
                para(doc, "Tables", bold=True, size=13)
                first = False
            para(doc, b, before=6, keep=True)
        elif k == "t":
            table(doc, b, size=8.5 if len(b[0]) > 5 else 9.5)
        else:
            para(doc, b, size=9, before=3, spacing=1.15)
    # figures: image, then legend below
    for n, (stem, legend) in enumerate(zip(FIGURES, legends), start=1):
        doc.add_page_break()
        if n == 1:
            para(doc, "Figures", bold=True, size=13)
        pic = doc.add_paragraph()
        pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pic.paragraph_format.keep_with_next = True
        pic.add_run().add_picture(str(stem.with_suffix(".png")), width=Cm(TEXT_WIDTH_CM))
        para(doc, legend, align=WD_ALIGN_PARAGRAPH.JUSTIFY, spacing=1.15)

    strict, whole = count_words(doc)
    lo, hi = WORD_RANGE
    if not (lo <= strict <= hi and lo <= whole <= hi):
        print(f"FAILED: {strict} words (text, declarations, references, appendices) and {whole} in the "
              f"whole document; Health Empirics asks for {lo:,}-{hi:,}")
        return 1
    wc.runs[0].text = (f"Word count: {strict:,} words (main text, declarations, references and appendices; "
                       f"excluding the title page, abstract, tables and figure legends). "
                       f"Abstract: {n_abs} words. Tables: {n_tables}. Figures: {len(legends)}. "
                       f"Appendices: {len(appendix_heads)}.")
    doc.save(OUT / DOCX_NAME)

    for n, stem in enumerate(FIGURES, start=1):
        im = Image.open(stem.with_suffix(".tif"))
        dpi = im.info.get("dpi", (600, 600))
        rgb = Image.new("RGB", im.size, "white")
        rgb.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
        rgb.save(OUT / f"Figure_{n}.tif", compression="tiff_lzw", dpi=dpi)

    build_letter()
    (OUT / "submission_email.txt").write_text(EMAIL.read_text(encoding="utf-8").strip() + "\n",
                                              encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {DOCX_NAME}, HE_cover_letter.docx, Figure_1.tif, "
          f"Figure_2.tif, submission_email.txt")
    print(f"abstract {n_abs} words; short title {n_short} words; references {len(refs)}; "
          f"word count {strict:,} (text, declarations, references, appendices) and {whole:,} "
          f"(whole document)")
    return 0


def count_words(doc) -> tuple[int, int]:
    """(strict, whole): strict runs from the '1. Introduction' heading (not counted) to the
    'Tables' heading, so it holds the text, declarations, references and appendices, appendix
    tables included; whole counts every word in the document body."""
    strict, whole, on = [], [], False
    for child in doc.element.body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        ps = [child] if tag == "p" else [q for q in child.iter() if q.tag.endswith("}p")]
        for p in ps:
            t = "".join(x.text or "" for x in p.iter() if x.tag.endswith("}t"))
            whole.append(t)
            if t.strip() == "1. Introduction":
                on = True
                continue
            if t.strip() == "Tables":
                on = False
            if on:
                strict.append(t)
    count = lambda xs: sum(1 for tok in " ".join(xs).split() if re.search(r"[^\W_]", tok))
    return count(strict), count(whole)


def build_letter() -> None:
    doc = new_doc()
    for line in LETTER.read_text(encoding="utf-8").splitlines():
        line = line.rstrip()
        if line.startswith("#"):
            continue
        para(doc, line, align=WD_ALIGN_PARAGRAPH.JUSTIFY if len(line) > 80 else None)
    doc.save(OUT / "HE_cover_letter.docx")


if __name__ == "__main__":
    sys.exit(build())
