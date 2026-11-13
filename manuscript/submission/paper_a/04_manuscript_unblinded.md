# What a tuberculosis budget cannot see: fiscal invisibility and the limits of the WHO funding-gap indicator in India, 2017–2025

**Running title:** What a TB budget cannot see

**Author:** Siddalingaiah H S
Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur – 572106, Karnataka, India.
Correspondence: hssling@yahoo.com · ORCID 0000-0002-4771-8285

**Target journal:** *Health Policy and Planning* (Original Article). Verified against the journal's author guidelines, 13 November 2026: abstract maximum **300** words, main text maximum **6,000** for a quantitative or fixed-design study, Key Messages **3-4** bullets, **author-date (Harvard)** referencing, and **double-anonymized** peer review, so the blinded copy is the one to upload.

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
- No tuberculosis intervention of the eleven examined has a budget line of its own: active case finding, airborne infection control and private-sector engagement are named by WHO's reporting form but pooled with thirteen other activities in a single figure, so what any of them costs cannot be recovered from the published record.
- Because cost cannot be attributed to activity, cost per case found cannot be computed and no activity in the national strategic plan can be assessed for value for money. Both problems are correctable without new money: report expected funding as what is anticipated rather than what is required, and record what money was spent *for* as well as what it bought.

---

## 1. Introduction

Tuberculosis control is planned against money. National strategic plans cost their activities, and the Global TB Report (WHO 2025) publishes, for every high-burden country, the budget required for the coming year and the funding expected against it. The difference between those two quantities — the **funding gap** — is read as a measure of under-resourcing. Funding-need figures of this kind are used in TB investment cases and advocacy (Reid et al. 2019), and the gap is shown in the Report's country comparisons (WHO 2025).

We should be precise about what the indicator is and is not used for, because our argument does not depend on overstating it. The Global Fund's published allocation methodology takes disease burden and economic capacity as the inputs to its allocation formula, followed by a qualitative adjustment (Global Fund 2024); it does **not** list the WHO reported funding gap among them. The gap's influence is of a different kind — it is the figure published, quoted and compared when a programme's resourcing is discussed. An indicator need not enter a formula to shape a judgement.

An indicator used that way carries an implicit claim: that the two numbers behind it are independently determined, so their difference is informative. This paper asks whether that claim holds, and finds that for India it does not. Three things here are new. The validity of the funding-gap indicator for an individual country has not previously been examined, although the monitoring system that produces it has been described by its custodians (Floyd et al. 2007). The reporting pattern that makes the indicator uninformative is quantified across all reporting countries rather than asserted for one. And the mapping of interventions to budget lines is judged against the collection instrument countries complete rather than the dictionary distributed with the data, which, as §4.2 shows, changes the answer by a factor of three. The global financial monitoring system that produces these figures has been described by its custodians, who set out its limitations: its restriction to public-sector provider costs, the difficulty of obtaining aggregated data from decentralized systems, and the limited opportunities to validate what countries report (Floyd et al. 2007). To our knowledge, however, no study has asked whether the two quantities behind the reported gap are independently determined for a given country, or examined the cross-country comparability of health-financing indicators of this kind.

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

Eleven tuberculosis interventions were mapped onto WHO budget line items by definition. Their ranking, and the definitions of the interventions themselves, are taken as given from a companion paper now in press (Siddalingaiah 2026a), in which they are ordered by a priority score built from the favourability of coded literature, not from a formal evidence synthesis. The mapping to budget lines does not depend on that ranking (§5).

