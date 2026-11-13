"""Estimate text-match self-similarity for the two manuscripts in this repo.

Method follows the checker written for the TB-BOPAS submission: normalise,
shingle into overlapping word 8-grams, and measure the share of the target's
distinct shingles that also occur in each comparison document. It is not
iThenticate -- it searches only the author's own prior work, which is the one
component the author can fix before submitting.

The comparison that matters most here is A against B. The two papers share a
dataset and a theme and were written in the same sessions, so they are the
likeliest source of an avoidable self-match.

Usage: python -I verification/check_self_similarity.py
Exit code 1 if any verbatim run of LONG_RUN or more words is found outside a
reference list. It deliberately does not gate on a percentage: no journal
publishes a numeric threshold and inventing one would dress a guess as a rule.
"""
from __future__ import annotations

import html
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUTER = REPO.parent

N = 8            # shingle length, in words
FLAG_PCT = 15.0  # a single source above this share warrants attention
LONG_RUN = 40    # verbatim words: the condition the exit code gates on

PAPER_A = REPO / "manuscript" / "manuscript_draft_v1.md"
PAPER_B = REPO / "manuscript" / "manuscript_b_draft_v1.md"

PRIOR = [
    ("TB-BOPAS, submitted IJTB-S-26-01305",
     OUTER / "manuscript_3_TB_BOPAS/IJTB_SUBMISSION/source/manuscript_IJTB_blinded.md"),
    ("OHB manuscript under review (R1)",
     OUTER / "submission_assets_OHB_bopas/REVISION_R1/01_OHB_Manuscript_BLINDED_R1_CLEAN.docx"),
    ("accepted IJTB review article (IJTB-1410)",
     Path(r"D:/One Health TB/mycobacteria_one_health/IJTB_submission_assets_v7_submission"
          r"/manuscript/IJTB_manuscript_v7.md")),
    ("TPT network meta-analysis (IJTB)",
     Path(r"D:/research-automation/TB_prevention_deliverables/09_outputs/IJTB_submission_assets"
          r"/manuscript/IJTB_manuscript_tpt_nma_v1.md")),
    # Paper A's section 4.3 replicates this paper's fiscal-invisibility finding in a
    # second programme, so it is the likeliest source of an avoidable self-match of
    # anything in the set. The accepted R1 text is used because the journal's own
    # proof PDFs are encrypted and this checker stays on the standard library.
    ("JSSTD NACP-V paper, accepted, in production",
     Path(r"D:/AI Book and Content Writer/STD abd HIV/JSSTD_HIV_STD"
          r"/Revision_R1/Manuscript.md")),
]


def read_any(p: Path) -> str:
    if not p.exists():
        return ""
    if p.suffix.lower() == ".docx":
        x = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8", "ignore")
        x = re.sub(r"</w:p>", "\n", x)
        return html.unescape(re.sub(r"<[^>]+>", "", x))
    return p.read_text(encoding="utf-8", errors="ignore")


def body_only(text: str) -> str:
    """Drop the reference list and the author's own notes. A shared reference
    list is not plagiarism and would otherwise dominate the overlap."""
    for marker in ("## References", "## Notes for the author"):
        i = text.find(marker)
        if i != -1:
            text = text[:i]
    return text


def normalise(t: str) -> list[str]:
    t = t.lower()
    t = re.sub(r"\[[0-9,\s\\]]*\]", " ", t)     # citation markers
    t = re.sub(r"[^a-z0-9%\.\- ]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.split()


def shingles(words: list[str], n: int = N) -> set[tuple[str, ...]]:
    return {tuple(words[i:i + n]) for i in range(max(0, len(words) - n + 1))}


def report(target_label: str, target: Path, sources) -> list[tuple[int, str]]:
    words = normalise(body_only(read_any(target)))
    tgt = shingles(words)
    print(f"\n{'=' * 78}\nTARGET: {target_label} ({target.name})")
    print(f"  {len(words)} normalised words, {len(tgt)} distinct {N}-grams, "
          f"references and author notes excluded")

    union: set[tuple[str, ...]] = set()
    print(f"\n  {'source':<44}{'shared':>10}{'% of target':>14}")
    for label, path in sources:
        text = read_any(path)
        if not text:
            print(f"  {label:<44}{'FILE NOT FOUND':>24}")
            continue
        shared = tgt & shingles(normalise(body_only(text)))
        union |= shared
        pct = 100.0 * len(shared) / len(tgt) if tgt else 0.0
        flag = "  <-- attention" if pct >= FLAG_PCT else ""
        print(f"  {label:<44}{len(shared):>10}{pct:>13.1f}%{flag}")
    total = 100.0 * len(union) / len(tgt) if tgt else 0.0
    print(f"  {'COMBINED (union)':<44}{len(union):>10}{total:>13.1f}%")

    runs, cur = [], []
    for i in range(len(words) - N + 1):
        if tuple(words[i:i + N]) in union:
            cur.append(i)
        else:
            if len(cur) >= 6:
                runs.append((cur[0], cur[-1] + N))
            cur = []
    if cur and len(cur) >= 6:
        runs.append((cur[0], cur[-1] + N))
    runs.sort(key=lambda r: r[1] - r[0], reverse=True)

    print("\n  longest overlapping passages:")
    if not runs:
        print("    none longer than a few words")
    for a, b in runs[:6]:
        print(f"    [{b - a:>3} words] ...{' '.join(words[a:b])[:170]}...")
    return [(b - a, " ".join(words[a:b])) for a, b in runs if b - a >= LONG_RUN]


def main() -> int:
    serious = []
    serious += [("A", n, t) for n, t in report("Paper A, India TB financing", PAPER_A,
                                               [("Paper B (this repo)", PAPER_B)] + PRIOR)]
    serious += [("B", n, t) for n, t in report("Paper B, WHO variable screen", PAPER_B,
                                               [("Paper A (this repo)", PAPER_A)] + PRIOR)]

    print(f"\n{'=' * 78}\nREADING")
    print("  A composite self-match in the teens is normal for a paper that reuses a")
    print("  Methods framework and says so. What gets a manuscript rejected is one")
    print(f"  source contributing a large share, or a verbatim run of {LONG_RUN}+ words.")
    print("  This is a screen, not iThenticate. Run the real check before uploading.")

    if serious:
        print(f"\nFAILED: {len(serious)} verbatim run(s) of {LONG_RUN}+ words")
        for paper, n, text in serious:
            print(f"  paper {paper}, {n} words: ...{text[:170]}...")
        return 1
    print(f"\nPASSED: no verbatim run of {LONG_RUN}+ words outside the reference lists")
    return 0


# Quoted manuscript text carries the rupee and section signs. Under Windows'
# default console encoding, printing them raised UnicodeEncodeError, so a
# check that had found a problem crashed instead of reporting it.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

if __name__ == "__main__":
    sys.exit(main())
