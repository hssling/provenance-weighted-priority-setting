# Supplementary material (for online publication only)

**The label says what kind, not how old: a reproducible screen of 443 variables in six WHO tuberculosis datasets**

This file holds the full screen specification, two failure modes of the method demonstrated on these data, and the extended limitations. Every figure in it regenerates from the code deposited with the paper. Section numbers refer to the main text.

---

## S1. Full specification of the screens

Each is computable from the published file. These screens are our own operationalisation of non-measurement, justified by face validity; we know of no published validation of them for country-reported programme data. The nearest framework we can cite, WHO's data quality assurance toolkit [6], assesses completeness and internal and external consistency of facility data. Our screens are of that general kind but were designed for published country returns and are not an implementation of it. For each variable with at least 100 non-missing values:

**S0 Categorical.** Runs first. A variable with five or fewer distinct values is classified *categorical* and excluded from the measurement/mixed/estimate classification entirely; it is reported separately and never counted as estimate-like. The rationale: a binary or categorical status flag (is the national reference laboratory accredited? is data available?) legitimately repeats year after year, takes few values and sits on round numbers, so it trips the repetition, granularity and modal-share tests for reasons that have nothing to do with carried-forward estimation. "Five or fewer" is a convention, not a derived quantity.

**S0b Untestable.** A continuous variable for which no country has an adjacent pair of observations (each country reports at most once) cannot be screened for repetition. It is classified *untestable* on S1, reported separately, and never counted as measurement-like: a test that could not run is not evidence of cleanliness. This rule was adopted after a discrepancy was found. An exploratory pass had silently dropped such variables through a division-by-zero guard, producing figures that matched no stated rule; reconciling the discrepancy exposed it, and the class was then made explicit. The rule raises the median repetition of two datasets (laboratory and outcomes), which favours the paper's argument, so we justify it on principle alone and report the results under both rules (§3.1). It does not touch the first two files, in which no variable is untestable.

**S1 Repetition.** The share of consecutive country-year pairs holding an identical value. A genuinely stable quantity repeats; we take a quantity that repeats in most countries in most years to be one that is not being re-measured.

**S2 Granularity.** Distinct values divided by observations; the share held by the single most common value; and the share falling on round numbers (multiples of ten, or of a thousand for monetary variables). We assume that estimates cluster on round numbers and on a small number of conventional values; this premise has not been validated against reported values of known provenance.

**S3 Identity.** Where a total and its components are both published, do the components sum to the total within 1%? This tests internal consistency rather than external validity, and a variable can be internally perfect while being an estimate.

**S4 Bounds.** Where a definition implies a range — a percentage must lie in [0, 100] — do the values respect it?

**S5 Comparison with the dictionary.** After classification, each variable's dictionary definition was read for a label of estimation. We counted a variable as *labelled* if its definition contains "estimat" or "typical". "Expected" (as in expected funding) and "average" were not counted: the first describes a forecast, the second a statistic. The rule is a convention and the result depends on it (§5).

**No single screen condemns a variable.** A small integer count is legitimately round; a stable quantity legitimately repeats. We therefore count how many of four tests a continuous variable trips (repetition, distinct ratio, modal share, roundness) and classify it as *measurement-like* (0–1), *mixed* (2) or *estimate-like* (3–4). Thresholds are conventions, stated in the code so a reader can change them; the classification is insensitive to small changes where the underlying distribution is strongly bimodal (§3.1).

---

## S0. The six input files

A seventh file from the same programme, public-private mix (`TB_ppm_2026-08-25.csv`), was screened after the analysis was complete. It is consistent with the counted/characterised division but contributes only two variables clearing the 100-observation threshold, both counts of new diagnoses, both measurement-like (median repetition 21.5%, 3.6% excluding zero-to-zero pairs). The headline counts exclude it.


- **TB budget** — 1,720 rows, 2018–2025, 43 columns.
- **TB expenditure and utilisation** — 2,123 rows, 2017–2026, 46 columns.
- **TB notifications** — 9,337 rows, 1980–2025, 221 columns.
- **TB outcomes** — 5,953 rows, 1994–2024, 97 columns.
- **TB laboratory diagnostic services** — 3,683 rows, 2009–2025, 75 columns.
- **TB contact tracing and preventive treatment** — 2,365 rows, 2015–2025, 37 columns.

All six are archived with the analysis code and hashed in `data/raw_file_manifest.csv`.

---

## S1a. Sensitivity to the S0b rule

The last column is a sensitivity analysis on the S0b rule (§2.2). Excluding untestable variables, laboratory repetition is 63.0% against 13.0-15.6% for the budget, expenditure and notification files, 4.0 to 4.8 times as high; scoring them as zero, it is 53.5%, 3.4 to 4.1 times as high. The division holds under either rule; it does not depend on the rule that favours it.

---

## S1c. A failure mode of the screen itself: the missing S0

