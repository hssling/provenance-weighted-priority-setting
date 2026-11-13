# Not every reported number is a measurement: a reproducible screen of 77 variables in WHO's tuberculosis financing and utilisation data

**Running title:** Measurement or estimate in WHO TB data

**Author:** Siddalingaiah H S
Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur – 572106, Karnataka, India.
Correspondence: hssling@yahoo.com · ORCID 0000-0002-4771-8285

**Target journal:** *BMC Medical Research Methodology* — alternatives: *PLOS Global Public Health*, *Gates Open Research*

---

## Abstract

**Background.** WHO publishes country-reported tuberculosis financing and service-utilisation data as a single annual dataset. Analysts treat its variables interchangeably as annual country reports. We asked whether they are.

**Methods.** We screened all 77 numeric variables in WHO's TB budget and TB expenditure-and-utilisation datasets (215 countries, 2017–2025) with four tests computable from the published files alone: **repetition** (share of consecutive country-year pairs with an identical value), **granularity** (distinct values per observation, modal share, share on round numbers), **identity** (do stated components reconcile with their stated total), and **bounds** (do values respect their definition's range). No single test condemns a variable; the signature is several at once.

**Results.** The variables separate almost completely into two populations. Seventy financial variables have a median repetition of 14.6% (range 2.2–64.4%); seven utilisation variables have a median of 65.8% (range 61.5–81.4%). Only one financial variable falls inside the utilisation range. Sixty-three variables screen as measurement-like, eight as mixed and six as estimate-like; all six estimate-like variables are utilisation measures or a single external-funding line. The financial data is internally immaculate: all five component-to-total identities reconcile in 100% of testable country-years (849/849, 845/845, 895/895, 892/892), and the funding-source identity in 98.9% (881/891). Against this, `hospd_prct_mdr` — the share of drug-resistant TB patients hospitalised — has 81 distinct values across 1,421 observations, 35.3% of them exactly 100, and is unchanged between a country's first and last reporting year in 42% of the 178 countries with four or more years.

**Conclusions.** Two kinds of data are distributed under one name, with nothing in the file distinguishing them. Analyses of trends in TB service delivery drawn from these variables describe reporting behaviour rather than practice. A single provenance flag per variable-year — measured, estimated, or carried forward — would resolve this at negligible cost, and the screen presented here can be run by any analyst on any version of the files.

**Keywords:** Data Accuracy; Datasets as Topic; Health Services Research; Reproducibility of Results; Tuberculosis; World Health Organization

---

## 1. Background

WHO's Global Tuberculosis Programme collects and republishes country-reported data on TB financing and service delivery. The files are widely used: for investment cases, for cross-country comparison of cost and delivery models, and as covariates in modelling studies. They are distributed as flat annual tables with a shared data dictionary, and their variables are, in practice, treated as equivalent — each a country's report for that year.

This paper asks a prior question. A number in an annual return may be a measurement taken that year; it may be an estimate entered once and repeated because no one revised it; or it may be a convention. These are different kinds of object, and only the first supports inference about change over time. Nothing in the published files says which is which.

We are not aware of prior work screening these datasets for that distinction. The question is tractable because several signatures of non-measurement are computable from the published file alone, without reference to any external source.

---

## 2. Methods

### 2.1 Data

Two files, retrieved November 2026 and archived with the analysis code:

- **TB budget** — 1,720 rows, 215 countries, 2018–2025, 43 variables.
- **TB expenditure and utilisation** — 2017–2026, 46 variables.

WHO's published data dictionary supplied every variable definition. The dictionary is used, not the column names: definitions and names diverge in ways that matter, as in `budget_prog`, defined as *"programme costs to treat drug-susceptible TB"* rather than programme costs generally.

### 2.2 Four screens

Each is computable from the published file. For each variable with at least 100 non-missing values:

**S1 Repetition.** The share of consecutive country-year pairs holding an identical value. A genuinely stable quantity repeats; a quantity that repeats in most countries in most years is not being re-measured.

**S2 Granularity.** Distinct values divided by observations; the share held by the single most common value; and the share falling on round numbers (multiples of ten, or of a thousand for monetary variables). Estimates cluster on round numbers and on a small number of conventional values.

**S3 Identity.** Where a total and its components are both published, do the components sum to the total within 1%? This tests internal consistency rather than external validity, and a variable can be internally perfect while being an estimate.

**S4 Bounds.** Where a definition implies a range — a percentage must lie in [0, 100] — do the values respect it?

**No single screen condemns a variable.** A small integer count is legitimately round; a stable quantity legitimately repeats. We therefore count how many screens a variable trips and classify it as *measurement-like* (0–1), *mixed* (2) or *estimate-like* (3–4). Thresholds are conventions, stated in the code so a reader can change them; the classification is insensitive to small changes because the underlying distribution is strongly bimodal (§3.1).

