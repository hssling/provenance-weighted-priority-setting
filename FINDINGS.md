# Findings

Durable record of results and methodological decisions from building the
instrument. The SDD working ledger under `.superpowers/` is deleted when the
plan completes; anything that matters to the paper lives here instead.

Every figure below was verified against the raw CSVs, independently of the
code that computes it.

---

## 1. Results on India's TB financing data

### 1.1 WHO's funding-gap indicator is structurally uninformative for India

India reports `cf_tot` (expected funding) **exactly equal** to `budget_tot`
(budget required) in all eight years 2018–2025, so WHO's funding gap is pinned
at zero by construction. It is not an observation.

This is not how the field is generally used. Of 106 countries with ≥5 years of
data, only **14** report budget == expected funding in every year; **44** report
a non-zero gap in every year (Vietnam ~72%, Nigeria ~69%, Indonesia ~59%,
Pakistan ~45%, China ~10%).

Meanwhile India's own TB Report shows ₹18,388 crore approved against ₹23,169
crore requested — a shortfall of 5.4% to 46.1% depending on year.

**Implication:** anyone ranking countries by WHO's TB funding gap would place
India among the best-funded TB programmes in the world. The indicator is in
active use for priority-setting.

### 1.2 Execution gap, corroborated across two independent sources

- WHO: total expenditure / budget required = **72%** (range 45–98%).
- India TB Report: ₹15,063 cr spent / ₹18,388 cr approved = **82%**;
  spent / requested = **65%**.

Two agencies, two accounting systems, same direction.

### 1.3 Financing has domesticated almost completely

Global Fund share of actual TB expenditure: **37% (2017) → 1% (2025)**.
Domestic share 62% → 96%. Monotone and large.

### 1.4 Fiscal invisibility

**Six** of eleven evidence-ranked TB interventions have **no budget line at all**:
airborne infection prevention and control (rank 2), whole-genome sequencing (4),
**active case finding (5)**, bovine TB control (7), private-sector engagement (8),
milk pasteurisation (10).

Three of the top five evidence-ranked interventions are fiscally untraceable.

Active case finding was initially mapped to `budget_prog`. That is wrong, and
WHO's own data dictionary settles it: `budget_prog` is *"Budget required for
programme costs to **treat** drug-susceptible TB"*. Case **finding** is not
treatment. The mapping was corrected after the implementer challenged it.

**Three mappings are partial rather than absent**, and this materially limits
any "evidence rank versus budget share" comparison:

| node | line | what the definition actually covers |
|---|---|---|
| TB preventive therapy (3) | `budget_tpt` | *"TB preventive treatment: **drugs**"* — not delivery, contact tracing or adherence support |
| Shorter all-oral regimen rollout (6) | `budget_sld` | *"**drugs** to treat drug-resistant TB"* — a rollout is programme work; DR-TB programme costs sit in `budget_mdrmgt`, which maps to no node |
| Integrated TB-HIV-diabetes care (11) | `budget_tbhiv` | *"collaborative **TB/HIV** activities"* — two of three arms; diabetes absent |

Only two mappings are full matches: molecular diagnostics → `budget_lab`
(laboratory equipment and supplies) and nutritional support → `budget_patsup`
(patient support, which is broader than nutrition but contains it).

**Caveat on the concordance comparison.** For the three partial nodes, budget
share is computed against a **drugs-only** line. An intervention can therefore
appear underfunded merely because the non-drug part of its cost is pooled
somewhere unattributable. The earlier observation that TB preventive therapy
receives ~0.3% of the TB budget is the share of its **drug** cost, not of its
total programme cost, and must be stated that way.

That pooling is itself a form of fiscal invisibility — not of the intervention,
but of the part of it that is not a commodity.

Every mapping is now checked against the dictionary definition, not against the
column name. A plausible-looking name is not evidence that a line item covers
the intervention — which is the same error, one level up, that this instrument
exists to catch.

This replicates the finding in the JSSTD NACP-V paper, where STI services, PrEP
and surveillance likewise had no traceable line item. Two programmes, two
ministries' demands, same structural property.

### 1.5 Where the identity test has signal, and where it does not

All five sum identities reconcile on India's real data — `exp_tot` 10/10,
`rcvd_tot` 10/10, `rcvd_tot` by funding source 10/10, `budget_tot` 8/8,
`cf_tot` 8/8.

