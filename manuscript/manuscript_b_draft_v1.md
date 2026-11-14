# Restated, never revised: a vintage analysis of WHO tuberculosis data and the spending estimate built on them

**Running title:** Vintage of WHO tuberculosis data

**Author:** Siddalingaiah H S
Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur – 572106, Karnataka, India.
Correspondence: hssling@yahoo.com · ORCID 0000-0002-4771-8285

**Target journal:** *International Journal of Epidemiology* (Original Article; hybrid, so the subscription route carries no article-processing charge).

---

## Abstract

**Background.** The World Health Organization (WHO) publishes country-reported tuberculosis (TB) data annually and uses them to estimate TB funding in low- and middle-income countries. Analysts treat each value as that year's report. Whether values are revised, restated or filled in has not been measured.

**Methods.** We compared three archived releases of WHO's TB finance and utilisation data (2024-2026), WHO's processed files for its 2025 and 2026 reports, and the code that turns them into published estimates. We measured revision between releases, restatement of a country's previous-year value and values supplied by WHO, and apportioned WHO's estimate of inpatient and outpatient care spending by the provenance of its inputs. The reconstruction reproduced WHO's published totals.

**Results.** None of 16,521 utilisation values changed between releases. Within releases, 62.2-71.3% of utilisation values repeated the country's previous-year value, against 4.8-10.9% for expenditure lines, and none of 3,613 restated values was later revised. WHO filled gaps from up to four years earlier or later. Of WHO's US$ 1.08 billion care estimate for 2025, 16.4% of US$ 6.57 billion total funding, 32.6% rested on inputs newly reported that year, 42.4% on restated inputs and 25.0% on inputs supplied by WHO. India's US$ 182 million rested on values last reported for 2022 and unchanged since 2020.

**Conclusions.** A sixth of WHO's published TB funding figure is computed mostly from numbers that do not describe the year they are used for. A flag recording whether each value was re-measured, restated or imputed would make this visible.

**Keywords:** Data Accuracy; Datasets as Topic; Health Expenditures; Reproducibility of Results; Tuberculosis; World Health Organization

## Key messages

- Across three archived releases, WHO never revised a published tuberculosis utilisation value, so a figure restated or filled in once remains in the record unchanged.
- Countries repeat their own previous-year value for 62-71% of hospital and clinic utilisation entries but for only 5-11% of expenditure lines, and these utilisation entries are the inputs to WHO's estimate of TB care spending.
- Only a third of WHO's US$ 1.08 billion estimate of TB care spending for 2025 rests on inputs reported for that year; the rest repeats earlier years or was supplied by WHO's own pipeline.

---

## 1. Background

WHO's Global Tuberculosis Programme collects country returns every year and republishes them as country-by-year tables [1,2]. They are used for cross-country comparison, investment cases and modelling, and WHO uses them to estimate how much is spent on TB in low- and middle-income countries: US$ 5.9 billion in 2024 in its 2025 report [1] and US$ 6.6 billion in 2025 in its 2026 report [2]. Part of that figure is not reported spending at all. WHO estimates the cost of inpatient and outpatient care from each country's reported share of patients hospitalised, days in hospital and outpatient visits per patient, priced at unit costs, and counts it as domestic funding [1].

Any such figure assumes that each annual value describes its year. Economics has a vocabulary for testing that assumption. A data vintage is a series as published on a given date; comparing vintages shows how much published history is revised, and whether conclusions survive the revisions [3,4]. National accounts are revised routinely, and the revisions are large enough to change inference [4].

Two features of country-reported health data make the question sharper. A value can be restated, entered unchanged from the previous return because nothing prompted a new measurement; and a value can be missing and filled in downstream. Routine health data have been audited for completeness and consistency [5,6], but, to our knowledge, not for vintage. WHO's archives make this testable: each annual report's repository holds a dated snapshot of the country data it used, the processed file it published from, and the code connecting them.

