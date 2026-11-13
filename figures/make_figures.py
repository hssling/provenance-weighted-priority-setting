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
    save(fig, "figure_b2_repetition_by_dataset.png")


# --------------------------------------------------------------------------
def figure_a2() -> None:
    """Paper A: which WHO budget line, if any, each intervention falls into.

    The table states the classification; this shows its shape -- that nine of
    eleven arrows converge on lines shared with other activities, three of
    them on the same one.
    """
    from provenance.existence import (NODE_LABELS, TB_BUDGET_MAPPING,
                                      TB_BUDGET_COMMODITY_ONLY, TB_BUDGET_POOLED)

    short = {
        "molecular_dx": "Molecular diagnostics", "airborne_ipc": "Airborne infection control",
        "tpt": "TB preventive therapy", "wgs_dst": "Whole-genome sequencing",
        "acf": "Active case finding", "short_regimen": "Shorter all-oral regimen",
        "bovine_tb": "Bovine TB control", "private_sector": "Private-sector engagement",
        "nutrition": "Nutritional support", "milk_pasteurisation": "Milk pasteurisation",
        "tb_hiv_dm": "TB-HIV-diabetes care",
    }
    lines = ["budget_lab", "budget_prog", "budget_tpt", "budget_sld",
             "budget_patsup", "budget_tbhiv", None]
    line_label = {
        "budget_lab": "budget_lab\nall laboratory costs",
        "budget_prog": "budget_prog\nfourteen activities pooled",
        "budget_tpt": "budget_tpt\npreventive-treatment drugs",
        "budget_sld": "budget_sld\ndrug-resistant TB drugs",
        "budget_patsup": "budget_patsup\nall patient support",
        "budget_tbhiv": "budget_tbhiv\nTB/HIV activities",
        None: "no WHO budget line",
    }
    style = {"pooled": (ORANGE, "-"), "commodity": (BLUE, "--"),
             "dominant": (BLUE, "-"), "none": (GREY, ":")}

    def cond(k):
        if TB_BUDGET_MAPPING[k] is None:
            return "none"
        if k in TB_BUDGET_POOLED:
            return "pooled"
        if k in TB_BUDGET_COMMODITY_ONLY:
            return "commodity"
        return "dominant"

    keys = list(NODE_LABELS)
    fig, ax = plt.subplots(figsize=(WIDTH_IN, WIDTH_IN * 0.52))
    ly = {k: len(keys) - 1 - i for i, k in enumerate(keys)}
    ry = {ln: (len(lines) - 1 - i) * (len(keys) - 1) / (len(lines) - 1)
          for i, ln in enumerate(lines)}

    for k in keys:
        c, ls = style[cond(k)]
        ax.annotate("", xy=(0.62, ry[TB_BUDGET_MAPPING[k]]), xytext=(0.16, ly[k]),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=2.4,
                                    linestyle=ls, alpha=0.85,
                                    connectionstyle="arc3,rad=0.12"), zorder=2)
        ax.text(0.15, ly[k], short[k], ha="right", va="center", fontsize=14)
    for ln in lines:
        ax.text(0.645, ry[ln], line_label[ln], ha="left", va="center", fontsize=14,
                bbox=dict(boxstyle="round,pad=0.42", facecolor="#f4f4f4",
                          edgecolor=GREY, linewidth=1.2))

    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([], [], color=ORANGE, lw=2.4, ls="-", label="Pooled: named by the form inside a line shared with others"),
        Line2D([], [], color=BLUE, lw=2.4, ls="--", label="Commodity only: the drug or one arm, not the delivery"),
        Line2D([], [], color=BLUE, lw=2.4, ls="-", label="Dominant: the line's scope is largely this activity"),
        Line2D([], [], color=GREY, lw=2.4, ls=":", label="No line covers the activity"),
    ], frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.02),
        ncol=2, fontsize=13.5)
    ax.set_xlim(-0.52, 1.25)
    ax.set_ylim(-1.4, len(keys) - 0.3)
    ax.axis("off")
    save(fig, "figure_a2_interventions_to_budget_lines.png")


