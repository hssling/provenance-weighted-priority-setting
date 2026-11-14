# What a tuberculosis budget cannot see: fiscal invisibility and the limits of the WHO funding-gap indicator in India, 2017–2025

**Author:** Siddalingaiah H S
Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur – 572106, Karnataka, India.
Correspondence: hssling@yahoo.com · Tel: +91-8941087719 · ORCID 0000-0002-4771-8285

**Running title:** What a TB budget cannot see

**Target journal:** *Indian Journal of Tuberculosis* (Original Article). Verified against the journal's Guide for Authors and the author's IJTB-S-26-01305 upload set, 13 November 2026: main text 3,000 words excluding abstract and references; abstract 250 words, structured; 1 to 7 keywords; 40 references or fewer; single-anonymized review, so the unblinded manuscript is the primary upload.

---

## Abstract

**Background/Objectives:** The World Health Organization (WHO) publishes, for every high-burden country, the tuberculosis (TB) budget required and the funding expected against it; their difference, the funding gap, is read as a measure of under-resourcing. We asked whether this gap is informative for India, and whether India's TB budget can show what individual interventions cost.

**Methods:** WHO TB budget and expenditure data for 215 countries (2017–2025) were compared with India's national programme accounts using dimensionless ratios, avoiding currency conversion. Eleven TB interventions were mapped onto WHO budget lines by definition, using WHO's data collection form and, for comparison, its data dictionary.

**Results:** India reported expected funding exactly equal to budget required in all eight years 2018–2025, so its published gap is zero by construction. Fourteen of 106 countries with five or more years report this way; 44 report a gap every year. India's own accounts record ₹18,388 crore approved against ₹23,169 crore requested, an annual shortfall of 5.4–46.1%. No intervention has a budget line of its own: two have none, three, including active case finding, are pooled in one line with fifteen activities, and three are visible only as drug costs. Against the dictionary instead of the form, five have no line, not two.

**Conclusions:** The global indicator cannot show India's shortfall, and India's accounts cannot show what active case finding costs, so cost per case found cannot be computed. Two reporting changes needing no new money would make the shortfall visible and programme activities evaluable for value for money.

**Keywords:** Data Accuracy; Financing, Government; Health Expenditures; Health Priorities; Program Evaluation; Resource Allocation

## Highlights

- India's WHO-reported TB funding gap is zero in every year 2018–2025, by construction
- India's own accounts show approvals 5.4–46.1% short of requests in each year
- No TB intervention, active case finding included, has a budget line of its own
- Without cost attribution, NTEP cannot compute its cost per additional case found
- Two reporting changes needing no new money would make TB activities evaluable

---

## 1. Introduction

India notifies more tuberculosis than any other country, and the National TB Elimination Programme (NTEP) now finances almost all of its response from domestic sources [1,2]. Its National Strategic Plan sets targets activity by activity — active case finding, private-sector engagement, preventive treatment, nutritional support [3] — and the programme reports outcomes against them in detail [2]. Whether money is moving to the activities that buy the most of those outcomes is a separate question, and it can be asked only of a financial record that says what each activity cost.

Two financial records exist. Nationally, the India TB Report publishes the budget requested, approved, released and spent [2]. Internationally, the Global Tuberculosis Report publishes, for every high-burden country, the budget required for the coming year and the funding expected against it [1]. Their difference, the funding gap, is used in TB investment cases and advocacy [4] and in the Report's country comparisons [1]. It does not enter the Global Fund's allocation formula, whose inputs are disease burden and economic capacity [5], but it is the figure quoted when a programme's resourcing is discussed.

The monitoring system that produces these figures has been described by its custodians, who noted its restriction to public-sector provider costs and the limited scope to validate what countries report [6]. To our knowledge, no study has asked whether the two quantities behind the gap are independently determined for a given country, or which TB interventions the budget classification can show at all.

This paper asks three questions of direct relevance to NTEP and the Central TB Division (CTD). Does the WHO funding gap register India's documented shortfall? Which TB interventions have a budget line of their own? And what would it take for the programme to compute what its activities cost per unit of outcome?

## 2. Methods

### 2.1 Data sources

