# RECORD checklist

**Manuscript.** Restated, never revised: a vintage analysis of WHO tuberculosis data and the spending estimate built on them.

**Guideline.** Benchimol EI, Smeeth L, Guttmann A, Harron K, Moher D, Petersen I, Sørensen HT, von Elm E, Langan SM; RECORD Working Committee. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) Statement. *PLOS Medicine* 2015;**12**(10):e1001885. doi: 10.1371/journal.pmed.1001885

The *International Journal of Epidemiology* requires RECORD for studies using routinely collected health data. Item text below is **paraphrased** for brevity; the authoritative wording is in the statement above and at the EQUATOR Network.

**A note on fit.** RECORD and STROBE are written for studies estimating associations between exposures and outcomes in people. This study has no participants, exposure or outcome: the units are **country-year values of published variables**, compared across dated releases, and the quantities estimated are rates of revision, restatement and imputation and the share of a published estimate resting on each. Items presupposing person-level analysis are marked *Not applicable* with the reason given. Items on data provenance, cleaning, linkage, access and code apply in full and are the subject of the paper.

| Item | Paraphrased requirement | Response | Location |
|---|---|---|---|
| **STROBE 1a / RECORD 1.1** | Indicate the design and the type of data in the title or abstract; name the databases | Title and abstract name the design (vintage analysis) and WHO's archived TB finance and utilisation releases | Title; Abstract |
| **RECORD 1.2** | Report geographic region and timeframe in title or abstract | Low- and middle-income countries in WHO's estimate; releases 2024-2026; reporting years 2018-2025 | Abstract; §2.1 |
| **RECORD 1.3** | State in title or abstract if databases were linked | Releases are compared on country and year, not linked at record level; the method is stated in the abstract | Abstract; §2.2 |
| **STROBE 1b** | Structured abstract | Four sections within the journal's 250-word limit | Abstract |
| **STROBE 2** | Background and rationale | §1 | §1 |
| **STROBE 3** | Objectives | Four questions, §1, final paragraph | §1 |
| **STROBE 4** | Study design | Comparison of dated releases of the same published data, and decomposition of a published estimate by the provenance of its inputs | §2.2; Figure 1 |
| **STROBE 5** | Setting, locations, periods | Three releases, their dates and the reporting years compared | §2.1; Supplementary Note 1 |
| **STROBE 6a / RECORD 6.1** | Eligibility criteria and selection methods | All country-years in each release; reporting years from 2018, the first every release can classify; WHO's own country inclusion for the funding estimate | §2.2 |
| **RECORD 6.2** | Reference any validation of the codes or algorithms used for selection | No selection algorithm beyond WHO's own country inclusion, which is used as published | §2.2 |
| **RECORD 6.3** | If validation was done for this study, give methods and results | The reconstruction is validated against WHO's three published funding totals and reproduces each | §2.2; Table 4 |
| **RECORD 6.4** | Consider a flow diagram | Figure 1 traces a country's return to WHO's published total | Figure 1 |
| **STROBE 7 / RECORD 7.1** | Define all variables; give the complete list of codes and algorithms | Revision, restatement and WHO-supplied values are defined in §2.2; WHO's fill rule and zeroing are documented from its code | §2.2; Supplementary Note 2 |
| **STROBE 8** | Data sources and measurement | Every file is identified by repository, commit and SHA-256 digest | §2.1; Supplementary Note 1 |
| **STROBE 9** | Bias | Restatement is distinguished from error; the classification of cost components is tested by a sensitivity analysis; the screen's failure modes are reported | §5; Table 4; Supplementary Notes 4–5 |
| **STROBE 10** | Study size | All values in each release; counts are given in every table | Tables 1–4 |
| **STROBE 11** | Quantitative variables handling | Values are compared exactly as published; no transformation | §2.2 |
| **STROBE 12a–e** | Statistical methods, subgroups, missing data, sensitivity | Descriptive. Missing values are a finding, classified by how WHO fills them; the sensitivity analysis counts a component current if any input was newly reported; the 2025 report is analysed as a replication | §2.2; Table 3; Supplementary Note 2 |
| **RECORD 12.1** | Describe the extent of access to the database population | Complete: all files are public, and the archived releases are fetched from pinned commits | §2.1; Data availability |
| **RECORD 12.2** | Describe data cleaning | **None was performed.** The study measures WHO's own cleaning and imputation instead | §2.2; Supplementary Note 2 |
| **RECORD 12.3** | State whether data were linked and how linkage quality was assessed | Releases are matched on country code and year; the reconstruction's agreement with WHO's published totals is the check | §2.2 |
| **STROBE 13 / RECORD 13.1** | Selection, including filtering on data quality and availability | Country-years, not participants; the reporting-year window and its reason are stated | §2.2 |
| **STROBE 14** | Descriptive data | Tables 1–3 | §3.1–§3.3 |
| **STROBE 15** | Outcome data | **Not applicable.** No outcome events | — |
| **STROBE 16** | Main results with estimates and precision | Counts and shares of the whole population of values; no sampling, so no confidence intervals | Tables 1–4; Figure 2 |
| **STROBE 17** | Other analyses | Sensitivity analysis; replication on the 2025 report; screen of 443 variables against the dictionary's labels | Table 4; Table 5; Supplementary Note 2 |
| **STROBE 18** | Key results | §4.1 | §4.1 |
| **STROBE 19 / RECORD 19.1** | Limitations, including implications of using data not created for this question | The data were created for programme monitoring and global reporting, not to document vintage, which is the gap the paper describes | §5; Supplementary Note 5 |
| **STROBE 20** | Interpretation | §4 | §4 |
| **STROBE 21** | Generalisability | One programme's finance data, three releases; other WHO programmes untested | §5 |
| **STROBE 22** | Funding | None | Declarations |
| **RECORD 22.1** | State how to access the protocol, raw data and code | Public datasets and code are deposited with a DOI; WHO's repository files are fetched and verified by script | Declarations, data availability |
