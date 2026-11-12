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
China ~10%; mean gap over the years reported). Pakistan is **not** one of the 44:
it reports a 43-66% gap in 2018-2023 and exactly 0.000 in 2024 and 2025. (An earlier
draft listed it among the 44; that was wrong.)

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

**Provenance finding about the source (not an error of ours).** The India TB Report's Table 16.1
is internally inconsistent. Over 2017-2021, the only years in which `released` is printed
(blank for 2022 and 2023), `released` sums to **3,825.31 crore** while `spent` sums to
**13,312.14 crore**: spending is **3.5x** the funds the same table says were released. In 2017
`spent` is 2,759.44 crore against 1,840.00 approved (**150%** of approved). Spending can exceed
release if states spend from their own or carried-over funds, but the table does not say so, so
the `released` column cannot be reconciled with `spent` from the page alone. The three published
column totals (requested 23,169.14; approved 18,388.23; spent 15,063.46) still reconcile exactly
with our recovery, so the OCR recovery in section 3 is sound; the inconsistency is in the source.
The 82% and 65% ratios above use `spent`, `approved` and `requested` and do not touch `released`.

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

All five sum identities reconcile on India's real data. `exp_tot`, `rcvd_tot` and `rcvd_tot`
by funding source each have **9** reconciling identity ratios (2017-2025); the year 2026 has no
ratio at all (total reported as 0, every component blank) and is the **completeness** failure,
so each scores 9/10 = 0.9. `budget_tot` 8/8 and `cf_tot` 8/8.

So T1's only India signal is:
- the **product** identity on `budget_tpt`, which diverges 3.3× (2024) and
  9.1× (2025); and
- **completeness**, which catches the 2026 expenditure row.

**The identity tolerance (+-10%) has no derivation; its sweep is recorded instead** (the same
treatment as `LEVEL_TOLERANCE`; pinned in `tests/test_identity.py`). From 0.01 to 0.15 every
sum identity above has the *same* score (budget_tot and cf_tot 1.0; the three expenditure
identities 0.9, the loss being the 2026 completeness failure, not arithmetic). The product
identity `budget_tpt` is *not* stable: 2/6 clean at tolerance 0.01-0.05, 4/6 from 0.08 to 0.15.
At 0.05 the 2023 ratio (0.90, a unit cost of 1 carrying +-50% rounding) is no longer absorbed.
The `budget_tpt` verdict therefore depends on a convention; the 2024 (3.3x) and 2025 (9.1x)
divergences fail at every tolerance in the sweep.

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

**A fifth, found in whole-branch review rather than by running the code (see 2.2):** a step size of
`|v/prev - 1|` is capped at 1 for any fall, so T3 and T4 could not flag a decline of any size once the
bound reached 1. It also hid the one declared known case (4.3.2). Fixed with an inversion-symmetric
step size. Like the other four, it silently disabled the test's own purpose; unlike them, no run
against real data could reveal it, because the failure was the absence of a flag.

### 2.2 T3 is untestable on budgeted unit costs, and the first version of this section was wrong

**The defect (C2).** T3 and T4 originally measured a step as `|v/prev - 1|`. For any fall,
`v/prev` lies in [0, 1), so that statistic is below 1 *always*: a fall can never exceed a bound of
1 or more, whatever its size (a 1000 -> 0.001 collapse scored exactly 1.0000 against a bound of
1.917). The derived bound was 1.917, so **no decline of any magnitude could be flagged**. Three
of India's seven `budget_cpp_xdr` steps are declines (-76%, -78%, -5%), including the ones the
specification names as motivating T3. The statistic is now the inversion-symmetric fold change
minus one, `max(v/prev, prev/v) - 1`, a monotone function of `|log(v/prev)|` (it flags exactly
what `|log|` flags; the units stay readable: 1.0 is a doubling or a halving). A step to or through
zero is +inf. T2's change mode is unchanged (it compares two sources' changes to each other, not
to a bound, and is not run on real data).

**What the earlier text claimed, and why it was false.** It said that WHO budgeted unit costs
are so volatile that "no year-on-year movement in them can be called implausible", as "a
characterisation of the field, not a weakness of the test". That conflated two things. It was a
weakness of the test for declines (structurally unflaggable); and for rises, a +192% step *would*
have been flagged, so "no movement" was simply untrue. The same text also reported the
clean score as if it were a finding.