Three public sources were used. The WHO TB budget dataset (release of 12 November 2026; 1,720 rows, 215 countries, 2018–2025) gives budget required and funding expected, each disaggregated into eleven line items and by source [7]. The WHO TB expenditure and utilisation dataset (release of 25 August 2026; 2017–2026) gives actual expenditure on the same line items [7]. The India TB Report 2024, in its table 16.1, gives the budget requested, approved, released and spent for fiscal years 2017–18 to 2023–24, in ₹ crore [2]. What each WHO variable covers was established from the WHO data dictionary [8] and the WHO TB data collection form [9].

### 2.2 Comparing sources without currency conversion

WHO reports in US dollars by calendar year; the national accounts report in ₹ crore by fiscal year. To avoid importing an exchange-rate assumption, each source's internal, dimensionless ratio was compared. WHO's reported gap is (budget required − funding expected) / budget required; the national shortfall is (requested − approved) / requested. Both measure the fraction of the needed budget that was not secured. Execution was measured as expenditure over budget required (WHO) and as spent over approved and over requested (national).

### 2.3 Mapping interventions to budget lines

Eleven interventions were examined, the set defined in a companion analysis of India's drug-resistant TB surveillance [10]: molecular diagnostics, whole-genome sequencing, active case finding, airborne infection control, private-sector engagement, TB preventive therapy, the shorter all-oral regimen, nutritional support, integrated TB-HIV-diabetes care, bovine TB control and milk pasteurisation. Each was mapped onto the WHO budget line that covers it by definition, not by name.

Two WHO documents define these lines, and they differ. The dictionary distributed with the data defines budget_prog as "programme costs to treat drug-susceptible TB" [8]. The collection form that countries complete defines the same line as fifteen activities, among them "public-private mix activities, community engagement, active case-finding, infection control" [9]. Mapping followed the form, because it determines what a country enters. Both definitions of every line used are set side by side in Supplementary S1, and the effect of the choice is reported as a result (§3.5).

Each mapping was classified as no line (no WHO line covers the activity), pooled (the form names the activity inside a line shared with many others), commodity only (the line covers the drug or one arm, not its delivery) or dominant (the line is largely this activity, though shared).

### 2.4 Analysis, reproducibility and reporting

The analysis is descriptive. Among countries with at least five years of data, each was classified by whether it reported expected funding equal to budget required in every year, in no year, or in some years. All computation is in Python with no third-party numerical dependency, and one command regenerates every number from the archived raw files, whose SHA-256 digests are recorded [11]. Reporting follows the RECORD statement for studies using routinely collected data [12], and the checklist is supplied.

## 3. Results

### 3.1 India's reported funding gap is zero by construction

In all eight years 2018–2025, India reported total expected funding exactly equal to total budget required, so its published gap is zero in every year (Table 1). Neither field's definition states that the two should be equal [8]; the equality is a reporting convention visible only in the data.

It is not universal practice. Of 106 countries with at least five years of data, 14 reported the two as equal in every year and 44 reported a non-zero gap in every year (Supplementary S2), including Vietnam (mean gap about 72%), Nigeria (about 69%), Indonesia (about 59%) and China (about 10%). Pakistan reported gaps of 43–66% for 2018–2023 and exactly zero in 2024 and 2025. No field distinguishes a country reporting need from one reporting availability.

### 3.2 India's own accounts record a substantial shortfall

Over 2017–18 to 2023–24 the programme requested ₹23,169.14 crore and was approved ₹18,388.23 crore, 79.4% of the request. The annual shortfall ranged from 5.4% to 46.1% (Table 1, Figure 1; Supplementary S3). The two sources disagree in every overlapping year at any tolerance below 5 percentage points, and in three of six years at a tolerance of 15 points.

**Table 1. Two sources, one programme: India's TB financing as reported to WHO and in the national accounts, 2017–2025.**