We asked four questions. Are published values revised between releases? How often does a country restate its previous value? What does WHO's pipeline do where a country reported nothing? And how much of WHO's published estimate of TB care spending rests on inputs reported for the year it describes?

---

## 2. Methods

### 2.1 Data

Three releases of WHO's TB finance and utilisation data were compared: the snapshots dated 29 July 2024 and 30 July 2025 in WHO's report repositories for 2024 and 2025, and the public release of 25 August 2026, which matches the 2026 report's snapshot date [7,8]. WHO's processed finance files for its 2025 and 2026 reports, and the R code that produced them, came from the same repositories [8]. Each file was downloaded from a pinned commit and is identified by its SHA-256 digest (Supplementary Note 1); the repositories carry no licence, so the files are not redistributed, but the fetch is reproducible byte for byte. Variable definitions are from WHO's data dictionary [9].

The six utilisation inputs are outpatient visits per patient, share of patients hospitalised and days in hospital, each for drug-susceptible and for multidrug- or rifampicin-resistant (MDR/RR) TB. Four expenditure lines reported in every release (first-line drugs, laboratory, staff, programme management) serve as comparators: they are counted from a programme's own accounts each year.

### 2.2 Measures

*Revision* compares the same country-year value of the same variable in two releases. *Restatement* is a value identical to the same country's value for the previous year in the same release. Both are computed for reporting years 2018 onwards, the first year every release can classify: the 2026 release starts in 2017, so earlier years have no previous year within it.

*WHO-supplied* values were identified by comparing each utilisation value in WHO's processed file with the country's reported value for that year. A reported value used unchanged is classed newly reported or restated; a reported value replaced is classed overridden; a value used where none was reported is classed by the year it matches. WHO's code fills a gap with the same country's value from up to four years earlier and then up to four years later (Supplementary Note 2), and matching was searched in that order.

*Consequence.* WHO's care estimate is the sum of four components per country-year: inpatient care (patients × share hospitalised × days × cost per bed-day) and outpatient care (patients × visits per patient × cost per visit), each for drug-susceptible and MDR/RR-TB. Each component was classed by its own inputs: WHO-supplied if any input was filled or overridden, restated if any other input repeated the previous year, otherwise newly reported. A sensitivity analysis counted a component as current if any one of its inputs was newly reported. Where WHO sets the care estimate to zero because a country's reported spending is believed to include it, nothing was apportioned. Total funding was reconstructed as WHO computes it, funding received by national programmes plus the care estimate, and checked against WHO's published totals.

### 2.3 Locating the affected variables

To test whether the six inputs are exceptional among WHO's TB data, every numeric variable with at least 100 observations in six public WHO TB datasets (443 variables, 217 countries and areas, 1980-2026) was screened for signatures of restatement: repetition of the previous year's value, few distinct values, a dominant modal value and round numbers. Variables with five or fewer distinct values were set aside as categorical and those with no adjacent years as untestable; the rest were classed measurement-like, mixed or estimate-like by how many signatures they showed. The screen is specified in full in Supplementary Note 3, with two failure modes it exhibits (Supplementary Note 4), and its verdicts were compared with the dictionary's own labels of estimation.

### 2.4 Reproducibility and reporting

All analyses are in Python with no third-party numerical dependency; R is used once, to convert WHO's R data files to text unchanged. One command regenerates every number and table from the fetched files [10]. A large language model was used as a drafting and analysis assistant; every analytical decision, the code and its verification are the author's. Code: https://github.com/hssling/provenance-weighted-priority-setting, doi:10.5281/zenodo.24214490. The study is reported following RECORD. Ethical approval was not required: the data are aggregated and public.

---

## 3. Results

### 3.1 Published values are never revised

Between the July 2024 and July 2025 releases, and again between July 2025 and August 2026, no utilisation value changed: none of 16,521 compared (Table 1). Of 8,024 expenditure values compared, three changed, all for one country-year, each by less than 0.1%. The history grows as late returns arrive but is otherwise fixed: a value published once stays as first published.