**What the corrected test says.** Derived from `budget_cpp_dstb` across 215 countries (691
comparable steps), the 95th percentile of the symmetric step size is **4.132** (a 5.1-fold
swing; linear interpolation, `(n-1)` convention). The reference is not stable: **28%** of its
691 steps (193) are exactly zero (unchanged from the previous year, consistent with a carried-forward figure), while its upper tail
swings five-fold. `implausibility.py` states a precondition, "a reference set believed stable";
this reference violates it. A bound of 4.13 would pass a process that quintuples and quarters at
will, so a score of 1.0 would be an artefact of the reference, not evidence about the series.
The rule is now explicit: a derived bound >= 1.0 (the reference's own p95 step is a doubling or
halving; 1.0 is a convention, also the point where the old statistic went blind to falls) makes
T3 and T4 return `testable=False`. **`budget_cpp_xdr` T3 and T4 are therefore not testable. They
were previously reported as 1.0.** (At the unadopted bound 4.132 the symmetric statistic would
still find no exceedance: the largest India steps have size 3.17 for 2019 and 3.50 for 2022.)

**Sensitivity, recorded and deliberately NOT adopted:** using `tx_dstb` (patients treated) as the
reference gives a bound of **0.423** (previously 0.355 under the asymmetric statistic), which flags
2019-2023 and scores 0.286 (2/7). Rejected for the same reason as before: the reference must be
the same *kind* of quantity as the target, and it is, not coincidentally, the reference that
would produce the desired answer. Adopting it would be reverse-engineering the threshold to the
conclusion.

**Consequence for an earlier claim.** The BPaLM unit-cost story was rejected partly on the grounds
that +-50-98% swings in `cpp_xdr` were "reporting noise". No valid reference exists to say whether
such swings are normal, so that argument is unanchored in either direction. The rejection still
stands on the independent timing argument: **87% of the decline pre-dates BPaLM**, which WHO
recommended in December 2022 and India rolled out from 2024.

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
rows, but it checks `value = scale * numerator / denominator` within one file (value, numerator and
denominator all come from `ntep_trajectories.csv`), not WHO's numbers. It can fail only on a
transcription slip, so it is **untestable** on the NTEP series (see 4.3), not a clean 1.0.

### 4.3 What goes into the composite, and what moved

Three separate corrections changed the NTEP composites. Each is reported because each moved a number.

1. **T4 subsumes T3 (Ruling GG).** T4 is T3 on the same steps plus credit for a disclosed break.
   Combining both penalised one implausible step twice; the composite uses T4 (T3 only if T4 is
   untestable); both are still reported. This moved `RRMDR_notif_100k` and `RR_new_pct` from 0.902
   to 0.926.
2. **The symmetric step size (C2, section 2.2).** Declines are now flaggable. The leave-one-out
   (p95) bounds moved: `RR_new_pct` 0.3211 to 0.3367, `preXDR_fqr_pct` 0.4006 to 0.4131,
   `MDR_TSR_pct` 0.4242 to 0.4330, `XDR_TSR_pct` 0.4237 to 0.4330, `BDQ_res_pct` 0.3690 to 0.3865;
   `RRMDR_notif_100k` unchanged at 0.3211. `RRMDR_notif_100k`'s T3 moved 0.857 to 0.714 and its T4
   0.857 to 0.786 (its declared 2020 decline is now a flagged step, see below); its composite moved
   0.926 to 0.886. The pooled-reference sensitivity bound moved 0.361 to 0.380.
3. **T1 is untestable on these series (I1).** `identity_score(..., independent=False)` marks a
   reconciliation whose components are built from the same record as the total. It can fail only
   on a transcription slip, yet it contributed 1.0 to every composite and 8 of the 15 Beta-prior
   observations. It is now reported as a transcription check (42 of 42 rows reconcile) and kept
   out of the composite and the observation counts. Each NTEP composite is now its T4 score
   alone (`n_testable` 1); `RRMDR_notif_100k` moved 0.886 to **0.786**.

| series | composite | observations behind it | T3 | T4 | bound |
|---|---|---|---|---|---|
| RRMDR_notif_100k | **0.786** | declared 7 | 0.714 | 0.786 | 0.321 |
| RR_new_pct | **0.857** | declared 7 | 0.857 | 0.857 | 0.337 |
| preXDR_fqr_pct | 1.0 | declared 5 | 1.0 | 1.0 | 0.413 |
| MDR_TSR_pct | 1.0 | declared 8 | 1.0 | 1.0 | 0.433 |
| XDR_TSR_pct | 1.0 | declared 8 | 1.0 | 1.0 | 0.433 |

