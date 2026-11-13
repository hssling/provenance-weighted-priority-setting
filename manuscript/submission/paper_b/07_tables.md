# Tables

**Table 1. Screen results by dataset.**

| Dataset | Continuous | Categorical | Untestable | Median repetition | Measurement | Mixed | Estimate | Median if untestable scored 0% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Budget | 37 | 0 | 0 | 13.0% | 35 | 1 | 1 | 13.0% |
| Expenditure and utilisation | 39 | 1 | 0 | 15.4% | 28 | 7 | 4 | 15.4% |
| Notifications | 166 | 16 | 3 | 15.6% | 104 | 39 | 23 | 14.9% |
| Treatment outcomes | 66 | 1 | 24 | 33.0% | 21 | 20 | 25 | 20.5% |
| Laboratory diagnostic services | 41 | 12 | 16 | **63.0%** | 9 | 1 | **31** | **53.5%** |
| Contact tracing / TPT | 9 | 12 | 0 | **3.5%** | 9 | 0 | 0 | 3.5% |

---

**Table 2. Repetition excluding adjacent pairs in which both values are zero.** Restricted to variables with at least 20 such pairs.

| Dataset | Median repetition | Excluding zero-to-zero pairs | Zero as modal value |
|---|---:|---:|---:|
| Budget | 13.0% | 9.2% | 30 / 37 |
| Expenditure and utilisation | 15.4% | 7.3% | 32 / 39 |
| Notifications | 15.6% | 5.2% | 129 / 166 |
| Treatment outcomes | 33.0% | 6.5% | 65 / 66 |
| Laboratory diagnostic services | **63.0%** | **48.0%** | **24 / 41** |
| Contact tracing / TPT | 3.5% | 1.9% | 8 / 9 |

---

**Table 3. The five estimate-like variables in the budget and expenditure files.**

| Variable | n | Distinct values | Repetition | Distinct / n | Modal value share | Round |
|---|---:|---:|---:|---:|---:|---:|
| `hospd_prct_mdr` | 1,421 | 81 | 69.6% | 0.06 | 35.3% | 66.6% |
| `hospd_dur_mdr` | 1,368 | 111 | 66.5% | 0.08 | 11.8% | 67.1% |
| `cf_tot_usaid` | 628 | 182 | 64.4% | 0.29 | 64.3% | 49.1% |
| `hcfvisit_mdr` | 1,364 | 197 | 61.6% | 0.14 | 11.1% | 40.4% |
| `hospd_prct_dstb` | 1,467 | 92 | 61.5% | 0.06 | 9.8% | 48.0% |

---

**Table 4. For contrast, the six least-repetitive variables in the budget and expenditure files.**

| Variable | n | Repetition | Distinct / n |
|---|---:|---:|---:|
| `cf_tot` | 845 | 2.2% | 0.98 |
| `cf_tot_sources` | 849 | 2.5% | 0.98 |
| `exp_fld` | 866 | 4.6% | 0.93 |
| `rcvd_sld` | 856 | 5.0% | 0.91 |
| `rcvd_fld` | 865 | 5.1% | 0.93 |
| `budget_fld` | 870 | 5.4% | 0.93 |

---

**Table 5. Component-to-total identities in the budget and expenditure files.**

| Identity | Reconcile | Untestable |
|---|---|---|
| `budget_tot` = Σ 11 budget lines | 849 / 849 (100%) | 871 |
| `cf_tot` = Σ 11 expected-funding lines | 845 / 845 (100%) | 875 |
| `exp_tot` = Σ 11 expenditure lines | 895 / 895 (100%) | 1,228 |
| `rcvd_tot` = Σ 11 receipt lines | 892 / 892 (100%) | 1,231 |
| `rcvd_tot` = Σ 4 funding sources | 881 / 891 (98.9%) | 1,232 |

---

**Table 6. Screen verdict by dictionary label.**

| | Estimate-like | Mixed | Measurement-like | Categorical | Untestable |
|---|---:|---:|---:|---:|---:|
| Labelled (6) | 4 | 2 | 0 | 0 | 0 |
| Not labelled (437) | 80 | 66 | 206 | 42 | 43 |
