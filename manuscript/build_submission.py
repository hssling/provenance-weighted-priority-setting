"""Build the per-journal submission set from the two manuscript sources.

Everything here is derived, never hand-maintained, so a correction to a
manuscript cannot leave a stale blinded copy or a wrong word count behind.
That failure mode has already cost this project once: a cover letter claimed
400 dpi for 600 dpi figures because the number was typed, not derived.

Writes manuscript/submission/paper_{a,b}/03_manuscript_blinded.md and prints
the counts the title pages must state.

Usage: python -I manuscript/build_submission.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "submission"

PAPERS = {
    "paper_a": ("manuscript_draft_v1.md", "## 1. Introduction"),
    "paper_b": ("manuscript_b_draft_v1.md", "## 1. Background"),
}

# Lines identifying the author. Removed from the blinded copy; each must be
# found, or the blinding is silently incomplete.
IDENTIFYING = [
    r"^\*\*Author:\*\*.*$",
    r"^Department of Community Medicine.*$",
    r"^Correspondence:.*$",
    r"^\*\*Target journal:\*\*.*$",
]


def count_words(text: str) -> int:
    text = re.sub(r"^\|.*$", "", text, flags=re.M)        # tables
    text = re.sub(r"\*\*|`|#", "", text)
    return len(text.split())


def section(text: str, start: str, end: str) -> str:
    i, j = text.index(start), text.index(end)
    return text[i + len(start):j]


def blind(text: str) -> tuple[str, int]:
    removed = 0
    for pat in IDENTIFYING:
        text, n = re.subn(pat, "", text, flags=re.M)
        if n == 0:
            raise SystemExit(f"blinding pattern never matched: {pat}")
        removed += n
    # the author's own working notes never go to a journal
    i = text.find("## Notes for the author")
    if i != -1:
        text = text[:i].rstrip() + "\n"
    # self-citations that name the author
    text = re.sub(r"Siddalingaiah HS?\.?", "[Author]", text)
    # The deposit identifiers de-anonymise the submission: the repository URL
    # carries the author's username, and resolving the DOI shows the author
    # record. A journal reviewing blind expects these to be withheld and given
    # to the editor instead. The unblinded source keeps them in full.
    text = re.sub(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
                  "[repository URL withheld for blind review]", text)
    text = re.sub(r"doi:10\.5281/zenodo\.[0-9]+",
                  "[archive DOI withheld for blind review]", text)
    # tidy what those substitutions leave behind
    text = text.replace("[repository URL withheld for blind review] and archived at Zenodo, "
                        "[archive DOI withheld for blind review]",
                        "[repository and archive DOI withheld for blind review]")
    text = re.sub(r" \(release v[0-9.]+; the concept DOI "
                  r"\[archive DOI withheld for blind review\][^)]*\)", "", text)
    text = re.sub(r" +([.,;])", r"\1", text)      # space left before punctuation
    return re.sub(r"\n{3,}", "\n\n", text), removed


def main() -> int:
    OUT.mkdir(exist_ok=True)
    print(f"{'paper':<9}{'abstract':>10}{'body':>8}{'refs':>6}{'tables':>8}  blinded to")
    for key, (fname, intro) in PAPERS.items():
        src = (HERE / fname).read_text(encoding="utf-8")
        abstract = count_words(section(src, "## Abstract", "**Keywords")
                               if "**Keywords" in src else
                               section(src, "## Abstract", "\n---"))
        body = count_words(section(src, intro, "## References"))
        reflist = src.split('## References')[1]
        nxt = reflist.find(chr(10) + '## ')
        if nxt != -1:
            reflist = reflist[:nxt]
        refs = len(re.findall(r'^\d+\. ', reflist, flags=re.M))
        tables = len(re.findall(r"^\*\*Table \d+\.", src, flags=re.M))

        text, _ = blind(src)
        d = OUT / key
        d.mkdir(exist_ok=True)
        dest = d / "03_manuscript_blinded.md"
        dest.write_text(text, encoding="utf-8")
        for leak in ("Siddalingaiah", "hssling", "ORCID", "Shridevi", "0000-0002",
                     "github.com", "zenodo."):
            assert leak not in text, f"{key}: blinded copy still contains {leak!r}"
        print(f"{key:<9}{abstract:>10}{body:>8}{refs:>6}{tables:>8}  {dest.relative_to(HERE)}")
    print("\nState these counts on the title pages. Do not retype them from memory.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