# --------------------------------------------------------------------------
def figure_b2() -> None:
    """Paper B: how a variable moves through the screen, with the counts."""
    import csv as _csv
    rows = list(_csv.DictReader((ROOT / "outputs" / "d2_variable_screen.csv")
                                .open(encoding="utf-8")))
    n_all = len(rows)
    # A row with no repetition was set aside by S0 or S0b; the two are told
    # apart by distinct values, exactly as screen_column decides them.
    aside = [r for r in rows if r["repetition"] == ""]
    cat = sum(1 for r in aside if int(r["n_distinct"]) <= 5)
    untestable = len(aside) - cat
    verdicts = {v: sum(1 for r in rows if r["verdict"] == v)
                for v in ("measurement-like", "mixed", "estimate-like")}
    n_cont = sum(verdicts.values())

    fig, ax = plt.subplots(figsize=(WIDTH_IN, WIDTH_IN * 0.60))

    boxes = []

    def box(x, y, w, h, text, edge=INK, face="white", fs=14.5):
        ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, facecolor=face,
                                   edgecolor=edge, linewidth=1.8, zorder=2))
        t = ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=3)
        boxes.append((t, x, y, w, h))

    def arrow(x1, y1, x2, y2, c=INK):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=2.0), zorder=1)

    box(0.5, 0.93, 0.52, 0.09,
        f"{n_all} numeric variables\nwith at least 100 observations")
    arrow(0.5, 0.885, 0.5, 0.80)
    box(0.5, 0.755, 0.52, 0.085, "S0  five or fewer distinct values?")
    arrow(0.76, 0.755, 0.90, 0.755, GREY)
    box(1.06, 0.755, 0.30, 0.075, f"categorical\n({cat})", edge=GREY, face="#f4f4f4", fs=13.5)
    arrow(0.5, 0.712, 0.5, 0.635)
    box(0.5, 0.59, 0.52, 0.085, "S0b  any country with adjacent years?")
    arrow(0.76, 0.59, 0.90, 0.59, GREY)
    box(1.06, 0.59, 0.30, 0.075,
        f"untestable\n({untestable})", edge=GREY, face="#f4f4f4", fs=13.5)
    arrow(0.5, 0.547, 0.5, 0.47)
    box(0.5, 0.425, 0.74, 0.105,
        f"{n_cont} continuous variables, each scored on four signatures:\n"
        "repetition  ·  distinct ratio  ·  modal share  ·  roundness")
    arrow(0.5, 0.372, 0.5, 0.30)
    box(0.5, 0.255, 0.44, 0.075, "how many signatures does it trip?")
    for x, lab, n, col in ((0.17, "none or one", verdicts["measurement-like"], BLUE),
                           (0.5, "two", verdicts["mixed"], GREY),
                           (0.83, "three or four", verdicts["estimate-like"], ORANGE)):
        arrow(0.5, 0.217, x, 0.145, col)
        box(x, 0.095, 0.30, 0.095,
            f"{lab}\n{'measurement-like' if col is BLUE else 'mixed' if col is GREY else 'estimate-like'}"
            f"\n({n})", edge=col, fs=13.5)
    ax.set_xlim(0.0, 1.30)
    ax.set_ylim(0.02, 1.0)
    ax.axis("off")
    # Text that spills past its own rectangle is the most common defect in a
    # hand-laid-out diagram and is invisible until someone looks. Checked.
    fig.canvas.draw()
    inv = ax.transData.inverted()
    for t, x, y, w, h in boxes:
        bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
        (x0, y0), (x1, y1) = inv.transform(bb.get_points())
        assert abs(x1 - x0) <= w * 0.97 and abs(y1 - y0) <= h * 0.97, (
            f"text overflows its box: {t.get_text()[:40]!r} "
            f"needs {abs(x1 - x0):.3f}x{abs(y1 - y0):.3f}, box is {w}x{h}")
    save(fig, "figure_b1_screen_flow.png")


if __name__ == "__main__":
    print("writing figures at 300 dpi:")
    figure_a1()
    figure_a2()
    figure_b2()
    figure_b1()
