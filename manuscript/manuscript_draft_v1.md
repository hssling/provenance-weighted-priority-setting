# What a tuberculosis budget cannot see: fiscal invisibility and the limits of the WHO funding-gap indicator in India, 2017–2025

**Running title:** What a TB budget cannot see

**Author:** Siddalingaiah H S
Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur – 572106, Karnataka, India.
Correspondence: hssling@yahoo.com · ORCID 0000-0002-4771-8285

**Target journal:** *BMJ Global Health* (Original Research) — alternative: *Health Policy and Planning*

---

## Abstract

**Background.** The World Health Organization's tuberculosis (TB) funding gap — budget required minus funding expected — is reported annually for every high-burden country and is used in investment cases and priority-setting. Whether it measures what it claims to measure for any given country has not been examined.

**Methods.** We analysed WHO's reported TB budget and expenditure data for 215 countries (2017–2025) alongside India's national programme accounts (India TB Report 2024) and WHO's data dictionary. The two sources were compared through dimensionless internal ratios, requiring no currency conversion, and eleven evidence-ranked TB interventions were mapped onto WHO budget line items by their published definitions rather than their names.

**Results.** India reported expected funding exactly equal to budget required in all eight years 2018–2025, so its WHO funding gap is zero **by construction** rather than by observation. Of 106 countries with five or more years of data, 14 report this way; 44 report a non-zero gap every year. Over the same period India's own accounts record ₹18,388 crore approved against ₹23,169 crore requested — a shortfall of 5.4% to 46.1% by year. The sources disagree on need but agree on execution: 72% of budget required was spent (WHO), 82% of approved (national accounts). Global Fund support fell from 37% of TB expenditure in 2017 to 1% in 2025. **Six of eleven evidence-ranked interventions, including three of the top five, have no budget line of any kind**; three more map only to drugs-only lines, leaving their delivery costs unattributable.

**Conclusions.** A budget records what a programme buys, not what it does. Commodities have line items; services and systems interventions largely do not, so the best-evidenced among them cannot be costed, defended at budget time or evaluated for value. Meanwhile the indicator intended to signal resource shortfall is, for India, structurally incapable of doing so. Neither finding concerns how much tuberculosis control receives; both concern what the financial record can show. Both are correctable: publish unmet need as its own field, and tag expenditure to interventions rather than to commodity classes alone.

**Keywords:** Antitubercular Agents; Costs and Cost Analysis; Financing, Government; Health Expenditures; Health Priorities; Healthcare Financing; India; Program Evaluation; Tuberculosis

---

## 1. Introduction

Tuberculosis control is planned against money. National strategic plans cost their activities, the Global Fund allocates against stated need, and the WHO Global TB Report publishes, for every high-burden country, the budget required for the coming year and the funding expected against it. The difference between those two quantities — the **funding gap** — is read as a measure of under-resourcing. It appears in investment cases, in advocacy, and in the comparative tables that shape where external financing goes.

An indicator used that way carries an implicit claim: that the two numbers behind it are independently determined, so their difference is informative. This paper asks whether that claim holds, and finds that for India it does not.

The question matters beyond measurement. India notifies more tuberculosis than any other country and now finances almost all of its response domestically. If the indicator that would signal a shortfall cannot register one, neither the national programme nor its partners have an external instrument that would show strain before it appeared in outcomes.

A second question follows from the first. Even where financing *is* recorded, it is recorded in categories, and those categories decide what can be counted. We therefore also ask which tuberculosis interventions have a budget line at all — and find that the answer divides along a line that is not about evidence or priority, but about whether an intervention has something to procure.

---

## 2. Methods

### 2.1 Data sources

Three public sources, all retrieved in November 2026:

1. **WHO TB budget dataset** (`TB_budget`, 1,720 rows, 215 countries, 2018–2025, 43 variables): budget required and funding expected, each disaggregated into eleven line items, plus expected funding by source (domestic, Global Fund, USAID, other) and budgeted cost per patient treated.
2. **WHO TB expenditure and utilisation dataset** (`TB_expenditure_utilisation`, 2017–2026): actual expenditure and funds received, on the same line-item structure.
3. **India TB Report 2024, Table 16.1** (p.174): budget requested, budget estimates/approved, total releases to states, and total expenditure for 2017-18 to 2023-24, in ₹ crore.

