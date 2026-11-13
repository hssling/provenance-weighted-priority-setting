"""Verify every DOI in both reference lists against Crossref, by title.

A DOI that resolves is not enough: this project has twice caught a DOI that
resolved to the wrong paper (a mosquito-genetics article in place of a TB
review), and once found Crossref's own record wrong ("Financial" for
"Financing", one author for three). So each DOI is resolved and the returned
title is compared word-by-word with the title written in the reference.

Network-dependent, so it is run on demand and not inside check_all.py.
One DOI is expected to fail: 10.25259/JSSTD_120_2026 is assigned by the
journal but not registered until publication. It is listed as such.

Usage: python -I verification/verify_dois.py
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = {
    "paper A": ROOT / "manuscript" / "manuscript_draft_v1.md",
    "paper B": ROOT / "manuscript" / "manuscript_b_draft_v1.md",
}
# Assigned by the publisher, registered only at publication: expected to 404.
NOT_YET_REGISTERED = {"10.25259/jsstd_120_2026"}
# Crossref's record is known to be wrong; PubMed and the article agree on the
# title used in the paper. See manuscript/references_verified.md.
CROSSREF_KNOWN_WRONG = {"10.2471/blt.06.034942"}


def references(text: str) -> list[str]:
    r = text[text.index("## References"):]
    nxt = r.find("\n## ", 5)
    r = r[:nxt] if nxt != -1 else r
    return [ln.strip() for ln in r.split("\n")
            if ln.strip() and not ln.startswith("## ")]


def words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 3}


def crossref_title(doi: str) -> tuple[int, str]:
    req = urllib.request.Request(
        f"https://api.crossref.org/works/{doi}",
        headers={"User-Agent": "reference-verification/1.0 (research use)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            msg = json.load(resp)["message"]
            return 200, (msg.get("title") or [""])[0]
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:                                    # noqa: BLE001
        return 0, str(e)


def main() -> int:
    problems = 0
    for name, path in PAPERS.items():
        refs = references(path.read_text(encoding="utf-8"))
        print(f"\n{name}: {len(refs)} references")
        for ref in refs:
            m = re.search(r"doi:\s*(10\.\S+?)(?:[.;,]?\s*$|[.;,]\s)", ref + " ")
            if not m:
                print(f"  no DOI   {ref[:80]}")
                continue
            doi = m.group(1).rstrip(".")
            key = doi.lower()
            code, title = crossref_title(doi)
            time.sleep(0.3)
            if key in NOT_YET_REGISTERED:
                verdict = "expected 404 (registered at publication)" if code == 404 \
                    else f"NOW REGISTERED ({code}) -- update the reference"
                print(f"  note     {doi}: {verdict}")
                continue
            if code != 200:
                print(f"  FAIL     {doi}: HTTP {code}")
                problems += 1
                continue
            overlap = len(words(title) & words(ref)) / max(1, len(words(title)))
            if key in CROSSREF_KNOWN_WRONG:
                print(f"  known    {doi}: Crossref title {title[:50]!r} is wrong; "
                      f"PubMed-verified title used")
            elif overlap < 0.7:
                print(f"  MISMATCH {doi}: {overlap:.0%} title overlap\n"
                      f"           crossref: {title[:90]}\n"
                      f"           ours:     {ref[:90]}")
                problems += 1
            else:
                print(f"  ok       {doi}  ({overlap:.0%})  {title[:55]}")
    print(f"\n{'FAILED' if problems else 'PASSED'}: {problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