**Table 1. Revision of published values between WHO releases.** Each value is one country-year of one variable present in both releases.

| Variables | Releases compared | Values in both releases | Values changed |
|---|---|---:|---:|
| Utilisation inputs (6) | Jul 2024 → Jul 2025 | 8,774 | 0 |
| Utilisation inputs (6) | Jul 2025 → Aug 2026 | 7,747 | 0 |
| Expenditure lines (4) | Jul 2024 → Jul 2025 | 3,837 | 0 |
| Expenditure lines (4) | Jul 2025 → Aug 2026 | 4,187 | 3 |

*The 3 changed values are the Russian Federation's 2024 expenditure (laboratory equipment and supplies, programme staff, programme management), each by less than 0.1%. Utilisation inputs: outpatient visits per patient, share hospitalised and days in hospital, each for drug-susceptible and MDR/RR-TB.*

### 3.2 Utilisation values are mostly restated

In every release, 62.2-71.3% of utilisation values were identical to the same country's value for the previous year, against 4.8-10.9% for the expenditure lines (Table 2). Share hospitalised with MDR/RR-TB was the most repetitive input in each release. Restated values persisted: none of the 3,613 utilisation values restated in the July 2024 release had been revised by August 2026.

**Table 2. Restatement: share of a country's values identical to its own value for the previous year, by release, reporting years 2018 onwards.** Consecutive country-year pairs compared in brackets.

| Variable | Jul 2024 | Jul 2025 | Aug 2026 |
|---|---:|---:|---:|
| Outpatient visits per patient, drug-susceptible TB | 63.6% (934) | 65.0% (1,077) | 64.0% (1,203) |
| Outpatient visits per patient, MDR/RR-TB | 63.8% (874) | 64.2% (1,009) | 62.2% (1,127) |
| Share hospitalised, drug-susceptible TB | 62.7% (940) | 63.5% (1,089) | 63.2% (1,206) |
| Share hospitalised, MDR/RR-TB | 70.9% (905) | 71.3% (1,047) | 70.0% (1,160) |
| Days in hospital, drug-susceptible TB | 67.2% (928) | 68.1% (1,071) | 67.6% (1,185) |
| Days in hospital, MDR/RR-TB | 69.4% (873) | 69.6% (1,010) | 67.9% (1,120) |
| Expenditure on first-line drugs | 4.9% (551) | 4.9% (634) | 4.8% (708) |
| Expenditure on laboratory equipment and supplies | 7.6% (540) | 8.0% (624) | 8.2% (697) |
| Expenditure on programme staff | 10.0% (538) | 10.8% (622) | 10.9% (695) |
| Expenditure on programme management | 8.3% (516) | 8.6% (595) | 8.4% (665) |

*Of the 3,613 utilisation values restated in the July 2024 release, 0 had been revised by the August 2026 release.*

### 3.3 WHO fills what countries do not report

In the 2026 report, 784 of the 6,272 utilisation values WHO used for 2018-2025 (12.5%) were supplied by WHO rather than reported for that year (Table 3). Most were filled from an earlier year (602); 49 came from a later year, so that a value reported for one year was used for an earlier one; 72 replaced a reported value. The 2025 report shows the same pattern at a lower level.

**Table 3. Where the utilisation inputs to WHO's spending estimate came from.** Country-year values for the six inputs, 2018–2024 in the 2025 report and 2018–2025 in the 2026 report, in the countries WHO includes.

| Provenance | 2025 report | 2026 report |
|---|---:|---:|
| Reported, differs from the previous year | 1,853 (33.7%) | 2,106 (33.5%) |
| Reported, identical to the previous year | 3,080 (56.0%) | 3,382 (53.8%) |
| Not reported; WHO used an earlier year's value | 449 (8.2%) | 602 (9.6%) |
| Not reported; WHO used a later year's value | 25 (0.5%) | 49 (0.8%) |
| Not reported; WHO value matches no reported year | 33 (0.6%) | 61 (1.0%) |
| Reported, but WHO used a different value | 48 (0.9%) | 72 (1.1%) |
| No value used | 14 (0.3%) | 16 (0.3%) |
| Total | 5,502 | 6,288 |

