"""Where each paper's upload files live, by role, for the build and every check.

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
}
