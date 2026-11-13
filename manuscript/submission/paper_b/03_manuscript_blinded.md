# The label says what kind, not how old: a reproducible screen of 443 variables in six WHO tuberculosis datasets

**Running title:** Kind and vintage in WHO TB data

---

## Abstract

**Background.** WHO publishes country-reported tuberculosis data as annual country-by-year tables, with variable definitions in a separate dictionary. The dictionary labels some quantities as estimates, but a label describes the kind of quantity, not the vintage of each value, and it is not in the data file, so analysts joining on column names never meet it.

**Methods.** We screened all 443 numeric variables with at least 100 observations across six WHO TB datasets (budget, expenditure, notifications, treatment outcomes, laboratory services, contact tracing). From the published files alone, variables with five or fewer distinct values were set aside as categorical; the rest were assessed on **repetition** (share of consecutive country-year pairs holding an identical value), granularity, internal identity and bounds, and the verdicts compared with the dictionary's labels.

**Results.** Of 358 continuous variables, 206 screened as measurement-like, 68 mixed and 84 estimate-like. Median repetition was 13.0-15.6% for budget, expenditure and notifications, and 3.5% for contact tracing, against **63.0% for laboratory diagnostic services**. The dictionary labels six variables as estimated or typical, all in the expenditure file; the screen places none in the measurement-like class (P = 0.006). For `hospd_prct_mdr` (share of drug-resistant patients hospitalised), 69.6% of consecutive pairs are identical and 42% of 178 countries with four or more years never change their entry; no field in any file says so. Seventy of the 80 variables flagged but unlabelled have zero as their most common value; a repeated zero is an absence, not a restated estimate. Excluding zero-to-zero pairs, median repetition falls to 5.2-9.2% in the three large counted files but only to **48.0%** in laboratory services, which has the fewest such variables (24 of 41, against 65 of 66 in treatment outcomes). The division is not an artefact of zero-reporting.

**Conclusions.** A trend analysis needs to know whether a value was revised, not only what kind of quantity it is. WHO's labels settle the second and are silent on the first; a per-value vintage flag in the data file would settle both.

**Keywords:** Data Accuracy; Datasets as Topic; Health Services Research; Reproducibility of Results; Tuberculosis; World Health Organization

---

## 1. Background

WHO's Global Tuberculosis Programme collects and republishes country-reported data on TB financing and service delivery [1,2]. The files are widely used: for investment cases, for cross-country comparison of cost and delivery models, and as covariates in modelling studies. They are distributed as flat annual tables. The data files carry column names only; the definitions are in a separate dictionary file. In practice the variables are treated as equivalent — each a country's report for that year.

This paper asks a prior question. A number in an annual return may be a measurement taken that year, or an estimate entered once and repeated because no one revised it. Only a value that is re-established each year supports inference about change over time. WHO's dictionary does say, for some variables, that the quantity is an estimate; for example the share of patients hospitalised is defined as an "Estimated percentage". Two things remain unsaid. The label is in a different file from the data. And it describes the kind of quantity, not the vintage of each value: whether this year's entry was revised from last year's, or simply restated.

The quality of routine health data has been assessed in other settings [3,4]. To our knowledge, there is no prior work screening these datasets for vintage. The question is tractable because several signatures of restatement are computable from the published file alone, without reference to any external source. We also compare the screen's verdicts with the dictionary's labels, which gives the screen a partial check that it otherwise lacks.

---

## 2. Methods

### 2.1 Data

Six files from WHO's TB programme, all retrieved in November 2026 and archived with the analysis code. File versions are WHO's own release dates: 12 November 2026 for the budget file and 25 August 2026 for the other five and the dictionary.

- **TB budget** — 1,720 rows, 2018–2025, 43 columns.
- **TB expenditure and utilisation** — 2,123 rows, 2017–2026, 46 columns.
- **TB notifications** — 9,337 rows, 1980–2025, 221 columns.
- **TB outcomes** — 5,953 rows, 1994–2024, 97 columns.
- **TB laboratory diagnostic services** — 3,683 rows, 2009–2025, 75 columns.
- **TB contact tracing and preventive treatment** — 2,365 rows, 2015–2025, 37 columns.