**Which definition governs.** Two WHO documents define these columns and they do not agree. The data dictionary distributed with the datasets gives `budget_prog` as *"Budget required for programme costs to treat drug-susceptible TB"*. The data collection form, the instrument countries actually complete, gives the same line as covering *"the management and supervision of the TB control programme, training, policy development, meetings, visits for supervision, purchase of office equipment/vehicles, construction of buildings for use by programme staff, routine surveillance, advocacy and communication, public-private mix activities, community engagement, active case-finding, infection control, management of TB drug procurement and distribution, and programme activities linked to contact investigation for TB preventive treatment"* (WHO 2026c). The dictionary's abbreviation excludes case-finding and infection control; the form includes them. **We map against the form**, because it is what determines what a country enters; Supplementary S1 sets both definitions of every column used side by side. An earlier version of this analysis mapped against the dictionary and reported three activities as having no budget line when the form names them; §4.2 reports that error, because it is the kind of error this paper is about.

Each mapping was then classified as **no line** (no WHO line covers the activity), **pooled** (the form names the activity inside a line it shares with many others), **commodity-only** (the line covers the drug or one arm, not the delivery), or **dominant** (the line's scope is largely this activity, though still shared). Mapping is declared data and is published with the code.

### 2.4 Reproducibility

All analysis is pure-Python with no third-party numerical dependency. Every number in this paper is regenerated from the raw files by a single command, following the practice of computational reproducibility (Peng 2011); the figures are drawn from the same outputs by a separate script, and a verification suite checks the derived quantities. A large language model was used as a drafting and analysis assistant; every analytical decision, the code and its verification are the author's. Code and data: https://github.com/hssling/provenance-weighted-priority-setting, doi:10.5281/zenodo.24187367.

### 2.5 Reporting

This study is reported in accordance with the RECORD statement for studies using routinely collected health data (Benchimol et al. 2015); the completed checklist accompanies this submission.

### 2.6 Ethics

Not required. The analysis uses aggregated, publicly available financial and programmatic summaries with no individual-level records and no patient-identifiable information. Institutional ethics approval and informed consent were not applicable.

---

## 3. Results

### 3.1 India's reported funding gap is zero by construction

In all eight years 2018–2025, India reported expected funding (`cf_tot`) **exactly equal** to budget required (`budget_tot`). The reported gap is therefore identically zero in every year — not as a finding about financing, but as a consequence of how the two fields are populated. WHO's dictionary defines `budget_tot` as "Total budget required (US Dollars)" and `cf_tot` as "Total expected funding for all budget line items (US Dollars)" (WHO 2026b); neither definition states that the two should be equal, so the equality is a reporting convention we infer from the data, not one WHO documents.

This is not universal practice. Among 106 countries with at least five years of data, **14** report budget equal to expected funding in every year (Supplementary S3 lists them). **44** report a non-zero gap in every year, including Vietnam (~72% mean gap), Nigeria (~69%), Indonesia (~59%) and China (~10%). Pakistan reports gaps of 43–66% from 2018 to 2023 and exactly zero in 2024 and 2025 — one of several countries whose reporting convention changes mid-series.

The indicator is therefore informative for most countries and uninformative for a minority, with no field distinguishing the two cases.

### 3.2 India's own accounts record a substantial shortfall over the same years

Over 2017-18 to 2023-24 the national programme requested ₹23,169.14 crore and was approved ₹18,388.23 crore — 79.4% of request. The annual shortfall ranges from 5.4% to 46.1% (Figure 1; Supplementary S2 gives the full series).

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

**Table 2. Interventions, in the rank order of a literature-favourability score from a companion paper in press (Siddalingaiah 2026a), against the budget classification. Coverage is judged against WHO's data collection form (WHO 2026c), not the data dictionary; §2.3 explains why they differ.**

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

*Ranking and intervention definitions are taken as given from Siddalingaiah (2026a), in press, and were not re-derived here. The rank is a priority-action score built from vocabulary-coded abstracts, without human validation, and its order changes with the coding rule; it is not a formal evidence ranking. Nothing in this section depends on the order.*

**Two interventions have no WHO budget line, and nine share a line with activities that are not theirs (Figure 2).** Only bovine tuberculosis control and milk pasteurisation are wholly absent, and both sit outside the TB programme's budget by design: they are animal-health and food-safety activities. The finding is not absence. It is that **no intervention in the table has a line of its own**, so for none of them can a published figure answer the question "what did this cost?"

The nine fall into three conditions. Three are **pooled**: airborne infection control, active case finding and private-sector engagement are each named in the form's definition of `budget_prog`, a single figure that also absorbs management, supervision, training, policy development, meetings, office equipment, buildings, routine surveillance, advocacy, community engagement, drug-procurement management and contact investigation — fourteen activities in one number. The form acknowledges these interventions exist; the published data cannot say what any of them cost. Three are **commodity-only**: `budget_tpt` is defined as preventive-treatment *drugs*, so the contact tracing, counselling and adherence support that deliver them are not in it; the same holds for the shorter regimen, whose drug cost sits in `budget_sld` while its programme cost sits in `budget_mdrmgt`, which no intervention in the table maps to. Three are **dominant**: the line's scope is largely the intervention, but `budget_lab` still carries every laboratory cost from construction to specimen transport, and `budget_patsup` every form of patient support.

The division that produces this is **procurement**, not priority. The lines that name a single thing name something a programme *buys*: drugs, laboratory equipment and supplies, cash and food for patients. The activities that get pooled are things a programme *does*: ventilating a facility, going out to find cases, working with private providers, visiting a district. A chart of accounts built for purchasing records purchases well and activity badly, and that is what these eleven rows show.

---

## 4. Discussion

### 4.1 Two different failures of visibility

The two principal findings are usually treated separately — one an indicator-validity problem, the other a classification problem — but they are the same failure at different scales.

The funding gap is uninformative for India because the two quantities behind it are not independently determined: expected funding is reported as equal to budget required, so their difference carries no information. The budget classification is uninformative about services because its categories track procurement, so the service half of tuberculosis control has no field to be recorded in.

In both cases the number exists, is published, and is read as a measurement. In both cases what it can represent was fixed by a reporting convention upstream of any policy decision.

### 4.2 The description that ships with the data is not the definition that governs it

The classification in Table 2 depends on which WHO document is used to decide what a budget line covers, and the two available documents do not agree.

The **data dictionary** is distributed with the datasets and is what an analyst joining on column names will find. It defines `budget_prog` as *"Budget required for programme costs to treat drug-susceptible TB"*. The **data collection form** is the instrument countries complete, is not distributed with the datasets, and defines the same line as covering, by name, *"public-private mix activities, community engagement, active case-finding, infection control"* together with ten other activities (WHO 2026c).

The difference is not cosmetic, and its size can be measured. Classifying the eleven interventions against the dictionary's definition places **six** of them outside the budget altogether, because active case finding, airborne infection control and private-sector engagement are not treatment. Classifying the same eleven against the form's definition places **two** outside it. The same data, the same interventions and the same method yield a threefold difference in the headline count according to which definition is consulted, and only one of the two documents travels with the data.

This has a direct consequence for secondary analysis. An analyst who reads the dictionary carefully, as good practice requires, will conclude that India's TB budget contains no provision for active case finding. That conclusion is false, and nothing in the datasets, the dictionary or the published figures would reveal it; the form has to be sought separately, in the Global TB Programme's report repository. We therefore classify against the form throughout (§2.3), and we report the discrepancy as a result rather than resolving it silently, because an analyst who does not know the two documents differ has no way to discover that their classification depends on the choice.

### 4.3 What this means for priority-setting

Three consequences follow directly.

**Cross-country comparisons of TB funding gaps are not comparing like with like.** A country reporting a 70% gap and a country reporting 0% may be describing the same financial reality through different conventions. Any judgement that reads the gap as need — and any rule that someday did — would systematically favour the former. We note again that the Global Fund's formula does not, so this is a caution about interpretation rather than a claim about current allocation.

**A country can domesticate its financing and simultaneously become harder to assess.** India's external financing fell to 1% of expenditure while its reported gap stayed at zero — so, on the reasoning of §3.4, neither the international indicator nor the external-financing share now carries information about domestic adequacy, which is more usually assessed through public expenditure and fiscal space (Tandon and Cashin 2010). The national accounts do, but they are not comparable across countries and, as shown, are internally inconsistent in at least one published table.

**Priority-setting cannot reach interventions with no line item.** An intervention that cannot be costed in the accounts cannot be defended at budget time, tracked in execution, or evaluated for value for money. Three of the five interventions the literature-favourability score places highest are in that position, with the caveat on that score given in §5. This is a hypothesis, not a finding: a plausible mechanism by which service and systems interventions could be under-resourced relative to commodities — not because they are judged less valuable, but because the budget has no place to put them. We have not shown that they are under-resourced, and we know of no study that tests the mechanism. Programme-based budgeting, which would organise budgets around what a programme does, is reported to remain relatively superficial in many low- and middle-income countries (Bertone et al. 2026); that is compatible with the mechanism but does not demonstrate it.

### 4.4 Replication in a second programme

The same structural absence was found in a separate analysis, by the same author, of India's National AIDS and STD Control Programme (Siddalingaiah 2026b), where sexually transmitted infection services, pre-exposure prophylaxis and surveillance likewise had no traceable line item while blood transfusion services — a commodity-intensive activity — were separately disaggregated.

Two programmes, two ministry demands, two disease areas, the same division between what is bought and what is done. That makes fiscal invisibility a candidate structural property of disease-control financing rather than an artefact of one programme's accounts.

### 4.5 What would fix it

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

### 4.6 What the National TB Elimination Programme can do about it

The two findings are not criticisms of India's programme. Neither concerns how much money tuberculosis control receives, how well it is spent, or whether the reported figures are accurate. Both concern what the financial record is able to show, and both are fixed by the people who complete the forms rather than by the people who fund them. Four changes follow, in increasing order of effort, and the first costs nothing.

**One field, in the next reporting round.** India enters total expected funding equal to total budget required. The Central TB Division already holds the components needed to enter something more informative: expected funding is reported by source, and those components reconcile with the total in every testable country-year (§3.1). Entering anticipated funding from identified sources — domestic approvals, Global Fund, other grants — in place of a figure set equal to requirement would make India's unmet need visible in the global dataset for the first time. At present the opposite is true. In WHO's published data India, the country with the largest tuberculosis burden in the world, reports no funding gap at all in any year from 2018 to 2025, while its own accounts record approvals falling short of requests by 5.4% to 46.1% (Figure 1). Whatever the shortfall is, the global record cannot show it, and the programme gets no credit for the need it has already documented domestically.

**Sub-codes under one budget line, in the next national strategic plan.** WHO's collection form pools fourteen activities into `budget_prog`, among them active case finding, airborne infection control and private-sector engagement (§3.5). Nothing in that form prevents a national programme from carrying its own sub-codes beneath that line. A programme that can state what it spent on active case finding can report cost per additional case found, defend that activity when budgets are reallocated, and evaluate whether intensified case finding is worth its cost. A programme that cannot state it has no evidence to offer in any of those three conversations, however well the activity performs. This is an internal accounting change, invisible to WHO's form, and it is the single change that would make the largest number of NSP activities evaluable.

**A footnote where the national table does not reconcile.** The India TB Report records released and spent amounts that cannot be reconciled on the page (§3.3). A reader cannot tell whether this reflects re-appropriation, lapse, carry-forward or an error. One sentence naming the mechanism converts an apparent inconsistency into interpretable information, at no analytical cost.

**A pre-submission check, taking minutes.** Before the annual return is submitted, three questions can be asked of it: does total expected funding equal total budget required, and if so is that intended; do the eleven components sum to each stated total; and is any value identical to last year's entry, and if so was it re-estimated or carried forward? The code accompanying this paper performs all three on a country-year table and is published with it. These are the checks we applied to 215 countries; a programme can apply them to its own submission before anyone else does.

### 4.7 Why this is a question about efficiency, not only about transparency

The reason attribution matters is that it is the precondition for every method by which a programme can improve the value it obtains from a fixed budget.

Allocative efficiency requires knowing the cost of an additional unit of outcome from each competing activity, so that money can move from activities with a poor return at the margin to activities with a better one. The National TB Elimination Programme has the outcome side of that calculation in detail: notifications, yield from contact investigation, treatment success, and the drug-resistance cascade are all reported annually and disaggregated. What it does not have is the cost side at the same resolution. Cost per case notified through active case finding cannot be computed, because the numerator is pooled with thirteen other activities in `budget_prog`. Cost per contact screened cannot be computed, because contact investigation is costed in the same pooled line while preventive-treatment drugs are costed separately in `budget_tpt`. The consequence is specific and it is not a transparency problem: **India cannot perform its own cost-effectiveness analysis of its own tuberculosis activities**, and must instead import effectiveness and cost estimates generated in other settings, with other unit costs, other salary structures and other epidemiology.

This also constrains evaluation. The national strategic plan sets targets by activity; the budget records money by commodity class. Performance against the plan can therefore be evaluated on whether an activity happened, but never on what it cost to make it happen, so no activity in the plan can be assessed for value for money. Programme budgeting and marginal analysis, the standard method for reallocating at the margin under a fixed envelope, requires exactly the attribution that is missing (Madden et al. 1995), and the omission of programme and delivery costs is a long-recognised weakness in intervention costing generally (Johns et al. 2003).

The remedy does not require activity-based costing across the whole programme, which would be disproportionate. It requires a second dimension on each transaction — what was bought, and what it was bought for — restricted to a small set of priority activities, perhaps six to eight, chosen because they are contested at budget time. That is the minimal form of programme-based budgeting, a reform India has adopted in principle elsewhere in health but which is reported to remain shallow in practice across comparable settings (Bertone et al. 2026). Once the second dimension exists, three things become computable that are not computable today: cost per additional case found, the marginal cost of each activity at its current scale, and the opportunity cost of expanding one activity rather than another. None of the three requires additional money. All three require that the chart of accounts record what the programme does as well as what it buys.

## 5. Limitations

This is a secondary analysis of reported data; we observe reporting behaviour, not financial reality. That a country reports expected funding equal to budget required does not establish that it faces no shortfall, only that the indicator cannot show one.

The intervention-to-budget-line mapping reflects analytic judgement, albeit judgement anchored to published definitions rather than to names. Readers who disagree with a specific mapping can recompute from the published file.

The ranking used to order the eleven interventions is external to this analysis and is not defended here (Siddalingaiah 2026a). It comes from a companion paper in press, rests on the favourability of coded literature rather than a formal evidence synthesis, and that manuscript reports that its rank order is sensitive to the coding rule used. The count of interventions with no budget line does not depend on the ranking being correct, only on the interventions being plausible candidates; the statement that three of the top five are among them does depend on it, and is descriptive only for that reason.

The national accounts cover 2017-18 to 2023-24 while the WHO budget data cover 2018–2025, so the overlapping window for direct comparison is six years.

Finally, WHO's reported figures are revised as countries submit corrections, so the dataset version is stated with the download date and is archived with the code.

---

## 6. Conclusions

A budget records what a programme buys, not what it does. In India's tuberculosis response, that distinction leaves no intervention of eleven with a line of its own: two fall outside the budget entirely, three are named by the reporting form but pooled with eleven other activities in one figure, three are visible only as a drug cost, and three sit inside a line far broader than themselves. In none of the eleven cases can the published record say what the intervention cost.

That is a constraint on efficiency, not only on transparency. Attribution of cost to activity is the precondition for computing cost per unit of outcome, and therefore for moving money towards what works at the margin. Neither remedy proposed here needs additional funding: one is a different entry in an existing field, the other a second dimension in an existing chart of accounts. Together they would let a programme that already measures its outcomes in detail begin to measure what those outcomes cost.

Meanwhile the international indicator intended to signal resource shortfall reports zero for India in every year, because the two quantities behind it are not independently determined — while the national accounts, over the same years, record that a fifth of the requested budget was never approved and a third of it was never spent.

Neither finding is about how much money tuberculosis control receives. Both are about what the financial record is capable of showing. Measurement conventions decided upstream of any policy choice determine which interventions can be defended at budget time and which countries appear to need help. Correcting them is cheaper than any of the interventions they obscure.

---

## References

Benchimol EI, Smeeth L, Guttmann A et al. 2015. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) Statement. *PLOS Medicine* **12**: e1001885. doi: 10.1371/journal.pmed.1001885

