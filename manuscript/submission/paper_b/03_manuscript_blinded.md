# The label says what kind, not how old: a reproducible screen of 443 variables in six WHO tuberculosis datasets

**Running title:** Kind and vintage in WHO TB data

---

## Abstract

**Background.** WHO publishes country-reported tuberculosis data as annual country-by-year tables, with definitions in a separate dictionary. That dictionary records the kind of quantity a variable holds, not the vintage of each value, and it is not in the data file.

**Methods.** We screened all 443 numeric variables having at least 100 observations across six WHO tuberculosis datasets, covering 217 countries, 1980 to 2026, and 25,181 country-year records. From the published files alone, variables with five or fewer distinct values were set aside as categorical; the rest were assessed on repetition (the share of consecutive country-year pairs with an identical value), granularity, identity and bounds, then compared with the dictionary's labels.

**Results.** Of 358 continuous variables, 206 screened as measurement-like, 68 as mixed and 84 as estimate-like. Median repetition was 13.0-15.6% for the budget, expenditure and notification files and 3.5% for contact tracing, against **63.0% for laboratory services**. The screen placed none of the six dictionary-labelled variables in the measurement-like class (P = 0.006). For `hospd_prct_mdr`, 69.6% of consecutive pairs are identical and 42% of 178 countries never change their entry. Seventy of the 80 unlabelled flagged variables are zero-dominated; excluding pairs in which both values are zero, median repetition fell to 5.2-9.2% in the three large counted files but only to **48.0%** in laboratory services.

**Conclusions.** A trend analysis needs to know whether a value was revised, not only what kind of quantity it is. WHO's labels settle the second, not the first; a per-value vintage flag would settle both.

**Keywords:** Data Accuracy; Datasets as Topic; Health Services Research; Reproducibility of Results; Tuberculosis; World Health Organization

## Key messages

- WHO's tuberculosis data dictionary records what kind of quantity each variable holds but no field in any published file records whether a given value was re-measured for that year or carried forward unchanged from the previous one.
- Screening all 443 numeric variables across six datasets separates quantities a programme counts from its own records, which repeat in 13.0-15.6% of consecutive country-year pairs, from quantities that characterise its standing configuration, which repeat in 63.0%.
- The separation is not an artefact of repeated zeros, because excluding pairs in which both values are zero widens it rather than closing it, and the file with the highest repetition holds the fewest zero-dominated variables.

---

## 1. Background

WHO's Global Tuberculosis Programme collects and republishes country-reported data on TB financing and service delivery [1,2]. The files are widely used: for investment cases, for cross-country comparison of cost and delivery models, and as covariates in modelling studies. They are distributed as flat annual tables. The data files carry column names only; the definitions are in a separate dictionary file. In practice the variables are treated as equivalent — each a country's report for that year.

This paper asks a prior question. A number in an annual return may be a measurement taken that year, or an estimate entered once and repeated because no one revised it. Only a value that is re-established each year supports inference about change over time. WHO's dictionary does say, for some variables, that the quantity is an estimate; for example the share of patients hospitalised is defined as an "Estimated percentage". Two things remain unsaid. The label is in a different file from the data. And it describes the kind of quantity, not the vintage of each value: whether this year's entry was revised from last year's, or simply restated.

The quality of routine health data has been assessed in other settings [3,4], but, to our knowledge, not for vintage in these datasets. The question is tractable because several signatures of restatement are computable from the published file alone. We also compare the screen's verdicts with the dictionary's labels, which gives the screen a partial check that it otherwise lacks.

---

## 2. Methods

### 2.1 Data

Six files from WHO's tuberculosis programme, retrieved in November 2026 and archived with the analysis code; file versions are WHO's own release dates, 12 November 2026 for the budget file and 25 August 2026 for the other five and the dictionary. Together they hold 25,181 country-year records for 217 countries and areas, 1980 to 2026; Supplementary S0 lists each file's rows, years and columns. The budget and expenditure files were screened first (77 variables) and the other four afterwards, as a replication.

