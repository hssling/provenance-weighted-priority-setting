# What a tuberculosis budget cannot see: fiscal invisibility and the limits of the WHO funding-gap indicator in India, 2017–2025

**Running title:** What a TB budget cannot see

**Author:** Siddalingaiah H S
Department of Community Medicine, Shridevi Institute of Medical Sciences and Research Hospital, Tumkur – 572106, Karnataka, India.
Correspondence: hssling@yahoo.com · ORCID 0000-0002-4771-8285

**Target journal:** *Health Policy and Planning* (Original Article). Verified against the journal's author guidelines, 13 November 2026: abstract maximum **300** words, main text maximum **6,000** for a quantitative or fixed-design study, Key Messages **3-4** bullets, **author-date (Harvard)** referencing, and **double-anonymized** peer review, so the blinded copy is the one to upload.

---

## Abstract

**Background.** WHO's tuberculosis (TB) funding gap — budget required minus funding expected — is published annually for high-burden countries and read as a measure of under-resourcing. Whether it does so for any given country is unexamined.

**Methods.** We compared WHO's reported TB budget and expenditure data for 215 countries (2017–2025) with India's national programme accounts, using dimensionless internal ratios (no currency conversion), and mapped eleven TB interventions onto WHO budget lines by definition, not name.

**Results.** India reported expected funding exactly equal to budget required in all eight years 2018–2025: its WHO funding gap is zero **by construction**, not by observation. Fourteen of the 106 countries with five or more years report this way; 44 report a non-zero gap every year. India's own accounts record ₹18,388 crore approved against ₹23,169 crore requested (shortfall 5.4–46.1% by year). The two sources agree on execution (72% and 82% of budget spent) and on Global Fund support falling from 37% of expenditure to 1%. **Six of the eleven interventions have no budget line**; three more map only to drugs-only lines, leaving delivery costs unattributable.

**Conclusions.** A budget records what a programme buys, not what it does. Commodities have line items; services largely do not, so spending on an intervention without a line cannot be identified. For India, the indicator meant to signal shortfall structurally cannot. Neither finding concerns how much TB control receives, and both are correctable: publish unmet need as its own field, and tag expenditure to interventions rather than commodity classes.

**Keywords:** Antitubercular Agents; Costs and Cost Analysis; Financing, Government; Health Expenditures; Health Priorities; Healthcare Financing; India; Program Evaluation; Tuberculosis

## Key messages

- WHO's tuberculosis funding gap is read as a measure of under-resourcing, but India reported expected funding exactly equal to budget required in all eight years from 2018 to 2025, so its published gap is zero by construction rather than by observation.
- Fourteen of the 106 countries with five or more years of data report the same way, while India's own national accounts record an annual shortfall of 5.4% to 46.1% between funds requested and approved, which the indicator cannot show.
- Six of eleven tuberculosis interventions have no budget line and three more map only to drugs-only lines, so spending on them cannot be identified in the published record. Both problems are correctable without new money: publish unmet need as a field in its own right, and tag expenditure to interventions rather than to commodity classes.

---

## 1. Introduction

Tuberculosis control is planned against money. National strategic plans cost their activities, and the Global TB Report (WHO 2025) publishes, for every high-burden country, the budget required for the coming year and the funding expected against it. The difference between those two quantities — the **funding gap** — is read as a measure of under-resourcing. Funding-need figures of this kind are used in TB investment cases and advocacy (Reid et al. 2019), and the gap is shown in the Report's country comparisons (WHO 2025).

We should be precise about what the indicator is and is not used for, because our argument does not depend on overstating it. The Global Fund's published allocation methodology takes disease burden and economic capacity as the inputs to its allocation formula, followed by a qualitative adjustment (Global Fund 2024); it does **not** list the WHO reported funding gap among them. The gap's influence is of a different kind — it is the figure published, quoted and compared when a programme's resourcing is discussed. An indicator need not enter a formula to shape a judgement.

An indicator used that way carries an implicit claim: that the two numbers behind it are independently determined, so their difference is informative. This paper asks whether that claim holds, and finds that for India it does not. To our knowledge, no study has examined the validity of the WHO funding-gap indicator, or the cross-country comparability of health-financing indicators of this kind.

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