Bertone MP, Barroy H, Sparkes S et al. 2026. Political economy of budgeting reforms: a comparative analysis of the adoption and implementation of programme-based budgeting in health across seven LMIC countries. *The International Journal of Health Planning and Management*, published online 29 September 2026. doi: 10.1002/hpm.70142

Central TB Division, Ministry of Health and Family Welfare, Government of India. 2024. *India TB Report 2024: National TB Elimination Programme Annual Report*. New Delhi: Ministry of Health and Family Welfare.

Floyd K, Fitzpatrick C, Pantoja A et al. 2013. Domestic and donor financing for tuberculosis care and control in low-income and middle-income countries: an analysis of trends, 2002-11, and requirements to meet 2015 targets. *The Lancet Global Health* **1**: e105-15.

Floyd K, Pantoja A, Dye C. 2007. Financing tuberculosis control: the role of a global financial monitoring system. *Bulletin of the World Health Organization* **85**: 334-40. doi: 10.2471/BLT.06.034942

Global Fund to Fight AIDS, Tuberculosis and Malaria. 2024. *Allocation Methodology for Grant Cycle 8 (2026-2028 Allocation Period)*. Board paper GF/B52/08B, 52nd Board Meeting, 20-22 November 2024. Geneva: The Global Fund. https://archive.theglobalfund.org/media/15310/archive_bm52-08b-allocation-methodology-gc8_report_en.pdf, accessed 13 November 2026.