WHO's published data dictionary [5] supplied every variable definition and is the comparison standard in §3.4. Definitions are used rather than column names, because the two diverge: `budget_prog` reads as programme costs generally but is defined as *"programme costs to treat drug-susceptible TB"*.

### 2.2 The screens

Each screen is computable from the published file alone (Figure 1); the full specification, with the convention chosen for every threshold, is in Supplementary S1. **S0** sets aside as *categorical* any variable with five or fewer distinct values, because a status flag legitimately repeats, takes few values and sits on round numbers for reasons unrelated to estimation. **S0b** sets aside as *untestable* any continuous variable for which no country has an adjacent pair of observations, since a test that could not run is not evidence of cleanliness. The remaining continuous variables are assessed on four signatures: **repetition**, the share of consecutive country-year pairs holding an identical value; **granularity**, the distinct-value ratio, the share held by the single most common value, and the share falling on round numbers; **identity**, whether published components sum to their published total; and **bounds**, whether values respect a range implied by the definition. A variable is classified *measurement-like* (trips none or one), *mixed* (two) or *estimate-like* (three or four). No single screen condemns a variable: a small count is legitimately round and a stable quantity legitimately repeats. Thresholds are conventions, stated in the code. Finally, **S5** compares each verdict with the variable's dictionary definition, counting a variable as labelled if that definition contains "estimat" or "typical".

These screens are our own operationalisation of non-measurement, justified by face validity; we know of no published validation of them for country-reported programme data. The nearest framework, WHO's data quality assurance toolkit [6], assesses completeness and internal and external consistency of facility data; our screens are of that general kind but were designed for published country returns and are not an implementation of it.

### 2.3 Reproducibility

The screen is a single pure-Python script with no third-party dependency. It regenerates every number in this paper from the raw files in one command [7], including the counterfactual without rule S0 (Supplementary S1c), and writes a per-variable results table; the figures are drawn from those outputs separately. A large language model was used as a drafting and analysis assistant; every analytical decision, the code and its verification are the author's. Code, archived inputs and the results table: [repository URL withheld for blind review], [archive DOI withheld for blind review].

### 2.4 Ethics

Not required: aggregated, publicly available programme data with no individual-level records.

---

## 3. Results

### 3.1 Six datasets: the division is counted versus characterised

Of 443 variables meeting the inclusion threshold across the six files, **42 are categorical (S0)** and **43 are untestable on repetition**. Of the remaining 358 continuous variables, **206 screen as measurement-like, 68 as mixed and 84 as estimate-like**, and the proportions differ sharply by file (Table 1).

[Table 1 about here]

**Repeated zeros do not produce the division (Figure 2).** A repeated zero is a stable absence, not a carried-forward estimate, and most variables in these files are zero-dominated (§3.4). Repetition was therefore recomputed over the subset of adjacent pairs in which at least one of the two values is non-zero (Table 2). Every file falls, but not equally: the three large counted files converge on 5.2-9.2% while laboratory diagnostic services remains at 48.0%, a 5.2 to 9.2-fold gap, wider than the unrestricted 4.0 to 4.8-fold one. The potential confound also runs the wrong way to explain the finding. Laboratory diagnostic services has the **lowest** share of zero-dominated variables of any file (24 of 41, 59%) and the highest repetition; treatment outcomes has the highest share (65 of 66, 98%) and, once zero-to-zero pairs are removed, ordinary repetition. The restricted statistic is reported only; it does not feed the classification in Table 1.

[Table 2 about here]

**Treatment outcomes appear intermediate (33.0%), but the appearance is repeated zeros.** Sixty-five of its 66 continuous variables are zero-modal -- they are counts of rare outcomes in disaggregated categories, mostly zero in most countries -- and excluding zero-to-zero pairs the file falls to 6.5%, the lowest of the three large files (Table 2). It is a counted file whose counts are usually zero, not a third kind. It also has the highest proportion of untestable variables (24 of 91), which we note and do not rely on.

