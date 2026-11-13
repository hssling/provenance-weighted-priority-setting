# Submission set

Two independent papers from one project. They share one dataset and are written to stand alone; a text-overlap
screen between them returns 0.6% (A against B) and 0.4% (B against A).

| | Paper A | Paper B |
|---|---|---|
| title | What a tuberculosis budget cannot see | The label says what kind, not how old |
| target | *Health Policy and Planning*, Original Article | *International Journal of Epidemiology* |
| abstract | 249 words | 331 words |
| main text | 2,904 words | 4,548 words |
| tables / figures | 2 / 0 | 6 / 0 |
| references | 16 | 13 |

Counts are derived by `manuscript/build_submission.py`, never typed. Rerun it after any edit; it also rewrites the
blinded copies. A cover letter in an earlier project claimed 400 dpi for 600 dpi figures because a number was typed
rather than derived, which is why nothing here is typed.

## Files

```
paper_a/  01_title_page.md  02_cover_letter.md  03_manuscript_blinded.md
paper_b/  01_title_page.md  02_cover_letter.md  03_manuscript_blinded.md
```

The blinded copy strips the author block, the target-journal line, the author's working notes, and replaces
self-citations by name with `[Author]`. Both journals may be single-blind, in which case the unblinded source
(`manuscript/manuscript_draft_v1.md`, `manuscript/manuscript_b_draft_v1.md`) is what to upload. Check the journal
before choosing. Declarations are inside each manuscript's own `## Declarations` section and are repeated on the
title page.

## Verified before submission

- **Every number regenerates from code.** `python -I verification/check_all.py` runs the test suite, both demos and
  the self-similarity screen.
- **References read, not just resolved.** Seven were read in full text against the sentences citing them on
  13 November 2026; see `manuscript/references_verified.md`. Two DOIs produced from memory earlier in this project
  were wrong and were caught by direct lookup, which is why that rule exists.
- **Self-similarity.** `verification/check_self_similarity.py` compares both papers against each other and against
  four prior manuscripts by the same author. It fails the build on a verbatim run of 40 or more words, and does not
  gate on a percentage: no journal publishes a numeric threshold and inventing one would dress a guess as a rule.
  It is a screen, not iThenticate — run the institutional check before uploading.

## Deposit

Archived at Zenodo on 13 November 2026, from GitHub release v1.0.0.

- **Version DOI, cite this one:** 10.5281/zenodo.24187367 — the exact archived state every number in both papers
  was computed from.
- Concept DOI: 10.5281/zenodo.24187366 — always resolves to the latest version.

Both data-availability statements now carry the version DOI. The **blinded** copies do not: the repository URL
contains the author's GitHub username and resolving the DOI shows the author record, so both are replaced with
"[repository and archive DOI withheld for blind review]". Give the identifiers to the editor separately if the
journal reviews blind. `build_submission.py` fails the build if any identifier survives into a blinded copy.

## Outstanding, in order

1. **Confirm each journal's current limits** — abstract length, main-text length, and whether *Health Policy and
   Planning* still requires its Key Messages box (3 to 5 bullets). The publisher's author-guideline pages are
   bot-protected and could not be read automatically; open them in a normal browser. Paper A's abstract is 249 words
   against a 250-word limit, so it has no margin if the limit has changed.
2. **One incomplete citation.** Paper A ref [13], the JSSTD paper, carries the DOI printed on the journal's R14
   proof (10.25259/JSSTD_120_2026). It does not resolve yet — the article is in production and the DOI is
   registered at publication. Volume and pages are still unassigned.
3. **Decide blinded versus unblinded** per journal, as above. The blinded copies also give a main-text count 7 words
   shorter for Paper B, which is the withheld identifier; the title pages state the unblinded counts.