Johns B, Baltussen R, Hutubessy R. 2003. Programme costs in the economic evaluation of health interventions. *Cost Effectiveness and Resource Allocation* **1**: 1. doi: 10.1186/1478-7547-1-1

Madden L, Hussey R, Mooney G, Church E. 1995. Public health and economics in tandem: programme budgeting, marginal analysis and priority setting in practice. *Health Policy* **33**: 161-8. doi: 10.1016/0168-8510(95)93676-R

Peng RD. 2011. Reproducible research in computational science. *Science* **334**: 1226-7.

Piatti-Funfkirchen M, Barroy H, Pivodic F et al. 2021. *Budget Execution in Health*. Washington, DC: World Bank. doi: 10.1596/36583

Reid MJA, Arinaminpathy N, Bloom A et al. 2019. Building a tuberculosis-free world: the Lancet Commission on tuberculosis. *The Lancet* **393**: 1331-84.

Resch S, Ryckman T, Hecht R. 2015. Funding AIDS programmes in the era of shared responsibility: an analysis of domestic spending in 12 low-income and middle-income countries. *The Lancet Global Health* **3**: e52-61.

Siddalingaiah HS. 2026a. Drug-resistant tuberculosis in India, 2017-2024: improving outcomes, no worsening axis, and a caution for NTEP trend analysis. *Indian Journal of Tuberculosis*, in press; assigned to a forthcoming issue (manuscript IJTB-S-26-01305). Volume and pages not yet available.

