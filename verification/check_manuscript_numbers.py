"""Check paper B's result tables against what the screen actually prints.

Numbers in this project have drifted before: an abstract measured by hand at
347 words was 331, a self-match reported as 12.6% of 191 pairs was 11.7% of
206, and a per-file median quoted as the headline moved when repeated zeros
were excluded. Each was caught by someone going back to the data. This makes
that step automatic.

It runs `demos/d2_who_data_screen.py` as a subprocess and parses its summary,
rather than recomputing the statistics here. Recomputing would only prove the
check and the screen share an assumption; running the published script proves
the paper matches the artefact it cites.

Usage: python -I verification/check_manuscript_numbers.py
Exit 1 on any mismatch, naming the cell.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCREEN = ROOT / "demos" / "d2_who_data_screen.py"
PAPER_B = ROOT / "manuscript" / "manuscript_b_draft_v1.md"

# The screen's internal keys, and the row labels paper B uses for them.
LABELS = {
    "budget": "Budget",
    "expenditure": "Expenditure and utilisation",
    "notifications": "Notifications",
    "outcomes": "Treatment outcomes",
    "laboratory": "Laboratory diagnostic services",
    "contact_tpt": "Contact tracing / TPT",
}


def run_screen() -> dict[str, dict[str, str]]:
    """Return {dataset: {field: value}} from the screen's per-dataset summary."""
    proc = subprocess.run([sys.executable, "-I", str(SCREEN)],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", cwd=ROOT)
    if proc.returncode != 0:
        raise SystemExit(f"the screen failed to run:\n{proc.stderr[-2000:]}")

    rows: dict[str, dict[str, str]] = {}
    in_block = False
    for line in proc.stdout.splitlines():
        if line.startswith("Per-dataset summary"):
            in_block = True
            continue
        if not in_block:
            continue
        if line.startswith("ALL"):
            break
        parts = line.split()
        if len(parts) == 11 and parts[0] in LABELS:
            rows[parts[0]] = dict(zip(
                ("cont", "cat", "untst", "median", "meas", "mixed", "est",
                 "incl", "nz", "zero_modal"), parts[1:]))
    missing = set(LABELS) - set(rows)
    if missing:
        raise SystemExit(f"screen output did not yield: {sorted(missing)}")
    return rows


def paper_rows(start_label: str, n_cols: int) -> dict[str, list[str]]:
    """Pull the table whose first data row is `start_label`, as plain cells."""
    text = PAPER_B.read_text(encoding="utf-8")
    out: dict[str, list[str]] = {}
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip().replace("**", "") for c in line.strip("|").split("|")]
        if len(cells) != n_cols or cells[0] not in LABELS.values():
            continue
        if cells[0] in out:          # a later table reusing the same labels
            continue
        out[cells[0]] = cells
    return out


def check(name: str, got: str, want: str, errors: list[str]) -> None:
    if got != want:
        errors.append(f"  {name}: paper says {want!r}, screen says {got!r}")


def main() -> int:
    screen = run_screen()
    errors: list[str] = []

    t5 = paper_rows("Budget", 9)      # Table 5, the screen, nine columns
    for key, label in LABELS.items():
        s = screen[key]
        if label not in t5:
            errors.append(f"  Table 5: no row for {label!r}")
        else:
            cells = t5[label]
            for i, field in enumerate(
                    ("cont", "cat", "untst", "median", "meas", "mixed", "est", "incl"), start=1):
                check(f"Table 5 {label} col {i}", s[field], cells[i], errors)

    errors += check_vintage_tables()
    errors += check_vintage_prose()
    errors += check_activity_counts()
    errors += check_dictionary_count()

    if errors:
        print(f"FAILED: {len(errors)} mismatch(es) between the papers and the code")
        print("\n".join(errors))
        return 1
    print(f"PASSED: paper B's Tables 1-4 and Supplementary Table S1 match a fresh rendering "
          f"from the vintage analysis, every derived number in its text matches the code, "
          f"all {len(LABELS)} rows of Table 5 match the screen, and every count of "
          f"budget_prog's activities in paper A matches the collection form")
    return 0