WHO's data dictionary was used to establish what each variable covers. This is not incidental: an early version of this analysis mapped active case finding to `budget_prog` on the strength of the name, when the dictionary defines it as *"programme costs to **treat** drug-susceptible TB"*. Case finding is not treatment, and the mapping was wrong. Every mapping reported here was checked against its definition.

### 2.2 Comparing sources that are not in the same units

WHO reports in US dollars on a calendar year; the national accounts report in ₹ crore on a fiscal year. Converting between them would import an exchange-rate assumption into the comparison.

We avoid this by comparing each source's **internal, dimensionless ratio**. WHO's reported gap is `(budget_tot − cf_tot) / budget_tot`. The national shortfall is `(requested − approved) / requested`. Both answer the same question — *what fraction of the budget that was needed was not secured?* — and neither carries a currency.

An earlier formulation compared year-on-year proportional change in each source, which cancels levels. It therefore could not detect the disagreement reported here, which is a level disagreement with no trend component. We record this because it is instructive: a comparison designed to avoid one assumption was blind to the finding it was built for.

### 2.3 Mapping interventions to budget lines

Eleven tuberculosis interventions, ranked by an independently derived evidence score, were mapped onto WHO budget line items by definition. Each mapping was classified as **full** (the line covers the intervention), **partial** (the line covers part of it), or **absent** (no line exists). Mapping is declared data and is published with the code.

### 2.4 Reproducibility

All analysis is pure-Python with no third-party numerical dependency. Every figure in this paper is regenerated from the raw files by a single command, and a verification suite (255 tests) checks the derived quantities, including that every number quoted here is reproduced from source rather than transcribed. Code and data: [repository URL to be inserted at acceptance].

### 2.5 Ethics

Not required. The analysis uses aggregated, publicly available financial and programmatic summaries with no individual-level records and no patient-identifiable information. Institutional ethics approval and informed consent were not applicable.

---

## 3. Results

### 3.1 India's reported funding gap is zero by construction

In all eight years 2018–2025, India reported expected funding (`cf_tot`) **exactly equal** to budget required (`budget_tot`). The reported gap is therefore identically zero in every year — not as a finding about financing, but as a consequence of how the two fields are populated.

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

Two agencies, two accounting systems, two currencies, and the same direction. Where the sources disagree is on *need*; where they agree is on *execution*.

**A caution about the national table.** Table 16.1 is internally inconsistent. Over 2017–2021, the only years for which `released` is printed, releases sum to ₹3,825.31 crore while expenditure sums to ₹13,312.14 crore — spending 3.5 times the funds the same table reports as released — and 2017 expenditure is 150% of the approved figure. Expenditure can legitimately exceed release where states spend from carried-over or own funds, but the table does not say so, and the `released` column cannot be reconciled with `spent` from the page alone. The three published column totals reconcile exactly, so the table is internally consistent in its totals; the inconsistency lies between its rows. The ratios above use `requested`, `approved` and `spent`, and do not involve `released`.

### 3.4 Financing has domesticated almost completely

Global Fund support fell from **37% of actual TB expenditure in 2017 to 1% in 2025**. Domestic financing rose from 62% to 96%. USAID contributed 1–7% throughout.

This is the clearest signal in the dataset and it is monotone. It also changes what the funding-gap indicator would be *for*: an indicator built to describe the external financing landscape has diminishing purchase on a programme financed almost entirely from domestic sources.

### 3.5 Six of eleven interventions have no budget line at all

**Table 2. Evidence-ranked interventions against the budget classification.**