Eleven tuberculosis interventions were mapped onto WHO budget line items by definition. Their ranking, and the definitions of the interventions themselves, are taken as given from a separate manuscript under review (Siddalingaiah 2026a), in which they are ordered by a priority score built from the favourability of coded literature, not from a formal evidence synthesis. The mapping to budget lines does not depend on that ranking (§5). Each mapping was classified as **full** (the line covers the intervention), **partial** (the line covers part of it), or **absent** (no line exists). Mapping is declared data and is published with the code.

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

### 3.5 Six of eleven interventions have no budget line at all

**Table 2. Interventions, in the rank order of a literature-favourability score from a manuscript under review (Siddalingaiah 2026a), against the budget classification.**

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

*Ranking and intervention definitions are taken as given from Siddalingaiah (2026a, under review) and were not re-derived here. The rank is a priority-action score built from vocabulary-coded abstracts, without human validation, and its order changes with the coding rule; it is not a formal evidence ranking.*

**Six of eleven interventions are fiscally untraceable, and only two map fully.** This count does not depend on the ranking. As a secondary observation, three of the six (ranks 2, 4 and 5) fall in the top five of the literature-favourability score in Siddalingaiah (2026a); because that score is not human-validated and its order is sensitive to its coding rule, we report this as descriptive and do not rest an argument on it.

The pattern is not about priority. It is about **procurement**. Every full or partial mapping corresponds to something a programme *buys*: drugs (`budget_tpt`, `budget_sld`), laboratory equipment and supplies (`budget_lab`), cash transfers to patients (`budget_patsup`). Every absent mapping corresponds to something a programme *does*: ventilation and triage in facilities, finding cases actively, engaging private providers, working across the animal-human interface.

Even where a line exists, the same division operates within it. `budget_tpt` is defined as *"TB preventive treatment: **drugs**"*. The drugs for preventive therapy are traceable; the contact tracing, counselling and adherence support that deliver them are not. The same holds for the shorter-regimen rollout, whose drug cost is in `budget_sld` while its programme cost sits in `budget_mdrmgt`, which maps to no intervention at all.

---

## 4. Discussion

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

The same structural absence was found in a separate analysis, by the same author, of India's National AIDS and STD Control Programme (Siddalingaiah 2026b), where sexually transmitted infection services, pre-exposure prophylaxis and surveillance likewise had no traceable line item while blood transfusion services — a commodity-intensive activity — were separately disaggregated.

Two programmes, two ministry demands, two disease areas, the same division between what is bought and what is done. That makes fiscal invisibility a candidate structural property of disease-control financing rather than an artefact of one programme's accounts.

### 4.4 What would fix it

Both findings have concrete, low-cost remedies.

**Publish unmet need as its own field.** WHO's reporting form could ask for budget required, funding expected **and** a separate statement of whether expected funding reflects need or availability. One additional field would make the existing indicator interpretable and would distinguish the 14 countries from the 44. Modelled estimates of resource need for health systems generally (Stenberg et al. 2017) and of TB spending by source and function (Su et al. 2020) exist, but they are external reconstructions; they do not replace the reporting form stating the distinction itself.

**Tag expenditure to interventions, not only to commodity classes.** A programme that reports what it spent on active case finding, infection control and private-sector engagement — even approximately, even as a share — becomes auditable on those activities. Without such tagging, no quantity of analysis can recover what was spent on them.

**Publish the reconciliation.** Where a national table reports releases and expenditure that cannot be reconciled on the page, a single footnote naming the mechanism would convert an apparent inconsistency into interpretable information.

---

## 5. Limitations

This is a secondary analysis of reported data; we observe reporting behaviour, not financial reality. That a country reports expected funding equal to budget required does not establish that it faces no shortfall, only that the indicator cannot show one.

The intervention-to-budget-line mapping reflects analytic judgement, albeit judgement anchored to published definitions rather than to names. Readers who disagree with a specific mapping can recompute from the published file.

The ranking used to order the eleven interventions is external to this analysis and is not defended here (Siddalingaiah 2026a). It comes from a manuscript under review, rests on the favourability of coded literature rather than a formal evidence synthesis, and that manuscript reports that its rank order is sensitive to the coding rule used. The count of interventions with no budget line does not depend on the ranking being correct, only on the interventions being plausible candidates; the statement that three of the top five are among them does depend on it, and is descriptive only for that reason.