*WHO's pipeline fills a missing value from the same country's nearest year, up to four years earlier and then up to four years later; the year is identified here by matching the value used to the country's reported values in that order.*

### 3.4 What the published care estimate rests on

WHO's care estimate was 11.4-21.5% of total funding in 2018-2025 (Table 4). For 2025 it was US$ 1.08 billion of US$ 6.57 billion. Of that, 32.6% was computed from inputs newly reported for 2025, 42.4% from inputs restated from 2024 and 25.0% from inputs WHO supplied (Figure 1). Across 2018-2025 the newly reported share ranged from 13.0% to 53.7% (Figure 2). Counting a component as current if any one of its inputs was newly reported raised it only to 14.5-56.8%.

**Table 4. WHO's estimate of spending on inpatient and outpatient TB care, by provenance of the inputs it was computed from, 2026 report.** Each cost component (bed-days and outpatient visits, for drug-susceptible and MDR/RR-TB) is classed by its own inputs: WHO-supplied if any input was filled or replaced by WHO, restated if any other input repeats the previous year, otherwise newly reported.

| Year | Total funding, US$ bn | Care estimate, US$ bn | Care, % of total | Newly reported | Restated | WHO-supplied | Any input newly reported |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 7.14 | 1.54 | 21.5% | 38.5% | 60.6% | 1.0% | 44.7% |
| 2019 | 7.17 | 1.44 | 20.1% | 14.1% | 81.6% | 4.4% | 17.1% |
| 2020 | 6.19 | 0.70 | 11.4% | 53.7% | 40.5% | 5.9% | 56.8% |
| 2021 | 6.19 | 0.81 | 13.1% | 23.8% | 75.5% | 0.7% | 29.0% |
| 2022 | 6.31 | 1.02 | 16.1% | 21.2% | 74.6% | 4.2% | 22.6% |
| 2023 | 6.01 | 1.04 | 17.3% | 13.0% | 64.8% | 22.1% | 14.5% |
| 2024 | 6.03 | 1.05 | 17.5% | 20.6% | 54.1% | 25.3% | 23.7% |
| 2025 | 6.57 | 1.08 | 16.4% | 32.6% | 42.4% | 25.0% | 35.6% |

*Total funding is funding received by national programmes plus the care estimate, as WHO computes it. The reconstruction reproduces WHO's published totals: US$ 6.03 billion for 2024 in the 2026 report (reconstructed 6.03); US$ 6.6 billion for 2025 in the 2026 report (reconstructed 6.57). The last column is a sensitivity analysis counting a component as current if any one of its inputs was newly reported.*

The largest single contribution, India's US$ 182 million in 2025 (16.9% of the care estimate), illustrates the mechanism. India last reported its utilisation inputs for 2022; its 2020, 2021 and 2022 entries were identical; and WHO's pipeline carried the 2022 values into 2023, 2024 and 2025. Every year of India's care estimate from 2020 to 2025 is therefore computed from one set of ratios, entered in the first year of the COVID-19 pandemic.

### 3.5 The six inputs are the most estimate-like variables WHO labels

Of the 443 variables screened, 42 were categorical and 43 untestable; of the 358 continuous variables, 206 screened as measurement-like, 68 as mixed and 84 as estimate-like (Table 5). WHO's dictionary labels exactly six variables as "Estimated" or "Typical" [9], and they are the six inputs to the care estimate. None screened as measurement-like: four were estimate-like and two mixed. WHO's own documentation thus marks these inputs as estimates, while its pipeline uses them as annual values.

**Table 5. Screen of 443 numeric variables in six WHO TB datasets, by dataset.**

