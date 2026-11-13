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

## 2. Searches and results (run after §1 was saved)

All searches run 13 November 2026. All four planned sources (D1–D4) were reachable and
were used. No publisher website was scraped; the one full text retrieved from a publisher
host is noted below with its HTTP status.

### 2.1 D1 Europe PMC — the protocol strings of §1.3

Europe PMC's default index covers full text of open-access records, so these counts are
full-text counts and are correspondingly high; they are reported as run.

| Tag | Query | Hits |
|---|---|---:|
| C1-a | `"carried forward" AND tuberculosis AND (data OR dataset OR surveillance)` | 1,809 |
| C1-b | `"carry-forward" AND ("routine health data" OR "administrative data")` | 73 |
| C1-c | `"data vintage" AND (health OR surveillance OR indicator)` | 63 |
| C1-d | `("unrevised" OR "stale") AND "consecutive years" AND (indicator OR "reported data")` | 7 |
| C1-e | `"repeated values" AND (dataset OR "data quality") AND health` | 197 |
| C1-f | `WHO AND "global tuberculosis" AND ("data quality" OR "quality of reported data")` | 176 |
| C1-g | `provenance AND ("country-reported" OR "country reported") AND (health OR surveillance) AND data` | 117 |
| C1-h | `"data quality" AND ("country-reported" OR "national programme") AND tuberculosis` | 206 |
| C1-i | `"global tuberculosis report" AND (reliability OR validity OR "data quality")` | 462 |
| C1-j | `("imputation" OR "carried forward") AND "last observation" AND surveillance AND aggregate` | 158 |
| C1-k | `"WHO tuberculosis database" OR "WHO TB database"` | 19 |
| C1-l | `("notification data" OR "programme data") AND tuberculosis AND (audit OR screen OR "internal consistency")` | 445 |
| C2-a | `"funding gap" AND tuberculosis AND WHO` | 354 |
| C2-b | `"funding gap" AND tuberculosis AND (indicator OR validity OR measure)` | 179 |
| C2-c | `"budget required" AND "funding expected" AND tuberculosis` | **0** |
| C2-d | `"resource gap" AND tuberculosis AND financing` | 50 |
| C2-e | `tuberculosis AND financing AND ("under-resourcing" OR "unmet need") AND indicator` | 215 |
| C2-f | `"global tuberculosis report" AND funding AND gap AND (analysis OR trends)` | 329 |
| C2-g | `tuberculosis AND "domestic funding" AND "donor funding" AND gap` | 97 |
| C2-h | `("funding gap" OR "financing gap") AND ("comparability" OR "cross-country") AND health` | 144 |
| C2-i | `tuberculosis AND financing AND India AND (budget OR expenditure) AND (gap OR shortfall)` | 1,124 |
| C2-j | `"TB financing" AND (indicator OR measurement OR validity)` | 17 |

**C2-c is a null search and is the most directly informative of the twenty-two.** The exact
pair of field names that constitute the indicator — "budget required" and "funding
expected" — co-occur in **no record in Europe PMC, including full text**.

### 2.2 D1 Europe PMC — title/abstract-restricted precision variants

The protocol anticipated (§1.3) that further strings might be needed. The full-text default
made several protocol strings unscreenable at the title stage, so each was re-run restricted
to `TITLE_ABS`. These are refinements of the pre-specified strings, not new concepts; the
inclusion and exclusion criteria were not changed. Top 25–30 records of each were screened
on title, and anything plausible was taken to abstract.

