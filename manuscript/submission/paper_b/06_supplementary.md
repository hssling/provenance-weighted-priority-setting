# Supplementary material (for online publication only)

**Restated, never revised: a vintage analysis of WHO tuberculosis data and the spending estimate built on them**

This file holds the data sources, WHO's processing steps, the screen of 443 variables, its failure modes and the extended limitations, as Supplementary Notes 1 to 5 in the order the main text cites them, and Supplementary Table S1. It is assembled by `manuscript/make_supplementary_b.py`: every table and count below is generated from the archived files and WHO's code. Section numbers (§) refer to the main text. The screening rules keep their own names, S0, S0b and S1 to S5, which are not note numbers.

---

## Supplementary Note 1. Data sources and their identification

WHO's Global TB Programme keeps one public repository per annual report. The files below were downloaded from fixed commits by `tools/fetch_vintages.py`, converted from R data to text without change by `tools/convert_vintages.R`, and are identified by SHA-256 digest. The repositories carry no licence, so the files are not redistributed; running the fetch script reproduces them byte for byte.

| Repository | Commit | File | Bytes | SHA-256 (first 16) |
|---|---|---|---:|---|
| gtbreport2024 | afbe537 | `data/gtb/snapshot_2024-07-29/finance.rda` | 207,059 | `1d7feff989f574f5` |
| gtbreport2025 | 666088c | `data/gtb/snapshot_2025-07-30/finance.rda` | 223,617 | `95ccc94f76b4e42a` |
| gtbreport2025 | 666088c | `finance/output/finance_imputed_constantus_included.rda` | 2,564,631 | `5f390379da2e9d1b` |
| gtbreport2025 | 666088c | `finance/2a_clean_raw_data.R` | 126,819 | `b7a785c91f1922d3` |
| gtbreport2025 | 666088c | `finance/3_prepare_imputed_data.R` | 101,487 | `59bf4813b83b0fd2` |
| gtbreport2026 | 11ebd9b | `data/gtb/snapshot_2026-08-25/expenditure.rda` | 267,342 | `7f87a8b3abf41378` |
| gtbreport2026 | 11ebd9b | `finance/output/finance_imputed_constantus_included.rda` | 2,201,461 | `f3dcbba03c913ace` |
| gtbreport2026 | 11ebd9b | `finance/2a_clean_raw_data.R` | 145,684 | `39e8ed709f60136a` |
| gtbreport2026 | 11ebd9b | `finance/3_prepare_imputed_data.R` | 101,495 | `2817f9e5ea849944` |

The 2026 release of the utilisation inputs is the public download of 25 August 2026 (`TB_expenditure_utilisation_2026-08-25.csv`), the same date as the 2026 report's snapshot, which stores expenditure without the utilisation fields. It is archived with the analysis code with the other five public datasets used for the screen in §2.3:

- **TB budget** — 1,720 rows, 2018–2025, 43 columns.
- **TB expenditure and utilisation** — 2,123 rows, 2017–2026, 46 columns.
- **TB notifications** — 9,337 rows, 1980–2025, 221 columns.
- **TB outcomes** — 5,953 rows, 1994–2024, 97 columns.
- **TB laboratory diagnostic services** — 3,683 rows, 2009–2025, 75 columns.
- **TB contact tracing and preventive treatment** — 2,365 rows, 2015–2025, 37 columns.

In the public 2026 download, total expenditure and total funding received are printed as 0 where WHO's archived snapshot holds no value. Comparisons of expenditure therefore use the archived snapshots, and the expenditure comparators in Tables 1 and 2 are line items, not totals.

---

## Supplementary Note 2. How WHO's pipeline turns country returns into the care estimate

Read from WHO's own code for the 2026 report (`finance/2a_clean_raw_data.R` and `finance/3_prepare_imputed_data.R`, commit 11ebd9b):

