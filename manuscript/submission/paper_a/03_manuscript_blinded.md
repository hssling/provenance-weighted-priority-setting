# What a tuberculosis budget cannot see: fiscal invisibility and the limits of the WHO funding-gap indicator in India, 2017–2025

**Running title:** What a TB budget cannot see

---

## Abstract

**Background.** WHO's tuberculosis (TB) funding gap — budget required minus funding expected — is published annually for high-burden countries and read as a measure of under-resourcing. The system that produces it has been described and its limitations set out by its custodians, but whether the two quantities behind it are independently determined for a given country has not been examined.

**Methods.** We compared WHO's reported TB budget and expenditure data for 215 countries (2017–2025) with India's national programme accounts, using dimensionless internal ratios (no currency conversion), and mapped eleven TB interventions onto WHO budget lines by definition, not name.

**Results.** India reported expected funding exactly equal to budget required in all eight years 2018–2025: its WHO funding gap is zero **by construction**, not by observation. Fourteen of 106 countries with five or more years report this way; 44 report a gap every year. India's own accounts record ₹18,388 crore approved against ₹23,169 crore requested (shortfall 5.4–46.1% by year). The sources agree on execution (72% and 82% of budget spent) and on Global Fund support falling from 37% of expenditure to 1%. **No intervention of eleven has a budget line of its own.** Two have no line; three are named by WHO's collection form inside one line pooling fourteen activities; three cover the drug but not its delivery.

**Conclusions.** A budget records what a programme buys, not what it does. Commodities have line items; services largely do not, so spending on an intervention without a line cannot be identified. For India, the indicator meant to signal shortfall structurally cannot. Neither finding concerns how much TB control receives, and both are correctable: publish unmet need as its own field, and tag expenditure to interventions rather than commodity classes.

**Keywords:** Antitubercular Agents; Costs and Cost Analysis; Financing, Government; Health Expenditures; Health Priorities; Healthcare Financing; India; Program Evaluation; Tuberculosis

## Key messages

- WHO's tuberculosis funding gap is read as a measure of under-resourcing, but India reported expected funding exactly equal to budget required in all eight years from 2018 to 2025, so its published gap is zero by construction rather than by observation.
- Fourteen of the 106 countries with five or more years of data report the same way, while India's own national accounts record an annual shortfall of 5.4% to 46.1% between funds requested and approved, which the indicator cannot show.
- No tuberculosis intervention of the eleven examined has a budget line of its own: active case finding, airborne infection control and private-sector engagement are named by WHO's reporting form but pooled with eleven other activities in a single figure, so what any of them costs cannot be recovered from the published record. Both problems are correctable without new money: publish unmet need as a field in its own right, and tag expenditure to interventions rather than to commodity classes.

---

## 1. Introduction

Tuberculosis control is planned against money. National strategic plans cost their activities, and the Global TB Report (WHO 2025) publishes, for every high-burden country, the budget required for the coming year and the funding expected against it. The difference between those two quantities — the **funding gap** — is read as a measure of under-resourcing. Funding-need figures of this kind are used in TB investment cases and advocacy (Reid et al. 2019), and the gap is shown in the Report's country comparisons (WHO 2025).

We should be precise about what the indicator is and is not used for, because our argument does not depend on overstating it. The Global Fund's published allocation methodology takes disease burden and economic capacity as the inputs to its allocation formula, followed by a qualitative adjustment (Global Fund 2024); it does **not** list the WHO reported funding gap among them. The gap's influence is of a different kind — it is the figure published, quoted and compared when a programme's resourcing is discussed. An indicator need not enter a formula to shape a judgement.

An indicator used that way carries an implicit claim: that the two numbers behind it are independently determined, so their difference is informative. This paper asks whether that claim holds, and finds that for India it does not. The global financial monitoring system that produces these figures has been described by its custodians, who set out its limitations: its restriction to public-sector provider costs, the difficulty of obtaining aggregated data from decentralized systems, and the limited opportunities to validate what countries report (Floyd et al. 2007). To our knowledge, however, no study has asked whether the two quantities behind the reported gap are independently determined for a given country, or examined the cross-country comparability of health-financing indicators of this kind.