| Year | WHO reported gap | National shortfall (requested → approved) | Expenditure / budget required (WHO) | Global Fund share of expenditure |
|---|---:|---:|---:|---:|
| 2017 | — | 16.4% | — | — |
| 2018 | **0.0%** | 23.7% | 83.4% | 17.7% |
| 2019 | **0.0%** | 5.4% | 74.2% | 14.7% |
| 2020 | **0.0%** | 12.5% | 79.5% | 14.7% |
| 2021 | **0.0%** | 6.0% | 54.5% | 40.2% |
| 2022 | **0.0%** | 46.1% | 51.8% | 31.2% |
| 2023 | **0.0%** | 38.2% | 45.1% | 8.4% |
| 2024 | **0.0%** | — | 97.8% | 3.9% |
| 2025 | **0.0%** | — | 92.4% | 0.8% |

*National years are the first year of India's April–March fiscal year (2018 denotes 2018–19). — denotes a year not covered by that source.*

### 3.3 Execution is incomplete, and financing has domesticated

The sources agree on execution. WHO data give expenditure as 72% of budget required across the period (range 45–98%); the national accounts give ₹15,063.46 crore spent against ₹18,388.23 crore approved (82%) and against ₹23,169.14 crore requested (65%). Under-execution of health budgets is common [13]; neither source records why funds went unspent.

Global Fund support fell from 37% of actual TB expenditure in 2017 to 1% in 2025, and domestic financing rose from 62% to 96%. Earlier analyses of TB financing end in 2011 [14] and 2017 [15].

The national report's table 16.1 does not reconcile across its rows. Over 2017–2021, the only years for which releases are printed, releases sum to ₹3,825.31 crore while expenditure sums to ₹13,312.14 crore, and 2017 expenditure is 150% of the approved amount. Expenditure can exceed release where states spend carried-over or own funds, but the table does not say so. The ratios above do not use the released column.

### 3.4 No intervention has a budget line of its own

Two interventions, bovine TB control and milk pasteurisation, have no WHO line; both are animal-health and food-safety activities outside the TB programme's budget by design (Table 2, Figure 2). The other nine share a line with activities that are not theirs.

Three are pooled. Active case finding, airborne infection control and private-sector engagement are named by the form inside budget_prog, which also carries management, supervision, training, policy development, meetings, office equipment, buildings, routine surveillance, advocacy, community engagement, drug-procurement management and contact investigation: fifteen activities in one figure. Three are commodity only. budget_tpt covers preventive-treatment drugs but not the contact tracing and adherence support that deliver them; the shorter regimen's drugs sit in budget_sld, its programme costs elsewhere; TB-HIV-diabetes care is visible only through its TB/HIV arm. Three are dominant: budget_lab carries molecular diagnostics and sequencing alongside every other laboratory cost, and budget_patsup carries nutritional support alongside all patient support.

The dividing line is procurement, not priority. The lines that name a single thing name something the programme buys: drugs, laboratory supplies, patient support. The activities that are pooled are things the programme does.

**Table 2. Eleven TB interventions against WHO's budget classification, listed in the order of the budget lines they reach. Coverage is judged against WHO's data collection form [9]; Supplementary S1 gives both WHO definitions of each line.**

| Intervention | WHO budget line | Coverage |
|---|---|---|
| Molecular diagnostic scale-up (Xpert MTB/RIF, MTB/XDR) | budget_lab | Dominant — shared with all laboratory costs |
| Whole-genome sequencing for drug-susceptibility prediction | budget_lab | Dominant — shared with all laboratory costs |
| Airborne infection prevention and control | budget_prog | **Pooled** — one of fifteen activities |
| Active case finding | budget_prog | **Pooled** — one of fifteen activities |
| Private-sector engagement | budget_prog | **Pooled** — one of fifteen activities |
| TB preventive therapy | budget_tpt | Commodity only — drugs |
| Shorter all-oral regimen rollout (BPaL/BPaL-M) | budget_sld | Commodity only — drugs |
| Nutritional support | budget_patsup | Dominant — shared with all patient support |
| Integrated TB-HIV-diabetes care | budget_tbhiv | Commodity only — TB/HIV arm |
| Bovine tuberculosis control | — | **No line** |
| Milk pasteurisation / dairy food chain | — | **No line** |

### 3.5 The document consulted changes the count

Classified against the dictionary instead of the form, five interventions have no budget line rather than two: active case finding, airborne infection control and private-sector engagement fall outside a line defined as programme costs "to treat" drug-susceptible TB [8]. Every other mapping is the same under either document. Only the dictionary is distributed with the datasets; the form must be sought in the Global TB Programme's report repository [9]. An analyst who read the dictionary carefully would conclude that India's TB budget contains no provision for active case finding, and nothing in the data would reveal the error.

