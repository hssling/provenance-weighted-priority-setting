"""Reject drafting-history language in anything that goes to a journal.

A submitted paper must stand on its own. "An earlier version of this paper
said", "we retract", "corrected here", "we committed it ourselves" all narrate
a revision history no reader has seen, and they are not publication grade.
Corrections belong in the paper as findings or as failure modes of the
method, stated so that they generalise.

This was found by hand three times -- in paper A's discussion, in paper B's
supplement where whole sections had been moved verbatim, and in a cover
letter -- so it is now checked across every submitted file rather than
remembered.

The author's own working notes are excluded: they are never submitted.

Usage: python -I verification/check_language.py
Exit 1 if any submitted file narrates its own drafting history.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
M = ROOT / "manuscript"

FILES = [M / "manuscript_draft_v1.md", M / "manuscript_b_draft_v1.md",
         M / "supplementary_paper_a.md", M / "supplementary_paper_b.md"]
FILES += sorted((M / "submission").glob("paper_*/0[125]_*.md"))

DRAFT_HISTORY = re.compile(
    r"earlier (?:version|draft)s?\b|still earlier|"
    r"\bour (?:first|earlier|previous) (?:reading|claim|version|analysis|draft)|"
    r"\bwe retract|\bretraction\b|\bretracted\b|"
    r"\b(?:is|was|are|were) withdrawn\b|"
    r"\bcorrected here\b|\bwe committed\b|\bthis paper made\b|"
    r"\bfirst analysis\b|\bown earlier drafts?\b|\bin a previous draft\b|"
    r"\bruling [A-Z]{1,2}\b",
    re.I)


def main() -> int:
    hits = []
    for f in FILES:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        i = text.find("## Notes for the author")
        text = text[:i] if i != -1 else text
        for m in DRAFT_HISTORY.finditer(text):
            ctx = text[max(0, m.start() - 45):m.end() + 30].replace("\n", " ")
            hits.append(f"  {f.relative_to(ROOT)}: ...{ctx}...")
    if hits:
        print(f"FAILED: {len(hits)} passage(s) narrate the drafting history")
        print("\n".join(hits))
        return 1
    print(f"PASSED: none of {len(FILES)} submitted files narrates its own drafting history")
    return 0


# Quoted manuscript text carries the rupee and section signs. Under Windows'
# default console encoding, printing them raised UnicodeEncodeError, so a
# check that had found a problem crashed instead of reporting it.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if __name__ == "__main__":
    sys.exit(main())
