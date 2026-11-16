# Paper B — strengthening analyses (plan, committed before any result is computed)

**Date:** 16 November 2026. **Context:** Paper B ("Restated, never revised") was declined by the
*International Journal of Epidemiology* without review. It is being prepared for *Tropical Medicine &
International Health*. The existing analyses (revision, restatement, filling, provenance of WHO's care
estimate) are unchanged. Three analyses are added to answer the question the paper leaves open: how much
the published care estimate depends on inputs that are not current, and where.

All three use release 2026 (WHO's processed finance file for the 2026 report) and reporting year 2025, the
latest year WHO publishes, with the same provenance classification as `demos/d3_vintages.py`
(`provenance()`, `component_class()`), and the same reconstruction, which reproduces WHO's published
totals. Year 2024 in release 2026 is reported alongside as a check of stability.

## S1. Age of the inputs behind the care estimate

For each cost component that reaches the published total (the four components in `COMPONENTS`), the
*age* of an input is the number of years since its value was last different in the country's reported
series: 0 for a newly reported value; for a restated value, the reporting year minus the first year of
its unchanged run; for a value WHO supplied from year *y − k* or *y + k*, the age of the source value plus
*k* (lead fills are given age *k*). A component's age is the maximum age of its inputs. Reported: the
share of the 2025 care estimate (US$) by component age (0, 1, 2, 3, 4 and 5 or more years).

## S2. Re-measurement adjustment (sensitivity bound)

Where a country re-measures an input (a reported value that differs from its previous reported value),
the annual rate of change is log(new / previous) divided by the years between them. Rates are pooled by
input variable over reporting years 2018–2025 of release 2026. For every non-current input, the value is
moved by the variable's **median** rate for each year of its age; the **25th** and **75th** percentiles
give a band. Each component is rescaled by the ratio of its adjusted to its original input product
(hospital: percentage hospitalised × duration; clinic: visits), which is how WHO's code builds it, so the
adjusted care estimate needs no other input. Newly reported inputs are not changed. Reported: the care
estimate as published, adjusted at the median rate, and the band, for 2025, globally and for the countries
in S3. This is a sensitivity bound, not a correction: it shows how far the estimate would move if non-
current inputs had changed as re-measured inputs typically do.

## S3. Concentration

Per country (2025): care estimate, share resting on newly reported inputs, and component age. Reported:
the number of countries, and their share of the global care estimate, in which less than half of the care
estimate rests on newly reported inputs; and the same list restricted to the high TB burden countries named
in WHO's *Global tuberculosis report 2026*.

## Fixed in advance

- No change to the existing results, tables or the reconstruction.
- Inputs equal to zero have rate undefined and are left unchanged in S2 (a zero is an absence, not an
  estimate; see FINDINGS trap 8). Rates with a previous value of zero are excluded from the pool.
- Results are reported whatever their direction or size. A material adjustment in S2 strengthens the
  paper's conclusion; a negligible one is reported as evidence that the dependence on old inputs, though
  large, matters little for the published total.

## Deviations

(Recorded here, dated, if any decision above changes after results are seen.)