| Tag | Query | Hits |
|---|---|---:|
| C1-a-TA | `TITLE_ABS:"carried forward" AND TITLE_ABS:tuberculosis` | 10 |
| C1-a2-TA | `TITLE_ABS:"carried forward" AND (TITLE_ABS:"data quality" OR TITLE_ABS:surveillance OR TITLE_ABS:indicator)` | 50 |
| C1-c-TA | `TITLE_ABS:"data vintage"` | 5 |
| C1-e-TA | `TITLE_ABS:"repeated values" OR TITLE_ABS:"repeated value"` | 51 |
| C1-f-TA | `TITLE_ABS:"global tuberculosis" AND TITLE_ABS:"data quality"` | 1 |
| C1-h-TA | `TITLE_ABS:"data quality" AND TITLE_ABS:tuberculosis` | 126 |
| C1-i-TA | `TITLE_ABS:"global tuberculosis report"` | 71 |
| C1-k-TA | `TITLE_ABS:"WHO tuberculosis database" OR "WHO TB database" OR "WHO global TB database"` | 12 |
| C1-m-TA | `TITLE_ABS:vintage AND TITLE_ABS:data AND (TITLE_ABS:health OR TITLE_ABS:surveillance)` | 129 |
| C1-n-TA | `TITLE_ABS:provenance AND TITLE_ABS:"data quality" AND TITLE_ABS:health` | 28 |
| C1-o-TA | `TITLE_ABS:"not updated" OR "unchanged values" OR "stale data"` | 128,103 (uninformative; not screened beyond first 30, all unrelated) |
| C2-a-TA | `TITLE_ABS:"funding gap" AND TITLE_ABS:tuberculosis` | 14 |
| C2-b-TA | `TITLE_ABS:"funding gap" AND (TITLE_ABS:indicator OR validity OR comparability OR construction)` | 3 (all non-health: nuclear finance, biodiversity credits, savannah fire management) |
| C2-c-TA | `TITLE_ABS:"budget required" AND TITLE_ABS:tuberculosis` | 4 |
| C2-d-TA | `TITLE_ABS:"resource gap" AND TITLE_ABS:tuberculosis` | 2 |
| C2-f-TA | `TITLE_ABS:tuberculosis AND financing AND (gap OR shortfall)` | 17 |
| C2-g-TA | `TITLE_ABS:"financing gap" AND (health OR tuberculosis OR HIV OR malaria)` | 39 |
| C2-i-TA | `TITLE_ABS:tuberculosis AND financing AND India` | 27 |

`C1-c-TA` is worth recording in full, because it establishes where the word "vintage" lives.
Its five records are: two copies of one 2026 outbreak-analytics preprint, one 2026 preprint
on a versioned archive of US State Cancer Profiles estimates, one 2026 outbreak-forecasting
preprint, and a 2022 paper on gridded census estimates. None concerns WHO TB data.

### 2.3 D4 PubMed (E-utilities)

| Tag | Query (tiab) | Hits |
|---|---|---:|
| P1 | `("carried forward" OR "carry forward" OR vintage) AND (surveillance OR "routine data" OR "programme data" OR "reported data")` | 69 |
| P2 | `tuberculosis AND ("data quality" OR "data validity") AND (WHO OR global)` | 47 |
| P3 | `("funding gap" OR "financing gap") AND tuberculosis` | 17 |
| P4 | `"funding gap" AND (validity OR indicator OR comparability OR "by construction")` | **0** |
| P5 | `tuberculosis AND budget AND ("line item" OR "line items" OR classification)` | 4 |
| P6 | `("repeated" AND "identical values") OR "value repetition"` | 7 |
| P7 | `"World Health Organization" AND database AND tuberculosis AND (quality OR reliability OR consistency)` | 26 |
| P8 | `("global tuberculosis report" OR "WHO TB data") AND (limitations OR critique OR caution OR artefact OR artifact)` | 2 |

**P4 is a null search.** In PubMed's title/abstract index, no record pairs "funding gap"
with any of validity, indicator, comparability or "by construction". P1's 69 records are,
on screening, almost entirely last-observation-carried-forward in clinical cohorts and
post-marketing surveillance studies (exclusion E4) plus dialysis "vintage" (a different
sense of the word); none concerns aggregate country-reported programme data.

### 2.4 D3 OpenAlex

Free-text `search=` was low precision (counts in the tens of thousands with no relevant
records in the first 20). The informative runs are the `title_and_abstract.search` filters.
Cursor paging was not used; `page=1` only, per the protocol note.

| Tag | Filter | Count |
|---|---|---:|
| O7 | `"funding gap" AND tuberculosis` | 50 |
| O8 | `"funding gap" AND (indicator OR validity OR comparability)` | 142 (all non-health finance/entrepreneurship on screening) |
| O9 | `"data vintage"` | 218 |
| O10 | `"carried forward" AND ("data quality" OR surveillance OR "routine data")` | 177 |
| O11 | `tuberculosis AND "data quality" AND (WHO OR global OR "country-reported")` | 158 |
| O12 | `"budget required" AND "expected funding"` | **0** |
| O13 | `tuberculosis AND budget AND (invisibility OR "line item" OR traceable)` | 21 |
| O14 | `"global tuberculosis report" AND (critique OR critical OR limitations OR caution)` | (run; no relevant record in the returned set) |
| O15 | `provenance AND (dataset OR "data quality") AND (surveillance OR "public health" OR health)` | (run; no relevant record in the returned set) |

