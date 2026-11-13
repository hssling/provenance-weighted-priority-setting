"""Apply journal table formatting directly to a built DOCX.

Pandoc's default output gives every table `<w:tblStyle w:val="Table"/>` but
ships no matching style definition, so Word falls back to no borders at all —
the manuscript's three tables arrived as bare floating text. Supplying a
modified `--reference-doc` did not fix it: pandoc dropped the table style from
the output's styles.xml even though the reference document was valid.

So the borders are written into each table directly, which Word honours
regardless of style resolution. The convention is the one journals use
("booktabs"): a rule above the header, a rule below the header, a rule under
the last row, no vertical rules and no interior grid. The header row is bolded
and a little cell padding keeps text off the rules.

Usage:  python style_docx_tables.py <file.docx> [<file.docx> ...]
"""
from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path

TBL_BORDERS = (
    "<w:tblBorders>"
    '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
    '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
    '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
    '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
    '<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
    '<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
    "</w:tblBorders>"
    "<w:tblCellMar>"
    '<w:top w:w="60" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
    '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="108" w:type="dxa"/>'
    "</w:tblCellMar>"
)

# rule under the header row, and bold header text
HDR_BORDER = ('<w:tcBorders><w:bottom w:val="single" w:sz="8" w:space="0" '
              'w:color="000000"/></w:tcBorders>')


def style_table(tbl: str) -> str:
    # table-level borders
    if "<w:tblBorders>" not in tbl:
        if "<w:tblPr>" in tbl:
            tbl = tbl.replace("<w:tblPr>", "<w:tblPr>" + TBL_BORDERS, 1)
        else:
            tbl = tbl.replace("<w:tbl>", "<w:tbl><w:tblPr>" + TBL_BORDERS + "</w:tblPr>", 1)

    # first row: rule beneath it, bold runs
    first = re.search(r"<w:tr[ >].*?</w:tr>", tbl, re.S)
    if first:
        row = first.group(0)
        new = row
        if "<w:tcBorders>" not in new:
            # pandoc writes an EMPTY, self-closing <w:tcPr /> for header cells,
            # so a rule matching "<w:tcPr>" alone never fires
            new = re.sub(r"<w:tcPr\s*/>", "<w:tcPr>" + HDR_BORDER + "</w:tcPr>", new)
            new = re.sub(r"<w:tcPr>(?!<w:tcBorders>)", "<w:tcPr>" + HDR_BORDER, new)
            new = re.sub(r"<w:tc><w:p", "<w:tc><w:tcPr>" + HDR_BORDER + "</w:tcPr><w:p", new)
        # bold every run in the header row
        new = re.sub(r"<w:rPr>(?!.*?<w:b/>)", "<w:rPr><w:b/>", new)
        new = re.sub(r"<w:r>(?!<w:rPr>)", "<w:r><w:rPr><w:b/></w:rPr>", new)
        tbl = tbl.replace(row, new, 1)

    tbl = fit_columns(tbl)
    return tbl


# Full text width on A4 with the 1-inch margins pandoc's default template uses.
TEXT_WIDTH_TWIPS = 9360  # 6.5 in
MIN_COL_TWIPS = 620      # ~0.43 in; below this even short headers break mid-word


