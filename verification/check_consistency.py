"""Cross-examine every submission asset against the manuscript it belongs to.

Each paper travels as several documents -- manuscript, title page, cover
letter, RECORD checklist, supplement -- and the same facts recur across them.
They drifted repeatedly during revision, each time caught only when someone
happened to look: a title page claiming 0 figures for papers with two, a cover
letter still giving a headline the paper had overturned, a README with stale
table counts. This check makes the agreement mechanical.

For each paper it verifies that:
  1. the title is identical in the manuscript, title page, cover letter,
     RECORD checklist and supplement;
  2. the target journal is the same in the manuscript header, title page and
     cover letter;
  3. the author's name, ORCID and email agree everywhere they appear;
  4. every Zenodo DOI cited is the deposit's version or concept DOI;
  5. the title page's counts equal counts taken afresh from the manuscript;
  6. every number in the abstract, the key messages and the cover letter is
     supported by the body of the paper or its supplement -- a number stated
     in a summary and nowhere in the results is stale or unsupported.

Usage: python -I verification/check_consistency.py
Exit 1 on any disagreement, naming the asset and the fact.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "manuscript"))
from submission_layout import LAYOUT  # noqa: E402
M = ROOT / "manuscript"
S = M / "submission"
PAPERS = {
    "paper A": dict(src=M / "manuscript_draft_v1.md", supp=M / "supplementary_paper_a.md",
                    folder=S / "paper_a", intro="## 1. Introduction"),
    "paper B": dict(src=M / "manuscript_b_draft_v1.md", supp=M / "supplementary_paper_b.md",
                    folder=S / "paper_b", intro="## 1. Background"),
}
DEPOSIT_DOIS = {"10.5281/zenodo.24187367", "10.5281/zenodo.24187366"}
AUTHOR = {"name": "Siddalingaiah H S", "orcid": "0000-0002-4771-8285",
          "email": "hssling@yahoo.com"}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def norm(s: str) -> str:
    """Compare titles ignoring markdown emphasis, dash style and spacing."""
    s = re.sub(r"[*_`]", "", s)
    s = s.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def section(text: str, start: str, stop: str = "\n## ") -> str:
    i = text.find(start)
    if i == -1:
        return ""
    j = text.find(stop, i + len(start))
    return text[i:j if j != -1 else len(text)]


# ---- 6: numbers in summaries must be supported by the body -----------------
NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d+))?(?![\w])")


def numbers(text: str) -> list[tuple[float, int, str]]:
    """(value, decimal places, as written) for every number worth checking.
    Bare years, small integers and reference markers are excluded: they are
    too common to carry signal."""
    out = []
    text = re.sub(r"\[\d+(?:\s*,\s*\d+)*\]", " ", text)            # [3,4] citations
    text = re.sub(r"10\.\d{4,}/\S+", " ", text)                      # DOIs
    for m in NUM.finditer(text):
        whole, dec = m.group(1).replace(",", ""), m.group(2)
        val = float(whole + ("." + dec if dec else ""))
        if not dec and 1900 <= val <= 2099:
            continue                                                 # a year
        if not dec and val < 10:
            continue                                                 # small integer
        out.append((val, len(dec) if dec else 0, m.group(0)))
    return out


def supported(val: float, places: int, body_vals: list[float]) -> bool:
    """A summary may round: 18,388 is supported by 18,388.23 in the body."""
    return any(round(b, places) == round(val, places) for b in body_vals)


def check_stated_overlap() -> list[str]:
    """Each cover letter tells the editor how much text the two papers share.
    The figure is computed, and it moves whenever either paper is edited:
    paper B's letter still said 0.4% after a cut to the word limit and some
    shared boilerplate had taken it to 1.0%. Recompute with the self-
    similarity screen's own method and require the letters to match."""
    sys.path.insert(0, str(ROOT / "verification"))
    import check_self_similarity as ss
    errs = []
    a_src, b_src = PAPERS["paper A"]["src"], PAPERS["paper B"]["src"]
    sh = {k: ss.shingles(ss.normalise(ss.body_only(ss.read_any(v))))
          for k, v in (("A", a_src), ("B", b_src))}
    measured = {"A": 100 * len(sh["A"] & sh["B"]) / len(sh["A"]),
                "B": 100 * len(sh["B"] & sh["A"]) / len(sh["B"])}
    for key, folder in (("A", S / "paper_a"), ("B", S / "paper_b")):
        m = re.search(r"overlap screen between them returns (\d+\.\d)%",
                      read(folder / LAYOUT[folder.name]["cover"]))
        if not m:
            errs.append(f"  paper {key}: cover letter states no overlap figure")
        elif abs(float(m.group(1)) - round(measured[key], 1)) > 1e-9:
            errs.append(f"  paper {key}: cover letter states {m.group(1)}% overlap with "
                        f"its companion; measured now {measured[key]:.1f}%")
    return errs