**O12 is a null search and corroborates C2-c:** OpenAlex indexes no title or abstract
containing both "budget required" and "expected funding".

**O9 is the single most useful result for Claim 1's framing.** "Data vintage" is a
well-established term — but in macroeconomic forecasting, not in health. Its 218 records are
dominated by the real-time-dataset literature (Croushore and Stark's Federal Reserve Bank of
Philadelphia working papers and the *Review of Economics and Statistics* paper derived from
them; *International Journal of Forecasting* papers on forecasting data vintages; *Fiscal
Studies* on data vintages and fiscal policy). A 2026 Zenodo deposit applies the idea to
precipitation data in hydrological machine learning. **Not one of the 218 applies it to a
country-reported health programme dataset.**

### 2.5 D2 Crossref

Crossref's free-text `query` and `query.bibliographic` returned between 6 × 10⁵ and 7 × 10⁶
results for each of the three strings run (X1 `tuberculosis WHO funding gap budget required
expected funding`; X2 `data vintage carried forward country reported health data`; X3 `WHO
tuberculosis dataset variable screening data quality`), with no relevance ranking usable for
screening: the first 20 of X1 included OECD education-funding indicator tables and a
*Who's Who* entry. **Crossref contributed no screenable records and is recorded here as an
unproductive source**, not as a null result. It was used as planned for DOI verification
(§2.8), where it is authoritative.

### 2.6 Records taken to abstract, and the reason each was excluded

All abstracts below were read in Europe PMC (`resultType=core`) or, where noted, in
OpenAlex. Where a full text was read, it is said so explicitly.

**Screened for Claim 1 (vintage):**

| Record | Verified DOI | Why it does not refute Claim 1 |
|---|---|---|
| Evaluating Tuberculosis Surveillance Using Global Standards and Benchmarks in the Philippines (JMIR Public Health Surveill 2026) | 10.2196/77058 | Abstract only. Assesses accuracy, completeness and timeliness of a *national* surveillance system against WHO standards, by facility visits and record review. Addresses under-reporting and delayed reporting, not whether a published value was re-measured or restated. **E2.** |
| Assessing the validity of tuberculosis surveillance data in California (BMC Public Health 2006) | 10.1186/1471-2458-6-217 | Abstract only. Case-level concordance of reported variables against the medical record as gold standard. External validation of individual records, not vintage of an annual country return. **E2.** |
| A situational analysis of TB surveillance and information systems in SEAR countries (Indian J Tuberc 2026) | 10.1016/j.ijtb.2026.08.014 | Abstract only. Describes 21 national information systems qualitatively; notes "reduced data quality" as a challenge. No analysis of published values. **E2.** |
| Evolution of TB programmatic information systems in India (Indian J Tuberc 2026) | 10.1016/j.ijtb.2026.07.017 | Abstract only. Narrative history of EpiCentre → Nikshay V1 → Nikshay V2. **E2.** |
| Decoding the WHO Global Tuberculosis Report 2024: A Critical Analysis of Global and Chinese Key Data (Zoonoses 2025) | 10.15212/zoonoses-2024-0061 | Abstract read in OpenAlex; no Europe PMC record. Despite "Critical Analysis" in the title, the abstract is an interpretive summary of the report's findings (burden, DR-TB, TB/HIV, COVID-19 impact, a call for funding). It does not examine the data's construction. **E1/E2.** |
| The Global Burden of Disease Study tuberculosis estimates from IHME (Int J Epidemiol 2024) | 10.1093/ije/dyae122 | No abstract available in Europe PMC; not retrieved in full. Concerns IHME's modelled TB estimates, not the vintage of WHO's country-reported files. **E3.** Recorded as screened on title and journal only. |
| Undernotification and underreporting of TB in Zambia: a national data quality assessment (BMC Health Serv Res 2022) | — (title screened via OpenAlex/PubMed) | Under-notification against facility registers. **E2.** |
| Audit of the Data Quality of the National TB Control Program, Senegal 2024; Botswana relapse-TB surveillance data quality (2026 preprint); TB data quality in São Paulo laboratory indicators (Procedia CS 2025); facility-based TB data quality in three South African districts (PLOS GPH 2022) | — | All are completeness/accuracy audits of sub-national or facility data against source registers. None examines repetition of values across reporting years. **E2** (screened as a group). |

