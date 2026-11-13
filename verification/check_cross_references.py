"""Check every internal cross-reference and placeholder in both papers.

Sections in both manuscripts were moved, merged, renumbered and sent to the
supplement repeatedly during revision. Each move can strand a pointer: a
"§3.4" that no longer exists, a "Supplementary S1c" that was never written,
a "[to be inserted at acceptance]" that a later pass missed. Two of these were
found by reading on the same afternoon -- a placeholder in paper A's methods
that the DOI pass had skipped, and a pointer to a counterfactual in a section
it had left. Reading does not scale; this does.

It verifies that:
  * every "§N" or "§N.N" names a section heading that exists in that paper;
  * every "Supplementary SN" names a section that exists in that paper's
    supplementary file;
  * no placeholder text remains anywhere in the manuscript or supplement.

Usage: python -I verification/check_cross_references.py
Exit 1 on any failure, naming the reference and the file.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
M = ROOT / "manuscript"
PAPERS = {
    "paper A": (M / "manuscript_draft_v1.md", M / "supplementary_paper_a.md"),
    "paper B": (M / "manuscript_b_draft_v1.md", M / "supplementary_paper_b.md"),
}

PLACEHOLDERS = [
    r"to be inserted", r"at acceptance\]", r"\bTODO\b", r"\bTBD\b", r"\bXXX\b",
    r"\[URL", r"\[DOI", r"\[citation needed", r"\?\?\?",
]


def strip_notes(text: str) -> str:
    """The author's own working notes are not submitted and may legitimately
    mention placeholders or old section numbers."""
    i = text.find("## Notes for the author")
    return text[:i] if i != -1 else text


def section_numbers(text: str) -> set[str]:
    """Numbers of every heading like '## 3. Results' or '### 4.1.1 Title'."""
    found = set()
    for m in re.finditer(r"(?m)^#{2,4} (\d+(?:\.\d+)*)\.?\s", text):
        found.add(m.group(1))
    return found


def supplement_sections(text: str) -> set[str]:
    return set(re.findall(r"(?m)^## (S\d+[a-z]?)\.", text))


# "Supplementary S1c and S2" and "Supplementary S1, S2" are ordinary prose, so
# every identifier in an enumerated list counts, not only the first one.
SUPP_LIST = re.compile(r"Supplementary\s+(S\d+[a-z]?(?:(?:\s*,\s*|\s+and\s+|\s*[-–]\s*)S\d+[a-z]?)*)")


def supplementary_refs(text: str) -> list[str]:
    refs: list[str] = []
    for m in SUPP_LIST.finditer(text):
        refs += re.findall(r"S\d+[a-z]?", m.group(1))
    return refs


def main() -> int:
    errors: list[str] = []
    for name, (paper, supp) in PAPERS.items():
        text = strip_notes(paper.read_text(encoding="utf-8"))
        have = section_numbers(text)
        sup_text = supp.read_text(encoding="utf-8") if supp.exists() else ""
        sup_have = supplement_sections(sup_text)

        for m in re.finditer(r"§\s?(\d+(?:\.\d+)*)", text):
            ref = m.group(1)
            if ref not in have:
                ctx = text[max(0, m.start() - 50):m.start() + 15].replace("\n", " ")
                errors.append(f"  {name}: §{ref} does not exist  ...{ctx}...")

        for ref in supplementary_refs(text):
            if not supp.exists():
                errors.append(f"  {name}: cites Supplementary {ref} "
                              f"but {supp.name} does not exist")
            elif ref not in sup_have:
                errors.append(f"  {name}: Supplementary {ref} is cited "
                              f"but {supp.name} has no such section "
                              f"(it has {sorted(sup_have)})")

        # Section numbering must be gapless at every level. Moving a section to
        # the supplement once left paper B running 3.1, 3.2, 3.3, 3.5.
        by_parent: dict[str, list[int]] = {}
        for num in have:
            parent, _, last = num.rpartition(".")
            by_parent.setdefault(parent, []).append(int(last))
        for parent, kids in by_parent.items():
            kids.sort()
            if kids != list(range(1, len(kids) + 1)):
                where = f"under §{parent}" if parent else "at the top level"
                errors.append(f"  {name}: section numbers {where} run {kids}, "
                              f"which has a gap or a repeat")

        # A supplementary section nobody points to is invisible to a reader.
        # Paper A's supplement was generated with three sections and none was
        # cited until this check existed.
        cited = set(supplementary_refs(text))
        cited |= {re.sub(r"[a-z]$", "", c) for c in cited}       # S1c covers S1
        for sec in sorted(sup_have):
            if sec not in cited and re.sub(r"[a-z]$", "", sec) not in cited:
                errors.append(f"  {name}: Supplementary {sec} exists but is never "
                              f"cited in the main text")

        for label, body in ((paper.name, text), (supp.name, sup_text)):
            for pat in PLACEHOLDERS:
                for m in re.finditer(pat, body, re.I):
                    ctx = body[max(0, m.start() - 40):m.end() + 20].replace("\n", " ")
                    errors.append(f"  {name}: placeholder in {label}: ...{ctx}...")

    if errors:
        print(f"FAILED: {len(errors)} broken reference(s) or placeholder(s)")
        print("\n".join(errors))
        return 1
    print("PASSED: every section and supplementary cross-reference resolves, "
          "and no placeholder remains in either paper or supplement")
    return 0


if __name__ == "__main__":
    sys.exit(main())
