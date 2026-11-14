# Submission set

Two independent papers from one project. They share one dataset and are written to stand alone; the measured
text overlap between them is stated in each cover letter and rechecked by `verification/check_consistency.py`.

| | Paper A | Paper B |
|---|---|---|
| title | What a tuberculosis budget cannot see | Restated, never revised |
| target | *Indian Journal of Tuberculosis*, Original Article | *International Journal of Epidemiology*, Original Article |
| layout | IJTB house set (as IJTB-S-26-01305) | generic set |

File names by role for each paper are in `manuscript/submission_layout.py`; the build and every check read
them from there. Current counts are on each title page, written by `manuscript/build_submission.py` on every
run, and are deliberately not repeated here. How to upload: `SUBMISSION_STEPS.md`.

## What is generated and what is hand-written

Generated on every build (never edit by hand): both manuscripts, the blinded copies, Paper A's highlights,
figure captions and supplement, Paper B's tables file and supplement (from `make_supplementary_b.py`
and its template), Paper B's Tables 1-4 (from `make_tables_b.py`, checked verbatim), all figures, and
every `.docx`. Paper B's vintage analysis needs WHO's archived files: run `tools/fetch_vintages.py`, then
`Rscript tools/convert_vintages.R`; both are verified by digest on every `check_all.py` run.

Hand-written, and checked by the suite: cover letters, title pages, Paper A's declarations, declaration of
interests and copyright transfer, and both RECORD checklists.

## Verified before submission

- **Every number regenerates from code**, including the counts that drifted when typed: budget_prog's fifteen
  activities and the five interventions with no line under the dictionary are both derived in
  `src/provenance/existence.py` and checked against every sentence that states them.
- **References.** Numbered in order of first citation, each URL with an access date, each journal article with
  a DOI that resolves (`verification/verify_dois.py`, on demand).
- **Rendered, not only built.** Both manuscripts were exported through Word to PDF and the reference numbering
  read back from the PDF.
- **Self-similarity** against each other and five prior manuscripts by the same author, failing on any verbatim
  run of 40+ words. A screen, not iThenticate.

## Deposit

Zenodo, from GitHub release v1.0.0: version DOI **10.5281/zenodo.24187367** (cite this); concept DOI
10.5281/zenodo.24187366. Blinded copies withhold the author's repository URL and the DOI; WHO's own GitHub
repository, cited for the data collection form, is kept.