**Screened for Claim 2 (the funding-gap indicator):**

| Record | Verified DOI | Why it does not refute Claim 2 |
|---|---|---|
| **Financing tuberculosis control: the role of a global financial monitoring system (Bull World Health Organ 2007)** | **10.2471/blt.06.034942** | **Full text read** (via PMC, PMC2636652, HTTP 200; the Europe PMC `fullTextXML` route returned HTTP 500 and the PMC XML route carries a publisher notice forbidding XML download, so the rendered page was used). **This is the strongest near-miss in the whole search — see §2.7.** It does not refute the claim, but it falsifies the claim as currently worded. |
| Financing for TB prevention, diagnosis and treatment services in the Western Pacific Region in 2005–2020 (West Pac Surveill Response J 2023) | 10.5365/wpsar.2023.14.3.976 | Abstract only. *Uses* the WHO global TB finance database — the same source — to describe funding levels and to project that "the funding gap will increase from US$ 326 million in 2020 to US$ 830 million by 2025". It reads the gap as a quantity, and does not ask whether the two fields behind it are independently determined. **E1** (using the gap is not examining it). It is nonetheless direct evidence that the indicator is read exactly as Paper A says it is read. |
| Costs of services and funding gap of the Bangladesh NTP 2016–2022 (PLoS One 2023) | 10.1371/journal.pone.0286560 | Abstract only. Builds an *independent* ingredient-based cost estimate with WHO's OneHealth Tool and subtracts allocated funds. A reconstruction that substitutes for the reported indicator rather than assessing it. **E3.** |
| Domestic and donor financing for TB care and control, 2002–11 (Lancet Glob Health 2013) | 10.1016/s2214-109x(13)70032-9 | Abstract only. Trend analysis of the same WHO-reported financing data; imputes missing country-years. Analyses funding levels and future needs, not the construction of the gap. **E1.** Already cited in Paper A §3.4. |
| Tracking total spending on TB by source and function in 135 LMICs, 2000–17 (Lancet Infect Dis 2020) | 10.1016/s1473-3099(20)30124-9 (title screened; already cited in Paper A as Su et al. 2020) | A financial modelling reconstruction. **E3**, and Paper A already says so in §4.4. |
| The potential impact of reductions in international donor funding on TB (Lancet Glob Health 2025) | 10.1016/s2214-109x(25)00232-3 | Abstract only. Epidemiological modelling of funding cuts. Assumes treatment-initiation rates fall in proportion to budget reductions; does not examine the reported gap. **E1.** |
| National TB spending efficiency in 121 LMICs, 2010–19 (Lancet Glob Health 2022) | 10.1016/s2214-109x(22)00085-7 (title/abstract screened) | Data envelopment and stochastic frontier analysis of reported TB spending. Treats the reported financial data as input; does not interrogate the budget/expected-funding pair. **E1.** |

**Post-hoc strings run to attack the two specific failure modes** (marked **[post hoc]**;
criteria unchanged):

