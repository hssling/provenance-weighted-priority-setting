"""Where each paper's upload files live, by role, for the build and every check.

Paper B's Journal of Clinical Epidemiology set ("paper_b_jce") is built by the
"jce" profile in build_submission.py; its sources are kept local, so every
check that reads it skips it cleanly where they are absent.

The two papers go to journals with different house conventions. Paper B
follows the generic set this project started with; paper A follows the
Indian Journal of Tuberculosis house set the author used for IJTB-S-26-01305
(cover letter first, a first page carrying the declarations, highlights,
figure captions, declarations, declaration of interests and copyright
transfer as separate uploads, 600 dpi TIFF figures). Naming the files by role
here, once, means a check cannot pass by reading a file the journal never
receives.
"""
from __future__ import annotations

LAYOUT: dict[str, dict] = {
    "paper_a": {
        "journal": "Indian Journal of Tuberculosis",
        "cover": "01_Cover_Letter.md",
        "title_page": "02_Title_Page.md",
        "manuscript": "03_Manuscript.md",           # unblinded: single-anonymized review
        "highlights": "04_Highlights.md",
        "captions": "05_Figure_Captions.md",
        "declarations": "06_Declarations.md",
        "interests": "07_Declaration_of_Interests.md",
        "copyright": "08_Copyright_Transfer.md",
        "supplement": "09_Supplementary_Material.md",
        "record": "10_RECORD_Checklist.md",
        "blinded": "91_Manuscript_Blinded.md",      # optional upload
        "figure": "{n}_Figure_{k}.tif",             # n = 10 + k
        "preview": "{n}_Figure_{k}_preview.png",    # n = 91 + k
        "figure_glob": "1[1-9]_Figure_*.tif",
        "tables_in_manuscript": True,               # IJTB: tables after the references
        "body_end": "## Contributors",              # IJTB counts Introduction to Conclusions
        "word_count_basis": ("words of main text (Introduction through Conclusions), "
                             "excluding abstract, tables, figure legends, declarations "
                             "and references"),
    },
    # Paper B as submitted to IJE (14 Nov 2026, declined 16 Nov): frozen, never rebuilt.
    "paper_b": {
        "journal": "International Journal of Epidemiology",
        "cover": "02_cover_letter.md",
        "title_page": "01_title_page.md",
        "manuscript": "04_manuscript_unblinded.md",
        "blinded": "03_manuscript_blinded.md",
        "supplement": "06_supplementary.md",
        "record": "05_RECORD_checklist.md",
        "tables_file": "07_tables.md",
        "figure": "08_Figure_{k}.png",
        "figure_glob": "08_Figure_*.png",
        "tables_in_manuscript": False,
        "body_end": "## References",
        "word_count_basis": ("words (main text, excluding abstract, key messages, tables, "
                             "figures, references and declarations)"),
    },
    # Paper B for Tropical Medicine & International Health (hybrid; no page charges).
    "paper_b_tmih": {
        "journal": "Tropical Medicine & International Health",
        "source": "manuscript_b_tmih.md",
        "supplement_source": "supplementary_paper_b_tmih.md",
        "figure_letter": "b",
        "cover": "02_cover_letter.md",
        "title_page": "01_title_page.md",
        "manuscript": "03_manuscript.md",          # TMIH extracts metadata from one manuscript file
        "blinded": "91_manuscript_blinded.md",     # kept for safety; TMIH review is not double-blind
        "supplement": "04_supplementary.md",
        "record": "05_RECORD_checklist.md",
        "tables_file": "06_tables.md",
        "figure": "07_Figure_{k}.png",
        "figure_glob": "07_Figure_*.png",
        "tables_in_manuscript": False,            # TMIH: tables uploaded as their own file
        "body_end": "## References",
        "word_count_basis": ("words (main body, excluding abstract, tables, figure legends, "
                             "references and declarations)"),
        "word_count_anchor": r"(?m)^\*\*Conflict of interest and funding:\*\*.*$",
        # Kept out of the public repository; build_submission.py appends it to the uploads.
        "reviewers": "private/suggested_reviewers_paper_b_tmih.md",
        # Front matter in the paragraph layout TMIH's metadata extraction expects.
        "identifying": [r"^Siddalingaiah H S, MD, Professor$", r"^Department of Community Medicine.*$",
                        r"^\*\*Corresponding author:\*\*.*$", r"^\*\*Target journal:\*\*.*$"],
    },
    # Paper B for the Journal of Clinical Epidemiology (Elsevier, hybrid; Original Research).
    # Sources and uploads are kept local; this entry and the build profile are the tooling.
    "paper_b_jce": {
        "journal": "Journal of Clinical Epidemiology",
        "profile": "jce",
        "source": "manuscript_b_jce.md",
        "supplement_source": "supplementary_paper_b_jce.md",
        "figure_letter": "b",
        "title_page": "01_title_page.md",
        "cover": "02_cover_letter.md",
        "manuscript": "03_manuscript.md",          # single anonymised review: author details kept
        "highlights": "04_highlights.md",          # Elsevier: "highlights" in the file name
        "supplement": "05_supplementary.md",
        "record": "06_RECORD_checklist.md",
        "blinded": "91_manuscript_blinded.md",     # kept in case the portal asks for one
        "figure": "{n:02d}_Figure_{k}.tif",        # n = 6 + k: 07_Figure_1.tif, 08_Figure_2.tif
        "figure_offset": 6,
        "preview": "{n}_Figure_{k}_preview.png",   # n = 91 + k
        "figure_glob": "0[7-9]_Figure_*.tif",
        "tables_in_manuscript": True,             # JCE: tables beside the text that cites them
        "citations": "brackets",                  # JCE: "[3,6]" in line, "[1]" in the list
        "body_start": "## 1. Introduction",
        "body_end": "## CRediT authorship contribution statement",
        "word_count_basis": ("words of main text (Introduction to Conclusions), excluding the abstract, "
                             "the What is new? box, tables, figure captions, declarations and references"),
        "word_count_anchor": r"(?m)^\*\*Corresponding author:\*\*.*$",
        # Working documents kept beside the uploads, never uploaded or converted.
        "working": ["journal_rules.md", "REPORT.md"],
        "limits": {"words": 3000, "abstract": 350, "references": 100, "figures": 5, "tables": 5,
                   "keywords": (1, 7), "highlights": (3, 5), "highlight_chars": 85, "what_is_new": (3, 5)},
        "identifying": [r"^Siddalingaiah H S\^a\^$", r"^\^a\^ Department of Community Medicine.*$",
                        r"^\*\*Corresponding author:\*\*.*$", r"^\*\*Target journal:\*\*.*$"],
    },
}
