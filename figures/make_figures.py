"""Generate the figures for both manuscripts.

This is the ONLY directory in the repository with a third-party dependency.
`src/` and `demos/` are standard library only, so that every number in both
papers regenerates on a bare Python install; drawing is a different job and
matplotlib is not worth reimplementing. The figures are derived from the same
files and the same code paths as the tables, never from retyped numbers.

Output: 300 dpi PNG, at least 3600 pixels wide, as the International Journal
of Epidemiology requires (minimum 300 dpi at a minimum width of 300 mm).

Usage: python figures/make_figures.py
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt       # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "demos"))
OUT = Path(__file__).resolve().parent
DPI = 300
WIDTH_IN = 15.5                        # tight bbox crops, so draw wider than
                                       # 12 in and assert the result in save()

# One restrained palette, colour-blind safe, used by both figures.
INK = "#1a1a1a"
GREY = "#8c8c8c"
BLUE = "#2b6cb0"
ORANGE = "#c05621"

plt.rcParams.update({
    "font.size": 15,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name: str) -> None:
    path = OUT / name
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    from PIL import Image
    with Image.open(path) as im:
        w, h = im.size
    assert w >= 3600, f"{name}: {w}px wide, IJE requires at least 3600"
    print(f"  {name}: {w} x {h} px at {DPI} dpi")


# --------------------------------------------------------------------------
def figure_a1() -> None:
    """Paper A: the reported gap is flat at zero while the national accounts
    show a shortfall that varies from 5% to 46%."""
    rows = list(csv.DictReader((ROOT / "data" / "india_tb_report_table16_1.csv")
                               .open(encoding="utf-8-sig")))
    years, shortfall = [], []
    for r in rows:
        req, app = float(r["requested"]), float(r["approved"])
        if req and int(r["year"]) >= 2018:
            years.append(int(r["year"]))
            shortfall.append(100.0 * (req - app) / req)

    fig, ax = plt.subplots(figsize=(WIDTH_IN, WIDTH_IN * 0.46))
    ax.plot(years, shortfall, marker="o", markersize=11, linewidth=3,
            color=ORANGE, label="Shortfall in India's own accounts\n"
                                "(requested minus approved, India TB Report 2024)",
            zorder=3)
    ax.plot(years, [0] * len(years), marker="s", markersize=11, linewidth=3,
            color=BLUE, label="Funding gap as reported to WHO\n"
                              "(budget required minus funding expected)", zorder=3)
    for x, y in zip(years, shortfall):
        ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points",
                    xytext=(0, 13), ha="center", fontsize=13, color=ORANGE)
    ax.set_ylabel("Shortfall, % of amount requested")
    ax.set_xlabel("Fiscal year")
    ax.set_ylim(-4, max(shortfall) + 12)
    ax.set_xticks(years)
    ax.axhline(0, color=GREY, linewidth=0.8, zorder=1)
    ax.grid(axis="y", color="#e6e6e6", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper left", fontsize=14, handlelength=2.4)
    save(fig, "figure_a1_two_accounts_of_the_same_shortfall.png")


# --------------------------------------------------------------------------
def figure_b1() -> None:
    """Paper B: every variable's repetition, by dataset, with and without
    zero-to-zero pairs. The table gives medians; this shows the distribution
    the medians summarise, which is where the separation is visible."""
    import d2_who_data_screen as d2

    labels = {"budget": "Budget", "expenditure": "Expenditure\nand utilisation",
              "notifications": "Notifications", "outcomes": "Treatment\noutcomes",
              "laboratory": "Laboratory\ndiagnostic services",
              "contact_tpt": "Contact tracing\nand TPT"}
    order = ["budget", "expenditure", "notifications", "outcomes",
             "contact_tpt", "laboratory"]

    rows = list(csv.DictReader((ROOT / "outputs" / "d2_variable_screen.csv")
                               .open(encoding="utf-8")))
    allp, nz = defaultdict(list), defaultdict(list)
    for r in rows:
        if r["dataset"] not in labels or not r["repetition"]:
            continue
        allp[r["dataset"]].append(float(r["repetition"]) * 100)
        if r["repetition_nz"]:
            nz[r["dataset"]].append(float(r["repetition_nz"]) * 100)

    fig, axes = plt.subplots(1, 2, figsize=(WIDTH_IN, WIDTH_IN * 0.50),
                             sharey=True)
    for ax, data, title in (
            (axes[0], allp, "All adjacent country-year pairs"),
            (axes[1], nz, "Excluding pairs where both values are zero")):
        for i, key in enumerate(order):
            vals = data.get(key, [])
            if not vals:
                continue
            colour = ORANGE if key == "laboratory" else BLUE
            ax.scatter(vals, [i] * len(vals), s=55, alpha=0.45,
                       color=colour, edgecolors="none", zorder=2)
            med = sorted(vals)[len(vals) // 2] if len(vals) % 2 else \
                sum(sorted(vals)[len(vals) // 2 - 1:len(vals) // 2 + 1]) / 2
            ax.plot([med], [i], marker="|", markersize=30, markeredgewidth=4,
                    color=INK, zorder=4)
            ax.annotate(f"{med:.1f}%", (med, i), textcoords="offset points",
                        xytext=(0, 16), ha="center", fontsize=13, color=INK)
        ax.set_yticks(range(len(order)))
        ax.set_yticklabels([labels[k] for k in order], fontsize=14)
        ax.set_xlim(-3, 103)
        ax.set_xlabel("Variables repeating the previous year's value, %")
        ax.set_title(title, fontsize=15, pad=26)
        ax.grid(axis="x", color="#ededed", linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
    axes[0].set_ylim(-0.7, len(order) - 0.3)
    save(fig, "figure_b1_repetition_by_dataset.png")


if __name__ == "__main__":
    print("writing figures at 300 dpi:")
    figure_a1()
    figure_b1()
