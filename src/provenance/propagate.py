"""Propagate series provenance into TB-BOPAS and report which cells change rank. Standard library only.

compute_bopas is IMPORTED from the published TB-BOPAS repository (DOI 10.5281/zenodo.24169718),
never copied and never modified. That repository is read-only to this project: it is loaded by
file path, with bytecode writing disabled so the import leaves nothing behind in it.

Provenance multiplies the trajectory-derived term T ONLY: T is what the audited surveillance
series produce. L (literature) and M (coupling matrix) were never audited and are not rescored.
BOPAS = L * max(T,0) * M * sqrt(C) is linear in T, so scaling T by p is the same as scaling the
slope by p (T = slope_nat / half_width, and the half-width does not depend on the slope). That is
how it is done: the adjusted grid is produced by the published function itself, on slopes scaled
by p, so there is no second copy of the scoring formula and `round()` is applied exactly where the
published code applies it. A provenance of 1.0 multiplies the slope by 1.0 (exact in IEEE 754), so
the adjusted grid is bit-identical to the unadjusted one.
"""
from __future__ import annotations

import importlib.util
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path

from provenance.composite import composite, composite_report
from provenance.series import TestResult

# src/provenance/propagate.py -> parents[3] is the directory holding both projects. The same
# sibling-repository convention series.NTEP_TRAJECTORIES_CSV uses.
BOPAS_SOURCE = Path(__file__).resolve().parents[3] / "tb_bopas_repo" / "code" / "build_tb_bopas_ijtb.py"

_module = None


def _bopas_module():
    """Load the published script once, by file path, without touching the repository.

    Importing it has two side effects this guards against: Python would write __pycache__ next to
    the source (bytecode writing is switched off for the duration), and the script calls
    random.seed() at import, which would silently reseed the caller's global generator (state is
    saved and restored). It also runs OUT.mkdir(exist_ok=True) on the repository's existing
    outputs/ directory, which is a no-op while that directory exists.
    """
    global _module
    if _module is None:
        spec = importlib.util.spec_from_file_location("build_tb_bopas_ijtb", BOPAS_SOURCE)
        mod = importlib.util.module_from_spec(spec)
        old_flag, state = sys.dont_write_bytecode, random.getstate()
        sys.dont_write_bytecode = True
        try:
            spec.loader.exec_module(mod)
        finally:
            sys.dont_write_bytecode = old_flag
            random.setstate(state)
        _module = mod
    return _module


def load_compute_bopas():
    return _bopas_module().compute_bopas


class PropagationResult(list):
    """list[dict] of BOPAS rows, plus `unassessable`: series whose provenance was None.

    A series with no testable provenance result is NOT assigned 1.0 (that would flatter exactly
    the series known least about). Its cells are left unadjusted and the series is listed here,
    so a report can say how much of the grid rests on unaudited series.
    """
    unassessable: list[str]


def _check(series: str, p) -> float | None:
    if p is None:
        return None
    if isinstance(p, bool) or not isinstance(p, (int, float)) or not 0.0 <= p <= 1.0:
        raise ValueError(f"provenance for series {series!r} must be a number in [0, 1] or None, got {p!r}")
    return float(p)


def propagate(node_counts, traj_rows, provenance: dict[str, float | None], *,
              slope_field: str = "slope_primary", **bopas_kwargs) -> PropagationResult:
    """BOPAS rows with `provenance`, `unassessable`, `T_adj` and `BOPAS_adj` added.

    Existing fields (L, T, M, C, BOPAS, ...) are the published function's unadjusted output,
    unchanged. `bopas_kwargs` (half_floor, use_C, lo_field, hi_field) pass through to it.
    Every series in `traj_rows` must have an entry in `provenance`: a missing one raises rather
    than defaulting to clean.
    """
    compute_bopas = load_compute_bopas()
    series_keys = [t["series"] for t in traj_rows]
    missing = [s for s in dict.fromkeys(series_keys) if s not in provenance]
    if missing:
        raise ValueError(f"no provenance given for series {missing}; pass None for 'unassessable', "
                         f"1.0 only if the series was audited clean")
    p = {s: _check(s, provenance[s]) for s in series_keys}

    # None -> factor 1.0 means "leave unadjusted", recorded separately as unassessable.
    scaled = [dict(t, **{slope_field: t[slope_field] * f}) if (f := p[t["series"]]) not in (None, 1.0)
              else dict(t) for t in traj_rows]
    before, _ = compute_bopas(node_counts, traj_rows, slope_field=slope_field, **bopas_kwargs)
    adjusted, _ = compute_bopas(node_counts, scaled, slope_field=slope_field, **bopas_kwargs)
    adj = {(r["intervention"], r["series"]): r for r in adjusted}

    out = PropagationResult()
    for r in before:
        a = adj[(r["intervention"], r["series"])]
        # "+ 0.0" turns -0.0 (a negative slope times 0.0) into 0.0 and leaves every other float as is
        out.append(dict(r, provenance=p[r["series"]], unassessable=p[r["series"]] is None,
                        T_adj=a["T"] + 0.0, BOPAS_adj=a["BOPAS"] + 0.0))
    out.unassessable = [s for s in dict.fromkeys(series_keys) if p[s] is None]
    return out


def provenance_from_results(results_by_series: dict[str, list[TestResult]], *,
                            rule: str | None = None) -> dict[str, float | None]:
    """series -> composite provenance (None when unassessable).

    Each series may contribute exactly ONE triangulation result. Change-mode and level-mode
    triangulation answer the same question from different angles and are not independent
    evidence; passing both would give T2 double weight, so composite_report raises on it and this
    function lets that error through, naming the series.
    """
    kw = {} if rule is None else {"rule": rule}
    out = {}
    for series, results in results_by_series.items():
        try:
            composite_report(results, **kw)   # validates: raises on a duplicated test
        except ValueError as e:
            raise ValueError(f"series {series!r}: {e}") from None
        out[series] = composite(results, **kw)
    return out


@dataclass(frozen=True)
class RankChange:
    intervention: str
    target: str
    rank_before: int
    rank_after: int


def _ranks(scores: dict[tuple[str, str], float]) -> dict[tuple[str, str], int]:
    # competition ranking: equal scores share a rank, so row order cannot manufacture a change
    return {k: 1 + sum(1 for v in scores.values() if v > s) for k, s in scores.items()}


def rank_changes(before: list[dict], after: list[dict]) -> list[RankChange]:
    """Cells whose rank differs between `before` (by BOPAS) and `after` (by BOPAS_adj).

    Cells are paired by (intervention, target), not by position. Ranks are on the published
    (rounded) scores, so cells tied at 0.0 share a rank; a rank change can therefore also arise
    when rounding creates or breaks a tie. Empty list means the ranking is unchanged.
    """
    b = {(r["intervention"], r["target"]): r["BOPAS"] for r in before}
    a = {(r["intervention"], r["target"]): r["BOPAS_adj"] for r in after}
    if len(b) != len(before) or len(a) != len(after):
        raise ValueError("duplicate (intervention, target) cells")
    if b.keys() != a.keys():
        raise ValueError("before and after cover different (intervention, target) cells")
    for v in (*b.values(), *a.values()):
        if isinstance(v, float) and math.isnan(v):
            raise ValueError("NaN score cannot be ranked")
    rb, ra = _ranks(b), _ranks(a)
    return sorted((RankChange(i, t, rb[(i, t)], ra[(i, t)]) for (i, t) in b if rb[(i, t)] != ra[(i, t)]),
                  key=lambda c: (c.rank_before, c.intervention, c.target))