The national accounts cover 2017-18 to 2023-24 while the WHO budget data cover 2018–2025, so the overlapping window for direct comparison is six years.

Finally, WHO's reported figures are revised as countries submit corrections, so the dataset version is stated with the download date and is archived with the code.

---

## 6. Conclusions

A budget records what a programme buys, not what it does. In India's tuberculosis response, that distinction leaves six of eleven interventions without any line item (three of them among the top five on a literature-favourability score whose order is coding-rule sensitive), and leaves the delivery cost of three more pooled into categories from which it cannot be recovered.

Meanwhile the international indicator intended to signal resource shortfall reports zero for India in every year, because the two quantities behind it are not independently determined — while the national accounts, over the same years, record that a fifth of the requested budget was never approved and a third of it was never spent.

Neither finding is about how much money tuberculosis control receives. Both are about what the financial record is capable of showing. Measurement conventions decided upstream of any policy choice determine which interventions can be defended at budget time and which countries appear to need help. Correcting them is cheaper than any of the interventions they obscure.

---

## References

Bertone MP, Barroy H, Sparkes S et al. 2026. Political economy of budgeting reforms: a comparative analysis of the adoption and implementation of programme-based budgeting in health across seven LMIC countries. *The International Journal of Health Planning and Management*, published online 29 September 2026. doi: 10.1002/hpm.70142

Central TB Division, Ministry of Health and Family Welfare, Government of India. 2024. *India TB Report 2024: National TB Elimination Programme Annual Report*. New Delhi: Ministry of Health and Family Welfare.

Floyd K, Fitzpatrick C, Pantoja A et al. 2013. Domestic and donor financing for tuberculosis care and control in low-income and middle-income countries: an analysis of trends, 2002-11, and requirements to meet 2015 targets. *The Lancet Global Health* **1**: e105-15.

Global Fund to Fight AIDS, Tuberculosis and Malaria. 2024. *Allocation Methodology for Grant Cycle 8 (2026-2028 Allocation Period)*. Board paper GF/B52/08B, 52nd Board Meeting, 20-22 November 2024. Geneva: The Global Fund. https://archive.theglobalfund.org/media/15310/archive_bm52-08b-allocation-methodology-gc8_report_en.pdf, accessed 13 November 2026.

Peng RD. 2011. Reproducible research in computational science. *Science* **334**: 1226-7.

Piatti-Funfkirchen M, Barroy H, Pivodic F et al. 2021. *Budget Execution in Health*. Washington, DC: World Bank. doi: 10.1596/36583

Reid MJA, Arinaminpathy N, Bloom A et al. 2019. Building a tuberculosis-free world: the Lancet Commission on tuberculosis. *The Lancet* **393**: 1331-84.

Resch S, Ryckman T, Hecht R. 2015. Funding AIDS programmes in the era of shared responsibility: an analysis of domestic spending in 12 low-income and middle-income countries. *The Lancet Global Health* **3**: e52-61.

Siddalingaiah HS. 2026a. Drug-resistant tuberculosis in India, 2017-2024: improving outcomes, no worsening axis, and a caution for NTEP trend analysis. Manuscript IJTB-S-26-01305, submitted to the *Indian Journal of Tuberculosis*, 13 November 2026. Under review.

Siddalingaiah HS. 2026b. India's human immunodeficiency virus and sexually transmitted infection response at the close of NACP-V: an evidence-practice gap analysis and a priority agenda for clinical sexually transmitted infection services. *Journal of Skin and Sexually Transmitted Diseases*, in production; volume and pages not yet assigned. doi: 10.25259/JSSTD_120_2026

Stenberg K, Hanssen O, Edejer TT et al. 2017. Financing transformative health systems towards achievement of the health Sustainable Development Goals: a model for projected resource needs in 67 low-income and middle-income countries. *The Lancet Global Health* **5**: e875-87.

Su Y, Garcia Baena I, Harle AC et al. 2020. Tracking total spending on tuberculosis by source and function in 135 low-income and middle-income countries, 2000-17: a financial modelling study. *The Lancet Infectious Diseases* **20**: 929-42.

Tandon A, Cashin C. 2010. *Assessing Public Expenditure on Health from a Fiscal Space Perspective*. Health, Nutrition and Population Discussion Paper. Washington, DC: World Bank. doi: 10.1596/13613

