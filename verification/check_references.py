"""Check citation integrity and reference metadata in both papers.

Paper B uses numbered Vancouver citations; paper A uses Health Policy and
Planning's author-date style. Each needs a different check, and both need the
same metadata rules.

Paper B (numbered):
  * the list is numbered 1..n with no gaps;
  * every reference is cited, and nothing is cited that is not listed;
  * references are numbered in order of first citation in the text.

Paper A (author-date):
  * every in-text citation resolves to exactly one list entry;
  * every list entry is cited at least once;
  * the list is alphabetical by first author, then year.

Both:
  * every reference giving a URL also gives an access date;
  * every journal article carries a DOI, unless it is recorded as in press
    or in production, when none can exist yet.

Usage: python -I verification/check_references.py
Exit 1 on any failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "manuscript" / "manuscript_draft_v1.md"
B = ROOT / "manuscript" / "manuscript_b_draft_v1.md"


def split(text: str) -> tuple[str, list[str], str]:
    """Return (text before the list, list entries, text after the list)."""
    i = text.index("## References")
    j = text.find("\n## ", i + 5)
    j = j if j != -1 else len(text)
    entries = [ln.strip() for ln in text[i:j].split("\n")[1:] if ln.strip()]
    after = text[j:]
    k = after.find("## Notes for the author")
    return text[:i], entries, (after[:k] if k != -1 else after)


def metadata(name: str, entries: list[str]) -> list[str]:
    errs = []
    for e in entries:
        short = e[:70]
        if "http" in e and not re.search(r"accessed \d{1,2} \w+ \d{4}|\[cited \d{4} \w{3} \d{1,2}\]", e):
            errs.append(f"  {name}: URL without an access date: {short}")
        is_article = bool(re.search(r"\*\*\d+\*\*:|\d{4};\d+(\(\d+\))?:", e))
        pending = re.search(r"in press|in production|online ahead of print", e, re.I)
        if is_article and "doi" not in e.lower() and not pending:
            errs.append(f"  {name}: journal article without a DOI: {short}")
    return errs


def check_numbered(text: str) -> list[str]:
    errs = []
    before, entries, after = split(text)
    nums = [int(m.group(1)) for e in entries if (m := re.match(r"(\d+)\. ", e))]
    if nums != list(range(1, len(nums) + 1)):
        errs.append(f"  paper B: reference list numbered {nums}, expected 1..{len(nums)}")
    order: list[int] = []
    # citations in the running text, then in the declarations after the list
    for m in re.finditer(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\]", before + after):
        for part in re.split(r"\s*,\s*", m.group(1)):
            if re.search(r"[–-]", part):
                a, b = (int(x) for x in re.split(r"\s*[–-]\s*", part))
                cited = list(range(a, b + 1))
            else:
                cited = [int(part)]
            for n in cited:
                if n not in order:
                    order.append(n)
    missing = sorted(set(nums) - set(order))
    phantom = sorted(set(order) - set(nums))
    if missing:
        errs.append(f"  paper B: listed but never cited: {missing}")
    if phantom:
        errs.append(f"  paper B: cited but not listed: {phantom}")
    if order != sorted(order):
        errs.append(f"  paper B: not numbered in order of first citation; "
                    f"first-citation order is {order}")
    return errs + metadata("paper B", entries)


def key_of(entry: str) -> tuple[str, str]:
    """(first author surname or corporate name, year-with-suffix)."""
    m = re.match(r"(.+?)\.\s(\d{4}[a-z]?)\.", entry)
    if not m:
        return entry[:20], ""
    head, year = m.group(1), m.group(2)
    if head.startswith("World Health Organization"):
        return "WHO", year
    if head.startswith("Global Fund"):
        return "Global Fund", year
    if head.startswith("Central TB Division"):
        return "Central TB Division", year
    return head.split(",")[0].split(" ")[0], year


def check_author_date(text: str) -> list[str]:
    errs = []
    before, entries, _ = split(text)
    keys = [key_of(e) for e in entries]
    if len(set(keys)) != len(keys):
        errs.append(f"  paper A: two list entries share an author-year key: "
                    f"{[k for k in keys if keys.count(k) > 1]}")

    sort_key = [(e.lower(), key_of(e)[1]) for e in entries]
    if sort_key != sorted(sort_key):
        errs.append("  paper A: reference list is not alphabetical")

    pattern = re.compile(
        r"(?:\(|\b)((?:WHO|Global Fund|Central TB Division|[A-Z][A-Za-z'\-]+)"
        r"(?: et al\.| and [A-Z][A-Za-z'\-]+)?)\s\(?(\d{4}[a-z]?)(?=[\),;])")
    months = {"January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"}
    cited = set()
    for m in pattern.finditer(before):
        name = m.group(1).replace(" et al.", "").split(" and ")[0]
        if name in months:                     # "12 November 2026" is a date
            continue
        k = (name, m.group(2))
        cited.add(k)
        if k not in keys:
            errs.append(f"  paper A: '{m.group(0).lstrip('(')}' has no reference list entry")
    for k, e in zip(keys, entries):
        if k not in cited:
            errs.append(f"  paper A: listed but never cited: {e[:60]}")
    return errs + metadata("paper A", entries)


def main() -> int:
    errs = check_author_date(A.read_text(encoding="utf-8"))
    errs += check_numbered(B.read_text(encoding="utf-8"))
    if errs:
        print(f"FAILED: {len(errs)} reference problem(s)")
        print("\n".join(errs))
        return 1
    print("PASSED: paper A's author-date citations and paper B's numbered citations "
          "all resolve and are all cited; B is in first-citation order, A is "
          "alphabetical; every URL has an access date and every journal article a DOI")
    return 0


if __name__ == "__main__":
    sys.exit(main())