| Dataset | Continuous | Categorical | Untestable | Median repetition | Measurement | Mixed | Estimate | Median if untestable scored 0% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Budget | 37 | 0 | 0 | 13.0% | 35 | 1 | 1 | 13.0% |
| Expenditure and utilisation | 39 | 1 | 0 | 15.4% | 28 | 7 | 4 | 15.4% |
| Notifications | 166 | 16 | 3 | 15.6% | 104 | 39 | 23 | 14.9% |
| Treatment outcomes | 66 | 1 | 24 | 33.0% | 21 | 20 | 25 | 20.5% |
| Laboratory diagnostic services | 41 | 12 | 16 | **63.0%** | 9 | 1 | **31** | **53.5%** |
| Contact tracing / TPT | 9 | 12 | 0 | **3.5%** | 9 | 0 | 0 | 3.5% |

*Median repetition is the median, across a dataset's continuous variables, of the share of consecutive country-year pairs holding an identical value. Most estimate-like variables outside the expenditure file are dominated by repeated zeros (Supplementary Note 4). TPT, TB preventive treatment.*

---

## 4. Discussion

### 4.1 Principal findings

WHO's TB country data are a record of first submissions. Nothing published is revised, most utilisation values are restated from the previous year, and gaps are filled from neighbouring years. Each practice is reasonable on its own. Together they mean that WHO's estimate of TB care spending, a sixth of its headline funding figure, is computed largely from ratios that were not measured for the year they are used for, and the published data carry no mark of which values those are.

This is a statement about information, not error. A restated share hospitalised may be correct; models of care change slowly. But a figure entered unchanged for six years cannot record a change if one occurred, and change was expected over this period: decentralised, largely ambulatory care for MDR/RR-TB achieves outcomes at least as good as hospital-based care [11]. Year-on-year movement in WHO's care estimate is then driven almost entirely by notifications and unit costs, with utilisation held fixed, which a reader of the published trend cannot see.

### 4.2 Comparison with other work

Real-time data research treats the vintage of a value as part of its meaning and shows that revisions to official statistics are large and not well behaved [3,4]. WHO's TB data show the opposite failure: the history is never revised, so a value carried forward is never replaced by a measurement. Audits of routine health data have concentrated on completeness, timeliness and internal consistency [5,6,12]; the expenditure data examined here are internally consistent, and the problem lies elsewhere, in when each value was last measured. Modelled estimates of TB spending by source and function [13] inherit these inputs.

### 4.3 Implications

**For WHO.** The pipeline already knows which values it filled; publishing that flag with the processed data would cost nothing. Asking countries to state, for each utilisation input, the year it was last measured would turn restatement from an invisible default into a recorded fact. Provenance metadata of this kind is a recognised element of data stewardship [14], and documentation shipped with datasets has precedent [15].

**For analysts.** The six utilisation inputs should be treated as slowly updated structural parameters, not annual observations. Trends in the care estimate, and in the domestic share of TB funding that includes it [1], warrant a sensitivity analysis holding utilisation at its last newly reported value or varying it across plausible ranges.

**For national programmes.** A programme that last measured its hospitalisation share years ago is represented in global estimates by that old figure. Periodic re-measurement through facility-based costing studies, and an explicit statement of the reference year in the annual return, would let the global figure reflect current practice.

---

## 5. Limitations

Restatement is not evidence of error: a stable practice yields identical values honestly, and the analysis cannot distinguish a re-confirmed value from one carried forward unexamined, which is precisely the information a vintage flag would supply. Only three dated releases of the finance data are archived, from 2024 onwards, so revision of older releases cannot be assessed. The source year of a WHO-supplied value is inferred by matching values in WHO's fill order; a value matching no reported year may result from a chained fill or a manual override in WHO's code. The classification of a cost component by "any input" is a convention, and the sensitivity analysis shows the conclusion does not depend on it. WHO's unit costs are themselves estimates and were not assessed. The screen in §2.3 has its own conventions and failure modes, stated in Supplementary Notes 3-5.

## 6. Conclusions