So T1's only India signal is:
- the **product** identity on `budget_tpt`, which diverges 3.3× (2024) and
  9.1× (2025); and
- **completeness**, which catches the 2026 expenditure row.

---

## 2. Methodological results

### 2.1 Four design choices that silently disabled their own purpose

Each was found by running the code against real data, not by reasoning about
it. This is the paper's methods argument.

| # | The choice | Why it was blind |
|---|---|---|
| 1 | Detect the "reported total, absent components" pathology with an identity test | India 2026 has `exp_tot = 0` with all 11 parts absent. **0 == 0 reconciles.** The identity test scores the worst row in the dataset as clean. Fixed by scoring **completeness** separately from identity. |
| 2 | A flat ±10% identity tolerance | `budget_cpp_tpt` is reported as an integer; in 2023 that integer is **1**, so ±0.5 rounding is ±50% relative. A flat band flags a ratio of 0.896 as a discrepancy that does not exist — a manufactured finding. Fixed by scaling the band to the reporting precision. |
| 3 | A symmetric rounding band | `c_true ∈ [c−0.5, c+0.5)` and ratio `= c/c_true`, so the admissible range is `(c/(c+0.5), c/(c−0.5)]` — at c=1 that is `(0.667, 2.0]`, not `[0.5, 1.5]`. Too strict above 1, which is the false-positive direction. Changed no verdict in this data; fixed anyway. |
| 4 | Compare year-on-year *change* across sources, to avoid an exchange rate | The WHO-vs-India contradiction is a **level** disagreement, and change cancels levels. The test was structurally blind to the finding it was built for. Fixed with dimensionless internal ratios, which need no currency conversion. |

### 2.2 T3 has no power on budgeted unit costs — an honest null

The implausibility bound must be derived, never chosen. Derived from
`budget_cpp_dstb` across 215 countries (691 comparable steps), the 95th
percentile of absolute year-on-year change is **1.917** (linear interpolation,
`(n−1)` convention).

At that bound, India's `budget_cpp_xdr` — whose steps run −76%, +50%, +50%,
−78%, +98%, −5%, +3% — has **zero** violations. Score 1.0.

**Sensitivity, recorded and deliberately NOT adopted:** using `tx_dstb`
(patients treated) as the reference gives a bound of **0.355**, which flags
2019–2023 and scores 0.29. It was rejected because the reference must be the
same *kind* of quantity as the target — `cpp_xdr` and `cpp_dstb` are both
budgeted unit costs; `tx_dstb` is a patient count — and because it is, not
coincidentally, the reference that produces the desired answer. Adopting it
would be reverse-engineering the threshold to the conclusion.

**Reading:** WHO budgeted unit costs are so volatile across countries that no
year-on-year movement in them can be called implausible. That is a
characterisation of the field, not a weakness of the test, and it suggests the
unit-cost fields do not measure a stable quantity.

**Consequence for an earlier claim.** The BPaLM unit-cost story was rejected
partly on the grounds that ±50–98% swings in `cpp_xdr` were "reporting noise".
The derived bound shows such swings are within the normal range for this field,
so that argument was unanchored. The rejection still stands on the independent
timing argument: **87% of the decline pre-dates BPaLM**, which WHO recommended
in December 2022 and India rolled out from 2024.

---

## 3. Data provenance

- `data/TB_budget_2026-11-12.csv` — WHO TB budget dataset, 1,720 rows, 215
  countries, 2018–2025, 43 columns.
- `data/TB_expenditure_utilisation_2026-08-25.csv` — downloaded from
  `github.com/GTB-TME/gtbreport2026`. India 2017–2026; the 2026 row reports
  `exp_tot = 0` with all components blank.
- `data/india_tb_report_table16_1.csv` — hand-entered from India TB Report 2024,
  Table 16.1, p.174. **Two cells were OCR-damaged in the source PDF.** The PDF
  prints the digit strings `305,742` and `188,882`; only the decimal point was
  lost in extraction. They are restored as 3057.42 and 1888.82 — digit-faithful,
  with the placement confirmed independently by all three published column
  totals (23169.14, 18388.23, 15063.46).

A project about data provenance cannot leave its own provenance undocumented.