The first two were screened first (77 variables); the other four were added as a replication after the first analysis was complete, and the replication overturned two of the first analysis's conclusions (§3.1, §4.1).

WHO's published data dictionary [5] supplied every variable definition, and its labels are the comparison standard in §3.5. The dictionary is used, not the column names: definitions and names diverge in ways that matter, as in `budget_prog`, defined as *"programme costs to treat drug-susceptible TB"* rather than programme costs generally.

### 2.2 The screens

Each is computable from the published file. These screens are our own operationalisation of non-measurement, justified by face validity; we know of no published validation of them for country-reported programme data. The nearest framework we can cite, WHO's data quality assurance toolkit [6], assesses completeness and internal and external consistency of facility data. Our screens are of that general kind but were designed for published country returns and are not an implementation of it. For each variable with at least 100 non-missing values:

**S0 Categorical.** Runs first. A variable with five or fewer distinct values is classified *categorical* and excluded from the measurement/mixed/estimate classification entirely; it is reported separately and never counted as estimate-like. The rationale: a binary or categorical status flag (is the national reference laboratory accredited? is data available?) legitimately repeats year after year, takes few values and sits on round numbers, so it trips the repetition, granularity and modal-share tests for reasons that have nothing to do with carried-forward estimation. "Five or fewer" is a convention, not a derived quantity.

**S0b Untestable.** A continuous variable for which no country has an adjacent pair of observations (each country reports at most once) cannot be screened for repetition. It is classified *untestable* on S1, reported separately, and never counted as measurement-like: a test that could not run is not evidence of cleanliness. This rule was adopted after a discrepancy was found. An exploratory pass had silently dropped such variables through a division-by-zero guard, producing figures that matched no stated rule; reconciling the discrepancy exposed it, and the class was then made explicit. The rule raises the median repetition of two datasets (laboratory and outcomes), which favours the paper's argument, so we justify it on principle alone and report the results under both rules (§3.1). It does not touch the first two files, in which no variable is untestable.

**S1 Repetition.** The share of consecutive country-year pairs holding an identical value. A genuinely stable quantity repeats; we take a quantity that repeats in most countries in most years to be one that is not being re-measured.

**S2 Granularity.** Distinct values divided by observations; the share held by the single most common value; and the share falling on round numbers (multiples of ten, or of a thousand for monetary variables). We assume that estimates cluster on round numbers and on a small number of conventional values; this premise has not been validated against reported values of known provenance.

**S3 Identity.** Where a total and its components are both published, do the components sum to the total within 1%? This tests internal consistency rather than external validity, and a variable can be internally perfect while being an estimate.

**S4 Bounds.** Where a definition implies a range — a percentage must lie in [0, 100] — do the values respect it?

**S5 Comparison with the dictionary.** After classification, each variable's dictionary definition was read for a label of estimation. We counted a variable as *labelled* if its definition contains "estimat" or "typical". "Expected" (as in expected funding) and "average" were not counted: the first describes a forecast, the second a statistic. The rule is a convention and the result depends on it (§5).

**No single screen condemns a variable.** A small integer count is legitimately round; a stable quantity legitimately repeats. We therefore count how many of four tests a continuous variable trips (repetition, distinct ratio, modal share, roundness) and classify it as *measurement-like* (0–1), *mixed* (2) or *estimate-like* (3–4). Thresholds are conventions, stated in the code so a reader can change them; the classification is insensitive to small changes where the underlying distribution is strongly bimodal (§3.1).

### 2.3 Reproducibility

The screen is a single pure-Python script with no third-party dependency. It regenerates every figure in this paper from the raw files in one command [7] (including the pre-S0 counterfactual of §3.1) and writes a per-variable results table. Code, archived inputs and the results table: [repository URL and DOI to be inserted at acceptance].

### 2.4 Ethics

Not required: aggregated, publicly available programme data with no individual-level records.

---

## 3. Results