def fit_columns(tbl: str) -> str:
    """Size columns to the text they actually hold.

    Pandoc derives column widths from how wide the columns were drawn in the
    markdown pipe table, which has nothing to do with content. In the priority
    grid that gave "Intervention node" 0.59 in — holding "Molecular diagnostic
    scale-up (Xpert MTB/RIF, MTB/XDR)" — while L, T and M got 0.79 in each to
    hold "0.606". The submission PDF broke words mid-syllable across four
    pages: "Classifi/cation", "Molecu/lar", "bootstr/ap".

    Widths are allocated on the square root of the longest cell text, not on
    the length itself: a column holding 50-character names needs more room than
    one holding 5-character numbers, but not ten times more, because long text
    wraps onto several lines while a number cannot wrap at all.
    """
    grid = re.search(r"<w:tblGrid>.*?</w:tblGrid>", tbl, re.S)
    if not grid:
        return tbl
    ncol = len(re.findall(r"<w:gridCol", grid.group(0)))
    if not ncol:
        return tbl

    # longest run of text in each column, measured over every row
    longest = [0] * ncol
    for row in re.findall(r"<w:tr[ >].*?</w:tr>", tbl, re.S):
        for i, cell in enumerate(re.findall(r"<w:tc>.*?</w:tc>", row, re.S)[:ncol]):
            # <w:t[^>]*> also matches <w:tcPr>, <w:tcW/> and <w:tbl> — the first
            # version of this measured XML tag soup and gave every column
            # the same width.
            text = "".join(re.findall(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", cell, re.S))
            # the longest single unbreakable word matters more than total length
            words = text.split()
            longest[i] = max(longest[i], len(text),
                             max((len(w) for w in words), default=0) * 3)

    weights = [max(w, 1) ** 0.5 for w in longest]
    total = sum(weights)
    widths = [max(MIN_COL_TWIPS, int(TEXT_WIDTH_TWIPS * w / total)) for w in weights]
    # rescale if the minimum pushed the total over the text width
    over = sum(widths) - TEXT_WIDTH_TWIPS
    if over > 0:
        slack = [i for i, w in enumerate(widths) if w > MIN_COL_TWIPS]
        for i in slack:
            widths[i] -= int(over / len(slack))

    new_grid = "<w:tblGrid>" + "".join(
        f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>"
    tbl = tbl.replace(grid.group(0), new_grid, 1)

    # Word honours the grid only under a fixed layout; with autofit it re-flows
    # to its own guess and the widths above are ignored.
    fixed = (f'<w:tblW w:w="{sum(widths)}" w:type="dxa"/>'
             '<w:tblLayout w:type="fixed"/>')
    tbl = re.sub(r"<w:tblW[^>]*/>", "", tbl)
    tbl = re.sub(r"<w:tblLayout[^>]*/>", "", tbl)
    if "<w:tblPr>" in tbl:
        tbl = tbl.replace("<w:tblPr>", "<w:tblPr>" + fixed, 1)

    # every cell must restate its own width under a fixed layout
    for row in re.findall(r"<w:tr[ >].*?</w:tr>", tbl, re.S):
        cells = re.findall(r"<w:tc>.*?</w:tc>", row, re.S)
        newrow = row
        for i, cell in enumerate(cells[:ncol]):
            w = widths[i]
            c = re.sub(r"<w:tcW[^>]*/>", "", cell)
            if "<w:tcPr>" in c:
                c = c.replace("<w:tcPr>", f'<w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>', 1)
            elif "<w:tcPr/>" in c or "<w:tcPr />" in c:
                c = re.sub(r"<w:tcPr\s*/>",
                           f'<w:tcPr><w:tcW w:w="{w}" w:type="dxa"/></w:tcPr>', c, 1)
            else:
                c = c.replace("<w:tc>", f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/></w:tcPr>', 1)
            newrow = newrow.replace(cell, c, 1)
        tbl = tbl.replace(row, newrow, 1)
    return tbl


def shrink_text(tbl: str, half_points: int) -> str:
    """Set an explicit font size on every run in the table. Supplementary data
    tables run to ten columns, where no column allocation can give a 14-letter
    word a full inch; 8pt is the usual answer for dense supplementary tables."""
    sz = f'<w:sz w:val="{half_points}"/><w:szCs w:val="{half_points}"/>'
    tbl = re.sub(r"<w:sz w:val=\"\d+\"/>", "", tbl)
    tbl = re.sub(r"<w:szCs w:val=\"\d+\"/>", "", tbl)
    tbl = re.sub(r"<w:rPr>", "<w:rPr>" + sz, tbl)
    tbl = re.sub(r"<w:r>(?!<w:rPr>)", "<w:r><w:rPr>" + sz + "</w:rPr>", tbl)
    return tbl


def process(path: Path) -> int:
    zin = zipfile.ZipFile(path)
    doc = zin.read("word/document.xml").decode("utf-8")
    tables = re.findall(r"<w:tbl>.*?</w:tbl>", doc, re.S)
    # Supplementary data tables carry up to ten columns; the manuscript's three
    # carry at most seven and stay at body size.
    small = "supplementary" in path.name.lower()
    for t in tables:
        styled = style_table(t)
        if small:
            styled = shrink_text(styled, 16)  # 8pt
        doc = doc.replace(t, styled, 1)
    tmp = path.with_suffix(".tmp.docx")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = doc.encode("utf-8")
            zout.writestr(item, data)
    zin.close()
    shutil.move(tmp, path)
    return len(tables)


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.exists():
            print(f"  skip (missing) {p.name}")
            continue
        n = process(p)
        print(f"  styled {n} table(s) in {p.name}")