(`BDQ_res_pct`, two points: composite 1.0 on one observation; not in the grid.) No test scored
exactly 0.0; no series is unassessable.

**Why the earlier 0.902 to 0.926 story is no longer the whole story.** It was reported as the effect
of removing a duplicate from the geometric mean. That was the *only* thing that moved, because
under the asymmetric statistic the disclosure mechanism was never exercised on real data:
`detail["declared"]` was empty for all six series and T4 equalled T3 on every series.

### 4.3.1 The one positive result: an undeclared level shift found without looking for it

T3 and T4 flag **`RR_new_pct` 2021: 2.5927 to 4.7320, +82.5%** (size 0.825 against a bound of
0.337, derived leave-one-out from the *other five* series, so without reference to this series).
The series carries no note; the shift is **undeclared (silent)**. It is persistent: 2022 4.5076,
2023 4.1850, 2024 3.6262 all stay above the pre-shift 2.5927. This is the series the specification
names as motivating case #1 (DR-TB surveillance, apparent worsening of rifampicin resistance, which
the specification attributes to a 2021 WHO definitional change plus DST scale-up). The instrument
located the 2021 step from the data alone. **This is the strongest evidence in the project that the
instrument works.** It is also robust to the percentile: the 2021 step is flagged at p80, p90, p95
and p99, leave-one-out and pooled. Caveats: a flag is a candidate, not proof of a definitional
change (the data alone cannot say why it moved), and it is one series.

### 4.3.2 The known declared case, and a miss that was a defect

`RRMDR_notif_100k` carries the only declared definitional break in the data: *"variable changed at
2020: conf_rrmdr discontinued, replaced by the rr_nfqr/rr_fqr split"*. Its 2020 step is -25.7%
(4.7699 to 3.5419).

- **As first built (asymmetric statistic), this known case was missed, and the miss was not
  reported.** The step's `|v/prev - 1|` of 0.257 was below the derived bound of 0.321, so T3 and T4
  never registered it. `detail["declared"]` was **empty for all six series** and T4's score equalled
  T3's exactly on every series: the disclosure mechanism had **never run on real data**. The
  specification says a missed known case is "a reportable limitation, not a reason to tune the
  test". The bound was correctly not tuned. But the cause was not the bound: it was the structural
  blindness of the statistic to falls (2.2), which no choice of bound could have fixed.
- **After the symmetric correction** (bound unchanged at 0.3211, derived and not adjusted), the 2020
  step has size 0.347, exceeds the bound, is **declared** by the series note, and T4 (0.786) now
  exceeds T3 (0.714): the disclosure mechanism fires on real data for the first time, in one step
  on one series (T4 differs from T3 on 1 of 6 series). The same series' 2018 step (+47.9%) is
  flagged and silent.
- **Fragility, reported.** The detection is bound-sensitive: size 0.347 sits just above the
  leave-one-out p95 bound (0.321). It is flagged at p80, p90 and p95, but **not at p99** (bound
  0.684) and **not under the pooled-reference p95** (bound 0.380; composite 0.857 against 0.786).
  The earlier statement that "pooling all six gives the same composite" is no longer true. The
  leave-one-out bound is kept for the reason given in 4.3 (no series sets its own yardstick), not
  because it catches this case.

The demo's summary reports every declared break and whether it was detected, and says "MISSED" if
it is not, so a miss cannot again go unreported.

### 4.4 The structural null

Provenance could not reorder this ranking. **49 of 60 cells score exactly 0.0, and all 11 positive
cells belong to one series, `RRMDR_notif_100k`.**

