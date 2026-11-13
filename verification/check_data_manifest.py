"""Hash every input file and check it against the committed manifest.

A paper arguing that published data carries no provenance metadata cannot
ship its own inputs without any. Until now `data/` held nine files with no
hashes, no retrieval record, and no statement of where six of them came
from: `FINDINGS.md` section 3 documented three.

The manifest records what is actually known and says "not recorded at
acquisition" where it is not, rather than reconstructing a plausible URL.
That distinction is the whole subject of both papers, so inventing one here
would be worse than the gap.

The idea and the column set are taken from the CAG-ICSSR road-safety project
(`research_project/data_raw/raw_file_manifest.csv`), which records authority,
resource page, direct download URL, retrieval date and SHA-256 per file.

Usage:
  python -I verification/check_data_manifest.py          # verify
  python -I verification/check_data_manifest.py --write  # regenerate hashes
Exit 1 if any file's hash differs, or a file is missing or unlisted.
"""
from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MANIFEST = DATA / "raw_file_manifest.csv"

FIELDS = ["file_id", "local_path", "authority", "source", "release_date",
          "retrieved_utc", "sha256", "bytes", "verification_status", "notes"]

UNKNOWN = "not recorded at acquisition"

# What is actually documented. Anything not stated here is recorded as
# unknown; see the module docstring.
KNOWN = {
    "TB_budget_2026-11-12.csv": dict(
        file_id="WHO-TB-BUDGET-2026-11-12",
        authority="WHO Global Tuberculosis Programme",
        source="https://extranet.who.int/tme/",
        release_date="2026-11-12",
        notes="1,720 rows, 215 countries, 2018-2025, 43 columns. "
              "Release date is the date in the file name, not the download date."),
    "TB_expenditure_utilisation_2026-08-25.csv": dict(
        file_id="WHO-TB-EXPENDITURE-2026-08-25",
        authority="WHO Global Tuberculosis Programme",
        source="https://github.com/GTB-TME/gtbreport2026",
        release_date="2026-08-25",
        notes="Downloaded from the Global TB Programme's own report repository. "
              "India 2017-2026; the 2026 row reports exp_tot = 0 with all "
              "components blank."),
    "india_tb_report_table16_1.csv": dict(
        file_id="INDIA-TB-REPORT-2024-T16-1",
        authority="Central TB Division, Ministry of Health and Family Welfare, "
                  "Government of India",
        source="India TB Report 2024, Table 16.1, p.174",
        release_date="2024",
        notes="Hand-entered from the published PDF, not downloaded. Two cells "
              "were OCR-damaged: the PDF prints 305,742 and 188,882, losing only "
              "the decimal point; restored as 3057.42 and 1888.82, confirmed "
              "independently by all three published column totals."),
}

# The remaining WHO files share an authority and a release date, and their
# acquisition route was not recorded at the time.
DEFAULT_WHO = dict(
    authority="WHO Global Tuberculosis Programme",
    source=UNKNOWN,
    notes="Release date is the date in the file name. The download route was "
          "not recorded at acquisition and is not reconstructed here.")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def describe(p: Path) -> dict:
    known = KNOWN.get(p.name)
    if known:
        row = dict(known)
    else:
        row = dict(DEFAULT_WHO)
        row["file_id"] = "WHO-" + p.stem.upper().replace("_", "-")
        row["release_date"] = p.stem[-10:] if p.stem[-10:-6].isdigit() else UNKNOWN
    row.update(local_path=f"data/{p.name}",
               retrieved_utc=UNKNOWN,
               sha256=sha256(p),
               bytes=p.stat().st_size,
               verification_status="hash recorded; contents unmodified since")
    return {k: row.get(k, "") for k in FIELDS}


def inputs() -> list[Path]:
    return sorted(q for q in DATA.glob("*.csv") if q.name != MANIFEST.name)


def write() -> int:
    rows = [describe(p) for p in inputs()]
    with MANIFEST.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {MANIFEST.relative_to(ROOT)} with {len(rows)} files")
    unknown = [r["local_path"] for r in rows if r["source"] == UNKNOWN]
    if unknown:
        print(f"  source not recorded for {len(unknown)}: "
              f"{', '.join(Path(u).name for u in unknown)}")
    return 0


def verify() -> int:
    if not MANIFEST.exists():
        print(f"FAILED: {MANIFEST.relative_to(ROOT)} does not exist; "
              f"run with --write")
        return 1
    listed = {r["local_path"]: r for r in
              csv.DictReader(MANIFEST.open(encoding="utf-8"))}
    on_disk = {f"data/{p.name}": p for p in inputs()}

    errors = []
    for path in sorted(set(listed) | set(on_disk)):
        if path not in listed:
            errors.append(f"  {path}: on disk but not in the manifest")
        elif path not in on_disk:
            errors.append(f"  {path}: in the manifest but not on disk")
        else:
            got = sha256(on_disk[path])
            if got != listed[path]["sha256"]:
                errors.append(f"  {path}: sha256 differs\n"
                              f"      manifest {listed[path]['sha256']}\n"
                              f"      on disk  {got}")
    if errors:
        print(f"FAILED: {len(errors)} problem(s) with the input archive")
        print("\n".join(errors))
        return 1
    n_unknown = sum(1 for r in listed.values() if r["source"] == UNKNOWN)
    print(f"PASSED: {len(listed)} input files match their recorded SHA-256 "
          f"({n_unknown} with no recorded source, stated as such)")
    return 0


if __name__ == "__main__":
    sys.exit(write() if "--write" in sys.argv else verify())