- **Fill rule.** A missing value of any of the six inputs is replaced by the same country's value from the previous year, then from up to 4 years earlier, then from up to 4 years later, in that order (`lag(.x,1)` … `lag(.x,4)`, then `lead(.x,1)` … `lead(.x,4)`).
- **Hand-coded substitutions.** The cleaning script contains 259 uses of `lag()`, most replacing a specific country-year's value with the previous year's, alongside fixed values written into the code for named countries.
- **Care estimate set to zero.** In WHO's processed file the care estimate is zero, although its components are not, for ARM (2015–2026); AZE (2015–2026); BLR (2016–2026); CHN (2015–2026); GEO (2019–2026); HND (2015–2023); KAZ (2015–2026); KGZ (2019–2026); RUS (2015–2026); SWZ (2024–2026); TJK (2019–2026); TKM (2015–2026); UKR (2019–2026). The code's comment on the main block of these reads "SET GHS to 0 for countries where it is believed to be already reported", that is, where national spending is thought to include it.

The care estimate for each country-year is the sum of four components: drug-susceptible bed-days (patients notified less MDR/RR-TB patients × share hospitalised × days) and MDR/RR-TB bed-days, each priced at a cost per bed-day, and drug-susceptible and MDR/RR-TB outpatient visits (patients × visits per patient), each priced at a cost per visit. In every country-year where the care estimate is not set to zero, the four components sum to it exactly; the analysis asserts this for each one.

**Supplementary Table S1. WHO's estimate of spending on inpatient and outpatient TB care, by provenance of the inputs it was computed from, 2025 report.** Each cost component (bed-days and outpatient visits, for drug-susceptible and MDR/RR-TB) is classed by its own inputs: WHO-supplied if any input was filled or replaced by WHO, restated if any other input repeats the previous year, otherwise newly reported.

| Year | Total funding, US$ bn | Care estimate, US$ bn | Care, % of total | Newly reported | Restated | WHO-supplied | Any input newly reported |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 6.92 | 1.48 | 21.4% | 38.6% | 60.5% | 1.0% | 44.8% |
| 2019 | 6.95 | 1.39 | 20.0% | 14.3% | 81.3% | 4.4% | 17.3% |
| 2020 | 6.03 | 0.68 | 11.2% | 54.1% | 39.9% | 6.0% | 57.1% |
| 2021 | 6.01 | 0.78 | 13.0% | 24.0% | 75.2% | 0.8% | 29.2% |
| 2022 | 6.12 | 0.98 | 16.0% | 21.6% | 74.2% | 4.2% | 23.0% |
| 2023 | 5.84 | 0.99 | 17.0% | 13.6% | 64.2% | 22.2% | 15.1% |
| 2024 | 5.85 | 1.02 | 17.4% | 21.1% | 52.0% | 26.9% | 24.3% |

*Total funding is funding received by national programmes plus the care estimate, as WHO computes it. The reconstruction reproduces WHO's published totals: US$ 5.9 billion for 2024 in the 2025 report (reconstructed 5.85). The last column is a sensitivity analysis counting a component as current if any one of its inputs was newly reported.*

Supplementary Table S1 repeats Table 4 of the main text on WHO's 2025 report. The two reports agree closely for the years they share; differences arise from late returns and from the 2026 report's use of 2025 values when filling earlier gaps.

---

## Supplementary Note 3. The screen of 443 variables

Each screen is computable from the published file. These screens are our own operationalisation of non-measurement, justified by face validity; we know of no published validation of them for country-reported programme data. The nearest framework, WHO's data quality assurance toolkit [12], assesses completeness and internal and external consistency of facility data. Our screens are of that general kind but were designed for published country returns and are not an implementation of it. For each variable with at least 100 non-missing values:

**S0 Categorical.** Runs first. A variable with five or fewer distinct values is classified *categorical* and excluded from the classification; it is reported separately and never counted as estimate-like, because a status flag legitimately repeats, takes few values and sits on round numbers. "Five or fewer" is a convention, not a derived quantity.