| Rank | Intervention | WHO budget line | Coverage |
|---:|---|---|---|
| 1 | Molecular diagnostic scale-up (Xpert MTB/RIF, MTB/XDR) | `budget_lab` | Full |
| 2 | Airborne infection prevention and control | — | **Absent** |
| 3 | TB preventive therapy | `budget_tpt` | Partial — *drugs only* |
| 4 | Whole-genome sequencing for DST prediction | — | **Absent** |
| 5 | Active case finding | — | **Absent** |
| 6 | Shorter all-oral regimen rollout (BPaL/BPaL-M) | `budget_sld` | Partial — *drugs only* |
| 7 | Bovine tuberculosis control | — | **Absent** |
| 8 | Private-sector engagement | — | **Absent** |
| 9 | Nutritional support | `budget_patsup` | Full |
| 10 | Milk pasteurisation / dairy food chain | — | **Absent** |
| 11 | Integrated TB-HIV-diabetes care | `budget_tbhiv` | Partial — *TB/HIV only* |

**Three of the top five evidence-ranked interventions are fiscally untraceable.** Only two of eleven map fully.

The pattern is not random with respect to evidence rank, and it is not about priority. It is about **procurement**. Every full or partial mapping corresponds to something a programme *buys*: drugs (`budget_tpt`, `budget_sld`), laboratory equipment and supplies (`budget_lab`), cash transfers to patients (`budget_patsup`). Every absent mapping corresponds to something a programme *does*: ventilation and triage in facilities, finding cases actively, engaging private providers, working across the animal-human interface.

Even where a line exists, the same division operates within it. `budget_tpt` is defined as *"TB preventive treatment: **drugs**"*. The drugs for preventive therapy are traceable; the contact tracing, counselling and adherence support that deliver them are not. The same holds for the shorter-regimen rollout, whose drug cost is in `budget_sld` while its programme cost sits in `budget_mdrmgt`, which maps to no intervention at all.

---

## 4. Discussion

### 4.1 Two different failures of visibility

The two principal findings are usually treated separately — one an indicator-validity problem, the other a classification problem — but they are the same failure at different scales.

The funding gap is uninformative for India because the two quantities behind it are not independently determined: expected funding is reported as equal to budget required, so their difference carries no information. The budget classification is uninformative about services because its categories track procurement, so the service half of tuberculosis control has no field to be recorded in.

In both cases the number exists, is published, and is read as a measurement. In both cases what it can represent was fixed by a reporting convention upstream of any policy decision.

### 4.2 What this means for priority-setting

Three consequences follow directly.

**Cross-country comparisons of TB funding gaps are not comparing like with like.** A country reporting a 70% gap and a country reporting 0% may be describing the same financial reality through different conventions. Any allocation rule that reads the gap as need will systematically favour the former.

**A country can domesticate its financing and simultaneously become harder to assess.** India's external financing fell to 1% of expenditure while its reported gap stayed at zero — so neither the international indicator nor the external-financing share now carries information about domestic adequacy. The national accounts do, but they are not comparable across countries and, as shown, are internally inconsistent in at least one published table.

**Evidence-based priority-setting cannot reach interventions with no line item.** An intervention that cannot be costed in the accounts cannot be defended at budget time, tracked in execution, or evaluated for value for money. Three of the five best-evidenced interventions in this analysis are in that position. This is a plausible mechanism by which service and systems interventions are persistently under-resourced relative to commodities — not because they are judged less valuable, but because the budget has no place to put them.

### 4.3 Replication in a second programme

The same structural absence was found in an independent analysis of India's National AIDS and STD Control Programme, where sexually transmitted infection services, pre-exposure prophylaxis and surveillance likewise had no traceable line item while blood transfusion services — a commodity-intensive activity — were separately disaggregated.

Two programmes, two ministry demands, two disease areas, the same division between what is bought and what is done. That makes fiscal invisibility a candidate structural property of disease-control financing rather than an artefact of one programme's accounts.

### 4.4 What would fix it

Both findings have concrete, low-cost remedies.

**Publish unmet need as its own field.** WHO's reporting form could ask for budget required, funding expected **and** a separate statement of whether expected funding reflects need or availability. One additional field would make the existing indicator interpretable and would distinguish the 14 countries from the 44.