The variables driving this are identifiable individually. Table 3 lists the five estimate-like variables of the budget and expenditure files, all of them hospitalisation or visit quantities; Table 4 lists the six least repetitive variables of the same two files for contrast, all of them counts or amounts.

[Table 3 about here]

[Table 4 about here]

### 3.2 The financial data is internally immaculate

Four of the five component-to-total identities reconcile in **100%** of testable country-years, and the fifth in **98.9%** (Table 5).

[Table 5 about here]

This matters for interpretation. The financial variables are not merely more variable than the characterised ones; they are demonstrably coherent. Whatever process produces them enforces arithmetic consistency across eleven line items in every reporting country. No comparable constraint operates on the characterised variables, which have no total to reconcile against.

### 3.3 What the characterised variables cannot support

`hospd_prct_mdr`, the share of drug-resistant TB patients hospitalised, illustrates the practical consequence. It covers **199 countries** and **1,421 country-years** — coverage that invites a cross-country or trend analysis.

Hospitalised versus ambulatory or decentralised management is a substantive model-of-care choice, reviewed systematically [8,9] and addressed in WHO's current guidance [10].

It has **81 distinct values**. **35.3%** of observations are exactly 100; **11.6%** are exactly 0; **70.5%** fall on multiples of ten. Among the 178 countries with four or more years of data, **42% report an identical value in their first and last year**.

A "global trend in DR-TB hospitalisation, 2017–2025" from this variable would be driven by whichever minority of countries revised their entry, and when. It would describe revision behaviour, not clinical practice. The same applies to duration of hospitalisation (66.5% repetition) and facility visits per patient (61.6%).

### 3.4 The screen's verdicts against the dictionary's labels

Of the 443 variables, the dictionary labels **six** as estimated or typical (S5), all in the expenditure file: `hospd_prct_dstb`, `hospd_prct_mdr`, `hospd_dur_dstb`, `hospd_dur_mdr`, `hcfvisit_dstb` and `hcfvisit_mdr`. Table 6 cross-tabulates them against the screen.

[Table 6 about here]

**Where they agree.** All six labelled variables are classified non-measurement-like, four estimate-like and two mixed, and none measurement-like. Of the 358 continuous variables 152 are non-measurement-like, so six labelled variables falling there by chance has probability 0.006. We read this as agreement, not proof: six variables, one file, and the six come in related pairs, so they are not independent.

**Where they disagree.** The screen flags 80 estimate-like variables that the dictionary does not label. Most are not evidence of estimation. Seventy of the 80 have zero as their most common value; in the notifications and outcomes files all 48 of the estimate-like variables do, mostly small counts of rare events. A repeated zero is what a stable absence of events looks like. The one financial variable among the 80, `cf_tot_usaid`, is defined as "Expected funding from USAID (US Dollars)", with no hint of estimation, yet screens estimate-like (64.4% repetition; 64.3% of values held by a single number). That number is zero. Among consecutive-year pairs with either value non-zero, 11.7% are identical, against 2.4-6.8% for the other expected-funding sources (§4.2). The screen therefore picked out a real difference between USAID and the other sources, but most of what it flagged is a repeated zero, and we do not call `cf_tot_usaid` an unlabelled estimate.

**What the comparison does and does not show.** The dictionary and the screen answer different questions. The dictionary says what a variable is; the screen says whether its values move. They agree where an estimate is labelled and moves rarely. The hospitalisation variables are the clearest case: they are labelled, and the screen shows the label's practical consequence, which the label itself does not state.

---

## 4. Discussion

### 4.1 What the dictionary settles, and what it does not

WHO's dictionary does distinguish kind: `hospd_prct_dstb`, `hospd_prct_mdr`, `hospd_dur_dstb` and `hospd_dur_mdr` are defined as "Estimated" quantities and `hcfvisit_dstb` and `hcfvisit_mdr` as "Typical" ones. The files are therefore not silent about what these variables are, and any claim that they are is wrong.

