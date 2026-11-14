# Submission steps

Two papers, two journals, submitted independently. Do one completely before starting the other.

Every requirement below was read from the journal's own guidance, and for Paper A also from the author's
own IJTB upload set for IJTB-S-26-01305 (read-only, `manuscript_3_TB_BOPAS/IJTB_SUBMISSION/`). Publisher
guideline PDFs are copyrighted and are never committed.

---

## 0. Run the build and the checks

```bash
cd "D:/onehealth amr meta nma/provenance_weighting" && python figures/make_figures.py
```

```bash
cd "D:/onehealth amr meta nma/provenance_weighting" && python -I manuscript/build_submission.py
```

```bash
cd "D:/onehealth amr meta nma/provenance_weighting" && python -I verification/check_all.py
```

The build writes the counts **into the title pages**, converts every upload to `.docx`, and rules the tables.
Type counts into the portal from the title page, never from memory.

---

## 1. What the two journals require, as verified

| | Paper A — *Indian Journal of Tuberculosis* | Paper B — *International Journal of Epidemiology* |
|---|---|---|
| Cost to author | **none** (subscription journal; APC only if open access is chosen after acceptance) | none (hybrid) |
| Article type | Original Article | Original Article |
| Main text limit | 3,000 words, Introduction to Conclusions | 3,000 words |
| Abstract | 250 words, Background/Objectives, Methods, Results, Conclusions | 250 words |
| Keywords | **1 to 7** | — |
| Highlights / Key messages | Highlights file, 5 bullets of at most 85 characters (house set) | exactly 3 key messages |
| References | 40 or fewer; superscript in the text, "1." in the list, no brackets (as IJTB prints) | 50 or fewer, numbered |
| Review model | **single-anonymized** → the unblinded manuscript is the primary upload | not anonymized |
| Figures | separate files; **600 dpi TIFF** (Elsevier minimum 500 dpi for line-and-tone art) | 300 dpi PNG, ≥3,600 px |
| Reporting guideline | none named; RECORD supplied | RECORD required |

Current counts are on each title page (`02_Title_Page` for A, `01_title_page` for B).

---

## 2. Paper A — upload to IJTB, in this order

Portal: <https://www.editorialmanager.com/ijtb/default.aspx> (Elsevier Editorial Manager).

```
paper_a/
  01_Cover_Letter.docx               Cover Letter
  02_Title_Page.docx                 Title Page (first page: author, counts, all declarations)
  03_Manuscript.docx                 Manuscript -- unblinded, tables after the references
  04_Highlights.docx                 Highlights
  05_Figure_Captions.docx            Figure captions
  06_Declarations.docx               Conflict of Interest / Declarations
  07_Declaration_of_Interests.docx   Declaration of Interests form -- sign, or replace (below)
  08_Copyright_Transfer.docx         Copyright Transfer Form -- sign
  09_Supplementary_Material.docx     Supplementary (S1-S3)
  10_RECORD_Checklist.docx           Supplementary / reporting checklist
  11_Figure_1.tif                    Figure 1, 600 dpi TIFF
  12_Figure_2.tif                    Figure 2, 600 dpi TIFF
  91_Manuscript_Blinded.docx         optional: only if the portal asks for a blinded file
  92_/93_Figure_N_preview.png        previews; not uploaded
```

Author-only steps, none of which can be done for you:

1. **Declaration of Interests.** The guide says the Elsevier declarations tool "should always be completed":
   generate the form at <https://declarations.elsevier.com/> (all answers "none"), save it over
   `07_Declaration_of_Interests.docx`, or sign the prefilled one if the portal accepts it, as it did for
   IJTB-S-26-01305.
2. **Sign** `08_Copyright_Transfer.docx`.
3. **Run iThenticate** on `03_Manuscript.docx`. The in-repo screen measures 1.8% against IJTB-S-26-01305 and
   2.3% composite with no verbatim run of 40+ words outside reference lists; it is a screen, not iThenticate.
4. **Portal fields:** article type Original Article; keywords exactly as on the title page (six); funding
   none; competing interests none; generative AI declared (text is in `06_Declarations`).

---

## 3. Paper B — upload to IJE

```
paper_b/  01_title_page  02_cover_letter  04_manuscript_unblinded (upload this)  03_manuscript_blinded
          05_RECORD_checklist  06_supplementary  07_tables  08_Figure_1.png  08_Figure_2.png
```

Paper B was rebuilt on 14 November 2026 as a vintage analysis of WHO's archived releases (title: *Restated,
never revised*). Five tables and two figures, within IJE's eight. Its cover letter says the companion goes to
IJTB and that IJTB-S-26-01305 is **under review**.

**Before submitting Paper B: cut a new Zenodo release.** The cited deposit, v1.0.0, predates the vintage
analysis and does not contain `demos/d3_vintages.py` or the fetch tools. Publish a GitHub release (v1.1.0)
so Zenodo mints a new version DOI, then replace 10.5281/zenodo.24187367 with it in Paper B's manuscript,
title page and cover letter. Paper A can keep v1.0.0, which contains everything it reports.

---

## 4. Before the final button

**Open the PDF the portal builds and read it.** Your IJTB-S-26-01305 portal PDF is where broken table
columns were caught. Check specifically:

- in-text citations are **superscript, after punctuation** (IJTB guide: "identify the reference numbers in the text in superscript"; your published IJTB article prints them so), and the reference list prints **1. to 22.** in order, with no brackets, as the printed journal does. Word restarted a list-numbered reference list at 1 on
  the third entry, so the build now writes the numbers as text; confirm they survived;
- tables have rules and no words broken mid-syllable; ₹, §, en-dashes and "Sempé" render;
- the abstract pasted into the portal matches the document word for word;
- reference 10 (IJTB-S-26-01305) reads **under review**, not in press. Elsevier's guide says "in press"
  implies acceptance. Change it only on an acceptance letter;
- reference 16 (JSSTD) carries doi:10.25259/JSSTD_120_2026, which **does not resolve until publication**.
  That is correct; do not "fix" it.

---

## 5. After submitting

Record the manuscript ID and tell me; I will update the project memory.

If a revision is requested, the repository is the source of truth. Edit `manuscript/manuscript_*.md`, rerun
the build and `check_all.py`, and never edit a file under `submission/` by hand except the hand-written
ones (cover letters, title pages, declarations, copyright, RECORD), which the build does not overwrite.