---

## 4. D1: the instrument run end to end on India's TB data

Reproduce with `python demos/d1_tb.py` (writes `outputs/d1_*.csv` and `d1_summary.txt`; `outputs/`
is gitignored). Numbers below were checked against the published TB-BOPAS outputs
(`ijtb_bopas_long.csv`, `ijtb_slopes.csv`), independently of the code that computes them.

### 4.1 What is audited, and what is not

The five tests were developed on **financing** data. TB-BOPAS consumes **epidemiological** series.
The provenance of a budget line says nothing about the provenance of a notification rate, so
propagating one into the other would be incoherent. D1 therefore audits the six series in
`ntep_trajectories.csv` (five are BOPAS targets; `BDQ_res_pct`, two points, is audited but not in
the 60-cell grid). The financing audit (sections 1.1 to 1.5, plus T5) is reported separately and is
**not** propagated.

### 4.2 T2 is untestable on every series the priority score uses

No NTEP series has an independent second source in the repository; `who_dataset` names a WHO table,
not an independent source. T2 returns untestable for all six. The test that produced the strongest
financing finding (WHO's funding gap contradicting the India TB Report, agreeing in 0 of 6 years)
therefore has **no power** on the series the priority score consumes. T1 here reconciles 42 of 42
rows, but it checks `value = scale * numerator / denominator` within the file, not WHO's numbers.

### 4.3 T3 and T4 double-counted; T4 now subsumes T3

T4 is T3 on the same steps plus credit for a disclosed break, so it is identical to T3 where nothing
is declared. Combining both penalised one implausible step twice. The composite now uses T1, T2 and
T4 (T3 only if T4 is untestable); both scores are still reported. Effect: composites for
`RRMDR_notif_100k` and `RR_new_pct` moved 0.902 to 0.926, and `n_testable` 3 to 2.
The T3/T4 bound is derived leave-one-out from the other five series (p95), so no series sets its
own yardstick; pooling all six gives the same composite.

| series | composite | observations behind it |
|---|---|---|
| RRMDR_notif_100k | 0.926 | identity 8, declared 7 |
| RR_new_pct | 0.926 | identity 8, declared 7 |
| preXDR_fqr_pct | 1.0 | identity 6, declared 5 |
| MDR_TSR_pct | 1.0 | identity 9, declared 8 |
| XDR_TSR_pct | 1.0 | identity 9, declared 8 |

No test scored exactly 0.0; no series is unassessable.

### 4.4 The structural null

Provenance could not reorder this ranking. **49 of 60 cells score exactly 0.0, and all 11 positive
cells belong to one series, `RRMDR_notif_100k`.** Provenance scales a series' cells uniformly, so it
cannot change the order within a series and cannot lift a zero cell.

- **0 inversions** (no two cells with distinct scores trade places) at every provenance value from
  0.0 to 1.0 in steps of 0.05.
- **1 tie split**: Milk pasteurisation moves from rank 9 to 10. Nutritional support and Milk
  pasteurisation both publish 0.033 and share rank 9; scaling then rounding gives 0.030 and 0.029.
  Published scores are rounded to 3 decimals, rounding is monotone, so it can create or break ties
  but never invert an order. `rank_changes` classifies each change as `inversion` or `tie_split`.
- At provenance 0.0 the series is wiped out and the 11 cells tie at zero; that destroys the ranking
  rather than reordering it.

The ranking rests on a single axis, the `RRMDR_notif_100k` slope, whose published bootstrap CI is
**[-0.11, +0.30]** and spans zero. The instrument could not discriminate on this instance because the
priority score is degenerate. D1 does **not** support the claim that provenance reorders priorities;
that is a question for D2 and D3, on instances where several series carry positive cells.

### 4.5 EVPR

Exactly **0.0 with standard error 0.0** for every series under all three priors (beta, uniform,
floor). The decision cannot change, so no audit of any series is worth buying on this grid. Same
cause as 4.4.

### 4.6 Reproducibility note

`fit_trajectories` bootstraps off the global RNG. D1 and the test fixture seed 20260908 (the
published script's seed) and restore state, which reproduces all five published CIs exactly. An
unseeded fit gives `RRMDR_notif_100k` [-0.1156, 0.2903], not the published [-0.1133, 0.2957].
