# Submission steps

Two papers, two journals, submitted independently. Do one completely before starting the other, so a portal
field typed for Paper A is never reused unchecked for Paper B.

Both journals are Oxford University Press titles and both use an online system reached from the journal's own
homepage. **Health Policy and Planning's limits below were read from the journal's own author-guidelines PDF**
(saved in this folder, not committed: it is the publisher's copyrighted document). The *International Journal
of Epidemiology* guidelines have **not** been read — its portal and guideline pages are bot-protected — so
check paper B's limits before uploading. Everything about the manuscripts themselves was verified from the
files and the code.

---

## 0. Run the pre-flight, once, before either submission

```bash
cd "D:/onehealth amr meta nma/provenance_weighting" && python -I verification/check_all.py
```

16 checks. It runs 264 tests, both demos, the self-similarity screen, and the check that paper B's Tables 1
and 2 still match what the screen prints. If anything fails, fix it before submitting — not after.

```bash
cd "D:/onehealth amr meta nma/provenance_weighting" && python -I manuscript/build_submission.py
```

Rebuilds the blinded copies and prints the word, table and reference counts. **Those printed counts are the
ones to type into the portal.** Do not take a count from memory or from an earlier version of this file; a
cover letter in an earlier project claimed 400 dpi for 600 dpi figures because a number was typed.

---

## 1. Decide blinded or unblinded, per journal

*Health Policy and Planning* is **double-anonymized** — confirmed from its guidelines — so paper A uploads
blinded. Paper B's journal has not been checked; confirm before choosing.

- **Single-blind** (reviewers see the author): upload the full source, `manuscript/manuscript_draft_v1.md` or
  `manuscript_b_draft_v1.md`, converted to the required format. These carry the repository URL and the Zenodo
  DOI in full.
- **Double-blind** (author anonymous): upload `submission/paper_X/03_manuscript_blinded.md`. These have the
  author block, affiliation, ORCID, correspondence line and working notes removed, self-citations replaced by
  `[Author]`, and — importantly — the repository URL and Zenodo DOI withheld, because the URL contains the
  author's GitHub username and resolving the DOI shows the author record. Supply both identifiers to the
  editor in the portal's confidential comments field instead.

The blinded Paper B runs 7 words shorter than the source for this reason. The title pages state the source
counts.

---

## 2. Paper A — *Health Policy and Planning*, Original Article

Upload in this order:

| # | file | portal file type |
|---|---|---|
| 1 | `paper_a/02_cover_letter.md` | Cover letter |
| 2 | `paper_a/01_title_page.md` | Title page (not for review) |
| 3 | `paper_a/03_manuscript_blinded.md` *or* the unblinded source | Main document |

Counts to enter: abstract **249 words**, main text **2,944 words**, **2 tables**, **0 figures**,
**16 references**.

Confirmed from the journal's author guidelines on 13 November 2026:

| requirement | HPP asks for | this paper |
|---|---|---|
| Abstract | maximum 300 words | 249, so 51 words of headroom |
| Main text | maximum 6,000 words (quantitative or fixed design) | 2,944 |
| Key Messages | 3–4 bullets | 3 |
| References | **author-date (Harvard)**, alphabetical | converted from Vancouver |
| Review model | **double-anonymized** | upload the blinded copy, `03_` |
| Structure | Title page, Abstract, Key Messages, Introduction, Methods, Results, Discussion, Conclusion, Acknowledgements, References | matches, with Limitations as its own section before Conclusions |

Because review is double-anonymized, **the blinded copy is not optional for this journal.** Give the
repository URL and the Zenodo DOI to the editor in the confidential comments box.

---

## 3. Paper B — *International Journal of Epidemiology*

| # | file | portal file type |
|---|---|---|
| 1 | `paper_b/02_cover_letter.md` | Cover letter |
| 2 | `paper_b/01_title_page.md` | Title page (not for review) |
| 3 | `paper_b/03_manuscript_blinded.md` *or* the unblinded source | Main document |

Counts to enter: abstract **331 words**, main text **4,548 words** (blinded copy 4,541), **6 tables**,
**0 figures**, **13 references**.

Also carries a three-bullet **Key messages** box; IJE uses the same convention.

If IJE declines it, the next targets in order are *Journal of Clinical Epidemiology* and *International
Journal of Health Policy and Management*, both hybrid. *BMC Medical Research Methodology* is the closest
topical fit but charges an article-processing charge, so it is a fallback only.

---

## 4. Fields both portals will ask for

- **Data availability** — already written into each manuscript. The deposit is
  `https://github.com/hssling/provenance-weighted-priority-setting`, archived at Zenodo,
  **doi:10.5281/zenodo.24187367** (v1.0.0, the exact state every number was computed from). The concept DOI
  10.5281/zenodo.24187366 resolves to the latest version.
- **Funding** — none.
- **Competing interests** — none.
- **Ethics** — not required; published aggregate data only, no individual-level records.
- **Generative AI** — declare it. The statement is already in each manuscript and cover letter.
- **Related submissions** — declare both the companion paper and IJTB-S-26-01305. Each cover letter already
  does this in full, including the measured text overlap between the two papers (0.6% and 0.4%).
- **Preprint** — neither paper is preprinted. Decide before submitting, since some journals ask.

---

## 5. Before you press the final button

**Open the PDF the portal generates and read it.** This is the one step that has cost this project before.
The portal rebuilds the document from your uploads, and what it produces is not always what you uploaded:
check that tables rendered, that the Key messages box survived, that special characters (₹, §, en-dashes) did
not mangle, that the blinded copy really is blinded, and that the reference list is complete and numbered.

Then check, specifically:

- No author name, affiliation, ORCID, email, GitHub username or Zenodo DOI anywhere in a double-blind upload.
- The abstract in the portal field matches the abstract in the document.
- Table numbering runs 1 to 5 in Paper B with no repeats — two tables shared a number until this was fixed.
- Reference 13 of Paper A carries the DOI the journal printed on its proof, 10.25259/JSSTD_120_2026, and
  says volume and pages are not yet assigned. The DOI does **not** resolve yet, because the article is in
  production and the DOI is not registered with Crossref until publication. That is expected; do not
  "correct" it. Add volume and pages once the issue is released.

---

## 6. After submitting

Record the manuscript ID. Tell me and I will update the project memory, as was done for IJTB-S-26-01305.

If a revision is requested, the repository is the source of truth: rerun `check_all.py`, make the change in
`manuscript/manuscript_*.md`, rerun `build_submission.py`, and never edit a file under `submission/` by hand
— it is generated and will be overwritten.

---

## Still outstanding

1. **Journal limits** — abstract and main-text limits, and whether either journal wants anything not listed
   here. Bot-protected; check in a browser.
2. **Paper A reference 13**, the JSSTD paper — DOI now carried (10.25259/JSSTD_120_2026, from the R14 proof).
   Volume and pages are still unassigned; add them when the issue is released.