def check_vintage_tables() -> list[str]:
    """Paper B's Tables 1-4 are rendered by manuscript/make_tables_b.py. The
    manuscript must carry each block exactly as a fresh rendering gives it,
    and the supplement must carry Supplementary Table S1."""
    sys.path.insert(0, str(ROOT / "manuscript"))
    import make_tables_b as mt
    blocks = mt.render()
    paper = PAPER_B.read_text(encoding="utf-8")
    supp = (ROOT / "manuscript" / "supplementary_paper_b.md").read_text(encoding="utf-8")
    errs = []
    for name, block in blocks.items():
        where, text = ("supplement", supp) if name.endswith("S1") else ("manuscript", paper)
        if block not in text:
            errs.append(f"  {name}: the {where} differs from a fresh rendering; "
                        f"rerun manuscript/make_tables_b.py and paste the block")
    return errs


def check_vintage_prose() -> list[str]:
    """Each derived number paper B states in its running text, as the code
    computes it now. A sentence carrying a stale figure fails here."""
    sys.path.insert(0, str(ROOT / "demos"))
    import d3_vintages as d3
    R = d3.results()
    paper = PAPER_B.read_text(encoding="utf-8")
    pct = lambda a, b: f"{100 * a / b:.1f}%"

    def span(group: str) -> str:
        v = [100 * r["identical"] / r["pairs"] for r in R["restatement"] if r["group"] == group]
        return f"{min(v):.1f}-{max(v):.1f}%"

    util_rev = [r for r in R["revision"] if r["group"] == "util"]
    cnt_rev = [r for r in R["revision"] if r["group"] == "counted"]
    rr = R["restated_then_revised"]
    f = R["filling"]["2026"]
    used = sum(n for s, n in f.items() if s != "absent")
    sup = f["filled_earlier"] + f["filled_later"] + f["filled_other"] + f["overridden"]
    last = R["latest"]["2026"]
    cons = [r for r in R["consequence"]["2026"] if d3.WINDOW_START <= r["year"] <= last]
    c = cons[-1]
    ind = R["india"]
    share = lambda k: [100 * r[k] / r["ghs"] for r in cons]
    care = [100 * r["ghs"] / r["total"] for r in cons]
    want = {
        "utilisation values never revised": f"None of {sum(r['pairs'] for r in util_rev):,} utilisation values",
        "expenditure values compared": f"Of {sum(r['pairs'] for r in cnt_rev):,} expenditure values compared, "
                                       f"{['zero', 'one', 'two', 'three', 'four'][sum(r['changed'] for r in cnt_rev)]} changed",
        "restatement, utilisation": span("util"),
        "restatement, expenditure": span("counted"),
        "restated then revised": f"none of the {sum(r['restated_2024'] for r in rr):,} utilisation values",
        "WHO-supplied share": f"{sup:,} of the {used:,} utilisation values WHO used for "
                              f"{d3.WINDOW_START}-{last} ({pct(sup, used)})",
        "filled earlier": f"from an earlier year ({f['filled_earlier']:,})",
        "filled later": f"{f['filled_later']:,} came from a later year",
        "overridden": f"{f['overridden']:,} replaced a reported value",
        "care share of total": f"{min(care):.1f}-{max(care):.1f}% of total funding",
        "care estimate": f"US$ {c['ghs'] / 1e9:.2f} billion of US$ {c['total'] / 1e9:.2f} billion",
        "new share": f"{pct(c['new'], c['ghs'])} was computed from inputs newly reported",
        "restated share": f"{pct(c['restated'], c['ghs'])} from inputs restated",
        "WHO share": f"{pct(c['WHO-supplied'], c['ghs'])} from inputs WHO supplied",
        "new range": f"from {min(share('new')):.1f}% to {max(share('new')):.1f}%",
        "lenient range": f"{min(share('new_any')):.1f}-{max(share('new_any')):.1f}%",
        "India amount": f"US$ {ind['care_latest'] / 1e6:.0f} million in {last} "
                        f"({pct(ind['care_latest'], c['ghs'])} of the care estimate)",
        "India last year": f"last reported its utilisation inputs for {ind['last_reported']}",
        "India first year": f"its {ind['first_year_of_values']}, {ind['first_year_of_values'] + 1} "
                            f"and {ind['last_reported']} entries were identical",
    }
    errs = []
    for label, s in want.items():
        if s not in paper:
            errs.append(f"  paper B text: expected {label} as {s!r}")
    # India must be the largest single contribution, as the text says
    top = max(((d3.num(r["c_ghs"]) or 0.0), r["iso3"]) for r in d3.rows("proc2026")
              if int(r["year"]) == last)
    if top[1] != "IND" and "largest single contribution, India" in paper:
        errs.append(f"  paper B text: India is not the largest contributor in {last} ({top[1]} is)")
    return errs