## 4. Discussion

### 4.1 Two failures of visibility

India's published funding gap cannot register a shortfall, because expected funding is entered equal to requirement; the national accounts, over the same years, record that a fifth of the requested budget was never approved. And the budget classification records what the programme buys rather than what it does, so no intervention has a figure of its own. Both are properties of reporting conventions fixed upstream of any policy decision. Neither concerns how much money TB control receives or how well it is spent.

The same division between what is bought and what is done was found in India's National AIDS and STD Control Programme, where sexually transmitted infection services, pre-exposure prophylaxis and surveillance had no traceable line while blood transfusion services were separately disaggregated [16]. Two programmes sharing the pattern make it a candidate structural property of disease-control financing rather than an artefact of one programme's accounts.

### 4.2 Why this is a question of efficiency

Allocative efficiency requires the cost of an additional unit of outcome from each competing activity, so that money can move from activities with a poor return at the margin to those with a better one. NTEP has the outcome side in detail: notifications, contact-investigation yield, treatment success and the drug-resistance cascade are reported annually [2]. It lacks the cost side at the same resolution. Cost per case notified through active case finding cannot be computed from the accounts, because its cost is one of fifteen activities in budget_prog. Cost per contact screened cannot be computed either, because contact investigation sits in the same pooled line while preventive-treatment drugs sit in budget_tpt.

India's unit costs for TB services therefore come from bespoke facility surveys. The most detailed to date sampled 20 facilities in two states to cost 50 services, with the explicit aim of supporting efficient allocation by NTEP, and it reported passive but not active case finding [17]. Such studies are valuable, but they are periodic, sampled and external to the accounts; they cannot follow an activity's marginal cost as it scales. Programme budgeting and marginal analysis, the standard method for reallocating under a fixed envelope, needs exactly the attribution that is missing [18], and the omission of programme and delivery costs is a long-recognised weakness in intervention costing [19]. Programme-based budgeting, which organises budgets around what a programme does, has remained shallow in practice across comparable settings [20].

A plausible consequence, not shown here, is that activities without a line of their own are harder to defend at budget time than commodities with one, whatever their value.

### 4.3 What NTEP and the Central TB Division can do

Four changes follow, in increasing order of effort, and none requires new money (Table 3).

**One field, in the next WHO reporting round.** India enters total expected funding equal to total budget required. Entering anticipated funding from identified sources — domestic approvals, Global Fund and other grants — would make India's unmet need visible in the global dataset, which today shows the country with the largest TB burden with no funding gap in any year. WHO could add one field recording whether expected funding reflects assessed need or anticipated availability, which would separate the 14 countries from the 44.

**Sub-codes beneath budget_prog, in the next National Strategic Plan.** Nothing in the WHO form prevents a national programme from carrying its own sub-codes beneath a pooled line. Tagging spending on active case finding, airborne infection control and private-sector engagement, even approximately or as shares, would make cost per additional case found reportable and those activities defensible at budget time. Restricting this second dimension to the six to eight activities contested at budget time keeps it proportionate; programme-wide activity-based costing is not needed.

**A footnote where the national table does not reconcile.** One sentence naming the mechanism — re-appropriation, lapse, carry-forward or state funds — wherever released and spent differ would make the report's table 16.1 interpretable.

**A pre-submission check.** Before the annual WHO return is filed, three questions can be asked of it: does expected funding equal requirement, and is that intended; do the components sum to each total; and is any value identical to last year's, and was it re-estimated or carried forward? The code accompanying this paper performs all three on a country-year table.

**Table 3. From finding to action. The last column states what would count as evidence of change.**