**S0b Untestable.** A continuous variable for which no country has an adjacent pair of observations cannot be screened for repetition. It is classified *untestable* on S1, reported separately, and never counted as measurement-like: a test that could not run is not evidence of cleanliness. The rule raises the median repetition of two datasets (laboratory and outcomes); the last column of Table 5 reports each median with untestable variables scored as zero instead.

**S1 Repetition.** The share of consecutive country-year pairs holding an identical value.

**S2 Granularity.** Distinct values divided by observations; the share held by the single most common value; and the share falling on round numbers (multiples of ten, or of a thousand for monetary variables). That estimates cluster on round and conventional values is an assumption, not validated against values of known provenance.

**S3 Identity.** Where a total and its components are both published, do the components sum to the total within 1%? In the budget and expenditure files four of five such identities reconcile in every testable country-year and the fifth in 98.9%; internal consistency is not validity.

**S4 Bounds.** Where a definition implies a range — a percentage must lie in [0, 100] — do the values respect it?

**S5 Comparison with the dictionary.** A variable counts as *labelled* if its dictionary definition [9] contains "estimat" or "typical". "Expected" and "average" are not counted: the first describes a forecast, the second a statistic.

**Classification.** A continuous variable is *measurement-like* if it trips none or one of four tests (repetition, distinct ratio, modal share, roundness), *mixed* if two and *estimate-like* if three or four. Thresholds are conventions stated in the code. The six dictionary-labelled variables are the six cost inputs: four screen estimate-like and two mixed, none measurement-like. Of the 358 continuous variables 152 are non-measurement-like, so six labelled variables falling there by chance has probability 0.006, though the six come in related pairs and are not independent.

---

## Supplementary Note 4. Failure modes of the screen

**Repeated zeros.** The screen flags 80 estimate-like variables that the dictionary does not label. Seventy of them have zero as their most common value, mostly small counts of rare events in the notifications and outcomes files. A repeated zero is a stable absence, not a restated estimate, and the screen does not distinguish them. The vintage analysis in the main text is not affected: it measures restatement directly, and a restated zero contributes nothing to the care estimate, whose components are products of the inputs.

**A missing categorical rule.** Without rule S0, the contact-tracing dataset looks estimate-like: its 12 categorical flags repeat and sit on round numbers by nature, giving a median repetition of 63.8% and 11 estimate-like variables. With S0 it has a median of 3.5% and none. The artefact surfaced only on replication in a further dataset.

**Two plausible denominators.** The expenditure file publishes both expenditure and funds received. Computing the Global Fund share of financing against expenditure produces shares above 100% in 14.5% of 841 country-years; against funds received, none of 842. The maximum, 28,417% (Chad, 2019), arises from a reported total TB expenditure of US$ 7,000, implausible for a national programme, although the expenditure variable passes every screen applied to it directly. A screen of variables one at a time cannot see a problem that appears only in a ratio.

---

## Supplementary Note 5. Extended limitations

Restatement is not error. A genuinely stable quantity is indistinguishable, on internal evidence, from an unrevised one, which is the ambiguity a vintage flag would remove. The analysis observes values, not the reporting process that produced them.

Finance data enter WHO's report repositories only from the 2024 report, so revision can be assessed over three releases and two intervals. Earlier releases may have been revised in ways not observable here.

The year a WHO-supplied value came from is inferred by matching values in WHO's fill order. Some values match no reported year; they result from chained fills or from the country-specific overrides in WHO's cleaning code, and are reported as such rather than assigned a source.

The cost components are classed by the provenance of their inputs only. Patient numbers come from notifications, which are counted annually, and unit costs are themselves WHO estimates; neither was assessed. The care estimate's dependence on restated inputs is therefore a statement about the utilisation ratios, not about every factor in the product.

The screen's thresholds are conventions chosen before the results were examined; the bimodality of the underlying distribution means moderate changes do not move variables between classes, but a reader preferring different cut-points can recompute. Variables with fewer than 100 observations were excluded, so the screen is silent about the most sparsely reported quantities. Six files from one programme at one point in time were screened; whether the pattern holds in other WHO disease programmes is open and directly testable.