### 2.3 Reproducibility

The screen is a single pure-Python script with no third-party dependency. It regenerates every figure in this paper from the raw files in one command and writes a per-variable results table. Code, archived inputs and the results table: [repository URL and DOI to be inserted at acceptance].

### 2.4 Ethics

Not required: aggregated, publicly available programme data with no individual-level records.

---

## 3. Results

### 3.1 The variables form two populations

Seventy-seven variables met the inclusion threshold. **Sixty-three screen as measurement-like, eight as mixed, six as estimate-like.**

The separation is almost complete and it follows the financial/utilisation boundary:

| Group | n | Median repetition | Range |
|---|---:|---:|---|
| Financial (budget, expenditure, funding) | 70 | **14.6%** | 2.2 – 64.4% |
| Utilisation (hospitalisation, facility visits) | 7 | **65.8%** | 61.5 – 81.4% |

Only one financial variable — `cf_tot_usaid`, at 64.4% repetition with 64.3% of its values held by a single number — falls inside the utilisation range. Every other financial variable repeats less often than every utilisation variable.

**Table 1. The six estimate-like variables.**

| Variable | n | Repetition | Distinct / n | Modal value share | Round |
|---|---:|---:|---:|---:|---:|
| `hosp_type_mdr` | 1,631 | 81.4% | 0.00 | 52.1% | 11.8% |
| `hospd_prct_mdr` | 1,421 | 69.6% | 0.06 | 35.3% | 66.6% |
| `hospd_dur_mdr` | 1,368 | 66.5% | 0.08 | 11.8% | 67.1% |
| `cf_tot_usaid` | 628 | 64.4% | 0.29 | 64.3% | 49.1% |
| `hcfvisit_mdr` | 1,364 | 61.6% | 0.14 | 11.1% | 40.4% |
| `hospd_prct_dstb` | 1,467 | 61.5% | 0.06 | 9.8% | 48.0% |

**Table 2. For contrast, the six least-repetitive variables.**

| Variable | n | Repetition | Distinct / n |
|---|---:|---:|---:|
| `cf_tot` | 845 | 2.2% | 0.98 |
| `cf_tot_sources` | 849 | 2.5% | 0.98 |
| `exp_fld` | 866 | 4.6% | 0.93 |
| `rcvd_sld` | 856 | 5.0% | 0.91 |
| `rcvd_fld` | 865 | 5.1% | 0.93 |
| `budget_fld` | 870 | 5.4% | 0.93 |

### 3.2 The financial data is internally immaculate

All five component-to-total identities reconcile in **100%** of testable country-years:

| Identity | Reconcile | Untestable |
|---|---|---|
| `budget_tot` = Σ 11 budget lines | 849 / 849 (100%) | 871 |
| `cf_tot` = Σ 11 expected-funding lines | 845 / 845 (100%) | 875 |
| `exp_tot` = Σ 11 expenditure lines | 895 / 895 (100%) | 1,228 |
| `rcvd_tot` = Σ 11 receipt lines | 892 / 892 (100%) | 1,231 |
| `rcvd_tot` = Σ 4 funding sources | 881 / 891 (98.9%) | 1,232 |

This matters for interpretation. The financial variables are not merely more variable than the utilisation ones; they are demonstrably coherent. Whatever process produces them enforces arithmetic consistency across eleven line items in every reporting country. No comparable constraint operates on the utilisation variables, which have no total to reconcile against.

### 3.3 What the utilisation variables cannot support

`hospd_prct_mdr`, the share of drug-resistant TB patients hospitalised, illustrates the practical consequence. It covers **199 countries** and **1,421 country-years** — coverage that invites a cross-country or trend analysis.

It has **81 distinct values**. **35.3%** of observations are exactly 100; **11.6%** are exactly 0; **70.5%** fall on multiples of ten. Among the 178 countries with four or more years of data, **42% report an identical value in their first and last year**.

A "global trend in DR-TB hospitalisation, 2017–2025" computed from this variable would be driven by whichever minority of countries revised their entry, and by when they did so. It would describe revision behaviour, not clinical practice. The same applies to duration of hospitalisation (66.5% repetition) and facility visits per patient (61.6%).

### 3.4 A second failure mode: two plausible denominators, one correct

The files publish both `exp_tot` (expenditure) and `rcvd_tot` (funds received). Computing the Global Fund share of financing against the first — the intuitive choice, since expenditure is what a programme did — produces shares exceeding 100% in **14.5%** of country-years, reaching 687%. Against `rcvd_tot`, no country-year exceeds 100% in **842** observations.

Receipts and expenditure differ because money received in one year may be spent in another. Both columns are correct; only one is the right denominator for a funding share, and nothing in the file names the pairing. We report this because we made the error ourselves and found it only when an implausible value forced a check.

---

## 4. Discussion

### 4.1 One dataset, two kinds of object

