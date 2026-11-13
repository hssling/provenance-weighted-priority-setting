# Pre-registered novelty search: two claims in two manuscripts

**Date protocol written:** 13 November 2026.
**Date searches run:** 13 November 2026 (every query is timestamped in §2).

> **Section 1 of this file (the protocol) was written and saved to disk before any search
> was run.** The inclusion and exclusion criteria below, and the decision rules for what
> counts as refutation, were fixed in advance so that they could not be shaped by what the
> searches returned. Section 2 (the searches and their results) and Section 3 (the
> verdicts) were appended afterwards.

---

## 1. Protocol (written before searching)

### 1.1 The two claims, verbatim

**Claim 1 — Paper B**, *"The label says what kind, not how old: a reproducible screen of
443 variables in six WHO tuberculosis datasets"*
(`provenance_weighting/manuscript/manuscript_b_draft_v1.md`), §1 Background:

> "The quality of routine health data has been assessed in other settings [3,4]. To our
> knowledge, there is no prior work screening these datasets for vintage."

Scope of the claim, as fixed by the manuscript:

- **"These datasets"** = the WHO Global Tuberculosis Programme's country-reported data
  files: TB budget; TB expenditure and utilisation; TB notifications; TB treatment
  outcomes; TB laboratory diagnostic services; TB contact tracing and preventive
  treatment (and, in §5, TB public-private mix).
- **"Vintage"** = whether a published value was re-measured for that reporting year or
  carried forward unchanged from a previous year - as distinct from what *kind* of
  quantity it is (which WHO's dictionary does label, for six variables, as "Estimated" or
  "Typical").
- **"Screening ... for vintage"** = assessing, from the published values themselves, which
  variables' values are re-established annually and which are restated.

**Claim 2 — Paper A**, *"What a tuberculosis budget cannot see: fiscal invisibility and
the limits of the WHO funding-gap indicator in India, 2017-2025"*
(`provenance_weighting/manuscript/manuscript_draft_v1.md`), Abstract, Background:

> "WHO's tuberculosis (TB) funding gap — budget required minus funding expected — is
> published annually for high-burden countries and read as a measure of under-resourcing.
> Whether it does so for any given country is unexamined."

The same claim appears in §1 Introduction in a more explicit form:

> "To our knowledge, no study has examined the validity of the WHO funding-gap indicator,
> or the cross-country comparability of health-financing indicators of this kind."

Scope of the claim: that no published study has examined whether the WHO TB funding-gap
indicator (`budget_tot` minus `cf_tot`) is valid, well-constructed or informative for a
given country — in particular where a country reports expected funding exactly equal to
budget required, making the published gap zero by construction.

### 1.2 Databases and interfaces

APIs only, preferred over web pages. Publisher sites are frequently bot-protected and
return HTTP 403; where that happens it will be recorded as such and no attempt will be
made to work around it.

| # | Source | Endpoint |
|---|---|---|
| D1 | Europe PMC | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=...&format=json` |
| D2 | Crossref | `https://api.crossref.org/works?query=...` (and `query.bibliographic=`) |
| D3 | OpenAlex | `https://api.openalex.org/works?search=...&page=N` (cursor paging requires auth as of Nov 2026; `page=` used instead) |
| D4 | PubMed | NCBI E-utilities `esearch.fcgi?db=pubmed&term=...&retmode=json`, then `esummary.fcgi` |

### 1.3 Search strings to be run

**For Claim 1** (vintage / carried-forward values in country-reported programme data):

- C1-a `"carried forward" AND tuberculosis AND (data OR dataset OR surveillance)`
- C1-b `"carry-forward" AND ("routine health data" OR "administrative data")`
- C1-c `"data vintage" AND (health OR surveillance OR indicator)`
- C1-d `("unrevised" OR "stale") AND "consecutive years" AND (indicator OR "reported data")`
- C1-e `"repeated values" AND (dataset OR "data quality") AND health`
- C1-f `WHO AND "global tuberculosis" AND ("data quality" OR "quality of reported data")`
- C1-g `provenance AND ("country-reported" OR "country reported") AND (health OR surveillance) AND data`
- C1-h `"data quality" AND ("country-reported" OR "national programme") AND tuberculosis`
- C1-i `"global tuberculosis report" AND (reliability OR validity OR "data quality")`
- C1-j `("imputation" OR "carried forward") AND "last observation" AND surveillance AND aggregate`
- C1-k `"WHO tuberculosis database" OR "WHO TB database"` (any assessment of it)
- C1-l `("notification data" OR "programme data") AND tuberculosis AND (audit OR screen OR "internal consistency")`

**For Claim 2** (validity / construction / informativeness of the WHO TB funding gap):