| Finding | Mechanism | Who can change it | Change | Evidence it worked |
|---|---|---|---|---|
| India's published funding gap is zero in all eight years; 14 of 106 countries report the same way | Expected funding is entered equal to budget required, so the gap is zero by construction | CTD (entry); WHO Global TB Programme (form) | Enter anticipated funding by source; add one field stating whether expected funding reflects need or availability | India's unmet need appears in the global dataset; the 14 countries become distinguishable from the 44 |
| No intervention has a line of its own; three service activities are among fifteen pooled in budget_prog | The chart of accounts is organised by what is purchased, so the cost of what is done is pooled | CTD and state programmes (chart of accounts) | Sub-code budget_prog for six to eight contested activities | Cost per additional case found through active case finding becomes reportable |
| Released and spent amounts do not reconcile in the national table | The reconciling mechanism is not stated | CTD | A footnote naming the mechanism wherever released and spent differ | The table becomes interpretable without altering any figure |

### 4.4 Comparison with other work

WHO's financial monitoring system and its limits have been described [6], and donor and domestic TB financing analysed to 2011 [14]; modelled estimates now track TB spending by source and function to 2017 [15] and project health-system resource needs [21]. These are external reconstructions. This study differs in asking whether the reported quantities can carry the meaning attached to them, and in judging coverage against the instrument countries complete. Domestic adequacy is more usually assessed through public expenditure and fiscal space [22]; with external financing at 1% of expenditure, neither the funding gap nor the external share now carries information about it for India.

## 5. Limitations

This is a secondary analysis of reported data: it observes reporting behaviour, not financial reality. A country reporting expected funding equal to requirement may or may not face a shortfall; the indicator simply cannot show one. The mapping reflects analytic judgement anchored to published definitions, and the mapping file is published so that any entry can be recomputed. The intervention set comes from a companion analysis [10]; it orders nothing here, and each intervention's classification rests on its own definition. The national and WHO series overlap for six years only, and WHO figures are revised as countries submit corrections, so release dates are stated and the files archived. Only India's accounts were examined in detail; whether other high-burden countries pool the same activities is untested.

## 6. Conclusions

A budget records what a programme buys, not what it does. In India's TB response no intervention of eleven has a budget line of its own, so the published record cannot say what active case finding, infection control or private-sector engagement cost, and NTEP cannot compute cost per additional case found from its own accounts. Meanwhile the international indicator intended to signal shortfall reports zero for India in every year, while the national accounts record that a fifth of the requested budget was never approved and a third of it was never spent. Neither finding concerns how much money TB control receives. Both are correctable without new money, by one different entry in an existing field and one added dimension in an existing chart of accounts, and together they would let a programme that already measures its outcomes in detail begin to measure what those outcomes cost.

## Contributors

The author is the sole contributor: conceived the study, assembled and verified the data, wrote the analysis code, performed all analyses, produced the figures and supplementary material, and wrote the manuscript. The author meets the ICMJE authorship criteria and takes responsibility for the integrity of the work as a whole.

## Ethical clearance

Not required. This study analysed only aggregated, publicly available financial and programmatic summaries, with no individual-level records and no patient-identifiable information. Institutional ethics approval and informed consent were therefore not applicable.

## Clinical trial registration number

Not applicable. This is a secondary analysis of published aggregate financial data, not a clinical trial, and it was not registered.

## Declaration of Artificial Intelligence in scientific writing

A large language model (Anthropic Claude) was used, under the author's direction and review, to write and test the analysis code, to render the figures and supplementary tables from the computed outputs, and to draft passages of text. The author made every interpretive decision, including the comparison design, the mapping of interventions to budget lines and its grounding in WHO's collection form, and the conclusions; checked each reference against Crossref or PubMed; and edited the final text, for which the author is fully responsible. The model is not an author, since it cannot answer for the work.

## Funding

None.

## Conflict of interest declaration

The author declares no competing financial, academic or personal interests that could have influenced the conduct or reporting of this work.

## Acknowledgements

The author acknowledges the open country data of the World Health Organization Global TB Programme, and the Central TB Division, Ministry of Health and Family Welfare, Government of India, for publishing programme accounts in the India TB Report.

## Data availability

All inputs are publicly available: the WHO TB budget and expenditure datasets and the India TB Report 2024. Analysis code, the archived input files, the intervention-to-budget-line mapping with its definitional basis, and the verification suite are deposited at https://github.com/hssling/provenance-weighted-priority-setting and archived at Zenodo, doi:10.5281/zenodo.24187367 (release v1.0.0; the concept DOI doi:10.5281/zenodo.24187366 always resolves to the latest version). Every input file is listed in data/raw_file_manifest.csv with its SHA-256 digest, so the archived copies can be checked byte for byte against those analysed.