World Health Organization (WHO). 2025. *Global Tuberculosis Report 2025*. Geneva: World Health Organization.

World Health Organization (WHO). 2026a. Global Tuberculosis Programme country data: TB budget, and TB expenditure and utilisation datasets. Geneva: World Health Organization. https://extranet.who.int/tme/, data files dated 25 August and 12 November 2026. This data-collection system no longer accepts updates; the archived input files are deposited with the analysis code.

World Health Organization (WHO). 2026b. Global Tuberculosis Programme data dictionary (file TB_dictionary_2026-08-25.csv). Geneva: World Health Organization. Archived with the analysis code.

---

## Declarations

**Contributors.** Sole author. Conceived the study, assembled and verified the data, wrote the analysis code, performed all analyses and wrote the manuscript. Meets ICMJE authorship criteria and is responsible for the integrity of the work as a whole.

**Funding.** None.

**Competing interests.** None declared.

**Ethical clearance.** Not required (see Methods 2.5).

**Data availability.** All inputs are publicly available: WHO TB budget and expenditure datasets, and the India TB Report 2024. Analysis code, the archived input files, the intervention-to-budget-line mapping with its definitional basis, and the verification suite are deposited at https://github.com/hssling/provenance-weighted-priority-setting and archived at Zenodo, doi:10.5281/zenodo.24187367 (release v1.0.0; the concept DOI doi:10.5281/zenodo.24187366 always resolves to the latest version).

**Use of generative artificial intelligence.** The author used a large language model as a drafting and analysis assistant. All analytical decisions, data verification and conclusions are the author's. The author reviewed and edited all content and takes full responsibility for it.

---

## Notes for the author — not for submission

**Before submitting:**
1. [done 13 Nov 2026] Repository public, Zenodo v1.0.0 minted: version DOI 10.5281/zenodo.24187367, concept DOI 10.5281/zenodo.24187366, both inserted in SS2.4 and Data availability.
2. [done 13 Nov 2026] Target journal: *Health Policy and Planning*. Abstract cut to 249 words against its 250 limit, so there is no margin if that limit has moved. Key messages box added (three bullets, house style confirmed against published HPP articles). The journal's guideline page is bot-protected and was not read; confirm the limits in a browser.
3. **References placed (16, Vancouver, numbered by first appearance).** (a) [done] SS1 Global Fund statement cites ref 16 (Board paper GF/B52/08B, read in full; the formula inputs are burden and economic capacity, and the paper does not name the WHO funding gap; it does say technical partners gave input on funding needs, so keep the wording at 'does not list ... among them'). (b) [done 13 Nov 2026] JSSTD ref 13 now carries the DOI printed on the journal's R14 proof, 10.25259/JSSTD_120_2026. It returns 404 today because the article is in production and the DOI is registered at publication; that is expected and is stated in the reference. Add volume and pages when the issue is released. (c) [done] Bertone 2026 cited as '2026 Sep 29 [online ahead of print]'; Crossref, PubMed and OpenAlex all carry null volume and pages, so this will not need revisiting. (d) OPEN: whether *Health Policy and Planning* accepts an under-review citation (ref 6) for Table 2 -- if not, give the ranking its own methods paragraph. (e) [done 13 Nov 2026] Reid 2019 (ref 2) and Su 2020 (ref 15) read in full text; both support the sentences citing them.
4. [done 13 Nov 2026] Self-similarity run with `verification/check_self_similarity.py`, which now includes the JSSTD paper. SS4.3 replicates its finding in a second programme and was the likeliest source of overlap; the measured share is **0.0%**, so the relationship is conceptual and the citation carries it. Paper B 0.6%, TB-BOPAS 0.3%, IJTB review 0.2%, combined 0.9%, no verbatim run over 40 words.
5. OPEN: consider whether Table 2's ranking needs its own methods paragraph or can be cited.

**Deliberately excluded from this draft:** the provenance-weighting instrument, the five tests, the composite, EVPR, and the BOPAS propagation. None of it is needed for these findings, and the instrument's central claim — that provenance weighting reorders priorities — is not yet supported. Keeping it out makes this paper defensible now and leaves the methods paper intact for when D2/D3 exist.