def main() -> int:
    errs: list[str] = []
    for name, p in PAPERS.items():
        src = read(p["src"])
        f = p["folder"]
        lay = LAYOUT[f.name]
        title_page, cover = read(f / lay["title_page"]), read(f / lay["cover"])
        record, supp = read(f / lay["record"]), read(p["supp"])

        # 1. title -------------------------------------------------------------
        title = norm(re.search(r"(?m)^# (.+)$", src).group(1))
        for label, text, pat in (
                ("title page", title_page, r"\*\*Title\.\*\*\s*(.+)"),
                ("cover letter", cover, r"\"([^\"]{30,})\""),
                ("RECORD checklist", record, r"\*\*Manuscript\.\*\*\s*(.+)"),
                ("supplement", supp, r"(?m)^\*\*(.{30,})\*\*\s*$")):
            m = re.search(pat, text)
            got = norm(m.group(1)).rstrip(".") if m else ""
            if got != title.rstrip("."):
                errs.append(f"  {name}: {label} title differs from the manuscript\n"
                            f"      manuscript: {title[:90]}\n      {label}: {got[:90] or '(none)'}")

        # 2. journal -----------------------------------------------------------
        j_src = re.search(r"\*\*Target journal:\*\*\s*\*([^*]+)\*", src)
        j_tp = re.search(r"\*\*Target journal\.\*\*\s*\*([^*]+)\*", title_page)
        j_cl = re.search(r"(?:To the Editors|The Editor-in-Chief), \*([^*]+)\*", cover)
        names = {k: (v.group(1).strip() if v else None)
                 for k, v in (("manuscript", j_src), ("title page", j_tp), ("cover letter", j_cl))}
        if len(set(names.values())) != 1 or None in names.values():
            errs.append(f"  {name}: target journal disagrees: {names}")

        # 3. author ------------------------------------------------------------
        for label, text in (("manuscript", src), ("title page", title_page), ("cover letter", cover)):
            if AUTHOR["orcid"] not in text:
                errs.append(f"  {name}: {label} lacks the ORCID {AUTHOR['orcid']}")
            if AUTHOR["email"] not in text:
                errs.append(f"  {name}: {label} lacks the email {AUTHOR['email']}")
            if not re.search(r"Siddalingaiah,? H\.? ?S", text):
                errs.append(f"  {name}: {label} does not name the author as Siddalingaiah H S")

        # 4. deposit DOI -------------------------------------------------------
        for label, text in (("manuscript", src), ("title page", title_page),
                            ("cover letter", cover), ("supplement", supp)):
            for d in set(re.findall(r"10\.5281/zenodo\.\d+", text)):
                if d not in DEPOSIT_DOIS:
                    errs.append(f"  {name}: {label} cites {d}, not the deposit's DOI")

        # 5. title-page counts against a fresh count ---------------------------
        fresh = {"Tables": len(re.findall(r"(?m)^\*\*Table \d+\.", src)),
                 "Figures": len(re.findall(r"(?m)^\*\*Figure \d+\.", src))}
        for row, value in fresh.items():
            m = re.search(rf"\| {row} \| (\d+) \|", title_page)
            if not m or int(m.group(1)) != value:
                errs.append(f"  {name}: title page says {row} = "
                            f"{m.group(1) if m else '(missing)'}, the manuscript has {value}")
        figs = list(f.glob(lay["figure_glob"]))
        if len(figs) != fresh["Figures"]:
            errs.append(f"  {name}: {len(figs)} figure files for {fresh['Figures']} figure captions")

        # 6. numbers in summaries ----------------------------------------------
        body = src[src.index(p["intro"]):src.index("## References")] + "\n" + supp
        body_vals = [v for v, _, _ in numbers(body)]
        summaries = {
            "abstract": section(src, "## Abstract"),
            "key messages": section(src, "## Key messages"),
            "highlights": section(src, "## Highlights"),
            "cover letter": section(cover, "**What the paper reports.**", "**Declarations.**"),
        }
        for label, text in summaries.items():
            for val, places, written in numbers(text):
                if not supported(val, places, body_vals):
                    i = text.find(written)
                    ctx = text[max(0, i - 45):i + 25].replace("\n", " ")
                    errs.append(f"  {name}: {label} states {written}, which the body "
                                f"and supplement do not support  ...{ctx}...")

    errs += check_stated_overlap()

    if errs:
        print(f"FAILED: {len(errs)} inconsistenc{'y' if len(errs) == 1 else 'ies'} across the submission")
        print("\n".join(errs))
        return 1
    print("PASSED: titles, journals, author details, deposit DOIs and title-page counts "
          "agree across every asset, and every number in each abstract, key message "
          "and cover letter is supported by the body of its paper")
    return 0


# Quoted manuscript text carries the rupee and section signs. Under Windows'
# default console encoding, printing them raised UnicodeEncodeError, so a
# check that had found a problem crashed instead of reporting it.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if __name__ == "__main__":
    sys.exit(main())
