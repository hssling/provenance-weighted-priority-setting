# RECORD checklist

**Manuscript.** What a tuberculosis budget cannot see: fiscal invisibility and the limits of the WHO funding-gap indicator in India, 2017–2025.

**Guideline.** Benchimol EI, Smeeth L, Guttmann A, Harron K, Moher D, Petersen I, Sørensen HT, von Elm E, Langan SM; RECORD Working Committee. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) Statement. *PLOS Medicine* 2015;**12**(10):e1001885. doi: 10.1371/journal.pmed.1001885

The *Indian Journal of Tuberculosis* names no reporting guideline for this design. This study analyses routinely collected programme data, so RECORD, the EQUATOR guideline for such data, is the closest fit and is completed here. Item text is **paraphrased** for brevity; the authoritative wording is in the statement above.

**A note on fit.** RECORD and STROBE assume a study estimating an association between an exposure and an outcome in people. This study has no participants, no exposure and no outcome: the units of analysis are **country-year financial records and budget line items**, and the quantities reported are accounting relationships within and between two published sources. Items presupposing person-level analysis are marked *Not applicable* with the reason stated. The items that carry RECORD's purpose — provenance of the data, cleaning, access, and availability of code — apply in full.

| Item | Paraphrased requirement | Response | Location |
|---|---|---|---|
| **STROBE 1a / RECORD 1.1** | Indicate design and type of data in title or abstract; name the databases | Abstract names WHO's reported TB budget and expenditure data and India's national programme accounts | Title; Abstract |
| **RECORD 1.2** | Report geographic region and timeframe in title or abstract | Title and abstract: India, 2017–2025; 215 countries for the comparison | Title; Abstract |
| **RECORD 1.3** | State if databases were linked | The two sources are **compared, not linked**: no record-level join is performed, and comparison is through dimensionless internal ratios | Abstract; §2.2 |
| **STROBE 1b** | Structured abstract | Four sections (Background/Objectives, Methods, Results, Conclusions) within the journal's 250-word limit | Abstract |
| **STROBE 2** | Background and rationale | §1 | §1 |
| **STROBE 3** | Objectives, including prespecified hypotheses | §1, final paragraph: three questions, with what is new stated in the preceding paragraph | §1 |
| **STROBE 4** | Study design | Cross-source comparison of two independently produced financial records, plus a definitional mapping of interventions to budget lines | §2.2, §2.3 |
| **STROBE 5** | Setting, locations, periods | §2.1 | §2.1 |
| **STROBE 6a / RECORD 6.1** | Eligibility criteria and selection methods | All 215 countries in the WHO budget file; the 106-country subset with five or more years is defined where used | §2.1, §3.1 |
| **RECORD 6.2** | Reference any validation of codes or algorithms used for selection | **Not applicable.** No codes or algorithms select a study population; all reported country-years are used | §2.1 |
| **RECORD 6.3** | If validation was done for this study, give methods and results | The two sources are used to validate each other on execution, agreeing in direction while disagreeing on need; both results are reported rather than one being preferred | §3.3 |
| **RECORD 6.4** | Consider a flow diagram for linkage | No linkage. A diagram is provided for the intervention-to-budget-line mapping, which is the study's one classification step | Figure 2 |
| **STROBE 7 / RECORD 7.1** | Define all variables; give the complete list of codes used | Every WHO budget column used is named, and both WHO definitions of each are quoted verbatim; the full mapping is declared data, published with the code | §2.3, Table 2; Supplementary S1 |
| **STROBE 8** | Data sources and measurement | §2.1; all input files archived and hashed, including the data collection form that governs the definitions | §2.1; `data/raw_file_manifest.csv` |
| **STROBE 9** | Bias | The classification depends on which WHO document defines a budget line; both are reported and the size of the difference is quantified | §3.5; Supplementary S1 |
| **STROBE 10** | Study size | 215 countries, 2017–2025; the whole reported population, not a sample | §2.1 |
| **STROBE 11** | Quantitative variables handling | Comparison uses dimensionless internal ratios, so no currency conversion or deflation is applied; the reason is stated | §2.2 |
| **STROBE 12a–e** | Statistical methods, subgroups, missing data, sensitivity | Descriptive accounting comparison; no model is fitted and no p-value is reported. Two cells damaged in text extraction from the national table are reported, with their restoration against the printed page | §2.2; Supplementary S3 |
| **RECORD 12.1** | Extent of access to the database population | Complete. Both sources are public and are archived with the analysis | §2.4; Data availability |
| **RECORD 12.2** | Describe data cleaning | **None, with one documented exception.** Values are used as published; two cells damaged in text extraction from the India TB Report were restored digit by digit against the printed page and confirmed against the published column totals | Supplementary S3 |
| **RECORD 12.3** | Linkage and linkage quality | **Not applicable.** No linkage | §2.2 |
| **STROBE 13 / RECORD 13.1** | Selection, including filtering on data quality and availability | Country-years, not persons. Where a subset is used (106 countries with ≥5 years) the rule and the count are stated | §3.1 |
| **STROBE 14** | Descriptive data | Tables 1–2, Figures 1–2 | §3 |
| **STROBE 15** | Outcome data | **Not applicable.** No outcome events | — |
| **STROBE 16** | Main results with estimates and precision | Reported gap, national shortfall by year, execution ratios, financing shares and the coverage classification; no confidence intervals, as these are accounting totals rather than estimates from a sample | §3.1–§3.5 |
| **STROBE 17** | Other analyses | Cross-country distribution of the reporting pattern; classification under the alternative WHO definition; the same pattern in a second national programme | §3.1, §3.5, §4.1 |
| **STROBE 18** | Key results | §6 | §6 |
| **STROBE 19 / RECORD 19.1** | Limitations, including implications of using data not created for this question | These data were created for programme monitoring and global reporting, not to support validity assessment of the indicator derived from them; what the analysis cannot establish is stated explicitly | §5 |
| **STROBE 20** | Interpretation | §4 | §4 |
| **STROBE 21** | Generalisability | One country in depth, with the cross-country frequency of the same reporting pattern reported so the reader can judge reach | §3.1, §5 |
| **STROBE 22** | Funding | None | Funding |
| **RECORD 22.1** | How to access protocol, raw data and code | All public: archived inputs, analysis code, intervention mapping and verification suite, deposited with a DOI | Data availability |