| Tag | Source | Query | Hits |
|---|---|---|---:|
| PH1 | D1 | `"zero funding gap" OR "no funding gap" AND tuberculosis` | 373 (screened to 20; all are aid-cut commentary or costing, none about zero-gap reporting) |
| PH2 | D1 | `TITLE_ABS:"financial monitoring" AND TITLE_ABS:tuberculosis` | **1** — Floyd, Pantoja and Dye 2007, and nothing else |
| PH3 | D1 | `AUTH:"Garcia Baena" AND tuberculosis AND financ*` | 17 (all unit-cost, catastrophic-cost or spending-efficiency work; **E1/E3**) |
| PH4 | D1 | `TITLE_ABS:tuberculosis AND TITLE_ABS:"resource tracking"` | 3 (none about the WHO TB gap) |
| PH5 | D1 | `"reported funding gap" AND tuberculosis` | 1 (a China bundled-payment simulation; **E1**) |
| PH6 | D1 | `TITLE_ABS:"hospd_prct" OR "budget_tot" OR "cf_tot"` | **0** |
| PH7 | D1 | `TITLE_ABS:("carried forward" OR "unchanged") AND TITLE_ABS:("country-reported" OR "country reported" OR "reported to WHO")` | 2 (a WHO eye-health indicator pilot; a 1984 lung-cancer series — neither relevant) |
| PH8 | D1 | `TITLE_ABS:"global health estimates" AND (revision OR vintage OR "carried forward" OR updated)` | 4 (none examines vintage of country-reported values) |
| PH9 | D1 | `TITLE_ABS:(reproducib* OR screen*) AND "WHO" AND dataset AND variables` | 219 (screened to 20; all clinical prediction-model work) |
| PH10 | D1 | `TITLE_ABS:"data dictionary" AND (WHO OR surveillance OR "public health")` | 69 (registry and terminology work; none compares a dictionary's labels with the values) |
| PH11 | D1 | `TITLE_ABS:"stale" AND (indicator OR dataset OR statistics)` | 35 (food spoilage, network staleness; none relevant) |
| PH12 | D1 | `TITLE_ABS:tuberculosis AND (hospitalisation OR hospitalization) AND ("WHO data" OR "reported data" OR "country data")` | 0 relevant in returned set |

**PH6 and PH2 are the two most decisive post-hoc results.** PH6 (zero hits) shows that no
indexed record names any of the three variables at the centre of the two papers. PH2 shows
that in the whole of Europe PMC exactly one title or abstract pairs "financial monitoring"
with tuberculosis, and that one record is the near-miss discussed next.

### 2.7 The strongest near-miss: Floyd, Pantoja and Dye 2007

This is the only record in the search that examines the *instrument* rather than using its
output, and it is therefore reported at length.

- **Verified DOI** 10.2471/blt.06.034942. Crossref returns the title *"Financial
  tuberculosis control: the role of a global financial monitoring system"*, journal
  *Bulletin of the World Health Organization*, vol. 85(5): 334–340, 2007, with a single
  author listed (Floyd). **Crossref's metadata for this record is defective**: PubMed
  (PMID 17639216), PMC (PMC2636652) and the article's own title page all give the title as
  *"Financing tuberculosis control: the role of a global financial monitoring system"* and
  three authors, Floyd K, Pantoja A, Dye C, all of the Stop TB Department, WHO. The
  discrepancy is recorded here per §1.7 rather than silently corrected; any citation should
  use the PubMed/PMC form, which matches the published article.
- **Full text read**, via the PMC rendered page (HTTP 200). Europe PMC's `fullTextXML`
  endpoint returned HTTP 500 and the NCBI PMC XML carries the notice that the publisher
  does not allow full-text XML download, so only the rendered page was used.
- **What it is.** The paper is by the custodians of the system, describing the WHO global
  financial monitoring system for TB control established in 2002 — the system that collects
  NTP budget data, expenditure data, line items, funding sources **and funding gaps**, by
  standardised questionnaire, and whose successor files are the `TB_budget` and
  `TB_expenditure_utilisation` datasets both manuscripts analyse. Table 1 traces how the
  budget line items and the funding-source categories (which include "gap" as a category)
  changed between the 2002 and 2006 rounds.
- **It examines the instrument.** It carries a section headed **"System limitations"**,
  which states limitations of data collection, analysis and dissemination: the system's
  restriction to public-sector provider costs, with no data on private-sector provision or
  on patient/household costs; the difficulty of obtaining aggregated national data where
  budgets are decentralised; expenditure data being consistently harder to collect than
  budget data; poor reporting by European countries; TB/HIV budgets being systematically
  underestimated; and that "more opportunities to validate data would be useful".
- **It also describes an internal check adjacent to Claim 1.** Under "Data management,
  follow-up and validation" it says the methods used to check and validate data include
  cross-checking against Global Fund proposals and databases, comparisons with costing
  studies, and "comparisons ... with data reported for previous years".

**Why it does not refute Claim 2, but does falsify Claim 2 as worded.** It never asks
whether budget required and funding expected are independently determined for a given
country, never reports how many countries report them equal, and never discusses what a zero
gap means or whether the gap is comparable across countries. Paper A's specific finding is
untouched. But Paper A's abstract says the question "is unexamined", and its §1 says "no
study has examined the validity of the WHO funding-gap indicator" — and here is a
peer-reviewed paper, by WHO's own Stop TB Department, whose stated purpose includes
analysing the system's strengths and limitations. A reviewer who knows this paper, and TB
financing reviewers will, can falsify the sentence as written without touching the finding.
That is exactly the failure mode this search exists to prevent.

**Why it does not refute Claim 1 either.** The "comparison with data reported for previous
years" is described as an internal consistency check applied during data collection, in one
sentence, with no results reported, no measure defined, no variable named and no coverage of
the four non-financial files. It is not a screen of the published datasets for vintage, and
nothing in it would tell an analyst which published values were re-measured. It is close
enough in subject matter to be worth a line in Paper B rather than silence.

### 2.8 DOI verification (§1.7)

Every DOI named in this file was looked up at `https://api.crossref.org/works/{DOI}` on
13 November 2026. All twelve resolved. The title Crossref returned is recorded for each.

| DOI | Title returned by Crossref | Container | Year |
|---|---|---|---|
| 10.2471/blt.06.034942 | Financial tuberculosis control: the role of a global financial monitoring system **(see §2.7 — Crossref title and author list are defective)** | Bulletin of the World Health Organization | 2007 |
| 10.5365/wpsar.2023.14.3.976 | Financing for tuberculosis prevention, diagnosis and treatment services in the Western Pacific Region in 2005–2020 | Western Pacific Surveillance and Response Journal | 2023 |
| 10.1371/journal.pone.0286560 | Costs of services and funding gap of the Bangladesh National Tuberculosis Control Programme 2016–2022: An ingredient based approach | PLOS ONE | 2023 |
| 10.1016/s2214-109x(13)70032-9 | Domestic and donor financing for tuberculosis care and control in low-income and middle-income countries: an analysis of trends, 2002–11, and requirements to meet 2015 targets | The Lancet Global Health | 2013 |
| 10.1016/s2214-109x(25)00232-3 | The potential impact of reductions in international donor funding on tuberculosis in low-income and middle-income countries: a modelling study | The Lancet Global Health | 2025 |
| 10.15212/zoonoses-2024-0061 | Decoding the WHO Global Tuberculosis Report 2024: A Critical Analysis of Global and Chinese Key Data | Zoonoses | 2025 |
| 10.2196/77058 | Evaluating Tuberculosis Surveillance Using Global Standards and Benchmarks in the Philippines: Mixed Methods Study | JMIR Public Health and Surveillance | 2026 |
| 10.1093/ije/dyae122 | The Global Burden of Disease Study tuberculosis estimates from the Institute for Health Metrics and Evaluation | International Journal of Epidemiology | 2024 |
| 10.1016/j.ijtb.2026.08.014 | A situational analysis of TB surveillance and information systems in SEAR countries | Indian Journal of Tuberculosis | 2026 |
| 10.1186/1471-2458-6-217 | Assessing the validity of tuberculosis surveillance data in California | BMC Public Health | 2006 |
| 10.1016/j.ijtb.2026.07.017 | Evolution of TB programmatic information systems in India | Indian Journal of Tuberculosis | 2026 |
| 10.1016/j.ijtb.2024.01.007 | Financial hardship of tuberculosis patients registered under NTEP in rural India: A longitudinal study | Indian Journal of Tuberculosis | 2024 |

### 2.9 What was read, and what was not

- **Read in full text:** one record, Floyd, Pantoja and Dye 2007, via the PMC rendered page.
- **Read as abstract only:** every other record named in §2.6. Each is marked "abstract
  only" there.
- **Screened on title and journal only:** records in the long result lists not named in
  §2.6, and 10.1093/ije/dyae122, for which Europe PMC holds no abstract.
- **No publisher site was circumvented.** Two retrieval routes failed and are recorded as
  failures, not worked around: Europe PMC `fullTextXML` for PMC2636652 returned HTTP 500,
  and NCBI's PMC XML for the same record carries the publisher's notice that full text may
  not be downloaded in XML form.

### 2.10 Coverage: what this search did not reach

Stated plainly, because §1.6's coverage rule depends on it.

- **Searched:** Europe PMC (including full text of open-access records and preprint
  servers), PubMed, OpenAlex, Crossref.
- **Not searched:** Scopus, Web of Science, Google Scholar, EconLit, and the grey literature
  of WHO, the World Bank and the Global Fund other than what those four indexes carry.
  **WHO's own Global TB Report methods annexes and the TB data-collection form guidance are
  not journal literature and were not searched;** they are the most likely place for a
  statement about how countries should populate budget required and funding expected, and
  Paper A's §3.1 already says WHO's dictionary does not document the equality.
- **Language:** no language restriction was applied in the queries, but screening was on
  English titles and abstracts (E5). One Chinese-language record surfaced in OpenAlex
  (*Analysis on funds budget of control of tuberculosis in Guizhou in 2012*, Journal of
  Medical Pest Control 2013, no DOI); it is a provincial budget analysis, not an examination
  of the WHO indicator, and was excluded on its English title (**E1**).

The coverage rule of §1.6 is met for both claims: four of four planned sources ran, three of
them productively, and the searches returned a large, interpretable, and in several cases
precisely null body of records. Neither claim is recorded as INCONCLUSIVE.

---

## 3. Verdicts

### 3.1 Claim 1 (Paper B, vintage) — **STANDS**

No record was found, in any of the four sources, that screens the WHO Global Tuberculosis
Programme's country-reported datasets — or any closely comparable country-reported
programme dataset — for whether published values were re-measured for the reporting year or
carried forward unchanged. The supporting evidence is as much in the null searches as in the
screening: `TITLE_ABS:"hospd_prct" OR "budget_tot" OR "cf_tot"` returns zero; the term "data
vintage" returns 218 OpenAlex records of which none is about health programme data and the
great majority are macroeconomic real-time-dataset papers; and the entire TB data-quality
literature retrieved (Philippines, SEAR, Zambia, Senegal, Botswana, São Paulo, South Africa,
California) assesses completeness, accuracy against source records, timeliness and
under-notification — never revision across reporting years.

The nearest thing to a near-miss is the sentence in Floyd, Pantoja and Dye 2007 (§2.7)
reporting that WHO's own validation of reported financial data includes "comparisons ...
with data reported for previous years". That is an undocumented internal check with no
published results, no defined measure and no coverage of the non-financial files; it does
not amount to prior work screening these datasets for vintage, and it leaves Claim 1
standing.

**No replacement sentence is required.** Two optional strengthenings, offered as the
author's choice and not as corrections:

1. The word "vintage" is borrowed from a real economics literature, and a methods reviewer
   may ask where it comes from. Paper B could say so in §1 or §2.2, which costs one
   sentence and gains the paper a lineage:

   > The term is borrowed from the real-time-data literature in economics, where a *vintage*
   > is the version of a series as it stood at a given date and the distinction between
   > vintages is known to change substantive conclusions [NEW REF].

   Suggested reference, in Paper B's numbered Vancouver style, DOI verified at Crossref on
   13 November 2026 (title returned: *"A Real-Time Data Set for Macroeconomists: Does the
   Data Vintage Matter?"*):

   > Croushore D, Stark T. A real-time data set for macroeconomists: does the data vintage
   > matter? Rev Econ Stat. 2003;85(3):605-17. doi:10.1162/003465303322369759

   *Caveat, per §1.7: this record was verified at Crossref and read only as a title and
   bibliographic record. If it is cited, read it first.*

2. Paper B's §2.2 currently says "we know of no published validation of them for
   country-reported programme data". That is unchanged by this search and remains correct.
   But the author may wish to note, in §4.2 or §5, that WHO itself compares reported
   financial values with the previous year's as an internal validation step, because it
   supports the paper's remedy — the comparison is already being made somewhere, it is
   simply not published per value:

   > WHO's own account of the financial monitoring system records that reported data are
   > checked against "data reported for previous years" as one of several validation steps
   > [NEW REF]; the comparison is therefore already made internally, but its result is not
   > carried in the published file.

   > Floyd K, Pantoja A, Dye C. Financing tuberculosis control: the role of a global
   > financial monitoring system. Bull World Health Organ. 2007;85(5):334-40.
   > doi:10.2471/BLT.06.034942

   *Caveat: Crossref's metadata for this DOI gives a wrong title and one author; the form
   above follows PubMed/PMC and the published article. Full text was read (§2.7).*

### 3.2 Claim 2 (Paper A, the funding-gap indicator) — **NEEDS SOFTENING**

Paper A's finding is untouched: nothing found examines whether budget required and funding
expected are independently determined for a given country, counts the countries reporting
them equal, or asks what a zero gap means. The two exact-phrase searches that would catch
such work returned zero in both Europe PMC full text (C2-c) and OpenAlex titles and
abstracts (O12), and PubMed returned zero for "funding gap" paired with validity, indicator,
comparability or "by construction" (P4).

But the claim as worded says the question is *unexamined* and that *no study has examined
the validity of the WHO funding-gap indicator*, and Floyd, Pantoja and Dye 2007 is a
peer-reviewed paper by WHO's Stop TB Department whose stated purpose includes analysing the
strengths and limitations of the very system that produces the figure, with a section headed
"System limitations" (§2.7). A reviewer can cite it against the sentence without touching
the finding. The sentence must be narrowed from "nobody has examined this indicator" to
"nobody has examined *this property* of it", which is both true and the stronger claim.

**Replacement sentences, in Paper A's style (author-date, Health Policy and Planning).**

**(a) Abstract, Background.** Replace:

> "WHO's tuberculosis (TB) funding gap — budget required minus funding expected — is
> published annually for high-burden countries and read as a measure of under-resourcing.
> Whether it does so for any given country is unexamined."

with:

> "WHO's tuberculosis (TB) funding gap — budget required minus funding expected — is
> published annually for high-burden countries and read as a measure of under-resourcing.
> The system that produces it has been described and its limitations reviewed by its
> custodians, but whether the two quantities behind it are independently determined for a
> given country has not been examined."

*(Word count: this replacement is 57 words against the original's 46, so it adds 11 words to
an abstract the author's note 2 records as already at 249 against a 250-word limit. A shorter
form that carries the same retreat, at 48 words, is: "WHO's tuberculosis (TB) funding gap —
budget required minus funding expected — is published annually for high-burden countries and
read as a measure of under-resourcing. Whether the two quantities behind it are independently
determined for a given country is unexamined." Either way, re-run the count before upload.)*

**(b) §1 Introduction.** Replace:

> "To our knowledge, no study has examined the validity of the WHO funding-gap indicator, or
> the cross-country comparability of health-financing indicators of this kind."

with:

> "The global financial monitoring system that produces these figures has been described by
> its custodians, who set out its limitations — chiefly its restriction to public-sector
> provider costs, the difficulty of obtaining aggregated data from decentralized systems,
> and the limited opportunities to validate what countries report (Floyd et al. 2007). To
> our knowledge, however, no study has asked whether the two quantities behind the reported
> gap are independently determined for a given country, or examined the cross-country
> comparability of health-financing indicators of this kind."

**(c) Reference to add**, in the paper's Harvard author-date list, between *Central TB
Division 2024* and *Global Fund 2024*:

> Floyd K, Pantoja A, Dye C. 2007. Financing tuberculosis control: the role of a global
> financial monitoring system. *Bulletin of the World Health Organization* **85**: 334-40.
> doi: 10.2471/BLT.06.034942

**Two notes on this reference, both required by §1.7.**

1. Crossref returns the title as *"Financial tuberculosis control: ..."* and lists one
   author. PubMed (PMID 17639216), PMC (PMC2636652) and the article itself give *"Financing
   tuberculosis control: ..."* and three authors. The form above is the article's own. If a
   reference manager is used, it will import the defective Crossref record; check it.
2. The full text was read (§2.7). The statements attributed to it above — the
   public-sector-only scope, decentralization, and limited validation opportunities — are
   from its "System limitations" section and are quoted or paraphrased from text that was
   read, not from the abstract.

**One further sentence worth checking while editing.** Paper A §3.4 says of the shrinking
relevance of an external-financing indicator: "We know of no study that tests this." That
sentence survives this search; nothing found tests it. §4.2 says of the under-resourcing
mechanism: "we know of no study that tests the mechanism." That sentence also survives.
Neither needs changing.

### 3.3 Summary

| Claim | Verdict | Forced by |
|---|---|---|
| **Claim 1** (Paper B §1: no prior work screening these WHO TB datasets for vintage) | **STANDS** | Nothing found. Decisive nulls: zero hits for the variable names (PH6); "data vintage" absent from the health-programme-data literature (O9, C1-c-TA); the whole retrieved TB data-quality literature is about completeness and accuracy, never revision. |
| **Claim 2** (Paper A abstract and §1: the WHO TB funding-gap indicator is unexamined) | **NEEDS SOFTENING** | Floyd K, Pantoja A, Dye C. 2007. *Bull World Health Organ* **85**: 334-40, doi:10.2471/BLT.06.034942 — a peer-reviewed examination, by the system's custodians, of the instrument that produces the indicator, with a "System limitations" section. The finding is untouched; the universal claim is not sustainable. |

Neither claim is REFUTED.