What no document settles is vintage. "Estimated percentage hospitalised" tells a reader the kind of quantity; it does not tell them that 69.6% of consecutive country-year pairs are identical, or that 42% of the 178 countries with four or more years never change their entry. That is what determines whether a trend analysis is possible, and no field in any file records it. Two things limit how far the label helps: it sits in a separate file, so an analyst joining on the expenditure file's 46 bare column names never meets the word "Estimated"; and only six of 443 variables are labelled.

### 4.1.1 Counted and characterised: an alternative explanation ruled out by replication

The obvious reading of the first two files is that the division runs between financial and utilisation variables. In those two files every high-repetition variable is a utilisation variable, so the two explanations cannot be told apart, and a study of the budget and expenditure files alone would be unable to distinguish them. Four further datasets from the same programme and the same countries separate them. Notifications and contact tracing are service-delivery data, not financial, and repeat 15.6% and 3.5% of the time, at or below the financial files; laboratory diagnostic services repeats 63.0% of the time. A financial/utilisation boundary predicts none of that.

What the replication supports instead is a distinction of kind. Quantities a programme **counts from its own records** (money spent, cases notified, contacts screened) are re-derived each year and repeat 13.0-15.6% of the time in the three large files and 3.5% in contact tracing. Quantities that **characterise the system's standing configuration** (laboratory infrastructure, typical share hospitalised and typical stay, visits per patient) repeat at 63.0% in laboratory diagnostic services and at 61.5-69.6% for the hospitalisation and visit variables. A programme cannot count its way to the second kind; it can only describe it, and describes it the same way until something changes. This is a post hoc reading of six datasets, not a tested hypothesis.

Distributing both kinds under one schema, one dictionary and no provenance field invites the inference that they are the same kind of thing. They are not, and the difference determines which analyses are possible.

### 4.2 Why the characterised variables are probably not errors

We do not read the repetition as carelessness. A programme asked every year for its laboratory configuration will reasonably restate its standing answer; a hospitalisation share and average stay are properties of a service-delivery model that does not change annually. The reporting behaviour is sensible; what is missing is the flag that would let an analyst see it. This is inference from the shape of the data, not from any account of how countries completed the return (§5).

The one financial variable the screen flags, `cf_tot_usaid`, is a different case. Its definition carries no label of estimation, but 64.3% of its values are zero: the repetition is largely countries repeatedly reporting no USAID funding. Over pairs in which either value is non-zero, 11.7% are identical (24 of 206), above the other expected-funding sources (2.4% Global Fund, 3.2% other grants, 6.8% domestic) but far below the 61-70% of the hospitalisation variables. That is a real difference between sources, not evidence of a restated estimate.

### 4.3 Implications for analysis and programme evaluation

**Trend claims from characterised variables need a vintage check first**; the screen in §2.2 takes seconds.

**Cross-sectional comparison is weaker than it looks.** With 81 distinct values over 199 countries, much apparent between-country variation is variation between conventional answers.

**Internal consistency is not validity.** The financial variables reconcile at 98.9-100% yet remain subject to definitional change and reporting convention; arithmetic cannot show that a line item means the same thing in two countries, a distinction WHO's data quality framework also draws [6].

**Programme evaluation inherits the same blind spot.** Strategic-plan reviews track laboratory capacity and models of care over time. An unchanged characterised variable may record an unchanged system or a figure nobody re-measured; only the reporting programme can say which, and an evaluation that does not ask will read restatement as stability.

**Published coverage is not evidential weight.** 1,421 observations across 199 countries reads as a strong dataset; after accounting for repetition the independent information is a small fraction of that.

### 4.4 What would fix it

**A vintage flag per value.** Because the kind of quantity is often already labelled (§4.1), the remedy is not to add a kind field. It is to record, for each variable-year, whether the value was newly established, re-confirmed or restated unchanged from the previous return, or the year in which it was last revised. Only the national programme completing the return knows which applies, and recording it costs nothing. Provenance metadata is a recognised element of data stewardship [11], with a substantial technical literature [12].

**Ship the labels with the data.** The dictionary's "Estimated" and "Typical" labels would reach analysts if carried in the data file or its column metadata, rather than in a separate download that a join on column names bypasses.