The question matters beyond measurement. India notifies more tuberculosis than any other country and now finances almost all of its response domestically. If the indicator that would signal a shortfall cannot register one, neither the national programme nor its partners have an external instrument that would show strain before it appeared in outcomes.

A second question follows from the first. Even where financing *is* recorded, it is recorded in categories, and those categories decide what can be counted. We therefore also ask which tuberculosis interventions have a budget line at all — and find that the answer divides along a line that is not about evidence or priority, but about whether an intervention has something to procure.

---

## 2. Methods

### 2.1 Data sources

Three public sources, retrieved in November 2026:

1. **WHO TB budget dataset** (`TB_budget`, WHO release of 12 November 2026; 1,720 rows, 215 countries, 2018–2025, 43 variables): budget required and funding expected, each disaggregated into eleven line items, plus expected funding by source (domestic, Global Fund, USAID, other) and budgeted cost per patient treated (WHO 2026a).
2. **WHO TB expenditure and utilisation dataset** (`TB_expenditure_utilisation`, WHO release of 25 August 2026; 2017–2026): actual expenditure and funds received, on the same line-item structure (WHO 2026a).
3. **India TB Report (Central TB Division 2024), Table 16.1** (p.174): budget requested, budget estimates/approved, total releases to states, and total expenditure for 2017-18 to 2023-24, in ₹ crore.

WHO's data dictionary (WHO 2026b) (release of 25 August 2026) was used to establish what each variable covers. This is not incidental: an early version of this analysis mapped active case finding to `budget_prog` on the strength of the name, when the dictionary defines it as *"programme costs to **treat** drug-susceptible TB"*. Case finding is not treatment, and the mapping was wrong. Every mapping reported here was checked against its definition.

### 2.2 Comparing sources that are not in the same units

WHO reports in US dollars on a calendar year; the national accounts report in ₹ crore on a fiscal year. Converting between them would import an exchange-rate assumption into the comparison.

We avoid this by comparing each source's **internal, dimensionless ratio**. WHO's reported gap is `(budget_tot − cf_tot) / budget_tot`. The national shortfall is `(requested − approved) / requested`. Both answer the same question — *what fraction of the budget that was needed was not secured?* — and neither carries a currency.

An earlier formulation compared year-on-year proportional change in each source, which cancels levels. It therefore could not detect the disagreement reported here, which is a level disagreement with no trend component. We record this because it is instructive: a comparison designed to avoid one assumption was blind to the finding it was built for.

### 2.3 Mapping interventions to budget lines

Eleven tuberculosis interventions were mapped onto WHO budget line items by definition. Their ranking, and the definitions of the interventions themselves, are taken as given from a separate manuscript under review ([Author] 2026a), in which they are ordered by a priority score built from the favourability of coded literature, not from a formal evidence synthesis. The mapping to budget lines does not depend on that ranking (§5).

**Which definition governs.** Two WHO documents define these columns and they do not agree. The data dictionary distributed with the datasets gives `budget_prog` as *"Budget required for programme costs to treat drug-susceptible TB"*. The data collection form, the instrument countries actually complete, gives the same line as covering *"the management and supervision of the TB control programme, training, policy development, meetings, visits for supervision, purchase of office equipment/vehicles, construction of buildings for use by programme staff, routine surveillance, advocacy and communication, public-private mix activities, community engagement, active case-finding, infection control, management of TB drug procurement and distribution, and programme activities linked to contact investigation for TB preventive treatment"* (WHO 2026c). The dictionary's abbreviation excludes case-finding and infection control; the form includes them. **We map against the form**, because it is what determines what a country enters. An earlier version of this analysis mapped against the dictionary and reported three activities as having no budget line when the form names them; §4.1.1 reports that error, because it is the kind of error this paper is about.