### 3.1 Six datasets: the division is counted versus characterised

Of 443 variables meeting the inclusion threshold across the six files, **42 are categorical (S0)** and **43 are untestable on repetition**. Of the remaining 358 continuous variables, **206 screen as measurement-like, 68 as mixed and 84 as estimate-like.**

**Table 1. Screen results by dataset.**

| Dataset | Continuous | Categorical | Untestable | Median repetition | Measurement | Mixed | Estimate | Median if untestable scored 0% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Budget | 37 | 0 | 0 | 13.0% | 35 | 1 | 1 | 13.0% |
| Expenditure and utilisation | 39 | 1 | 0 | 15.4% | 28 | 7 | 4 | 15.4% |
| Notifications | 166 | 16 | 3 | 15.6% | 104 | 39 | 23 | 14.9% |
| Treatment outcomes | 66 | 1 | 24 | 33.0% | 21 | 20 | 25 | 20.5% |
| Laboratory diagnostic services | 41 | 12 | 16 | **63.0%** | 9 | 1 | **31** | **53.5%** |
| Contact tracing / TPT | 9 | 12 | 0 | **3.5%** | 9 | 0 | 0 | 3.5% |

The last column is a sensitivity analysis on the S0b rule (§2.2). Excluding untestable variables, laboratory repetition is 63.0% against 13.0-15.6% for the budget, expenditure and notification files, 4.0 to 4.8 times as high; scoring them as zero, it is 53.5%, 3.4 to 4.1 times as high. The division holds under either rule; it does not depend on the rule that favours it.

**Repeated zeros do not produce the division.** A repeated zero is a stable absence of events, not a carried-forward estimate, and most variables in these files are zero-dominated (§3.5). Repetition was therefore recomputed over the subset of adjacent pairs in which at least one of the two values is non-zero (Table 2). Every file falls, but not equally: the three large counted files converge on 5.2-9.2% while laboratory diagnostic services remains at 48.0%, a 5.2 to 9.2-fold gap, wider in relative terms than the unrestricted 4.0 to 4.8-fold one. The potential confound also runs the wrong way to explain the finding. Laboratory diagnostic services has the **lowest** share of zero-dominated variables of any file (24 of 41, 59%) and the highest repetition; treatment outcomes has the highest share (65 of 66, 98%) and, once zero-to-zero pairs are removed, ordinary repetition. The restricted statistic is reported only; it does not feed the classification in Table 1, which stands as specified.

**Table 2. Repetition excluding adjacent pairs in which both values are zero.** Restricted to variables with at least 20 such pairs.

| Dataset | Median repetition | Excluding zero-to-zero pairs | Zero as modal value |
|---|---:|---:|---:|
| Budget | 13.0% | 9.2% | 30 / 37 |
| Expenditure and utilisation | 15.4% | 7.3% | 32 / 39 |
| Notifications | 15.6% | 5.2% | 129 / 166 |
| Treatment outcomes | 33.0% | 6.5% | 65 / 66 |
| Laboratory diagnostic services | **63.0%** | **48.0%** | **24 / 41** |
| Contact tracing / TPT | 3.5% | 1.9% | 8 / 9 |

**The division is not financial versus utilisation.** Notifications (15.6%) and contact tracing (3.5%) are service-delivery data, yet they repeat as rarely as the financial files. Laboratory diagnostic services repeats at 63.0%. The first two files alone had suggested a financial/utilisation split because their high-repetition variables were all utilisation variables; the replication shows that was a confound, not the principle (§4.1). What the high-repetition variables share is that they *characterise* the system (laboratory capacity and status, typical hospitalisation share and duration, facility visits per patient), whereas the low-repetition ones are *counted* from the programme's own records (money spent, cases notified, contacts screened).