**Publish the screen with the data.** The tests here are generic. Running them at release and shipping the results table would let every user see, before analysis, which variables carry annual information; until a vintage flag exists, this is a stand-in for it. Documentation shipped with a dataset has precedent in the datasheet proposal [13].

---

## 5. Limitations

The screens detect signatures consistent with non-measurement; they cannot prove any particular value was carried forward rather than re-measured and found unchanged. A genuinely stable quantity is indistinguishable, on internal evidence, from an unrevised one, which is precisely the ambiguity a provenance flag would remove. The thresholds are conventions chosen before the results were examined and stated in the code; the bimodality of the underlying distribution means moderate changes do not move variables between classes, but a reader preferring different cut-points can recompute. We screened six files from one programme at one point in time, and the counted/characterised division was found post hoc, so whether it generalises to other WHO disease programmes is an open and directly testable question. The 43 untestable variables are unclassified, not clean, and are concentrated in treatment outcomes and laboratory data. Supplementary S3 states these limitations in full, and Supplementary S1c and S2 demonstrate two failure modes the method itself exhibits on these data.

## 6. Conclusions

WHO's dictionary tells an analyst what kind of quantity a variable is: that the share of drug-resistant TB patients hospitalised, for example, is an estimate. It sits in a separate file from the data, and it does not say how often any value is revised. Across six WHO tuberculosis datasets, variables a programme counts from its own records repeat in 15.6% of consecutive country-year pairs or fewer, while the hospitalisation and visit variables repeat in 61.5-69.6% and, for 42% of countries with four or more years, never change at all. The screen agrees with every one of the dictionary's six labels and flags 80 variables it does not label, although most of those are dominated by repeated zeros, which bounds what the screen can claim about them.

Two changes would settle this at source: a vintage flag for each value, which the reporting country is already in a position to supply, and the dictionary's labels carried inside the data file rather than beside it. Until then, the screen costs seconds and tells an analyst which of these numbers can support a question about change, and which cannot.

## References

1. World Health Organization. Global Tuberculosis Programme country data: budget, expenditure and utilisation, notifications, treatment outcomes, laboratory diagnostic services, and contact tracing and preventive treatment datasets. Geneva: World Health Organization; 2026. Available from: https://extranet.who.int/tme/ [cited 2026 Nov 13] [data files dated 25 August and 12 November 2026]. This data-collection system no longer accepts updates; the archived input files are deposited with the analysis code.
2. World Health Organization. Global tuberculosis report 2025. Geneva: World Health Organization; 2025. Available from: https://www.who.int/teams/global-programme-on-tuberculosis-and-lung-health/tb-reports/global-tuberculosis-report-2025 [cited 2026 Nov 13].
3. Maiga A, Jiwani SS, Mutua MK, Porth TA, Taylor CM, Asiki G, et al. Generating statistics from health facility data: the state of routine health information systems in Eastern and Southern Africa. BMJ Glob Health. 2019;4(5):e001849. doi:10.1136/bmjgh-2019-001849
4. Lundin R, Mariani I, Peven K, Day LT, Lazzerini M. Quality of routine health facility data used for newborn indicators in low- and middle-income countries: a systematic review. J Glob Health. 2022;12:04019. doi:10.7189/jogh.12.04019
5. World Health Organization. Global Tuberculosis Programme data dictionary [file TB_dictionary_2026-08-25.csv]. Geneva: World Health Organization; 2026. Available from: https://extranet.who.int/tme/ [cited 2026 Nov 13]. Archived with the analysis code.
6. World Health Organization. Data quality assurance: module 1: framework and metrics. Geneva: World Health Organization; 2023. ISBN 978-92-4-004735-8. Available from: https://www.who.int/publications/i/item/9789240047365 [cited 2026 Nov 13].
7. Peng RD. Reproducible research in computational science. Science. 2011;334(6060):1226-7. doi:10.1126/science.1213847
8. Bassili A, Fitzpatrick C, Qadeer E, Fatima R, Floyd K, Jaramillo E. A systematic review of the effectiveness of hospital- and ambulatory-based management of multidrug-resistant tuberculosis. Am J Trop Med Hyg. 2013;89(2):271-80. doi:10.4269/ajtmh.13-0004
9. Ho J, Byrne AL, Linh NN, Jaramillo E, Fox GJ. Decentralized care for multidrug-resistant tuberculosis: a systematic review and meta-analysis. Bull World Health Organ. 2017;95(8):584-93. doi:10.2471/BLT.17.193375
10. World Health Organization. WHO consolidated guidelines on tuberculosis. Module 4: treatment and care. 2nd ed. Geneva: World Health Organization; 2026. ISBN 978-92-4-012512-4. Available from: https://www.who.int/publications/i/item/9789240125124 [cited 2026 Nov 13].
11. Wilkinson MD, Dumontier M, Aalbersberg IJ, Appleton G, Axton M, Baak A, et al. The FAIR Guiding Principles for scientific data management and stewardship. Sci Data. 2016;3:160018. doi:10.1038/sdata.2016.18
12. Herschel M, Diestelkamper R, Ben Lahmar H. A survey on provenance: what for? What form? What from? VLDB J. 2017;26(6):881-906. doi:10.1007/s00778-017-0486-1
13. Gebru T, Morgenstern J, Vecchione B, Vaughan JW, Wallach H, Daume H 3rd, et al. Datasheets for datasets. Commun ACM. 2021;64(12):86-92. doi:10.1145/3458723
14. Benchimol EI, Smeeth L, Guttmann A, Harron K, Moher D, Petersen I, et al. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) Statement. PLOS Med. 2015;12(10):e1001885. doi:10.1371/journal.pmed.1001885