## References

1. World Health Organization. Global tuberculosis report 2025. Geneva: World Health Organization; 2025. Available from: https://www.who.int/teams/global-programme-on-tuberculosis-and-lung-health/tb-reports/global-tuberculosis-report-2025 [accessed 13 November 2026].
2. Central TB Division, Ministry of Health and Family Welfare, Government of India. India TB Report 2024: National TB Elimination Programme annual report. New Delhi: Ministry of Health and Family Welfare; 2024. Available from: https://tbcindia.mohfw.gov.in/wp-content/uploads/2024/10/TB-Report_for-Web_08_10-2024-1.pdf [accessed 13 November 2026].
3. Central TB Division, Ministry of Health and Family Welfare, Government of India. National Strategic Plan for Tuberculosis Elimination 2017–2025. New Delhi: Ministry of Health and Family Welfare; 2017.
4. Reid MJA, Arinaminpathy N, Bloom A, Bloom BR, Boehme C, Chaisson R, et al. Building a tuberculosis-free world: the Lancet Commission on tuberculosis. Lancet 2019;393(10178):1331–84. doi:10.1016/S0140-6736(19)30024-8
5. Global Fund to Fight AIDS, Tuberculosis and Malaria. Allocation methodology for Grant Cycle 8 (2026–2028 allocation period). Board paper GF/B52/08B, 52nd Board Meeting, 20–22 November 2024. Geneva: The Global Fund; 2024. Available from: https://archive.theglobalfund.org/media/15310/archive_bm52-08b-allocation-methodology-gc8_report_en.pdf [accessed 13 November 2026].
6. Floyd K, Pantoja A, Dye C. Financing tuberculosis control: the role of a global financial monitoring system. Bull World Health Organ 2007;85(5):334–40. doi:10.2471/BLT.06.034942
7. [dataset] World Health Organization. Global Tuberculosis Programme country data: TB budget (release of 12 November 2026) and TB expenditure and utilisation (release of 25 August 2026) datasets. Geneva: World Health Organization; 2026. Available from: https://extranet.who.int/tme/ [accessed 13 November 2026]. This data-collection system no longer accepts updates; the input files are archived with the analysis code.
8. World Health Organization. Global Tuberculosis Programme data dictionary (file TB_dictionary_2026-08-25.csv). Geneva: World Health Organization; 2026. Available from: https://extranet.who.int/tme/ [accessed 13 November 2026].
9. World Health Organization. WHO TB data collection form 2026, version 2026-03-25. Geneva: World Health Organization; 2026. Available from: https://github.com/GTB-TME/gtbreport2026 (file doc/who_tb_dcf2026.pdf) [accessed 13 November 2026].
10. Siddalingaiah HS. Drug-resistant tuberculosis in India, 2017–2024: improving outcomes, no worsening axis, and a caution for NTEP trend analysis. Manuscript under review at the Indian Journal of Tuberculosis (IJTB-D-26-00777), submitted 12 November 2026.
11. Peng RD. Reproducible research in computational science. Science 2011;334(6060):1226–7. doi:10.1126/science.1213847
12. Benchimol EI, Smeeth L, Guttmann A, Harron K, Moher D, Petersen I, et al. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) statement. PLoS Med 2015;12(10):e1001885. doi:10.1371/journal.pmed.1001885
13. Piatti-Funfkirchen M, Barroy H, Pivodic F, Margini F. Budget execution in health. Washington, DC: World Bank; 2021. doi:10.1596/36583
14. Floyd K, Fitzpatrick C, Pantoja A, Raviglione M. Domestic and donor financing for tuberculosis care and control in low-income and middle-income countries: an analysis of trends, 2002–11, and requirements to meet 2015 targets. Lancet Glob Health 2013;1(2):e105–15. doi:10.1016/S2214-109X(13)70032-9
15. Su Y, Garcia Baena I, Harle AC, Crosby SW, Micah AE, Siroka A, et al. Tracking total spending on tuberculosis by source and function in 135 low-income and middle-income countries, 2000–17: a financial modelling study. Lancet Infect Dis 2020;20(8):929–42. doi:10.1016/S1473-3099(20)30124-9
16. Siddalingaiah HS. India's human immunodeficiency virus and sexually transmitted infection response at the close of NACP-V: an evidence-practice gap analysis and a priority agenda for clinical sexually transmitted infection services. J Skin Sex Transm Dis 2026; in production, volume and pages not yet assigned. doi:10.25259/JSSTD_120_2026
17. Chatterjee S, Toshniwal MN, Bhide P, Sachdeva KS, Rao R, Laurence YV, et al. Costs of TB services in India. Int J Tuberc Lung Dis 2021;25(12):1013–8. doi:10.5588/ijtld.21.0105
18. Madden L, Hussey R, Mooney G, Church E. Public health and economics in tandem: programme budgeting, marginal analysis and priority setting in practice. Health Policy 1995;33(2):161–8. doi:10.1016/0168-8510(95)93676-R
19. Johns B, Baltussen R, Hutubessy R. Programme costs in the economic evaluation of health interventions. Cost Eff Resour Alloc 2003;1(1):1. doi:10.1186/1478-7547-1-1
20. Bertone MP, Barroy H, Sparkes S, Sempé L, Yungrattanachai M, Witter S. Political economy of budgeting reforms: a comparative analysis of the adoption and implementation of programme-based budgeting in health across seven LMIC countries. Int J Health Plann Manage 2026 Sep 29 [online ahead of print]. doi:10.1002/hpm.70142
21. Stenberg K, Hanssen O, Edejer TT, Bertram M, Brindley C, Meshreky A, et al. Financing transformative health systems towards achievement of the health Sustainable Development Goals: a model for projected resource needs in 67 low-income and middle-income countries. Lancet Glob Health 2017;5(9):e875–87. doi:10.1016/S2214-109X(17)30263-2
22. Tandon A, Cashin C. Assessing public expenditure on health from a fiscal space perspective. Health, Nutrition and Population Discussion Paper. Washington, DC: World Bank; 2010. doi:10.1596/13613