Siddalingaiah HS. 2026b. India's human immunodeficiency virus and sexually transmitted infection response at the close of NACP-V: an evidence-practice gap analysis and a priority agenda for clinical sexually transmitted infection services. *Journal of Skin and Sexually Transmitted Diseases*, in production; volume and pages not yet assigned. doi: 10.25259/JSSTD_120_2026

Stenberg K, Hanssen O, Edejer TT et al. 2017. Financing transformative health systems towards achievement of the health Sustainable Development Goals: a model for projected resource needs in 67 low-income and middle-income countries. *The Lancet Global Health* **5**: e875-87.

Su Y, Garcia Baena I, Harle AC et al. 2020. Tracking total spending on tuberculosis by source and function in 135 low-income and middle-income countries, 2000-17: a financial modelling study. *The Lancet Infectious Diseases* **20**: 929-42.

Tandon A, Cashin C. 2010. *Assessing Public Expenditure on Health from a Fiscal Space Perspective*. Health, Nutrition and Population Discussion Paper. Washington, DC: World Bank. doi: 10.1596/13613

World Health Organization (WHO). 2025. *Global Tuberculosis Report 2025*. Geneva: World Health Organization.

World Health Organization (WHO). 2026a. Global Tuberculosis Programme country data: TB budget, and TB expenditure and utilisation datasets. Geneva: World Health Organization. https://extranet.who.int/tme/, data files dated 25 August and 12 November 2026. This data-collection system no longer accepts updates; the archived input files are deposited with the analysis code.