**Treatment outcomes appear intermediate (33.0%, or 20.5% under the inclusive rule), but the appearance is repeated zeros.** Sixty-five of its 66 continuous variables have zero as their most common value -- they are counts of rare outcomes in disaggregated categories, mostly zero in most countries -- and excluding zero-to-zero pairs the file falls to 6.5%, the lowest of the three large files (Table 2). It is a counted file whose counts are usually zero, not a third kind. It also has the highest proportion of untestable variables: 24 of its 91 variables have no country with an adjacent pair, which suggests that some cohort outcome data is reported in a way that yields a single observation per country. We note this and do not rely on it.

**The screen's own false positive.** Before S0 existed, the contact-tracing dataset looked estimate-like. Its 12 categorical flags (`prevtx_data_available`, `tpt_3hp` and similar) repeat and sit on round numbers by nature. Scored without S0, the dataset had 20 testable variables, a median repetition of 63.8% (59.7% with its one untestable variable scored as zero) and 11 estimate-like variables. With S0 it has a median of 3.5% and none. Its apparent unreliability was entirely an artefact of the screen, and we found it only by replicating on a further dataset (§5).

**In the two files first screened (77 variables)**, one variable is categorical, **`hosp_type_mdr`** (4 distinct values: 2, 140, 141, 142; a code, not a measure), and none is untestable, so the S0b rule leaves them unaffected. Of the 76 continuous variables, **63 are measurement-like, 8 mixed and 5 estimate-like.** An earlier version of this paper reported six estimate-like variables and listed `hosp_type_mdr` among them; that was the S0 error, corrected here.

**Table 3. The five estimate-like variables in the budget and expenditure files.**

| Variable | n | Distinct values | Repetition | Distinct / n | Modal value share | Round |
|---|---:|---:|---:|---:|---:|---:|
| `hospd_prct_mdr` | 1,421 | 81 | 69.6% | 0.06 | 35.3% | 66.6% |
| `hospd_dur_mdr` | 1,368 | 111 | 66.5% | 0.08 | 11.8% | 67.1% |
| `cf_tot_usaid` | 628 | 182 | 64.4% | 0.29 | 64.3% | 49.1% |
| `hcfvisit_mdr` | 1,364 | 197 | 61.6% | 0.14 | 11.1% | 40.4% |
| `hospd_prct_dstb` | 1,467 | 92 | 61.5% | 0.06 | 9.8% | 48.0% |

Reported separately as categorical: `hosp_type_mdr` (n = 1,631; 4 distinct values).

**Table 4. For contrast, the six least-repetitive variables in the budget and expenditure files.**

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

This matters for interpretation. The financial variables are not merely more variable than the characterised ones; they are demonstrably coherent. Whatever process produces them enforces arithmetic consistency across eleven line items in every reporting country. No comparable constraint operates on the characterised variables, which have no total to reconcile against.

### 3.3 What the characterised variables cannot support

`hospd_prct_mdr`, the share of drug-resistant TB patients hospitalised, illustrates the practical consequence. It covers **199 countries** and **1,421 country-years** — coverage that invites a cross-country or trend analysis.

Whether patients with drug-resistant TB are hospitalised or managed in ambulatory or decentralised settings is a substantive model-of-care choice. The effectiveness of the two approaches has been reviewed systematically [8,9], and WHO's current treatment guidance addresses models of care [10].

It has **81 distinct values**. **35.3%** of observations are exactly 100; **11.6%** are exactly 0; **70.5%** fall on multiples of ten. Among the 178 countries with four or more years of data, **42% report an identical value in their first and last year**.

A "global trend in DR-TB hospitalisation, 2017–2025" computed from this variable would be driven by whichever minority of countries revised their entry, and by when they did so. It would describe revision behaviour, not clinical practice. The same applies to duration of hospitalisation (66.5% repetition) and facility visits per patient (61.6%).

### 3.4 A second failure mode: two plausible denominators, one correct

The files publish both `exp_tot` (expenditure) and `rcvd_tot` (funds received). Computing the Global Fund share of financing against the first — the intuitive choice, since expenditure is what a programme did — produces shares exceeding 100% in **14.5%** of 841 country-years. Against `rcvd_tot`, **no country-year exceeds 100% in 842 observations**.