**Tag expenditure to interventions, not only to commodity classes.** A programme that reports what it spent on active case finding, infection control and private-sector engagement — even approximately, even as a share — becomes auditable on those activities. Without such tagging, no quantity of analysis can recover what was spent on them.

**Publish the reconciliation.** Where a national table reports releases and expenditure that cannot be reconciled on the page, a single footnote naming the mechanism would convert an apparent inconsistency into interpretable information.

---

## 5. Limitations

This is a secondary analysis of reported data; we observe reporting behaviour, not financial reality. That a country reports expected funding equal to budget required does not establish that it faces no shortfall, only that the indicator cannot show one.

The intervention-to-budget-line mapping reflects analytic judgement, albeit judgement anchored to published definitions rather than to names. Readers who disagree with a specific mapping can recompute from the published file.

The evidence ranking used to order the eleven interventions is external to this analysis and is not defended here; the fiscal-invisibility finding does not depend on the ranking being correct, only on the interventions being plausible candidates.

The national accounts cover 2017-18 to 2023-24 while the WHO budget data cover 2018–2025, so the overlapping window for direct comparison is six years.

Finally, WHO's reported figures are revised as countries submit corrections, so the dataset version is stated with the download date and is archived with the code.

---

## 6. Conclusions

A budget records what a programme buys, not what it does. In India's tuberculosis response, that distinction leaves three of the five best-evidenced interventions without any line item, and leaves the delivery cost of three more pooled into categories from which it cannot be recovered.

Meanwhile the international indicator intended to signal resource shortfall reports zero for India in every year, because the two quantities behind it are not independently determined — while the national accounts, over the same years, record that a fifth of the requested budget was never approved and a third of it was never spent.

Neither finding is about how much money tuberculosis control receives. Both are about what the financial record is capable of showing. Measurement conventions decided upstream of any policy choice determine which interventions can be defended at budget time and which countries appear to need help. Correcting them is cheaper than any of the interventions they obscure.

---

## Declarations

**Contributors.** Sole author. Conceived the study, assembled and verified the data, wrote the analysis code, performed all analyses and wrote the manuscript. Meets ICMJE authorship criteria and is responsible for the integrity of the work as a whole.

**Funding.** None.

**Competing interests.** None declared.

**Ethical clearance.** Not required (see Methods 2.5).

**Data availability.** All inputs are publicly available: WHO TB budget and expenditure datasets, and the India TB Report 2024. Analysis code, the archived input files, the intervention-to-budget-line mapping with its definitional basis, and the verification suite are deposited at [repository URL and DOI to be inserted at acceptance].

**Use of generative artificial intelligence.** The author used a large language model as a drafting and analysis assistant. All analytical decisions, data verification and conclusions are the author's. The author reviewed and edited all content and takes full responsibility for it.

---

## Notes for the author — not for submission

**Before submitting:**
1. Make the GitHub repository public and mint a Zenodo DOI; insert both in §2.4 and Data availability.
2. Decide the target journal and reformat to its structure. BMJ Global Health takes a 300-word structured abstract and Vancouver references; Health Policy and Planning differs.
3. **References are not yet written.** Needed: WHO Global TB Report 2025; WHO TB data dictionary; India TB Report 2024; the NACP-V analysis for §4.3; 2–3 citations on health-financing indicator validity; 1–2 on TB investment cases; the source of the evidence ranking in Table 2.
4. Run the self-similarity check against the IJTB submission and the JSSTD paper before uploading — §4.3 overlaps the latter by construction and must be cited, not reused.
5. Consider whether Table 2's evidence ranking needs its own methods paragraph or can be cited.

**Deliberately excluded from this draft:** the provenance-weighting instrument, the five tests, the composite, EVPR, and the BOPAS propagation. None of it is needed for these findings, and the instrument's central claim — that provenance weighting reorders priorities — is not yet supported. Keeping it out makes this paper defensible now and leaves the methods paper intact for when D2/D3 exist.
