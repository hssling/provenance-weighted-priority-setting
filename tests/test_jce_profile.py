"""The Journal of Clinical Epidemiology profile check must fail on each breach it names.

Each test feeds the check a minimal manuscript with one rule broken, so that a check
which passes for the wrong reason is caught here rather than at the journal.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "verification"))
sys.path.insert(0, str(ROOT / "manuscript"))

import check_jce_profile as cj  # noqa: E402
from build_submission import bracket_reference_numbers, blind  # noqa: E402

LIM = cj.LAY["limits"]

GOOD = """# Title

## Abstract

**Background and Objective.** Aim.

**Methods.** Methods.

**Results.** Results.

**Discussion and Conclusion.** Conclusion.

**Keywords:** One; Two; Three

## What is new?

**Key findings**

- Finding one.
- Finding two.

**What this adds to what is known**

- Addition.

**What is the implication and what should change now**

- Change.

## 1. Introduction

Text citing Supplementary Note 1 and then Supplementary Table S1 [1].

## 2. Results

Later text citing Supplementary Notes 2 and 3, and Supplementary Tables S2-S3 [2].

## 3. Conclusions

Done.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

Statement.

## References

1. First.
2. Second.
"""

SUPP = """## Supplementary Note 1. One

**Supplementary Table S1. A.**

## Supplementary Note 2. Two

**Supplementary Table S2. B.**

**Supplementary Table S3. C.**

## Supplementary Note 3. Three
"""

COUNTS = dict(body=2000, abstract=300, references=30, figures=2, tables=5, keywords=7)


def test_limits_pass_and_fail():
    assert cj.check_limits(COUNTS, LIM) == []
    for key, bad in (("body", 3001), ("abstract", 351), ("references", 101),
                     ("figures", 6), ("tables", 6), ("keywords", 8), ("keywords", 0)):
        assert cj.check_limits({**COUNTS, key: bad}, LIM), key


def test_abstract_headings():
    assert cj.check_abstract(GOOD) == []
    assert cj.check_abstract(GOOD.replace("**Methods.**", "**Design.**"))
    assert cj.check_abstract(GOOD.replace("Aim.", "Aim [3]."))


def test_what_is_new_box():
    assert cj.check_what_is_new(GOOD, LIM["what_is_new"]) == []
    missing = GOOD.replace("## What is new?", "## Summary")
    assert cj.check_what_is_new(missing, LIM["what_is_new"])
    too_many = GOOD.replace("- Change.", "- Change.\n- More.\n- More.")
    assert cj.check_what_is_new(too_many, LIM["what_is_new"])
    moved = GOOD.replace("## What is new?", "## Placeholder", 1).replace(
        "## 3. Conclusions", "## What is new?\n\n## 3. Conclusions")
    assert cj.check_what_is_new(moved, LIM["what_is_new"])


def test_highlights():
    ok = ["a" * 85, "b", "c"]
    assert cj.check_highlights(ok, "04_highlights.md", LIM["highlights"], 85) == []
    assert cj.check_highlights(ok, "04_bullets.md", LIM["highlights"], 85)
    assert cj.check_highlights(["a" * 86, "b", "c"], "04_highlights.md", LIM["highlights"], 85)
    assert cj.check_highlights(["a", "b"], "04_highlights.md", LIM["highlights"], 85)
    assert cj.check_highlights(list("abcdef"), "04_highlights.md", LIM["highlights"], 85)


def test_ai_declaration_position():
    assert cj.check_ai_declaration(GOOD.replace("## 3. Conclusions", "## 6. Conclusions")) == []
    after_refs = GOOD.replace("## 3. Conclusions", "## 6. Conclusions")
    head, ai = after_refs.split("## Declaration of generative AI")
    ai_block, refs = ai.split("## References")
    moved = head + "## References" + refs + "\n## Declaration of generative AI" + ai_block
    assert cj.check_ai_declaration(moved)
    assert cj.check_ai_declaration(GOOD.replace(cj.AI_HEADING, "## Use of AI"))


def test_supplementary_order():
    src = GOOD.replace("## 1. Introduction", cj.LAY["body_start"])
    assert cj.check_supplementary_order(src, SUPP) == []
    swapped = src.replace("Supplementary Table S1 [1]", "Supplementary Table S2 [1]").replace(
        "Supplementary Tables S2-S3", "Supplementary Tables S1 and S3")
    assert cj.check_supplementary_order(swapped, SUPP)
    uncited = src.replace("Supplementary Notes 2 and 3", "Supplementary Note 2")
    assert cj.check_supplementary_order(uncited, SUPP)
    misplaced = SUPP.replace("## Supplementary Note 2. Two", "## Supplementary Note 3. Two").replace(
        "## Supplementary Note 3. Three", "## Supplementary Note 2. Three")
    assert cj.check_supplementary_order(src, misplaced)


def test_causal_wording():
    assert cj.check_causal({"text": "Inputs fell; the estimate was lower when they moved."}) == []
    for phrase in ("this caused a fall", "because of restatement", "due to filling",
                   "which led to error", "driven by notifications", "the impact of filling",
                   "the effect of age", "as a result the estimate"):
        assert cj.check_causal({"text": phrase}), phrase


def test_stamped_counts():
    page = "| Tables | 5 |"
    assert cj.check_stamped(page, [(r"\| Tables \| (\d+) \|", 5)], "p") == []
    assert cj.check_stamped(page, [(r"\| Tables \| (\d+) \|", 4)], "p")
    assert cj.check_stamped("no row", [(r"\| Tables \| (\d+) \|", 5)], "p")


def test_reference_list_keeps_square_brackets():
    out = bracket_reference_numbers("Text [1].\n\n## References\n\n1. First.\n2. Second.\n")
    assert "\\[1\\] First." in out and "\\[2\\] Second." in out
    assert "Text [1]." in out


def test_blinding_removes_spaced_initials():
    text = ("**Target journal:** x\n\n**Siddalingaiah H S:** Conceptualization.\n"
            "https://doi.org/10.5281/zenodo.123\n")
    out, _ = blind(text, [r"^\*\*Target journal:\*\*.*$"])
    assert "Siddalingaiah" not in out and "[Author] S" not in out and "zenodo." not in out