World Health Organization (WHO). 2026b. Global Tuberculosis Programme data dictionary (file TB_dictionary_2026-08-25.csv). Geneva: World Health Organization. Archived with the analysis code.

World Health Organization (WHO). 2026c. *WHO TB data collection form 2026*, version 2026-03-25. Geneva: World Health Organization. Distributed in the Global TB Programme's report repository at https://github.com/GTB-TME/gtbreport2026 (doc/who_tb_dcf2026.pdf); not distributed with the datasets.


## Figure captions

**Figure 1. Two accounts of the same years.** India's funding gap as reported to WHO, against the shortfall recorded in India's own programme accounts, 2018–2023. The WHO-reported gap is zero in every year because expected funding is reported equal to budget required; over the same years the national accounts record approvals falling short of requests by 5.4% to 46.1%. Values are percentages of the amount requested. Sources: WHO TB budget dataset (WHO 2026a) and India TB Report 2024, Table 16.1 (Central TB Division 2024).

*Alt text: A line chart from 2018 to 2023 with two series. One series, the funding gap reported to WHO, is a flat line at zero across all six years. The other, the shortfall in India's own accounts, varies between 5.4% and 46.1%, rising sharply to 46.1% in 2022.*

**Figure 2. Where each intervention falls in WHO's budget classification.** Eleven tuberculosis interventions, in the rank order of Table 2, mapped onto the WHO budget line that covers them, judged against the data collection form (WHO 2026c). Arrows are styled by the condition of that coverage: pooled, where the form names the activity inside a line it shares with many others; commodity only, where the line covers the drug or one arm but not the delivery; dominant, where the line's scope is largely the activity though still shared; and no line, where no WHO line covers the activity. Three interventions converge on `budget_prog`, a single figure that also absorbs eleven other activities. No arrow terminates at a line specific to its own intervention.