**The screen's own false positive.** Before S0 existed, the contact-tracing dataset looked estimate-like. Its 12 categorical flags (`prevtx_data_available`, `tpt_3hp` and similar) repeat and sit on round numbers by nature. Scored without S0, the dataset had 20 testable variables, a median repetition of 63.8% (59.7% with its one untestable variable scored as zero) and 11 estimate-like variables. With S0 it has a median of 3.5% and none. Its apparent unreliability was entirely an artefact of the screen, and we found it only by replicating on a further dataset (§5).

---

## S1b. The two files screened first

**In the two files first screened (77 variables)**, one variable is categorical, **`hosp_type_mdr`** (4 distinct values: 2, 140, 141, 142; a code, not a measure), and none is untestable, so the S0b rule leaves them unaffected. Of the 76 continuous variables, **63 are measurement-like, 8 mixed and 5 estimate-like.** Without rule S0, `hosp_type_mdr` would be counted as a sixth estimate-like variable: as a code it repeats, takes few values and sits on round numbers, which is the failure mode S0 exists to prevent (S1c).

---

## S2. A second failure mode: two plausible denominators, one correct

The files publish both `exp_tot` (expenditure) and `rcvd_tot` (funds received). Computing the Global Fund share of financing against the first — the intuitive choice, since expenditure is what a programme did — produces shares exceeding 100% in **14.5%** of 841 country-years. Against `rcvd_tot`, **no country-year exceeds 100% in 842 observations**.

The dictionary defines `exp_tot` as "Total actual expenditure (US Dollars)" and `rcvd_tot` as "Total funding received for all budget line items (US Dollars)" [5]. We read the difference as one of timing: money received in one year may be spent in another. The dictionary does not state this. Both columns are correct; only one is the right denominator for a funding share, and nothing in the file names the pairing.

The extreme case is instructive beyond the pairing. The maximum ratio is **28,417%** (Chad, 2019): US$1,989,218 reported as received from the Global Fund against a reported total TB expenditure of **US$7,000** for the year. A national programme expenditure of seven thousand dollars is not plausible, so the implausibility that the wrong denominator exposes is not only in the ratio — it is in the denominator itself. A screen applied to a derived quantity can therefore surface a problem in a variable that passes every screen applied to it directly: `exp_tot` is measurement-like on all four tests.

The case also shows why this failure is easy to compound. A maximum computed on a filtered subset of country-years can understate the extreme by orders of magnitude, so the check must run on the full file. Errors of both kinds are caught the same way — an implausible value prompting a check against the full data — and neither would be caught by the screens in §2.2, which assess variables one at a time rather than the ratios analysts build from them.

---

**Implication for publishers.** Where a file publishes two plausible denominators, the dictionary should state which belongs with which numerator. Nothing in the file can settle it, and the two choices give materially different answers.

---

## S3. Extended limitations

The screens detect signatures consistent with non-measurement; they cannot prove that any particular value was carried forward rather than re-measured and found unchanged. A genuinely stable quantity is indistinguishable, on internal evidence, from an unrevised one — which is precisely the ambiguity a provenance flag would remove.

The classification thresholds are conventions. We chose them before examining the results and state them in the code; the bimodality of the underlying distribution (§3.1) means moderate changes do not move variables between groups, but a reader preferring different cut-points can recompute.

Variables with fewer than 100 observations were excluded, so the screen is silent about sparsely reported quantities, which may be the least reliable of all.

We screened six files from one programme at one point in time. Whether the counted/characterised division generalises to other WHO disease programmes is an open and directly testable question. The division itself was found post hoc. A seventh file from the same programme, public-private mix (`TB_ppm`), was screened after the analysis was complete and is consistent with it but adds little: only two of its variables clear the 100-observation threshold, both counts of new diagnoses, and both screen measurement-like (median repetition 21.5%, 3.6% excluding zero-to-zero pairs). It is reported for completeness and the headline counts above exclude it.

**The screen's validation is partial.** Before S0 existed it produced a false positive on the contact-tracing dataset, labelling a set of ordinary yes/no flags as estimate-like, and we found it only by replication on a further dataset. Both the five-or-fewer-values convention of S0 and the untestable class of S0b were added in response to failures. The comparison with the dictionary (§3.5) is the first external check, and it is thin: it covers six variables, all in one file, defined by a wording rule we chose, and it can show only that the screen does not miss labelled estimates, not that the 80 variables it flags beyond them are estimates. We found that 70 of those 80 have zero as their most common value, as do 71 of all 84 estimate-like variables, including 21 of the 31 in the laboratory file. A repeated zero (no such test performed, no such event) is not a restated estimate, and the screen does not distinguish them; the laboratory median of 63.0% in §3.1 should be read with that in mind. The hospitalisation and visit variables are not affected (of the four labelled estimate-like variables, only one has zero as its most common value). Other failure modes may remain: a six-valued code, for example, would not be caught by S0.

The 43 untestable variables are unclassified, not clean; they are concentrated in treatment outcomes and laboratory data.

Finally, we cannot observe the national reporting process, so §4.2's benign interpretation is inference from the data's shape, not evidence about what reporters did.

---

---