WHO never revises the TB country data it publishes, countries restate most of their hospital and clinic utilisation figures from one year to the next, and WHO fills the remaining gaps from other years. As a result, only about a third of WHO's US$ 1.08 billion estimate of TB care spending for 2025 rests on inputs reported for 2025. Recording, for each value, whether it was re-measured, restated or imputed would let every user of these data see what each year's figure actually describes.

## References

1. World Health Organization. Global tuberculosis report 2025. Geneva: World Health Organization; 2025. Section 4.1, Financing for TB prevention, diagnostic and treatment services. Available from: https://www.who.int/teams/global-programme-on-tuberculosis-and-lung-health/tb-reports/global-tuberculosis-report-2025/tb-financing/4-1-financing-for-tb-prevention--diagnostic-and-treatment-services [cited 2026 Nov 14].
2. World Health Organization. Global tuberculosis report 2026. Geneva: World Health Organization; 2026. Available from: https://iris.who.int/server/api/core/bitstreams/726b4727-ac22-432d-96e7-563210b8fb32/content [cited 2026 Nov 14].
3. Croushore D, Stark T. A real-time data set for macroeconomists: does the data vintage matter? Rev Econ Stat. 2003;85(3):605-17. doi:10.1162/003465303322369759
4. Aruoba SB. Data revisions are not well behaved. J Money Credit Bank. 2008;40(2-3):319-40. doi:10.1111/j.1538-4616.2008.00115.x
5. Maiga A, Jiwani SS, Mutua MK, Porth TA, Taylor CM, Asiki G, et al. Generating statistics from health facility data: the state of routine health information systems in Eastern and Southern Africa. BMJ Glob Health. 2019;4(5):e001849. doi:10.1136/bmjgh-2019-001849
6. Lundin R, Mariani I, Peven K, Day LT, Lazzerini M. Quality of routine health facility data used for newborn indicators in low- and middle-income countries: a systematic review. J Glob Health. 2022;12:04019. doi:10.7189/jogh.12.04019
7. World Health Organization. Global Tuberculosis Programme country data: expenditure and utilisation, budget, notifications, treatment outcomes, laboratory diagnostic services, and contact tracing and preventive treatment datasets. Geneva: World Health Organization; 2026. Available from: https://extranet.who.int/tme/ [cited 2026 Nov 13] [data files dated 25 August and 12 November 2026].
8. World Health Organization Global Tuberculosis Programme. Global tuberculosis report repositories gtbreport2024, gtbreport2025 and gtbreport2026 (commits afbe537, 666088c and 11ebd9b). GitHub; 2024-2026. Available from: https://github.com/GTB-TME [cited 2026 Nov 14].
9. World Health Organization. Global Tuberculosis Programme data dictionary [file TB_dictionary_2026-08-25.csv]. Geneva: World Health Organization; 2026. Available from: https://extranet.who.int/tme/ [cited 2026 Nov 13].
10. Peng RD. Reproducible research in computational science. Science. 2011;334(6060):1226-7. doi:10.1126/science.1213847
11. Ho J, Byrne AL, Linh NN, Jaramillo E, Fox GJ. Decentralized care for multidrug-resistant tuberculosis: a systematic review and meta-analysis. Bull World Health Organ. 2017;95(8):584-93. doi:10.2471/BLT.17.193375
12. World Health Organization. Data quality assurance: module 1: framework and metrics. Geneva: World Health Organization; 2023. ISBN 978-92-4-004735-8. Available from: https://www.who.int/publications/i/item/9789240047365 [cited 2026 Nov 13].
13. Su Y, Garcia Baena I, Harle AC, Crosby SW, Micah AE, Siroka A, et al. Tracking total spending on tuberculosis by source and function in 135 low-income and middle-income countries, 2000-17: a financial modelling study. Lancet Infect Dis. 2020;20(8):929-42. doi:10.1016/S1473-3099(20)30124-9
14. Wilkinson MD, Dumontier M, Aalbersberg IJ, Appleton G, Axton M, Baak A, et al. The FAIR Guiding Principles for scientific data management and stewardship. Sci Data. 2016;3:160018. doi:10.1038/sdata.2016.18
15. Gebru T, Morgenstern J, Vecchione B, Vaughan JW, Wallach H, Daume H 3rd, et al. Datasheets for datasets. Commun ACM. 2021;64(12):86-92. doi:10.1145/3458723
16. Benchimol EI, Smeeth L, Guttmann A, Harron K, Moher D, Petersen I, et al. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) Statement. PLOS Med. 2015;12(10):e1001885. doi:10.1371/journal.pmed.1001885

