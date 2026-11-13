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

    if errors:
        print(f"FAILED: {len(errors)} mismatch(es) between paper B and the screen")
        print("\n".join(errors))
        return 1
    print(f"PASSED: all {len(LABELS)} rows of paper B's Tables 1 and 2 match "
          f"the screen's current output")
    return 0


if __name__ == "__main__":
    sys.exit(main())