*Alt text: A diagram with eleven tuberculosis interventions listed on the left and seven WHO budget categories on the right, joined by arrows. Three arrows, for airborne infection control, active case finding and private-sector engagement, converge on a single category labelled budget_prog, fourteen activities pooled. Two arrows, for bovine TB control and milk pasteurisation, go to a category labelled no WHO budget line. No intervention has a category of its own.*

---

## Declarations

**Contributors.** Sole author. Conceived the study, assembled and verified the data, wrote the analysis code, performed all analyses and wrote the manuscript. Meets ICMJE authorship criteria and is responsible for the integrity of the work as a whole.

**Funding.** None.

**Competing interests.** None declared.

**Ethical clearance.** Not required (see Methods 2.5).

**Data availability.** All inputs are publicly available: WHO TB budget and expenditure datasets, and the India TB Report 2024. Analysis code, the archived input files, the intervention-to-budget-line mapping with its definitional basis, and the verification suite are deposited at https://github.com/hssling/provenance-weighted-priority-setting and archived at Zenodo, doi:10.5281/zenodo.24187367 (release v1.0.0; the concept DOI doi:10.5281/zenodo.24187366 always resolves to the latest version). Every input file is listed in `data/raw_file_manifest.csv` with its SHA-256 digest, so the archived copies can be checked byte for byte against the ones analysed. The manifest also records what is not known: for six of the nine files the download route was not noted at acquisition, and it says so rather than reconstructing a plausible one.