- C2-a `"funding gap" AND tuberculosis AND WHO`
- C2-b `"funding gap" AND tuberculosis AND (indicator OR validity OR measure)`
- C2-c `"budget required" AND "funding expected" AND tuberculosis`
- C2-d `"resource gap" AND tuberculosis AND financing`
- C2-e `tuberculosis AND financing AND ("under-resourcing" OR "unmet need") AND indicator`
- C2-f `"global tuberculosis report" AND funding AND gap AND (analysis OR trends)`
- C2-g `tuberculosis AND "domestic funding" AND "donor funding" AND gap`
- C2-h `("funding gap" OR "financing gap") AND ("comparability" OR "cross-country") AND health`
- C2-i `tuberculosis AND financing AND India AND (budget OR expenditure) AND (gap OR shortfall)`
- C2-j `"TB financing" AND (indicator OR measurement OR validity)`

Additional strings may be added if a result suggests an unexplored term. Any such addition
will be marked **[post hoc]** in §2 and screened against the criteria below, which do not
change.

### 1.4 Inclusion criteria

A record is **included for full screening** if its title/abstract indicates that it:

- **For Claim 1:** empirically examines, in a *country-reported, routinely compiled,
  programme or surveillance dataset*, whether published values were re-measured for the
  reporting period or repeated/carried forward unchanged from an earlier period — by any
  method (repetition statistics, revision tracking, version comparison, provenance
  metadata, digit or round-number analysis aimed at detecting restatement). The dataset
  must be one of the six WHO TB files, or a closely comparable country-reported programme
  dataset (e.g. WHO HIV or malaria country returns, GBD country inputs, UNAIDS country
  reports, DHIS2 national aggregates reported upward).

- **For Claim 2:** examines the *validity, construction, interpretation or informativeness
  of the WHO TB funding-gap figure itself* — budget required minus funding expected as
  reported to WHO — including any analysis of how countries populate those two fields,
  whether the two are independently determined, whether a zero gap is meaningful, or
  whether the gap is comparable across countries.

### 1.5 Exclusion criteria

A record is **excluded** if it is:

- **(E1)** About TB financing, TB costs, TB resource needs or TB investment cases in
  general, without examining the WHO-reported gap figure as a measure. *Using* the gap
  (quoting it, projecting it forward) is not *examining* it.
- **(E2)** About routine health-data quality in general — completeness, timeliness,
  accuracy against a gold standard, facility-level verification — without addressing
  whether values were re-measured or carried forward across reporting periods.
- **(E3)** A modelled reconstruction of resource need or spending (e.g. financial
  modelling of TB spending by source and function) rather than an assessment of the
  reported indicator. Such work substitutes for the indicator; it does not examine it.
- **(E4)** About individual-level or clinical data vintage (last-observation-carried-forward
  in trials or cohorts), which is a different problem with the same vocabulary.
- **(E5)** Not in English and without an English abstract, or not retrievable in any form.
- **(E6)** A duplicate of a record already screened.

Every record excluded at full-screening stage that is a **near-miss** (i.e. it reached full
screening rather than being discarded on title) will be listed in §2 with a one-line
reason.

### 1.6 Decision rules fixed in advance

For **each** claim, one of three verdicts:

- **REFUTED** — at least one retrievable record meets the inclusion criterion for that
  claim. For Claim 1, work that detects carried-forward or unrevised values in these or
  closely comparable country-reported programme datasets. For Claim 2, work that assesses
  the validity, construction or informativeness of the WHO TB funding-gap figure itself.
  The "to our knowledge" sentence must then be deleted and replaced with a citation.

- **NEEDS SOFTENING** — no record fully meets the inclusion criterion, but at least one
  retrievable record is close enough that a reviewer could reasonably say the claim
  overreaches: for Claim 1, a study detecting value-repetition or non-revision in a
  country-reported dataset of a different programme or by a different route; for Claim 2,
  a study that criticises the construction or comparability of a closely analogous
  published health-financing gap indicator. The claim must then be narrowed and the
  near-miss cited.

- **STANDS** — no record meets the inclusion criterion and no near-miss of the kind above
  was found, **and** search coverage was adequate (see next rule).

- **Coverage rule, binding.** If the searches could not be executed against at least two of
  D1-D4, or if the executed searches returned so few interpretable records that absence of
  evidence cannot be distinguished from absence of search, the verdict for the affected
  claim is recorded as **INCONCLUSIVE — SEARCH INADEQUATE**, not STANDS. A claim that
  merely looks novel because searching was hard is not novel.

### 1.7 Verification rules fixed in advance

- **Every DOI reported in this file will be verified by direct lookup at
  `https://api.crossref.org/works/{DOI}`, and the title Crossref returns will be recorded
  next to it.** No DOI will be written from memory. (This project has already caught two
  fabricated-from-memory DOIs this way.)
- **No paper will be described as "read" unless its full text was retrieved.** Where only
  title and abstract were available, the record will say "abstract only". Where the
  publisher site returned 403 or otherwise refused, that will be stated.
- **Null searches will be recorded.** A query returning zero hits is evidence and will
  appear in §2 with its zero.

---
