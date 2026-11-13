"""Check that every table and figure is numbered, cited, and cited in order.

Journals reject on this and reviewers notice it. Both papers have been
renumbered more than once in this project -- paper B once had two tables
sharing a number, and paper A's discussion sections were numbered out of
sequence -- so it is checked rather than read.

For each manuscript it verifies that:
  * captions run 1..n with no gaps and no repeats;
  * every numbered exhibit is cited at least once in the running text;
  * the first citation of exhibit k precedes the first citation of k+1;
  * no citation refers to an exhibit that has no caption.

Usage: python -I verification/check_exhibit_order.py
Exit 1 on any failure, naming the exhibit.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = {
    "paper A": ROOT / "manuscript" / "manuscript_draft_v1.md",
    "paper B": ROOT / "manuscript" / "manuscript_b_draft_v1.md",
}


def body_of(text: str) -> str:
    """Running text: everything before the reference list, minus the author's
    own notes, the caption lines themselves and the table rows."""
    for marker in ("## References", "## Notes for the author"):
        i = text.find(marker)
        if i != -1:
            text = text[:i]
    # The abstract and key messages are not running text, and journals do not
    # allow exhibits to be cited in them. Counting them let a "Figure 1" in
    # paper A's abstract satisfy the first-citation check, which passed for the
    # wrong reason until this was excluded.
    for start, stop in (("## Abstract", "\n## "), ("## Key messages", "\n## "),
                        ("## Highlights", "\n## ")):
        i = text.find(start)
        if i != -1:
            j = text.find(stop, i + len(start))
            text = text[:i] + (text[j:] if j != -1 else "")
    text = re.sub(r"(?m)^\*\*(Table|Figure) \d+\..*$", "", text)   # captions
    text = re.sub(r"(?m)^\|.*$", "", text)                          # table rows
    return text


def check(name: str, path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    body = body_of(text)

    for kind in ("Table", "Figure"):
        captions = [int(n) for n in
                    re.findall(rf"(?m)^\*\*{kind} (\d+)\.", text)]
        if not captions:
            continue
        expected = list(range(1, len(captions) + 1))
        if sorted(captions) != expected:
            errors.append(f"  {name}: {kind} captions are {captions}, "
                          f"expected {expected}")
        if captions != sorted(captions):
            errors.append(f"  {name}: {kind} captions appear out of order: {captions}")

        first: dict[int, int] = {}
        # The negative lookahead keeps a reference to another document's
        # "Table 16.1" from being read as a citation of this paper's Table 16.
        for m in re.finditer(rf"\b{kind}s? (\d+)(?!\.\d)", body):
            k = int(m.group(1))
            first.setdefault(k, m.start())

        for k in sorted(set(captions)):
            if k not in first:
                errors.append(f"  {name}: {kind} {k} has a caption but is "
                              f"never cited in the text")
        for k in sorted(first):
            if k not in captions:
                errors.append(f"  {name}: text cites {kind} {k}, which has no caption")

        cited = [k for k in sorted(first) if k in captions]
        positions = [first[k] for k in cited]
        if positions != sorted(positions):
            out_of_order = [k for k, nxt in zip(cited, cited[1:])
                            if first[k] > first[nxt]]
            errors.append(f"  {name}: {kind}s are first cited out of sequence "
                          f"(at {out_of_order})")
    return errors


def main() -> int:
    errors: list[str] = []
    for name, path in PAPERS.items():
        if not path.exists():
            errors.append(f"  {name}: {path.name} not found")
            continue
        errors += check(name, path)
    if errors:
        print(f"FAILED: {len(errors)} problem(s) with exhibit numbering or order")
        print("\n".join(errors))
        return 1
    print("PASSED: tables and figures in both papers are numbered from 1, "
          "each cited in the text, and cited in ascending order")
    return 0


# Quoted manuscript text carries the rupee and section signs. Under Windows'
# default console encoding, printing them raised UnicodeEncodeError, so a
# check that had found a problem crashed instead of reporting it.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if __name__ == "__main__":
    sys.exit(main())