Two things make the null, and both are named. The first is the **data**: the priority score is
degenerate on this instance (49 of 60 zeros, one live series, a slope CI that spans zero). The
second is the **design**: one provenance scalar per series scales that series' cells uniformly, so
it can only reorder cells *across* series. It cannot change the order within a series and cannot
lift a zero cell. On *any* grid in which the positive cells sit in one series, reordering is
impossible by construction, whatever the data. The null is therefore evidence about neither the
instrument nor, wholly, BOPAS. An earlier phrasing ("the instrument could not discriminate ...
because the priority score is degenerate") attributed it to the priority score alone.

- **0 inversions** (no two cells with distinct scores trade places) at every provenance value from
  0.0 to 1.0 in steps of 0.05.
- **0 tie splits** at the current composite (0.786). The published grid contains a rounding tie at
  0.033 (Nutritional support and Milk pasteurisation), and scaling then rounding can split it at some
  provenance values and not others (at 0.9 it splits, Milk 9 to 10; at 0.91 it does not). Whether
  it splits is an artefact of the value, never a finding. (Under the earlier composite 0.926 it
  split; the earlier text reported that one rank change.) `rank_changes` classifies each change as
  `inversion` or `tie_split`; rounding is monotone, so it can create or break ties but never invert.
- At provenance 0.0 the series is wiped out and the 11 cells tie at zero; that destroys the ranking
  rather than reordering it. Literal rank changes still occur at 12 of the 19 interior sweep values
  (rounding ties).

The ranking rests on a single axis, the `RRMDR_notif_100k` slope, whose published bootstrap CI is
**[-0.11, +0.30]** and spans zero.

**State of the branch (I7).** The project currently has **zero** instances of provenance reordering
a ranking anywhere. D2 and D3 do not exist. The specification's central claim, that a method which
changes no ranking anywhere has failed (its anti-goal), is therefore **unmet at present**. D1 does
not support the claim that provenance reorders priorities; that is a question for D2 and D3, on
instances where several series carry positive cells, and those have not been built.

### 4.5 EVPR

Exactly **0.0 with standard error 0.0** for every series under all three priors (beta, uniform,
floor). The decision cannot change, so no audit of any series is worth buying on this grid. Same
cause as 4.4. The Beta prior's observation counts are now the T4 counts only (7, 7, 5, 8, 8), not
the T1 + T4 counts; this does not move any EVPR, which is zero for structural reasons.

### 4.6 Reproducibility note

`fit_trajectories` bootstraps off the global RNG. D1 and the test fixture seed 20260908 (the
published script's seed) and restore state, which reproduces all five published CIs exactly. An
unseeded fit gives `RRMDR_notif_100k` [-0.1156, 0.2903], not the published [-0.1133, 0.2957].

---

## 5. Limitations and open questions

### 5.1 Limitations the instrument carries

- **The reference population is the audited population (I4).** Leave-one-out removes a series from
  its *own* reference but not from the others'. If other series carry undeclared shifts, they inflate
  everyone else's bound: `RR_new_pct`'s silent +82.5% step is part of the reference for the other five
  series' bounds. Leave-one-out does not fix a contaminated reference; it removes only self-reference.
  A reference external to the audited series would; none exists in this repository.
- **T1 on the NTEP inputs has no power (I1).** It is a transcription check, not evidence. It would not
  catch a wrong numerator copied consistently.
- **T2 is untestable on every series the priority score uses (4.2).** Each NTEP composite therefore
  rests on one test, T4.
- **Composites are not comparable across series with different `n_testable` (I5).** Untestable tests
  are dropped, and adding a testable *clean* test raises the composite (a lone 0.9 becomes 0.949 with a
  clean 1.0 beside it). A series testable by more tests looks better for that reason alone. It is
  invisible in D1, where every series has `n_testable` = 1, but D2 and D3 will not be so uniform. The
  comparison must be restricted to series with the same tests, or `n_testable` reported beside every
  score. Documented in `composite.py`.
- **The EVPR prior is not a posterior (I2).** `Beta(P*m + 1, (1-P)*m + 1)` borrows the shape of the
  binomial `Beta(k+1, n-k+1)` idiom but is not derived from any likelihood the composite satisfies:
  `P` is a geometric mean of per-test pass fractions, not a binomial proportion, and `m` sums
  observation counts that can count the same year more than once across tests. It is a pragmatic
  evidence-weighted prior; an earlier claim that it is "the same construction the parent project uses
  for literature support" has been removed. The three-prior sensitivity is the guard.
- **T3/T4 require a stable reference (I3).** Where the derived bound is >= 1.0 the tests are untestable
  rather than clean. The threshold of 1.0 is a convention.
- **The identity tolerance and the 0.5 declared-break credit are conventions.** The tolerance's sweep
  is in 1.5; the credit is documented in `declared.py` as affecting scores but not the
  declared-over-silent ordering.

### 5.2 Open question, unresolved, owned by the project author

> **The composite is a pass-rate: "how often did provenance move" (the fraction of tests or steps that
> came out clean). `propagate()` uses it as a multiplicative attenuation on the slope: "how much did
> provenance move the number". Nothing in the code or the record argues that these are the same
> quantity.** A series with 1 of 7 steps over the bound is scaled by 0.857 whether that step is a 33% blip
> or a 10-fold break (T4 counts steps over the bound, not how far over). This is the paper's
> load-bearing step.

This is **not resolved here and not addressed by any change in this fix wave.** It is a conceptual
question for the project author, not a code change.
