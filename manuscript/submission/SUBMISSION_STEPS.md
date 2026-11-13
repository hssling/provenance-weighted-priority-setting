# Submission steps

Two papers, two journals, submitted independently. Do one completely before starting the other.

Every requirement below was read from the journal's own author-guidelines PDF (both saved in this folder,
neither committed: they are the publishers' copyrighted documents). Nothing here is from memory.

---

## 0. Run the build and the checks

```bash
cd "D:/onehealth amr meta nma/provenance_weighting" && python -I verification/check_all.py
```

```bash
cd "D:/onehealth amr meta nma/provenance_weighting" && python -I manuscript/build_submission.py
```

```bash
cd "D:/onehealth amr meta nma/provenance_weighting" && python figures/make_figures.py
```

The build writes the counts **into the title pages** and converts every upload file to `.docx`. Type the
counts into the portal from there, never from memory. The checks verify, among other things, that each
table and figure is numbered from 1, cited in the text, and cited in ascending order; that no author
identifier survives into a blinded file, including in `.docx` document properties; and that paper B's
result tables still match what the screen prints.

---

## 1. What the two journals require, as verified

| | Paper A — *Health Policy and Planning* | Paper B — *International Journal of Epidemiology* |
|---|---|---|
| Article type | Original Article | Original Article |
| Main text limit | 6,000 words (quantitative or fixed design) | **3,000 words** |
| Abstract limit | 300 words | **250 words** |
| Key Messages | 3–4 bullets | **exactly 3, each one complete sentence** |
| Tables + figures | not specified | **8 maximum** |
| References | not specified | 50 maximum (14 used) |
| Referencing style | **author–date (Harvard)**, alphabetical | numbered, Oxford SCIMED |
| Review model | **double-anonymized** → upload `03_` | **not anonymized**; the main document carries author names → upload `04_` |
| Reporting guideline | EQUATOR recommended | **RECORD required** |
| Language | — | **UK English** (checked; clean) |
| Layout | — | double spaced, 2.5 cm margins, pages numbered, no footnotes in text |

Both journals want **tables and figures in separate files, not inside the main text.**

The table gives each journal's **limits** only. The paper's **current counts** are on its title page,
`01_title_page`, which the build writes on every run — so they cannot go stale the way a typed number does.

---

## 2. Files to upload

```
paper_a/   paper_b/
  01_title_page.docx            title page, with the word count the journal asks for
  02_cover_letter.docx          cover letter
  03_manuscript_blinded.docx    → upload this one for Paper A (double-anonymized)
  04_manuscript_unblinded.docx  → upload this one for Paper B (not anonymized)
  05_RECORD_checklist.docx      reporting checklist
  06_supplementary.docx         supplementary material, online only
  07_tables.docx                every table, with its caption and note, in one separate file
figures/
  figure_a1_two_accounts_of_the_same_shortfall.png   Paper A, Figure 1
  figure_a2_interventions_to_budget_lines.png        Paper A, Figure 2
  figure_b1_screen_flow.png                          Paper B, Figure 1
  figure_b2_repetition_by_dataset.png                Paper B, Figure 2
```

All four figures are 300 dpi PNG and at least 3,600 pixels wide, which is IJE's stated minimum and
comfortably above anything HPP requires. The build asserts both, so a figure cannot silently fall short.

Tables are **already split out** into `07_tables.docx`, as both journals require. Each manuscript keeps a
`[Table N about here]` marker where the table stood, and every in-text citation is left in place. The build
asserts that the number of tables split out equals the number of table captions, so none can be lost.

Figure captions and alt text are already in a `Figure captions` section at the end of each main document,
as IJE specifies; paste the same text into the portal's caption box so the two match exactly.

---

## 3. Fields both portals will ask for

- **Data availability** — written into both manuscripts. Repository
  `https://github.com/hssling/provenance-weighted-priority-setting`, archived at Zenodo,
  **doi:10.5281/zenodo.24187367** (v1.0.0; concept DOI 10.5281/zenodo.24187366 tracks the latest).
  Every input file is listed with its SHA-256 in `data/raw_file_manifest.csv`.
- **Funding** — none. **Competing interests** — none. **Ethics** — not required; published aggregate data only.
- **Generative AI** — declare it. IJE asks for disclosure in the **Methods section as well as** the
  declarations; both papers now carry it in both places.
- **Related submissions** — both cover letters disclose the companion paper, with the measured text
  overlap between them (0.6% and 0.4%), and the IJTB paper now in press.
- **Preprint** — neither paper is preprinted. Decide before submitting.

For Paper A, which is double-anonymized: the blinded file withholds the repository URL and the Zenodo DOI,
because the URL contains the author's username and the DOI resolves to the author record. Give both to the
editor in the confidential comments box.

---

## 4. Before the final button

**Open the PDF the portal generates and read it.** This is the step that has cost this project before. The
portal rebuilds the document from your uploads and what it produces is not always what you sent: check
that tables rendered, that the Key Messages box survived, that ₹, § and en-dashes did not mangle, that the
blinded file really is blinded, and that the reference list is complete and correctly numbered.

Then check specifically:

- no author name, affiliation, ORCID, email, GitHub username or Zenodo DOI anywhere in Paper A's upload;
- the abstract in the portal field matches the abstract in the document, word for word;
- figures appear at the numbers the text cites, in both papers;
- Paper A's reference 6 reads "in press; assigned to a forthcoming issue"; reference 13, the JSSTD paper,
  carries doi:10.25259/JSSTD_120_2026. **That DOI does not resolve yet and that is correct** — Scientific
  Scholar registers it at publication. Do not "fix" it.

---

## 5. After submitting

Record the manuscript ID and tell me; I will update the project memory as was done for IJTB-S-26-01305.

If a revision is requested, the repository is the source of truth. Edit `manuscript/manuscript_*.md`, rerun
`build_submission.py` and `check_all.py`, and never edit a file under `submission/` by hand — it is
generated and will be overwritten.
