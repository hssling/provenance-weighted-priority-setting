"""Fetch WHO's archived data releases for the vintage analysis, at pinned commits.

WHO's Global TB Programme keeps one public repository per annual report
(github.com/GTB-TME/gtbreport2024 ... gtbreport2026). Each holds the dated
snapshot of the country-reported data that report was built on, and the
finance code that turned it into published spending estimates. Comparing the
same country-year value across snapshots measures revision directly, which is
what "vintage" means in the real-time data literature (Croushore and Stark).

The repositories carry no licence, so the files are not redistributed: this
script downloads them from a fixed commit, so the bytes cannot change under the
analysis, and records each file's SHA-256 in data/vintages/vintage_manifest.csv.
A second run verifies instead of overwriting.

Standard library only. Usage: python -I tools/fetch_vintages.py
"""
from __future__ import annotations

import csv
import hashlib
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "vintages" / "raw"
MANIFEST = ROOT / "data" / "vintages" / "vintage_manifest.csv"

# repository -> (commit, [paths]). Commits are the repositories' HEADs on
# 14 November 2026; pinning them is what makes the download reproducible.
SOURCES: dict[str, tuple[str, list[str]]] = {
    "gtbreport2024": ("afbe537729f227f08d670e0e82b214634f4610af", [
        "data/gtb/snapshot_2024-07-29/finance.rda",
    ]),
    "gtbreport2025": ("666088cac1e20dd1e9e52016ea857a9c48e0ba8d", [
        "data/gtb/snapshot_2025-07-30/finance.rda",
        "finance/output/finance_imputed_constantus_included.rda",
        "finance/2a_clean_raw_data.R",
        "finance/3_prepare_imputed_data.R",
    ]),
    "gtbreport2026": ("11ebd9b09a37cfd1c9a563058dfcb887711bc5e9", [
        "data/gtb/snapshot_2026-08-25/expenditure.rda",
        "finance/output/finance_imputed_constantus_included.rda",
        "finance/2a_clean_raw_data.R",
        "finance/3_prepare_imputed_data.R",
    ]),
}
FIELDS = ["file_id", "local_path", "repository", "commit", "source_path", "url",
          "retrieved_utc", "sha256", "bytes"]


def local_name(repo: str, path: str) -> str:
    return f"{repo}__{path.replace('/', '__')}"


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    known = {}
    if MANIFEST.exists():
        known = {r["local_path"]: r for r in csv.DictReader(MANIFEST.open(encoding="utf-8"))}
    rows, problems = [], []
    for repo, (commit, paths) in SOURCES.items():
        for path in paths:
            dest = RAW / local_name(repo, path)
            rel = dest.relative_to(ROOT).as_posix()
            url = f"https://raw.githubusercontent.com/GTB-TME/{repo}/{commit}/{path}"
            if not dest.exists():
                req = urllib.request.Request(url, headers={"User-Agent": "vintage-fetch/1.0"})
                with urllib.request.urlopen(req, timeout=120) as r:
                    dest.write_bytes(r.read())
                when = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                when = known.get(rel, {}).get("retrieved_utc", "before this run")
            data = dest.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            if rel in known and known[rel]["sha256"] != digest:
                problems.append(f"{rel}: SHA-256 differs from the manifest")
            rows.append({"file_id": f"{repo}:{path}", "local_path": rel, "repository":
                         f"github.com/GTB-TME/{repo}", "commit": commit, "source_path": path,
                         "url": url, "retrieved_utc": when, "sha256": digest,
                         "bytes": len(data)})
            print(f"  {len(data):>9,} B  {digest[:12]}  {rel}")
    if problems:
        print("FAILED:\n  " + "\n  ".join(problems))
        return 1
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"PASSED: {len(rows)} files at pinned commits; manifest {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