**Use of generative artificial intelligence.** The author used a large language model as a drafting and analysis assistant. All analytical decisions, data verification and conclusions are the author's. The author reviewed and edited all content and takes full responsibility for it.

---

## Notes for the author — not for submission

**Before submitting:**
1. [done 13 Nov 2026] Repository public, Zenodo v1.0.0 minted: version DOI 10.5281/zenodo.24187367, concept DOI 10.5281/zenodo.24187366, both inserted in SS2.4 and Data availability.
2. [done 13 Nov 2026] Target journal: *Health Policy and Planning*. Abstract cut to 249 words against its 250 limit, so there is no margin if that limit has moved. Key messages box added (three bullets, house style confirmed against published HPP articles). The journal's guideline page is bot-protected and was not read; confirm the limits in a browser.
3. **References placed (16, Vancouver, numbered by first appearance).** (a) [done] SS1 Global Fund statement cites ref 16 (Board paper GF/B52/08B, read in full; the formula inputs are burden and economic capacity, and the paper does not name the WHO funding gap; it does say technical partners gave input on funding needs, so keep the wording at 'does not list ... among them'). (b) [done 13 Nov 2026] JSSTD ref 13 now carries the DOI printed on the journal's R14 proof, 10.25259/JSSTD_120_2026. It returns 404 today because the article is in production and the DOI is registered at publication; that is expected and is stated in the reference. Add volume and pages when the issue is released. (c) [done] Bertone 2026 cited as '2026 Sep 29 [online ahead of print]'; Crossref, PubMed and OpenAlex all carry null volume and pages, so this will not need revisiting. (d) OPEN: whether *Health Policy and Planning* accepts an under-review citation (ref 6) for Table 2 -- if not, give the ranking its own methods paragraph. (e) [done 13 Nov 2026] Reid 2019 (ref 2) and Su 2020 (ref 15) read in full text; both support the sentences citing them.
4. [done 13 Nov 2026] Self-similarity run with `verification/check_self_similarity.py`, which now includes the JSSTD paper. SS4.3 replicates its finding in a second programme and was the likeliest source of overlap; the measured share is **0.0%**, so the relationship is conceptual and the citation carries it. Paper B 0.6%, TB-BOPAS 0.3%, IJTB review 0.2%, combined 0.9%, no verbatim run over 40 words.
5. OPEN: consider whether Table 2's ranking needs its own methods paragraph or can be cited.
6. [done 13 Nov 2026] Novelty claim tested by a pre-registered search, `manuscript/novelty_search.md`: protocol written and committed before any query ran. Verdict NEEDS SOFTENING, not refuted. Floyd et al. (2007) describes the WHO global financial monitoring system that produces `budget_tot` and `cf_tot` and sets out its limitations, so "the indicator is unexamined" was too strong and a TB-financing reviewer could have cited it against us. It does not touch the finding: it never asks whether the two quantities are independently determined, never counts countries reporting them equal, never discusses a zero gap. The abstract and §1 now claim the narrower and true thing. Paper B's novelty claim STANDS unchanged.

**Deliberately excluded from this draft:** the provenance-weighting instrument, the five tests, the composite, EVPR, and the BOPAS propagation. None of it is needed for these findings, and the instrument's central claim — that provenance weighting reorders priorities — is not yet supported. Keeping it out makes this paper defensible now and leaves the methods paper intact for when D2/D3 exist.