The file is titled *expenditure and utilisation*, and that conjunction is the problem. Its expenditure half behaves like measurement: highly granular, rarely repeated, arithmetically coherent across eleven components in every country. Its utilisation half behaves like a standing estimate: a small set of round values, over half of them unchanged from year to year, with no internal constraint to violate.

Distributing both under one schema, with one dictionary and no provenance field, invites the inference that they are the same kind of thing. They are not, and the difference determines which analyses are possible.

### 4.2 Why the utilisation variables are probably not errors

We do not read the repetition as carelessness. Hospitalisation share and average stay are properties of a country's service-delivery model, and that model does not change annually. A programme asked each year for a figure it has no new survey to support will reasonably repeat its best standing estimate. The reporting behaviour is sensible; what is missing is the flag that would let an analyst see it.

That reading is supported by `cf_tot_usaid`, the one financial variable in the utilisation range: a fixed external commitment, restated unchanged until it changes. Repetition here is a feature of the quantity, not a defect in the reporting.

### 4.3 Implications for secondary analysis

**Trend claims from utilisation variables should not be made** without first showing that the variable moves for reasons other than revision. The screen in §2.2 takes seconds and settles it.

**Cross-sectional comparison is weaker than it looks.** With 81 distinct values over 199 countries, much apparent between-country variation is variation between conventional answers.

**Internal consistency is not validity.** The financial variables reconcile perfectly and are still subject to definitional change, pooling and reporting convention; perfect arithmetic says nothing about whether a line item means the same thing in two countries.

**Published coverage is not evidential weight.** 1,421 observations across 199 countries reads as a strong dataset; after accounting for repetition the independent information is a small fraction of that.

### 4.4 What would fix it

**A provenance flag per variable-year.** Three values — *measured*, *estimated*, *carried forward* — would make every analysis in this paper unnecessary and every downstream analysis sounder. Countries already know which applies when they complete the return.

**A stated denominator pairing.** Where a file publishes two plausible denominators, the dictionary should say which belongs with which numerator.

**Publish the screen with the data.** The four tests here are generic. Running them at release and shipping the results table would let every user see, before analysis, which variables carry annual information.

---

## 5. Limitations

The screens detect signatures consistent with non-measurement; they cannot prove that any particular value was carried forward rather than re-measured and found unchanged. A genuinely stable quantity is indistinguishable, on internal evidence, from an unrevised one — which is precisely the ambiguity a provenance flag would remove.

The classification thresholds are conventions. We chose them before examining the results and state them in the code; the bimodality of the underlying distribution (§3.1) means moderate changes do not move variables between groups, but a reader preferring different cut-points can recompute.

Variables with fewer than 100 observations were excluded, so the screen is silent about sparsely reported quantities, which may be the least reliable of all.

We screened two files from one programme at one point in time. Whether the financial/utilisation division generalises to other WHO disease programmes is an open and directly testable question.

Finally, we cannot observe the national reporting process, so §4.2's benign interpretation is inference from the data's shape, not evidence about what reporters did.

---

## 6. Conclusions

Seventy-seven variables, four screens, and a near-complete separation: WHO's TB financing variables behave like measurements and are arithmetically immaculate; its utilisation variables behave like standing estimates, over half of them unchanged year on year. Both are published under one name with nothing to tell them apart.

The remedy is a single flag the reporting country is already in a position to supply. Until it exists, the screen presented here is a few seconds of work that tells an analyst which of these widely used numbers can support the question being asked.

---

## Declarations

**Contributors.** Sole author: conception, analysis, code, verification, manuscript.

**Funding.** None. **Competing interests.** None declared. **Ethical clearance.** Not required (§2.4).

**Data availability.** Inputs are public WHO datasets; the archived copies, the screening script and the per-variable results table are deposited at [URL and DOI at acceptance].

**Use of generative AI.** The author used a large language model as a drafting and analysis assistant. All analytical decisions, verification and conclusions are the author's, who takes full responsibility.

---

## Notes for the author — not for submission

1. **References not yet written.** Needed: WHO Global TB Report 2025; the WHO TB data dictionary; 3–4 on secondary analysis of routine health data quality; 1–2 on TB service-delivery models / ambulatory DR-TB care (to motivate §3.3); 1–2 on data provenance or FAIR metadata standards for §4.4.
2. **Companion paper.** The India financing analysis (`manuscript_draft_v1.md`) shares §3.4's dataset and the general theme. They must cite each other and be written independently — run `check_self_similarity.py` across both before submitting either.
3. **Possible strengthening:** repeat the screen on one other WHO programme dataset (HIV or malaria financing). If the financial/utilisation division replicates, §5's open question becomes a finding and the paper is materially stronger. Roughly a day's work on the same code.
4. **Honest framing to preserve:** §3.4 discloses an error we made. Keep it. A methods paper about data traps that conceals its author's own is worth less.