## Figure captions

**Figure 1. How each variable moves through the screen.** The 443 numeric variables with at least 100 observations, showing the two rules that set variables aside before classification and the four signatures on which the remainder are scored, with the count at each step. S0, categorical rule; S0b, untestable-on-repetition rule.

*Alt text: A flow diagram beginning with 443 numeric variables. A first rule sets aside 42 categorical variables, a second sets aside 43 that cannot be tested for repetition, leaving 358 continuous variables scored on four signatures and classified as 206 measurement-like, 68 mixed and 84 estimate-like.*

*Alt text: Two side-by-side dot plots of six WHO tuberculosis datasets. In the left panel most datasets cluster below 20% repetition while laboratory diagnostic services sits around 63%. In the right panel, excluding pairs where both values are zero, the other datasets fall to between 2% and 9% while laboratory diagnostic services remains at 48%, so the gap widens.*

---

**Figure 2. Repetition by dataset, before and after excluding repeated zeros.** Each point is one continuous variable; the horizontal position is the share of that variable's adjacent country-year pairs holding an identical value. The vertical rule marks the dataset median. The left panel uses all adjacent pairs; the right panel uses only pairs in which at least one of the two values is non-zero, since a repeated zero is a stable absence rather than a carried-forward estimate. Laboratory diagnostic services, shown in a separate colour, separates from the other five datasets in both panels, and the separation is wider in the right panel. TPT, tuberculosis preventive treatment.

## Declarations

**Reporting.** This study is reported in accordance with the RECORD statement for studies using routinely collected health data [14]; the completed checklist accompanies this submission.

**Contributors.** Sole author: conception, analysis, code, verification, manuscript.

**Funding.** None. **Competing interests.** None declared. **Ethical clearance.** Not required (§2.4).

**Data availability.** Inputs are public WHO datasets; the archived copies, the screening script and the per-variable results table are deposited at [repository and archive DOI withheld for blind review]. Every input file is listed in `data/raw_file_manifest.csv` with its SHA-256 digest, so the archived copies can be checked byte for byte against the ones analysed. The manifest also records what is not known: for six of the nine files the download route was not noted at acquisition, and it says so rather than reconstructing a plausible one.

**Use of generative AI.** The author used a large language model as a drafting and analysis assistant. All analytical decisions, verification and conclusions are the author's, who takes full responsibility.

---