Each mapping was then classified as **no line** (no WHO line covers the activity), **pooled** (the form names the activity inside a line it shares with many others), **commodity-only** (the line covers the drug or one arm, not the delivery), or **dominant** (the line's scope is largely this activity, though still shared). Mapping is declared data and is published with the code.

### 2.4 Reproducibility

All analysis is pure-Python with no third-party numerical dependency. Every figure in this paper is regenerated from the raw files by a single command, following the practice of computational reproducibility (Peng 2011), and a verification suite (255 tests) checks the derived quantities, including that every number quoted here is reproduced from source rather than transcribed. Code and data: [repository URL to be inserted at acceptance].

### 2.5 Ethics

Not required. The analysis uses aggregated, publicly available financial and programmatic summaries with no individual-level records and no patient-identifiable information. Institutional ethics approval and informed consent were not applicable.

---

## 3. Results

### 3.1 India's reported funding gap is zero by construction

In all eight years 2018–2025, India reported expected funding (`cf_tot`) **exactly equal** to budget required (`budget_tot`). The reported gap is therefore identically zero in every year — not as a finding about financing, but as a consequence of how the two fields are populated. WHO's dictionary defines `budget_tot` as "Total budget required (US Dollars)" and `cf_tot` as "Total expected funding for all budget line items (US Dollars)" (WHO 2026b); neither definition states that the two should be equal, so the equality is a reporting convention we infer from the data, not one WHO documents.

This is not universal practice. Among 106 countries with at least five years of data, **14** report budget equal to expected funding in every year. **44** report a non-zero gap in every year, including Vietnam (~72% mean gap), Nigeria (~69%), Indonesia (~59%) and China (~10%). Pakistan reports gaps of 43–66% from 2018 to 2023 and exactly zero in 2024 and 2025 — one of several countries whose reporting convention changes mid-series.

The indicator is therefore informative for most countries and uninformative for a minority, with no field distinguishing the two cases.

### 3.2 India's own accounts record a substantial shortfall over the same years

Over 2017-18 to 2023-24 the national programme requested ₹23,169.14 crore and was approved ₹18,388.23 crore — 79.4% of request. The annual shortfall ranges from 5.4% to 46.1%.

**Table 1. Two sources, one programme, 2017–2025.**

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

The two sources disagree in every overlapping year at any tolerance below 5 percentage points; disagreement persists in three of six years even at a 15-point tolerance.

### 3.3 Execution is incomplete, and the two sources agree that it is

WHO data give total expenditure as **72%** of budget required across the period (range 45–98%). The national accounts give ₹15,063.46 crore spent against ₹18,388.23 crore approved — **82%** — and against ₹23,169.14 crore requested — **65%**.

Two agencies, two accounting systems, two currencies, and the same direction. Where the sources disagree is on *need*; where they agree is on *execution*. Under-execution of health budgets is a recognised problem in health financing (Piatti-Funfkirchen et al. 2021). We do not explain it here: neither source records why funds went unspent, and explanations such as limited absorptive capacity would need data we do not have.

**A caution about the national table.** Table 16.1 is internally inconsistent. Over 2017–2021, the only years for which `released` is printed, releases sum to ₹3,825.31 crore while expenditure sums to ₹13,312.14 crore — spending 3.5 times the funds the same table reports as released — and 2017 expenditure is 150% of the approved figure. Expenditure can legitimately exceed release where states spend from carried-over or own funds, but the table does not say so, and the `released` column cannot be reconciled with `spent` from the page alone. The three published column totals reconcile exactly, so the table is internally consistent in its totals; the inconsistency lies between its rows. The ratios above use `requested`, `approved` and `spent`, and do not involve `released`.

### 3.4 Financing has domesticated almost completely

Global Fund support fell from **37% of actual TB expenditure in 2017 to 1% in 2025**. Domestic financing rose from 62% to 96%. USAID contributed 1–7% throughout. Earlier work on TB financing, which ends in 2011, analysed trends in domestic and donor funding (Floyd et al. 2013), and domestic spending on AIDS programmes has been analysed for 12 countries (Resch et al. 2015); neither reaches the period studied here, and the 2017–2025 figures are our own analysis of WHO data.

This is the clearest signal in the dataset and it is monotone. It also changes what the funding-gap indicator would be *for*: on our reasoning, an indicator built to describe the external financing landscape has diminishing purchase on a programme financed almost entirely from domestic sources. We know of no study that tests this.

### 3.5 No intervention has a budget line of its own

**Table 2. Interventions, in the rank order of a literature-favourability score from a manuscript under review ([Author] 2026a), against the budget classification. Coverage is judged against WHO's data collection form (WHO 2026c), not the data dictionary; §2.3 explains why they differ.**

| Rank | Intervention | WHO budget line | Coverage |
|---:|---|---|---|
| 1 | Molecular diagnostic scale-up (Xpert MTB/RIF, MTB/XDR) | `budget_lab` | Dominant — shared with all laboratory costs |
| 2 | Airborne infection prevention and control | `budget_prog` | **Pooled** — one of fourteen activities |
| 3 | TB preventive therapy | `budget_tpt` | Commodity only — *drugs* |
| 4 | Whole-genome sequencing for DST prediction | `budget_lab` | Dominant — shared with all laboratory costs |
| 5 | Active case finding | `budget_prog` | **Pooled** — one of fourteen activities |
| 6 | Shorter all-oral regimen rollout (BPaL/BPaL-M) | `budget_sld` | Commodity only — *drugs* |
| 7 | Bovine tuberculosis control | — | **No line** |
| 8 | Private-sector engagement | `budget_prog` | **Pooled** — one of fourteen activities |
| 9 | Nutritional support | `budget_patsup` | Dominant — shared with all patient support |
| 10 | Milk pasteurisation / dairy food chain | — | **No line** |
| 11 | Integrated TB-HIV-diabetes care | `budget_tbhiv` | Commodity only — *TB/HIV arms* |

*Ranking and intervention definitions are taken as given from [Author] (2026a, under review) and were not re-derived here. The rank is a priority-action score built from vocabulary-coded abstracts, without human validation, and its order changes with the coding rule; it is not a formal evidence ranking. Nothing in this section depends on the order.*

**Two interventions have no WHO budget line, and nine share a line with activities that are not theirs.** Only bovine tuberculosis control and milk pasteurisation are wholly absent, and both sit outside the TB programme's budget by design: they are animal-health and food-safety activities. The finding is not absence. It is that **no intervention in the table has a line of its own**, so for none of them can a published figure answer the question "what did this cost?"

The nine fall into three conditions. Three are **pooled**: airborne infection control, active case finding and private-sector engagement are each named in the form's definition of `budget_prog`, a single figure that also absorbs management, supervision, training, policy development, meetings, office equipment, buildings, routine surveillance, advocacy, community engagement, drug-procurement management and contact investigation — fourteen activities in one number. The form acknowledges these interventions exist; the published data cannot say what any of them cost. Three are **commodity-only**: `budget_tpt` is defined as preventive-treatment *drugs*, so the contact tracing, counselling and adherence support that deliver them are not in it; the same holds for the shorter regimen, whose drug cost sits in `budget_sld` while its programme cost sits in `budget_mdrmgt`, which no intervention in the table maps to. Three are **dominant**: the line's scope is largely the intervention, but `budget_lab` still carries every laboratory cost from construction to specimen transport, and `budget_patsup` every form of patient support.

The division that produces this is **procurement**, not priority. The lines that name a single thing name something a programme *buys*: drugs, laboratory equipment and supplies, cash and food for patients. The activities that get pooled are things a programme *does*: ventilating a facility, going out to find cases, working with private providers, visiting a district. A chart of accounts built for purchasing records purchases well and activity badly, and that is what these eleven rows show.

---

## 4. Discussion

### 4.1.1 An error this paper made, and how it was found

An earlier version of this analysis reported that six of the eleven interventions had **no budget line at all**, among them active case finding, airborne infection control and private-sector engagement. That was wrong, and it was wrong for the reason the paper is about.

The mapping was judged against the data dictionary distributed with the datasets, which defines `budget_prog` as *"programme costs to treat drug-susceptible TB"*. Active case finding is not treatment, so it was recorded as having no line. The data collection form, which is the document countries actually complete, defines the same line as covering *"active case-finding"* and *"infection control"* and *"public-private mix activities"* by name (WHO 2026c). The dictionary is an abbreviation of the form, and the abbreviation changed the meaning.

Two things follow. The first is the correction above: the count of interventions with no line falls from six to two, and the finding is restated as the absence of a *separable* line rather than of any line. The second is that an analyst working from the file that ships with the data, as we did, reaches a false conclusion about what the programme budgets for — and nothing in the data, the dictionary or the published figures would reveal it. The form is a separate document, is not distributed with the datasets, and was found only by going to the Global TB Programme's own report repository. That is the same failure the funding-gap result describes, in a different register: the published artefact is not self-describing, and the description that travels with it is not sufficient.

### 4.1 Two different failures of visibility

The two principal findings are usually treated separately — one an indicator-validity problem, the other a classification problem — but they are the same failure at different scales.

The funding gap is uninformative for India because the two quantities behind it are not independently determined: expected funding is reported as equal to budget required, so their difference carries no information. The budget classification is uninformative about services because its categories track procurement, so the service half of tuberculosis control has no field to be recorded in.

In both cases the number exists, is published, and is read as a measurement. In both cases what it can represent was fixed by a reporting convention upstream of any policy decision.

### 4.2 What this means for priority-setting

Three consequences follow directly.

**Cross-country comparisons of TB funding gaps are not comparing like with like.** A country reporting a 70% gap and a country reporting 0% may be describing the same financial reality through different conventions. Any judgement that reads the gap as need — and any rule that someday did — would systematically favour the former. We note again that the Global Fund's formula does not, so this is a caution about interpretation rather than a claim about current allocation.

**A country can domesticate its financing and simultaneously become harder to assess.** India's external financing fell to 1% of expenditure while its reported gap stayed at zero — so, on the reasoning of §3.4, neither the international indicator nor the external-financing share now carries information about domestic adequacy, which is more usually assessed through public expenditure and fiscal space (Tandon and Cashin 2010). The national accounts do, but they are not comparable across countries and, as shown, are internally inconsistent in at least one published table.

**Priority-setting cannot reach interventions with no line item.** An intervention that cannot be costed in the accounts cannot be defended at budget time, tracked in execution, or evaluated for value for money. Three of the five interventions the literature-favourability score places highest are in that position, with the caveat on that score given in §5. This is a hypothesis, not a finding: a plausible mechanism by which service and systems interventions could be under-resourced relative to commodities — not because they are judged less valuable, but because the budget has no place to put them. We have not shown that they are under-resourced, and we know of no study that tests the mechanism. Programme-based budgeting, which would organise budgets around what a programme does, is reported to remain relatively superficial in many low- and middle-income countries (Bertone et al. 2026); that is compatible with the mechanism but does not demonstrate it.

### 4.3 Replication in a second programme

The same structural absence was found in a separate analysis, by the same author, of India's National AIDS and STD Control Programme ([Author] 2026b), where sexually transmitted infection services, pre-exposure prophylaxis and surveillance likewise had no traceable line item while blood transfusion services — a commodity-intensive activity — were separately disaggregated.

Two programmes, two ministry demands, two disease areas, the same division between what is bought and what is done. That makes fiscal invisibility a candidate structural property of disease-control financing rather than an artefact of one programme's accounts.

### 4.4 What would fix it

Both findings have concrete, low-cost remedies.

**Publish unmet need as its own field.** WHO's reporting form could ask for budget required, funding expected **and** a separate statement of whether expected funding reflects need or availability. One additional field would make the existing indicator interpretable and would distinguish the 14 countries from the 44. Modelled estimates of resource need for health systems generally (Stenberg et al. 2017) and of TB spending by source and function (Su et al. 2020) exist, but they are external reconstructions; they do not replace the reporting form stating the distinction itself.

**Tag expenditure to interventions, not only to commodity classes.** A programme that reports what it spent on active case finding, infection control and private-sector engagement — even approximately, even as a share — becomes auditable on those activities. Without such tagging, no quantity of analysis can recover what was spent on them.

**Publish the reconciliation.** Where a national table reports releases and expenditure that cannot be reconciled on the page, a single footnote naming the mechanism would convert an apparent inconsistency into interpretable information.

Table 3 sets out the three together: what was found, the mechanism that produces it, who is in a position to change it, and what would count as evidence that the change had worked. None of the three requires new money, a new survey or a new indicator; each is a change to how an existing figure is recorded.

**Table 3. From finding to action. The last column states what would count as evidence of change, so that each recommendation is falsifiable rather than exhortatory.**

| Finding | Mechanism that produces it | Who can change it | Change | Evidence it worked |
|---|---|---|---|---|
| India's published funding gap is zero in all eight years; 14 of 106 countries report the same way | Expected funding is reported equal to budget required, so the derived gap is zero by construction and carries no information about shortfall | WHO Global TB Programme, which defines the reporting form | One additional field recording whether the expected-funding figure reflects assessed need or anticipated availability | The 14 countries become distinguishable from the 44 that report a gap every year, with no change to any existing field |
| No intervention of eleven has a line of its own; three service-delivery activities share one line with eleven others | The chart of accounts is organised by what is purchased, so the cost of doing something is pooled into a line named for managing the programme | WHO Global TB Programme (reporting form) and national programmes (chart of accounts) | Tag expenditure to interventions as well as to commodity classes, approximately or as a share | Spending on active case finding, airborne infection control and private-sector engagement becomes a reportable number instead of an absence |
| Released and spent amounts do not reconcile on the published page | The reconciling mechanism -- re-appropriation, lapse, carry-forward -- is not stated, so an arithmetic difference cannot be distinguished from an error | Central TB Division, India | A footnote naming the mechanism wherever released and spent differ | An apparent inconsistency becomes interpretable without altering any underlying figure |

The structure of that table -- finding, mechanism, accountable body, action, verification -- follows audit practice, in which a finding is not closed by a recommendation but by evidence that the recommendation changed something.

---

## 5. Limitations

This is a secondary analysis of reported data; we observe reporting behaviour, not financial reality. That a country reports expected funding equal to budget required does not establish that it faces no shortfall, only that the indicator cannot show one.

The intervention-to-budget-line mapping reflects analytic judgement, albeit judgement anchored to published definitions rather than to names. Readers who disagree with a specific mapping can recompute from the published file.

The ranking used to order the eleven interventions is external to this analysis and is not defended here ([Author] 2026a). It comes from a manuscript under review, rests on the favourability of coded literature rather than a formal evidence synthesis, and that manuscript reports that its rank order is sensitive to the coding rule used. The count of interventions with no budget line does not depend on the ranking being correct, only on the interventions being plausible candidates; the statement that three of the top five are among them does depend on it, and is descriptive only for that reason.

The national accounts cover 2017-18 to 2023-24 while the WHO budget data cover 2018–2025, so the overlapping window for direct comparison is six years.

Finally, WHO's reported figures are revised as countries submit corrections, so the dataset version is stated with the download date and is archived with the code.

---

## 6. Conclusions

A budget records what a programme buys, not what it does. In India's tuberculosis response, that distinction leaves no intervention of eleven with a line of its own: two fall outside the budget entirely, three are named by the reporting form but pooled with eleven other activities in one figure, three are visible only as a drug cost, and three sit inside a line far broader than themselves. In none of the eleven cases can the published record say what the intervention cost.

Meanwhile the international indicator intended to signal resource shortfall reports zero for India in every year, because the two quantities behind it are not independently determined — while the national accounts, over the same years, record that a fifth of the requested budget was never approved and a third of it was never spent.

Neither finding is about how much money tuberculosis control receives. Both are about what the financial record is capable of showing. Measurement conventions decided upstream of any policy choice determine which interventions can be defended at budget time and which countries appear to need help. Correcting them is cheaper than any of the interventions they obscure.

---

## References

Bertone MP, Barroy H, Sparkes S et al. 2026. Political economy of budgeting reforms: a comparative analysis of the adoption and implementation of programme-based budgeting in health across seven LMIC countries. *The International Journal of Health Planning and Management*, published online 29 September 2026. doi: 10.1002/hpm.70142

Central TB Division, Ministry of Health and Family Welfare, Government of India. 2024. *India TB Report 2024: National TB Elimination Programme Annual Report*. New Delhi: Ministry of Health and Family Welfare.

Floyd K, Fitzpatrick C, Pantoja A et al. 2013. Domestic and donor financing for tuberculosis care and control in low-income and middle-income countries: an analysis of trends, 2002-11, and requirements to meet 2015 targets. *The Lancet Global Health* **1**: e105-15.

Floyd K, Pantoja A, Dye C. 2007. Financing tuberculosis control: the role of a global financial monitoring system. *Bulletin of the World Health Organization* **85**: 334-40. doi: 10.2471/BLT.06.034942

Global Fund to Fight AIDS, Tuberculosis and Malaria. 2024. *Allocation Methodology for Grant Cycle 8 (2026-2028 Allocation Period)*. Board paper GF/B52/08B, 52nd Board Meeting, 20-22 November 2024. Geneva: The Global Fund. https://archive.theglobalfund.org/media/15310/archive_bm52-08b-allocation-methodology-gc8_report_en.pdf, accessed 13 November 2026.

Peng RD. 2011. Reproducible research in computational science. *Science* **334**: 1226-7.

Piatti-Funfkirchen M, Barroy H, Pivodic F et al. 2021. *Budget Execution in Health*. Washington, DC: World Bank. doi: 10.1596/36583

Reid MJA, Arinaminpathy N, Bloom A et al. 2019. Building a tuberculosis-free world: the Lancet Commission on tuberculosis. *The Lancet* **393**: 1331-84.

Resch S, Ryckman T, Hecht R. 2015. Funding AIDS programmes in the era of shared responsibility: an analysis of domestic spending in 12 low-income and middle-income countries. *The Lancet Global Health* **3**: e52-61.

[Author] 2026a. Drug-resistant tuberculosis in India, 2017-2024: improving outcomes, no worsening axis, and a caution for NTEP trend analysis. Manuscript IJTB-S-26-01305, submitted to the *Indian Journal of Tuberculosis*, 13 November 2026. Under review.

[Author] 2026b. India's human immunodeficiency virus and sexually transmitted infection response at the close of NACP-V: an evidence-practice gap analysis and a priority agenda for clinical sexually transmitted infection services. *Journal of Skin and Sexually Transmitted Diseases*, in production; volume and pages not yet assigned. doi: 10.25259/JSSTD_120_2026

Stenberg K, Hanssen O, Edejer TT et al. 2017. Financing transformative health systems towards achievement of the health Sustainable Development Goals: a model for projected resource needs in 67 low-income and middle-income countries. *The Lancet Global Health* **5**: e875-87.

Su Y, Garcia Baena I, Harle AC et al. 2020. Tracking total spending on tuberculosis by source and function in 135 low-income and middle-income countries, 2000-17: a financial modelling study. *The Lancet Infectious Diseases* **20**: 929-42.

Tandon A, Cashin C. 2010. *Assessing Public Expenditure on Health from a Fiscal Space Perspective*. Health, Nutrition and Population Discussion Paper. Washington, DC: World Bank. doi: 10.1596/13613

World Health Organization (WHO). 2025. *Global Tuberculosis Report 2025*. Geneva: World Health Organization.

World Health Organization (WHO). 2026a. Global Tuberculosis Programme country data: TB budget, and TB expenditure and utilisation datasets. Geneva: World Health Organization. https://extranet.who.int/tme/, data files dated 25 August and 12 November 2026. This data-collection system no longer accepts updates; the archived input files are deposited with the analysis code.

World Health Organization (WHO). 2026b. Global Tuberculosis Programme data dictionary (file TB_dictionary_2026-08-25.csv). Geneva: World Health Organization. Archived with the analysis code.

World Health Organization (WHO). 2026c. *WHO TB data collection form 2026*, version 2026-03-25. Geneva: World Health Organization. Distributed in the Global TB Programme's report repository at [repository URL withheld for blind review] (doc/who_tb_dcf2026.pdf); not distributed with the datasets.

---

## Declarations

**Contributors.** Sole author. Conceived the study, assembled and verified the data, wrote the analysis code, performed all analyses and wrote the manuscript. Meets ICMJE authorship criteria and is responsible for the integrity of the work as a whole.

**Funding.** None.

**Competing interests.** None declared.

**Ethical clearance.** Not required (see Methods 2.5).

**Data availability.** All inputs are publicly available: WHO TB budget and expenditure datasets, and the India TB Report 2024. Analysis code, the archived input files, the intervention-to-budget-line mapping with its definitional basis, and the verification suite are deposited at [repository and archive DOI withheld for blind review]. Every input file is listed in `data/raw_file_manifest.csv` with its SHA-256 digest, so the archived copies can be checked byte for byte against the ones analysed. The manifest also records what is not known: for six of the nine files the download route was not noted at acquisition, and it says so rather than reconstructing a plausible one.

**Use of generative artificial intelligence.** The author used a large language model as a drafting and analysis assistant. All analytical decisions, data verification and conclusions are the author's. The author reviewed and edited all content and takes full responsibility for it.

---