WORDS = {w: n for n, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen "
    "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


def check_activity_counts() -> list[str]:
    """Paper A says how many activities WHO's form pools into budget_prog,
    in several phrasings. The count was typed as fourteen and was wrong --
    the form lists fifteen -- and the error had reached the text, a figure
    and the cover letter. The true count is read from the code, which counts
    it from the form, and every phrasing must agree with it:
      a total ("pools fifteen activities", "one of fifteen activities")
      must equal the count;
      "N other activities" must be the count less one (one intervention's
      view) or less three (the three pooled interventions together)."""
    sys.path.insert(0, str(ROOT / "src"))
    from provenance.existence import BUDGET_PROG_ACTIVITIES as total
    errs = []
    files = [ROOT / "manuscript" / "manuscript_draft_v1.md",
             ROOT / "manuscript" / "submission" / "paper_a" / "01_Cover_Letter.md"]
    num = r"(\d+|" + "|".join(WORDS) + r")"
    for f in files:
        text = f.read_text(encoding="utf-8")
        i = text.find("## Notes for the author")
        text = text[:i] if i != -1 else text
        for m in re.finditer(rf"(?i)\b{num} other activities\b", text):
            n = int(m.group(1)) if m.group(1).isdigit() else WORDS[m.group(1).lower()]
            if n not in (total - 1, total - 3):
                errs.append(f"  {f.name}: '{m.group(0)}' -- expected {total - 1} or "
                            f"{total - 3} (form lists {total})")
        for m in re.finditer(rf"(?i)\b(?:pools?|pooling|one of|absorbs?|among)\s+{num}\s+(?:pooled\s+)?activities"
                             rf"|\b{num}\s+(?:pooled\s+)?activities\s+(?:pooled|in one number)", text):
            word = next(g for g in m.groups() if g)
            n = int(word) if word.isdigit() else WORDS[word.lower()]
            if n != total:
                errs.append(f"  {f.name}: '{m.group(0)}' -- the form lists {total}")
    return errs


def check_dictionary_count() -> list[str]:
    """Paper A states how many interventions would have no budget line if the
    data dictionary, not the collection form, defined the lines. It was once
    typed as six, which silently counted a separate mapping error as a
    dictionary effect; the true figure is derived in the code. Every sentence
    that ties a no-line count to the dictionary must agree with it."""
    sys.path.insert(0, str(ROOT / "src"))
    from provenance.existence import TB_BUDGET_NO_LINE_BY_DICTIONARY as by_dict
    want = len(by_dict)
    errs, seen = [], 0
    num = r"(\d+|" + "|".join(WORDS) + r")"
    pat = re.compile(rf"(?is)dictionary[^.]{{0,90}}?\b{num} (?:interventions )?(?:would )?"
                     rf"have no (?:budget )?line")
    for f in (ROOT / "manuscript" / "manuscript_draft_v1.md",
              ROOT / "manuscript" / "submission" / "paper_a" / "01_Cover_Letter.md"):
        text = f.read_text(encoding="utf-8")
        i = text.find("## Notes for the author")
        text = text[:i] if i != -1 else text
        for m in pat.finditer(text):
            seen += 1
            n = int(m.group(1)) if m.group(1).isdigit() else WORDS[m.group(1).lower()]
            if n != want:
                errs.append(f"  {f.name}: '...{m.group(0)[-60:]}' -- the code derives {want}")
    if not seen:
        errs.append("  no sentence states the dictionary no-line count; the pattern "
                    "may no longer match the wording")
    return errs


# Quoted manuscript text carries the rupee and section signs. Under Windows'
# default console encoding, printing them raised UnicodeEncodeError, so a
# check that had found a problem crashed instead of reporting it.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if __name__ == "__main__":
    sys.exit(main())
