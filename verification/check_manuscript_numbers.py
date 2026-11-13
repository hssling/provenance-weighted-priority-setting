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

    t1 = paper_rows("Budget", 9)      # Table 1, nine columns
    t2 = paper_rows("Budget", 4)      # Table 2, four columns
    for key, label in LABELS.items():
        s = screen[key]
        if label not in t1:
            errors.append(f"  Table 1: no row for {label!r}")
        else:
            cells = t1[label]
            for i, field in enumerate(
                    ("cont", "cat", "untst", "median", "meas", "mixed", "est", "incl"), start=1):
                check(f"Table 1 {label} col {i}", s[field], cells[i], errors)
        if label not in t2:
            errors.append(f"  Table 2: no row for {label!r}")
        else:
            cells = t2[label]
            check(f"Table 2 {label} median", s["median"], cells[1], errors)
            check(f"Table 2 {label} excl 0-0", s["nz"], cells[2], errors)
            check(f"Table 2 {label} zero-modal",
                  s["zero_modal"].replace("/", " / "), cells[3], errors)

    errors += check_activity_counts()
    errors += check_dictionary_count()

    if errors:
        print(f"FAILED: {len(errors)} mismatch(es) between the papers and the code")
        print("\n".join(errors))
        return 1
    print(f"PASSED: all {len(LABELS)} rows of paper B's Tables 1 and 2 match "
          f"the screen's current output, and every count of budget_prog's "
          f"activities in paper A matches the collection form")
    return 0


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
