"""Check the files that are actually uploaded, as the journal will receive them.

Every other check reads the source manuscripts. This one reads the upload
set in manuscript/submission/, Markdown and .docx alike, because the .docx is
what the portal receives. It exists because paper B's upload to IJE carried
two things written for the author alone: a "Target journal" line naming the
alternatives considered, one "held as a fallback", and the entire "Notes for
the author -- not for submission" section. The source keeps both, usefully;
no upload may.

Rules for every upload file:
  * none of the author-only markers below appears;
and for each manuscript (03 blinded, 04 unblinded):
  * the derived word count is on its title section, as IJE requires.

Usage: python -I verification/check_uploads.py
"""
from __future__ import annotations

import html
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "manuscript" / "submission"
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "manuscript"))
from submission_layout import LAYOUT  # noqa: E402

AUTHOR_ONLY = [
    r"\*?\*?Target journal:\*?\*?",          # the internal header line (colon form)
    r"Notes for the author", r"not for submission",
    r"held as a fallback", r"\[done\b", r"\bOPEN:", r"\bTODO\b",
]


def text_of(p: Path) -> str:
    if p.suffix == ".docx":
        x = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8", "ignore")
        return html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"</w:p>", "\n", x)))
    return p.read_text(encoding="utf-8")


def main() -> int:
    errs: list[str] = []
    # Every document in a paper's folder is an upload; the folders hold
    # nothing else. Figures are images and carry no text to check.
    uploads = sorted(f for f in S.glob("paper_*/*") if f.suffix in (".md", ".docx"))
    if not uploads:
        print("FAILED: no upload files found; run manuscript/build_submission.py")
        return 1
    for f in uploads:
        t = text_of(f)
        for pat in AUTHOR_ONLY:
            for m in re.finditer(pat, t, re.I):
                ctx = t[max(0, m.start() - 30):m.end() + 40].replace("\n", " ")
                errs.append(f"  {f.relative_to(S)}: author-only content  ...{ctx}...")
        lay = LAYOUT[f.parent.name]
        names = {Path(lay[k]).stem for k in ("manuscript", "blinded")}
        if f.stem in names and not re.search(
                r"Word count:\s*\*?\*?\s*[\d,]+ words", t):
            errs.append(f"  {f.relative_to(S)}: no word count on the title section")
    if errs:
        print(f"FAILED: {len(errs)} problem(s) in the files that would be uploaded")
        print("\n".join(errs))
        return 1
    print(f"PASSED: none of {len(uploads)} upload files (Markdown and .docx) carries "
          f"author-only content, and every manuscript states its word count")
    return 0


# Quoted manuscript text carries the rupee and section signs.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if __name__ == "__main__":
    sys.exit(main())