## Figure captions

**Figure 1. From a country's annual return to WHO's published TB funding figure.** The utilisation inputs reported by a country, their restatement, the absence of revision between WHO releases, WHO's filling of gaps from neighbouring years, the cost model that converts them into an estimate of inpatient and outpatient care spending, and the provenance of that estimate for 2025 in WHO's 2026 report. Each number is computed by the analysis code from WHO's archived files.

*Alt text: A vertical flow diagram. A country's annual return feeds WHO's published data, then WHO's gap-filling pipeline, then a cost model, then the published 2025 TB funding total of US$ 6.57 billion, of which the care estimate is US$ 1.08 billion. Three boxes at the bottom split the care estimate: 32.6% from new inputs, 42.4% from restated inputs and 25.0% from inputs supplied by WHO.*

**Figure 2. WHO's estimate of TB care spending, 2018-2025, by provenance of its inputs.** Stacked bars show the care estimate in each year of WHO's 2026 report, divided by whether the inputs to each cost component were newly reported that year (solid), restated from the previous year (diagonal hatching) or supplied by WHO's pipeline (cross-hatching). The label above each bar is the newly reported share.

*Alt text: A stacked bar chart for 2018 to 2025. Each bar is between about 0.7 and 1.5 billion US dollars. The solid newly reported portion is a minority in most years, between 13% and 54%; the hatched restated portion is the largest in most years; the cross-hatched WHO-supplied portion grows from 2023 onwards.*

## Declarations

**Reporting.** This study is reported in accordance with the RECORD statement for studies using routinely collected health data [16]; the completed checklist accompanies this submission.

**Contributors.** Sole author: conception, analysis, code, verification, manuscript.

**Funding.** None. **Competing interests.** None declared. **Ethical clearance.** Not required (§2.4).

**Data availability.** The public WHO datasets are archived with the code at https://github.com/hssling/provenance-weighted-priority-setting and archived at Zenodo, doi:10.5281/zenodo.24214490 (release v1.1.0; the concept DOI doi:10.5281/zenodo.24187366 always resolves to the latest version). WHO's report-repository files carry no licence and are not redistributed; tools/fetch_vintages.py downloads them from pinned commits and verifies each against the SHA-256 digest recorded in data/vintages/vintage_manifest.csv.

**Use of generative AI.** The author used a large language model as a drafting and analysis assistant. All analytical decisions, verification and conclusions are the author's, who takes full responsibility.

---

## Notes for the author — not for submission

0. SUBMITTED to the International Journal of Epidemiology as IJE-2026-11-2170 (14 Nov 2026), citing deposit v1.1.0 (doi:10.5281/zenodo.24214490). Signed competing-interests and authorship forms are kept locally only.
1. Rebuilt 14 November 2026 around a vintage analysis of WHO's archived releases (demos/d3_vintages.py). Tables 1-4 are rendered by manuscript/make_tables_b.py and checked verbatim; Table 5 is checked against demos/d2_who_data_screen.py.
2. [done 14 Nov 2026] Release v1.1.0 published; Zenodo version DOI 10.5281/zenodo.24214490 (contains demos/d3_vintages.py and the fetch tools) now cited here, on the title page and in the cover letter. Paper A keeps v1.0.0 (10.5281/zenodo.24187367), which contains everything it reports.
3. Ho 2017 was read against the sentence it supports (decentralised care outcomes). Aruoba 2008 verified on Crossref; supports "revisions are large and not well behaved".
