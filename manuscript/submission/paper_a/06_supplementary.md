# Supplementary material (for online publication only)

**What a tuberculosis budget cannot see: fiscal invisibility and the limits of the WHO funding-gap indicator in India, 2017-2025**

Every table in this file is generated from the archived input files and the deposited code by `manuscript/make_supplementary_a.py`; none is hand-entered. Section numbers refer to the main text.

---

## S1. The intervention-to-budget-line mapping, with both WHO definitions

Table 2 of the main text classifies each intervention. This table gives the evidence: the WHO budget column each intervention maps to, the definition of that column in the **data dictionary** distributed with the datasets, and the definition of the same column in the **data collection form** that countries complete (WHO 2026c). Where the two differ, the form governs (§2.3), and §4.2 reports the consequence of that choice.

| Rank | Intervention | Column | Coverage | Dictionary definition | Collection-form definition |
|---:|---|---|---|---|---|
| 1 | Molecular diagnostic scale-up (Xpert MTB/RIF, Xpert MTB/XDR) | `budget_lab` | dominant | Budget required for laboratory infrastructure, equipment and supplies (US Dollars) | Building, maintaining, and renovating TB laboratories, laboratory equipment purchase and maintenance, consumables for all tests (including TB screening for people living with HIV/AIDS and diagnosis of latent TB infection), quality assurance, retooling and the transportation of specimens. |
| 2 | Airborne infection prevention and control | `budget_prog` | pooled | Budget required for programme costs to treat drug-susceptible TB (US Dollars) | The management and supervision of the TB control programme, training, policy development, meetings, visits for supervision, purchase of office equipment/vehicles, construction of buildings for use by programme staff, routine surveillance, advocacy and communication, public-private mix activities, community engagement, active case-finding, infection control, management of TB drug procurement and distribution, and programme activities linked to contact investigation for TB preventive treatment |
| 3 | TB preventive therapy | `budget_tpt` | commodity only | Budget required for TB preventive treatment: drugs (US Dollars) | Drugs for TB preventive treatment, as per latest WHO guidance (6H, 9H, 4R, 3HR and Levofloxacin) |
| 4 | Whole-genome sequencing for drug-susceptibility prediction | `budget_lab` | dominant | Budget required for laboratory infrastructure, equipment and supplies (US Dollars) | Building, maintaining, and renovating TB laboratories, laboratory equipment purchase and maintenance, consumables for all tests (including TB screening for people living with HIV/AIDS and diagnosis of latent TB infection), quality assurance, retooling and the transportation of specimens. |
| 5 | Active case finding | `budget_prog` | pooled | Budget required for programme costs to treat drug-susceptible TB (US Dollars) | The management and supervision of the TB control programme, training, policy development, meetings, visits for supervision, purchase of office equipment/vehicles, construction of buildings for use by programme staff, routine surveillance, advocacy and communication, public-private mix activities, community engagement, active case-finding, infection control, management of TB drug procurement and distribution, and programme activities linked to contact investigation for TB preventive treatment |
| 6 | Shorter all-oral regimen rollout (BPaL/BPaL-M) | `budget_sld` | commodity only | Budget required for drugs to treat drug-resistant TB (US Dollars) | Drugs to treat drug-resistant TB (RR-TB, MDR-TB, pre-XDR-TB or XDR-TB). Include drugs to deal with adverse event |
| 7 | Bovine tuberculosis control | — | no line | — | — |
| 8 | Private-sector engagement | `budget_prog` | pooled | Budget required for programme costs to treat drug-susceptible TB (US Dollars) | The management and supervision of the TB control programme, training, policy development, meetings, visits for supervision, purchase of office equipment/vehicles, construction of buildings for use by programme staff, routine surveillance, advocacy and communication, public-private mix activities, community engagement, active case-finding, infection control, management of TB drug procurement and distribution, and programme activities linked to contact investigation for TB preventive treatment |
| 9 | Nutritional support | `budget_patsup` | dominant | Budget required for patient support (US Dollars) | Cash transfers, food packages, transportation vouchers, educational and emotional support to patient or other in-kind benefits given to TB patients, mobile phone (airtime or device for V.O.T), medications monitors (digital box, 99 DOTS) |
| 10 | Milk pasteurisation / dairy food chain | — | no line | — | — |
| 11 | Integrated TB-HIV-diabetes care | `budget_tbhiv` | commodity only | Budget required for collaborative TB/HIV activities (US Dollars) | Collaboration between TB and HIV programmes aimed at reducing the impact of HIV-related TB. |

Notes on the pooled and commodity-only conditions, verbatim from the code:

- **Airborne infection prevention and control** — budget_prog names 'infection control' among fourteen activities pooled in one figure, from staff supervision to drug procurement management.
- **Active case finding** — budget_prog names 'active case-finding' among fourteen pooled activities.
- **Private-sector engagement** — budget_prog names 'public-private mix activities' among fourteen pooled activities.
- **TB preventive therapy** — budget_tpt covers TB preventive treatment drugs only. Delivery, contact tracing and adherence support are not covered; the form puts contact investigation in budget_prog, pooled.
- **Shorter all-oral regimen rollout (BPaL/BPaL-M)** — budget_sld covers drugs to treat drug-resistant TB only. Rollout programme work is not covered; DR-TB programme costs sit in budget_mdrmgt, which no node maps to.
- **Integrated TB-HIV-diabetes care** — budget_tbhiv covers collaborative TB/HIV activities. The diabetes arm is not covered.

---

## S2. India's national programme accounts, year by year

The series behind Figure 1, as published in the India TB Report 2024, Table 16.1 (p.174). Amounts are in INR crore. The shortfall column is (requested - approved) / requested. Two cells of the source table were damaged by OCR and are restored digit-faithfully; see §2.1.

| Fiscal year | Requested | Approved | Released | Spent | Shortfall |
|---|---:|---:|---:|---:|---:|
| 2017 | 2,200.00 | 1,840.00 | 871.36 | 2,759.44 | 16.4% |
| 2018 | 4,115.00 | 3,140.00 | 907.65 | 2,237.79 | 23.7% |
| 2019 | 3,525.00 | 3,333.21 | 870.81 | 3,130.11 | 5.4% |
| 2020 | 3,554.00 | 3,109.93 | 629.71 | 3,097.98 | 12.5% |
| 2021 | 3,628.85 | 3,409.94 | 545.78 | 2,086.82 | 6.0% |
| 2022 | 3,088.87 | 1,666.33 | not published | 910.83 | 46.1% |
| 2023 | 3,057.42 | 1,888.82 | not published | 840.49 | 38.2% |
| **Total** | **23,169.14** | **18,388.23** | **3,825.31** | **15,063.46** | **20.6%** |

---

## S3. How countries report the two fields

Of the **106** countries with five or more years of both `budget_tot` and `cf_tot`, **14** report expected funding exactly equal to budget required in every year, so their published funding gap is zero by construction; **44** report a non-zero gap in every year. The remainder do both at different times.

**Always equal (14):** ARG, BGR, BIH, BOL, CPV, FSM, IND, LBY, MEX, MYS, RUS, SLB, SLV, TLS.

**Never equal (44):** BDI, BEN, BGD, BTN, BWA, CAF, CHN, CIV, COD, DOM, ETH, GEO, GHA, GNB, GUY, HTI, IDN, IRQ, JOR, KEN, KHM, LBN, LSO, MMR, MWI, NAM, NGA, PER, PHL, PNG, PRK, PRY, SEN, SLE, SUR, TCD, TJK, TZA, UGA, VEN, VNM, YEM, ZMB, ZWE.