The dictionary defines `exp_tot` as "Total actual expenditure (US Dollars)" and `rcvd_tot` as "Total funding received for all budget line items (US Dollars)" [5]. We read the difference as one of timing: money received in one year may be spent in another. The dictionary does not state this. Both columns are correct; only one is the right denominator for a funding share, and nothing in the file names the pairing.

The extreme case is instructive beyond the pairing. The maximum ratio is **28,417%** (Chad, 2019): US$1,989,218 reported as received from the Global Fund against a reported total TB expenditure of **US$7,000** for the year. A national programme expenditure of seven thousand dollars is not plausible, so the implausibility that the wrong denominator exposes is not only in the ratio — it is in the denominator itself. A screen applied to a derived quantity can therefore surface a problem in a variable that passes every screen applied to it directly: `exp_tot` is measurement-like on all four tests.

We report this failure mode because we committed it ourselves. We also mis-reported its magnitude: an earlier draft gave the maximum as 687%, which was the largest value in a filtered subset we happened to be examining rather than the maximum in the data. Both errors were found the same way — by a value that looked wrong forcing a check — and neither would have been caught by the screens in §2.2.

### 3.5 The screen's verdicts against the dictionary's labels

Of the 443 variables, the dictionary labels **six** as estimated or typical (S5), all in the expenditure file: `hospd_prct_dstb`, `hospd_prct_mdr`, `hospd_dur_dstb`, `hospd_dur_mdr`, `hcfvisit_dstb` and `hcfvisit_mdr`. Table 5 cross-tabulates them against the screen.

**Table 5. Screen verdict by dictionary label.**

| | Estimate-like | Mixed | Measurement-like | Categorical | Untestable |
|---|---:|---:|---:|---:|---:|
| Labelled (6) | 4 | 2 | 0 | 0 | 0 |
| Not labelled (437) | 80 | 66 | 206 | 42 | 43 |

**Where they agree.** All six labelled variables are classified non-measurement-like, four estimate-like and two mixed, and none measurement-like. Of the 358 continuous variables 152 are non-measurement-like, so six labelled variables falling there by chance has probability 0.006. We read this as agreement, not proof: six variables, one file, and the six come in related pairs, so they are not independent.

**Where they disagree.** The screen flags 80 estimate-like variables that the dictionary does not label. Most are not evidence of estimation. Seventy of the 80 have zero as their most common value; in the notifications and outcomes files all 48 of the estimate-like variables do, mostly small counts of rare events. A repeated zero is what a stable absence of events looks like. The one financial variable among the 80, `cf_tot_usaid`, is defined as "Expected funding from USAID (US Dollars)", with no hint of estimation, yet screens estimate-like (64.4% repetition; 64.3% of values held by a single number). That number is zero. Among consecutive-year pairs with either value non-zero, 11.7% are identical, against 2.4-6.8% for the other expected-funding sources (§4.2). The screen therefore picked out a real difference between USAID and the other sources, but most of what it flagged is a repeated zero, and we do not call `cf_tot_usaid` an unlabelled estimate.

**What the comparison does and does not show.** The dictionary and the screen answer different questions. The dictionary says what a variable is; the screen says whether its values move. They agree where an estimate is labelled and moves rarely. The hospitalisation variables are the clearest case: they are labelled, and the screen shows the label's practical consequence, which the label itself does not state.

---

## 4. Discussion

### 4.1 Kind is labelled, vintage is not: a retraction of our central claim

**An earlier version of this paper said, in its abstract and here, that "nothing in the files distinguishes" measurements from estimates. That was wrong.** WHO's dictionary defines `hospd_prct_dstb`, `hospd_prct_mdr`, `hospd_dur_dstb` and `hospd_dur_mdr` as "Estimated" quantities and `hcfvisit_dstb` and `hcfvisit_mdr` as "Typical" ones. Four of the five variables the earlier version used as its headline example were therefore already labelled by WHO,, which the earlier text did not account for. What was wrong was the inference that the files are silent; what survives is narrower.