## Figure captions

**Figure 1. Two accounts of the same years.** India's funding gap as reported to WHO, against the shortfall recorded in India's own programme accounts, 2018–2023. The WHO-reported gap is zero in every year because expected funding is reported equal to budget required; over the same years the national accounts record approvals falling short of requests by 5.4% to 46.1%. Values are percentages of the amount required (WHO) or requested (national accounts). National years are the first year of India's April–March fiscal year (2018 denotes 2018–19); the WHO series is plotted by reporting year. Sources: WHO TB budget dataset [7] and India TB Report 2024, report table 16.1 [2].

**Figure 2. Where each intervention falls in WHO's budget classification.** Eleven TB interventions, in the order of Table 2, joined to the WHO budget line that covers them as judged against the data collection form [9]. Line style marks the condition of that coverage: pooled, where the form names the activity inside a line shared with many others; commodity only, where the line covers the drug or one arm but not the delivery; dominant, where the line is largely the activity though still shared; and no line. Three interventions converge on budget_prog, one figure pooling fifteen activities. No arrow ends at a line specific to its own intervention.

---

## Notes for the author — not for submission

0. SUBMITTED to the Indian Journal of Tuberculosis as IJTB-D-26-00779 (13 Nov 2026), status With Editor on 14 Nov. Ref 10 now carries TB-BOPAS's manuscript number IJTB-D-26-00777 for any revision.
1. Journal history: *Health Policy and Planning* rejected by the author (fully open access with an APC); *Health Policy* not suitable (high-income scope); *Indian Journal of Tuberculosis* chosen 13 November 2026 (subscription journal; no charge unless open access is elected after acceptance).
2. Ref 10 (TB-BOPAS) was submitted to IJTB on 13 November 2026 and is under review, not in press. Elsevier's guide says "in press" implies acceptance, so it is cited as under review. Update it to "in press" only on an acceptance letter, and to full citation on publication.
3. Ref 16 (JSSTD) carries the DOI printed on the R14 proof; it returns 404 until publication. Add volume and pages when the issue is released.
4. The dictionary comparison (§3.5) is derived in code as `TB_BUDGET_NO_LINE_BY_DICTIONARY` (five), not typed.
