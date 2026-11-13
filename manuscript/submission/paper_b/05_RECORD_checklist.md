# RECORD checklist

**Manuscript.** The label says what kind, not how old: a reproducible screen of 443 variables in six WHO tuberculosis datasets.

**Guideline.** Benchimol EI, Smeeth L, Guttmann A, Harron K, Moher D, Petersen I, Sørensen HT, von Elm E, Langan SM; RECORD Working Committee. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) Statement. *PLOS Medicine* 2015;**12**(10):e1001885. doi: 10.1371/journal.pmed.1001885

The *International Journal of Epidemiology* requires RECORD for studies using routinely collected health data. Item text below is **paraphrased** for brevity; the authoritative wording is in the statement above and at the EQUATOR Network.

**A note on fit.** RECORD and STROBE are written for studies that use routinely collected data to estimate associations between exposures and outcomes in people. This study has no participants, no exposure, no outcome and no effect estimate: the units of analysis are **variables in published country-year tables**, and the quantity estimated is how often each variable's values repeat. Items that presuppose person-level analysis are therefore marked *Not applicable*, with the reason given rather than left blank. Items about data provenance, cleaning, access and code — the heart of RECORD — apply in full and are the subject of the paper.

| Item | Paraphrased requirement | Response | Location |
|---|---|---|---|
| **STROBE 1a / RECORD 1.1** | Indicate the design and the type of data in the title or abstract; name the databases | Title names the datasets screened; abstract names all six WHO datasets and the record count | Title; Abstract, Methods |
| **RECORD 1.2** | Report geographic region and timeframe in title or abstract | Abstract: 217 countries and areas, reporting years 1980 to 2026, 25,181 country-year records | Abstract, Methods |
| **RECORD 1.3** | State in title or abstract if databases were linked | **Not applicable.** No linkage was performed. The six files are screened independently; none is joined to another | §2.1 |
| **STROBE 1b** | Structured abstract | Four sections, 250 words, as the journal specifies | Abstract |
| **STROBE 2** | Background and rationale | §1 | §1 |
| **STROBE 3** | Objectives | §1, final paragraph | §1 |
| **STROBE 4** | Study design | Cross-sectional screen of every numeric variable in six published datasets | §2.2, Figure 1 |
| **STROBE 5** | Setting, locations, periods | §2.1 and Supplementary S0 give each file's rows, years and columns | §2.1; Supplementary S0 |
| **STROBE 6a / RECORD 6.1** | Eligibility criteria and selection methods | Every numeric variable with ≥100 non-missing values; the two rules that set variables aside (S0, S0b) are stated with their counts | §2.2; Figure 1 |
| **RECORD 6.2** | Reference any validation of the codes or algorithms used for selection | **None exists.** We know of no published validation of these screens for country-reported programme data, and we say so rather than implying one | §2.2; §5 |
| **RECORD 6.3** | If validation was done for this study, give methods and results | The screen's verdicts are compared against WHO's own dictionary labels as an external standard (§3.5); agreement is reported with its chance probability | §3.5 |
| **RECORD 6.4** | Consider a flow diagram for the data linkage process | No linkage; a flow diagram is nonetheless provided for variable selection and classification | Figure 1 |
| **STROBE 7 / RECORD 7.1** | Define all variables; give the complete list of codes and algorithms | Every screen is defined in §2.2 and specified in full in Supplementary S1; the code that computes them is deposited, and the per-variable results table is published | §2.2; Supplementary S1; data availability |
| **STROBE 8** | Data sources and measurement | §2.1; all six input files are archived and hashed | §2.1; `data/raw_file_manifest.csv` |
| **STROBE 9** | Bias | Two failure modes of the method itself are demonstrated on these data and reported, not removed | §5; Supplementary S1c, S2 |
| **STROBE 10** | Study size | 443 variables, 25,181 country-year records; no sample-size calculation applies as the entire population of variables is screened | Abstract; §2.1 |
| **STROBE 11** | Quantitative variables handling | Thresholds for every screen were fixed before results were examined and are stated in the code | §2.2; Supplementary S1 |
| **STROBE 12a–e** | Statistical methods, subgroups, missing data, loss to follow-up, sensitivity | Descriptive throughout; missing values are excluded per variable; the zero-exclusion sensitivity and the S0b sensitivity are both reported | §3.1, Table 2; Supplementary S1a |
| **RECORD 12.1** | Describe the extent of access to the database population | Complete. All six files are public, were downloaded in full, and are archived with the analysis | §2.1; data availability |
| **RECORD 12.2** | Describe data cleaning | **None was performed.** The files are screened exactly as published; no value was recoded, imputed or removed. This is a deliberate condition of the study, since cleaning would destroy the signal being measured | §2.1; §2.2 |
| **RECORD 12.3** | State whether data were linked and how linkage quality was assessed | **Not applicable.** No linkage | §2.1 |
| **STROBE 13 / RECORD 13.1** | Participant selection, including filtering on data quality and availability | Variables, not participants. Selection and the two set-aside rules are reported with counts at each step | Figure 1; §3.1, Table 1 |
| **STROBE 14** | Descriptive data | Table 1, Table 2, Figure 2 | §3.1 |
| **STROBE 15** | Outcome data | **Not applicable.** No outcome events | — |
| **STROBE 16** | Main results with estimates and precision | Repetition by dataset and by variable, with medians and full distributions; no confidence intervals are reported because every variable in the population is screened rather than sampled | §3.1, Tables 1–2, Figure 2 |
| **STROBE 17** | Other analyses | Comparison against dictionary labels; zero-exclusion sensitivity | §3.1, §3.5 |
| **STROBE 18** | Key results | §6 | §6 |
| **STROBE 19 / RECORD 19.1** | Limitations, including the implications of using data not created to answer this question | The data were created for programme monitoring, not for provenance research; what the screen cannot establish is stated first, and the method's own failure modes are reported | §5; Supplementary S3 |
| **STROBE 20** | Interpretation | §4, §6 | §4, §6 |
| **STROBE 21** | Generalisability | Six files, one programme, one time point; generalisation beyond TB is stated as open and directly testable | §5 |
| **STROBE 22** | Funding | None | Declarations |
| **RECORD 22.1** | State how to access the protocol, raw data and code | All three are public: archived input files, screening code, per-variable results table and a verification suite, deposited with a DOI | Declarations, data availability |