Three things survive. First, the label sits in a different file from the data, so an analyst joining on the 46 bare column names of the expenditure file never meets the word "Estimated". Second, the label describes the kind of quantity, not the vintage of each value. "Estimated percentage hospitalised" does not tell a reader that 69.6% of consecutive country-year pairs are identical, or that 42% of the 178 countries with four or more years never change their entry, and no field in any file does. That is what determines whether a trend analysis is possible, and it is this paper's finding. Third, the screen can be checked against the labels (§3.5): it agrees with them where they exist and flags variables they leave unlabelled, though the one financial example, `cf_tot_usaid`, turned out to reflect repeated zeros rather than repeated estimates, which limits what the screen can claim.

### 4.1.1 Counted versus characterised: an earlier retraction

**A still earlier version said the division ran between financial and utilisation variables. Our own replication refutes that.** The reading rested on two files in which every high-repetition variable happened to be a utilisation variable, so the two explanations could not be told apart. Four further datasets from the same programme and countries separate them. Notifications and contact tracing are service-delivery data, not financial, and repeat 15.6% and 3.5% of the time, like or below the financial files; laboratory diagnostic services repeats 63.0% of the time. A financial/utilisation boundary predicts none of that. (The earlier version's classification was also inflated by a screen defect, the missing S0; the contact-tracing result in §3.1 is its clearest demonstration.)

What survives is a distinction of kind. Quantities a programme can **count from its own records** (money spent, cases notified, contacts screened) are re-derived each year and repeat 13.0-15.6% of the time in the three large files, 3.5% in contact tracing. Quantities that **characterise the system's standing configuration** (laboratory infrastructure, typical share hospitalised and typical stay, visits per patient) repeat at 63.0% (53.5% under the inclusive rule) in laboratory diagnostic services and at 61.5-69.6% for the hospitalisation and visit variables of the expenditure file. A programme cannot count its way to the second kind; it can only describe it, and describes it the same way until something changes. This is a post hoc reading of six datasets, not a tested hypothesis. The treatment-outcomes file appeared to sit between the two at 33.0%; once repeated zeros are excluded it falls to 6.5% and belongs with the counted files (§3.1).

Distributing both kinds under one schema, one dictionary and no provenance field invites the inference that they are the same kind of thing. They are not, and the difference determines which analyses are possible.

### 4.2 Why the characterised variables are probably not errors

We do not read the repetition as carelessness, and the replication strengthens the benign reading. A programme asked every year for its laboratory configuration will reasonably restate its standing answer; a hospitalisation share and average stay are properties of a service-delivery model that does not change annually. The reporting behaviour is sensible; what is missing is the flag that would let an analyst see it. This is inference from the shape of the data, not from any account of how countries completed the return (§5).

The one financial variable the screen flags, `cf_tot_usaid`, is a different case and we do not read it as a restated estimate. Its dictionary definition ("Expected funding from USAID") carries no label of estimation, like every other financial variable. But 64.3% of its values are zero, and the high repetition is largely countries repeatedly reporting no USAID funding. Restricted to consecutive-year pairs in which either value is non-zero, 11.7% are identical (24 of 206 pairs), higher than the other expected-funding sources (2.4% for Global Fund, 3.2% for other grants, 6.8% for domestic) but far from the 61-70% of the hospitalisation variables. An earlier version of this section called `cf_tot_usaid` a fixed external commitment restated until it changes; the data do not support that, and the sentence is withdrawn.

### 4.3 Implications for secondary analysis

**Trend claims from characterised variables should not be made** without first showing that the variable moves for reasons other than revision. The screen in §2.2 takes seconds and settles it.

**Cross-sectional comparison is weaker than it looks.** With 81 distinct values over 199 countries, much apparent between-country variation is variation between conventional answers.

**Internal consistency is not validity.** The financial variables reconcile perfectly and are still subject to definitional change, pooling and reporting convention; perfect arithmetic says nothing about whether a line item means the same thing in two countries. WHO's data quality framework likewise separates internal from external consistency [6].

**Published coverage is not evidential weight.** 1,421 observations across 199 countries reads as a strong dataset; after accounting for repetition the independent information is a small fraction of that.

### 4.4 What would fix it

**A vintage flag per value.** Because the kind of quantity is often already labelled (§4.1), the remedy is not to add a kind field. It is to record, for each variable-year, whether the value was newly established, re-confirmed or restated unchanged from the previous return, or the year in which it was last revised. Countries presumably know which applies when they complete the return, though we cannot observe that process (§5). Provenance metadata is a recognised element of data stewardship [11], with a substantial technical literature [12].

**Ship the labels with the data.** The dictionary's definitions, including its "Estimated" and "Typical" labels, would reach analysts if they were carried in the data file or its column metadata, so that they are not a separate download that a join on column names bypasses.

**A stated denominator pairing.** Where a file publishes two plausible denominators, the dictionary should say which belongs with which numerator.

**Publish the screen with the data.** The tests here are generic. Running them at release and shipping the results table would let every user see, before analysis, which variables carry annual information; until a vintage flag exists, this is a stand-in for it. Documentation shipped with a dataset has precedent in the datasheet proposal [13].

---

## 5. Limitations

The screens detect signatures consistent with non-measurement; they cannot prove that any particular value was carried forward rather than re-measured and found unchanged. A genuinely stable quantity is indistinguishable, on internal evidence, from an unrevised one — which is precisely the ambiguity a provenance flag would remove.

The classification thresholds are conventions. We chose them before examining the results and state them in the code; the bimodality of the underlying distribution (§3.1) means moderate changes do not move variables between groups, but a reader preferring different cut-points can recompute.

Variables with fewer than 100 observations were excluded, so the screen is silent about sparsely reported quantities, which may be the least reliable of all.

We screened six files from one programme at one point in time. Whether the counted/characterised division generalises to other WHO disease programmes is an open and directly testable question. The division itself was found post hoc. A seventh file from the same programme, public-private mix (`TB_ppm`), was screened after the analysis was complete and is consistent with it but adds little: only two of its variables clear the 100-observation threshold, both counts of new diagnoses, and both screen measurement-like (median repetition 21.5%, 3.6% excluding zero-to-zero pairs). It is reported for completeness and the headline counts above exclude it.

**The screen's validation is partial.** Before S0 existed it produced a false positive on the contact-tracing dataset, labelling a set of ordinary yes/no flags as estimate-like, and we found it only by replication on a further dataset. Both the five-or-fewer-values convention of S0 and the untestable class of S0b were added in response to failures. The comparison with the dictionary (§3.5) is the first external check, and it is thin: it covers six variables, all in one file, defined by a wording rule we chose, and it can show only that the screen does not miss labelled estimates, not that the 80 variables it flags beyond them are estimates. We found that 70 of those 80 have zero as their most common value, as do 71 of all 84 estimate-like variables, including 21 of the 31 in the laboratory file. A repeated zero (no such test performed, no such event) is not a restated estimate, and the screen does not distinguish them; the laboratory median of 63.0% in §3.1 should be read with that in mind. The hospitalisation and visit variables are not affected (of the four labelled estimate-like variables, only one has zero as its most common value). Other failure modes may remain: a six-valued code, for example, would not be caught by S0.

The 43 untestable variables are unclassified, not clean; they are concentrated in treatment outcomes and laboratory data.

Finally, we cannot observe the national reporting process, so §4.2's benign interpretation is inference from the data's shape, not evidence about what reporters did.

---

## 6. Conclusions

WHO's dictionary tells an analyst what kind of quantity a variable is, for example that the share of drug-resistant TB patients hospitalised is an estimate. It is a separate file from the data, and it does not say how often each value is revised. Across six WHO TB datasets, variables a programme counts from its own records (expenditure, notifications, contacts screened) repeat 15.6% of the time or less, while the hospitalisation and visit variables repeat 61.5-69.6% of the time and, for 42% of countries with four or more years, never change. The screen agrees with every one of the dictionary's labels (six of six fall outside the measurement-like class), but it cannot separate a repeated estimate from a repeated zero, which limits what it says about the 80 variables the dictionary leaves unlabelled. Of the 77 variables first screened, five are estimate-like, not six: `hosp_type_mdr` is a categorical code. Our first reading of the division as financial versus utilisation was wrong, and so was our claim that nothing in the files distinguishes measurements from estimates.

The remedy is a vintage flag per value, which the reporting country is presumably already in a position to supply, and the dictionary's labels carried in the data file. Until then, the screen is a few seconds of work that tells an analyst which of these numbers can support a question about change.

---

## References

1. World Health Organization. Global Tuberculosis Programme country data: budget, expenditure and utilisation, notifications, treatment outcomes, laboratory diagnostic services, and contact tracing and preventive treatment datasets. Geneva: World Health Organization; 2026. Available from: https://extranet.who.int/tme/ [data files dated 25 August and 12 November 2026]. This data-collection system no longer accepts updates; the archived input files are deposited with the analysis code.
2. World Health Organization. Global tuberculosis report 2025. Geneva: World Health Organization; 2025.
3. Maiga A, Jiwani SS, Mutua MK, Porth TA, Taylor CM, Asiki G, et al. Generating statistics from health facility data: the state of routine health information systems in Eastern and Southern Africa. BMJ Glob Health. 2019;4(5):e001849. doi:10.1136/bmjgh-2019-001849
4. Lundin R, Mariani I, Peven K, Day LT, Lazzerini M. Quality of routine health facility data used for newborn indicators in low- and middle-income countries: a systematic review. J Glob Health. 2022;12:04019. doi:10.7189/jogh.12.04019
5. World Health Organization. Global Tuberculosis Programme data dictionary [file TB_dictionary_2026-08-25.csv]. Geneva: World Health Organization; 2026. Archived with the analysis code.
6. World Health Organization. Data quality assurance: module 1: framework and metrics. Geneva: World Health Organization; 2023. ISBN 978-92-4-004735-8. Available from: https://www.who.int/publications/i/item/9789240047365
7. Peng RD. Reproducible research in computational science. Science. 2011;334(6060):1226-7. doi:10.1126/science.1213847
8. Bassili A, Fitzpatrick C, Qadeer E, Fatima R, Floyd K, Jaramillo E. A systematic review of the effectiveness of hospital- and ambulatory-based management of multidrug-resistant tuberculosis. Am J Trop Med Hyg. 2013;89(2):271-80. doi:10.4269/ajtmh.13-0004
9. Ho J, Byrne AL, Linh NN, Jaramillo E, Fox GJ. Decentralized care for multidrug-resistant tuberculosis: a systematic review and meta-analysis. Bull World Health Organ. 2017;95(8):584-93. doi:10.2471/BLT.17.193375
10. World Health Organization. WHO consolidated guidelines on tuberculosis. Module 4: treatment and care. 2nd ed. Geneva: World Health Organization; 2026. ISBN 978-92-4-012512-4.
11. Wilkinson MD, Dumontier M, Aalbersberg IJ, Appleton G, Axton M, Baak A, et al. The FAIR Guiding Principles for scientific data management and stewardship. Sci Data. 2016;3:160018. doi:10.1038/sdata.2016.18
12. Herschel M, Diestelkamper R, Ben Lahmar H. A survey on provenance: what for? What form? What from? VLDB J. 2017;26(6):881-906. doi:10.1007/s00778-017-0486-1
13. Gebru T, Morgenstern J, Vecchione B, Vaughan JW, Wallach H, Daume H 3rd, et al. Datasheets for datasets. Commun ACM. 2021;64(12):86-92. doi:10.1145/3458723

---

## Declarations

**Contributors.** Sole author: conception, analysis, code, verification, manuscript.

**Funding.** None. **Competing interests.** None declared. **Ethical clearance.** Not required (§2.4).

**Data availability.** Inputs are public WHO datasets; the archived copies, the screening script and the per-variable results table are deposited at [URL and DOI at acceptance].

**Use of generative AI.** The author used a large language model as a drafting and analysis assistant. All analytical decisions, verification and conclusions are the author's, who takes full responsibility.

---
