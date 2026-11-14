"""Generate the figures for both manuscripts.

This is the ONLY directory in the repository with a third-party dependency.
`src/` and `demos/` are standard library only, so that every number in both
papers regenerates on a bare Python install; drawing is a different job and
matplotlib is not worth reimplementing. The figures are derived from the same
files and the same code paths as the tables, never from retyped numbers.

Output: PNG at DPI below, at least 3600 pixels wide, as the International
Journal of Epidemiology requires (minimum 300 dpi at a minimum width of 300 mm);
paper A's figures are also written as 600 dpi LZW-compressed TIFF for the
Indian Journal of Tuberculosis.

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
# Drawn at about IJE's stated 300 mm width and rendered at 360 dpi, so the file
# exceeds the 3600-pixel minimum while the text stays large relative to the
# figure. An earlier 15.5 in canvas met the pixel rule but shrank 14 pt labels
# to about 6 pt at a 170 mm print width -- the "large figures with tiny labels"
# the journal's guidelines warn against. PRINT_MIN_PT is asserted in save().
DPI = 400
WIDTH_IN = 12.0
PRINT_WIDTH_IN = 170 / 25.4            # full-page width in print
PRINT_MIN_PT = 7.0
TIFF_DPI = 600                         # paper A's IJTB print masters

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
    # Smallest text in the figure, in points, before it is saved.
    fig.canvas.draw()
    sizes = [t.get_fontsize() for t in fig.findobj(matplotlib.text.Text)
             if t.get_text().strip() and t.get_visible()]
    smallest = min(sizes) if sizes else 0
    # No two pieces of text may overlap. Paper B's two panel axis labels once
    # ran into each other and off the canvas; nothing caught it but a look.
    r = fig.canvas.get_renderer()
    texts = [(t, t.get_window_extent(renderer=r)) for t in fig.findobj(matplotlib.text.Text)
             if t.get_text().strip() and t.get_visible()]
    for i, (ta, a) in enumerate(texts):
        for tb, b in texts[i + 1:]:
            w_ = min(a.x1, b.x1) - max(a.x0, b.x0)
            h_ = min(a.y1, b.y1) - max(a.y0, b.y0)
            assert not (w_ > 2 and h_ > 2), (
                f"{name}: text {ta.get_text()[:30]!r} overlaps {tb.get_text()[:30]!r}")
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    # Paper A goes to the Indian Journal of Tuberculosis, whose production
    # takes TIFF print masters; the author's accepted IJTB papers supplied them
    # at 600 dpi, above Elsevier's 500 dpi minimum for line-and-tone artwork.
    # Rendered from the same figure object, so the TIFF cannot drift from the PNG.
    if name.startswith("figure_a"):
        fig.savefig(path.with_suffix(".tif"), dpi=TIFF_DPI, bbox_inches="tight",
                    facecolor="white", pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)
    from PIL import Image
    if name.startswith("figure_a"):
        with Image.open(path.with_suffix(".tif")) as tif:
            dpi = tif.info.get("dpi", (0, 0))
            assert round(dpi[0]) >= TIFF_DPI, f"{name}: TIFF saved at {dpi} dpi"
    with Image.open(path) as im:
        w, h = im.size
    assert w >= 3600, f"{name}: {w}px wide, IJE requires at least 3600"
    # The saved image is w/DPI inches wide; printed at full-page width every
    # font scales by PRINT_WIDTH_IN / (w/DPI).
    printed = smallest * PRINT_WIDTH_IN / (w / DPI)
    assert printed >= PRINT_MIN_PT, (
        f"{name}: smallest text prints at {printed:.1f} pt at 170 mm width; "
        f"minimum is {PRINT_MIN_PT} pt")
    print(f"  {name}: {w} x {h} px at {DPI} dpi; smallest text "
          f"{smallest:.1f} pt prints at {printed:.1f} pt at 170 mm")


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
    # Labels sit above their points. A label just above a local minimum lands
    # on the segment climbing out of it, as "6.0%" did on the steep 2021-2022
    # rise, so minima are lifted clear of both segments. They cannot go below:
    # the WHO series runs along zero with a marker under every year.
    # Endpoints are never minima -- they have only one neighbour.
    for k, (x, y) in enumerate(zip(years, shortfall)):
        is_min = (0 < k < len(shortfall) - 1
                  and y < shortfall[k - 1] and y < shortfall[k + 1])
        ax.annotate(f"{y:.1f}%", (x, y), textcoords="offset points",
                    xytext=(0, 34 if is_min else 13), ha="center",
                    va="bottom", fontsize=13, color=ORANGE)
    # The WHO series is a share of budget REQUIRED, the national series a share
    # of the amount REQUESTED; the axis must not describe only one of them.
    ax.set_ylabel("Gap, % of amount required or requested")
    ax.set_xlabel("Fiscal year")
    ax.set_ylim(-4, max(shortfall) + 12)
    ax.set_xticks(years)
    ax.axhline(0, color=GREY, linewidth=0.8, zorder=1)
    ax.grid(axis="y", color="#e6e6e6", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper left", fontsize=14, handlelength=2.4)
    save(fig, "figure_a1_two_accounts_of_the_same_shortfall.png")


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
def figure_a2() -> None:
    """Paper A: which WHO budget line, if any, each intervention falls into.

    The table states the classification; this shows its shape -- that nine of
    eleven arrows converge on lines shared with other activities, three of
    them on the same one.
    """
    from provenance.existence import (NODE_LABELS, TB_BUDGET_MAPPING,
                                      TB_BUDGET_COMMODITY_ONLY, TB_BUDGET_POOLED,
                                      BUDGET_PROG_ACTIVITIES)

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
        "budget_prog": f"budget_prog\n{BUDGET_PROG_ACTIVITIES} activities pooled",
        "budget_tpt": "budget_tpt\npreventive-treatment drugs",
        "budget_sld": "budget_sld\ndrug-resistant TB drugs",
        "budget_patsup": "budget_patsup\nall patient support",
        "budget_tbhiv": "budget_tbhiv\nTB/HIV activities",
        None: "no WHO budget line",
    }
    # Every condition gets its own line style, so the figure survives greyscale
    # printing and colour-blind reading. Pooled and dominant were once both
    # solid, told apart only by orange against blue -- two colours of nearly
    # equal luminance, which print as the same grey. Pooled is also drawn
    # heavier, since it carries the finding.
    style = {"pooled": (ORANGE, "-", 3.6), "commodity": (BLUE, "--", 2.4),
             "dominant": (BLUE, "-.", 2.4), "none": (GREY, ":", 2.4)}

    def cond(k):
        if TB_BUDGET_MAPPING[k] is None:
            return "none"
        if k in TB_BUDGET_POOLED:
            return "pooled"
        if k in TB_BUDGET_COMMODITY_ONLY:
            return "commodity"
        return "dominant"

    # Interventions are listed in the order of the budget lines they reach, so
    # arrows to the same line sit together and do not cross. Table 2 uses the
    # same order. Nothing is ranked: the classification does not depend on order.
    keys = sorted(NODE_LABELS, key=lambda k: (lines.index(TB_BUDGET_MAPPING[k]),
                                              list(NODE_LABELS).index(k)))
    fig, ax = plt.subplots(figsize=(WIDTH_IN, WIDTH_IN * 0.52))
    ly = {k: len(keys) - 1 - i for i, k in enumerate(keys)}
    ry = {ln: (len(lines) - 1 - i) * (len(keys) - 1) / (len(lines) - 1)
          for i, ln in enumerate(lines)}

    for k in keys:
        c, ls, lw = style[cond(k)]
        ax.annotate("", xy=(0.62, ry[TB_BUDGET_MAPPING[k]]), xytext=(0.16, ly[k]),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=lw,
                                    linestyle=ls, alpha=0.85,
                                    connectionstyle="arc3,rad=0.12"), zorder=2)
        ax.text(0.15, ly[k], short[k], ha="right", va="center", fontsize=14)
    for ln in lines:
        ax.text(0.645, ry[ln], line_label[ln], ha="left", va="center", fontsize=14,
                bbox=dict(boxstyle="round,pad=0.42", facecolor="#f4f4f4",
                          edgecolor=GREY, linewidth=1.2))

    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([], [], color=c, lw=lw, ls=ls, label=lab)
        for (c, ls, lw), lab in (
            (style["pooled"], "Pooled: named by the form inside a line shared with others"),
            (style["commodity"], "Commodity only: the drug or one arm, not the delivery"),
            (style["dominant"], "Dominant: the line's scope is largely this activity"),
            (style["none"], "No line covers the activity"))
    ], frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.02),
        ncol=2, fontsize=13.5)
    ax.set_xlim(-0.52, 1.25)
    ax.set_ylim(-1.4, len(keys) - 0.3)
    ax.axis("off")
    save(fig, "figure_a2_interventions_to_budget_lines.png")


# --------------------------------------------------------------------------
def _d3_results():
    import d3_vintages as d3
    return d3, d3.results()


def figure_b1() -> None:
    """Paper B: from a country's annual return to WHO's published total, with
    the measured share at each step. Every number is read from d3."""
    d3, R = _d3_results()
    util_rst = [r for r in R["restatement"] if r["group"] == "util"]
    lo = min(100 * r["identical"] / r["pairs"] for r in util_rst)
    hi = max(100 * r["identical"] / r["pairs"] for r in util_rst)
    rev = [r for r in R["revision"] if r["group"] == "util"]
    n_pairs, n_changed = sum(r["pairs"] for r in rev), sum(r["changed"] for r in rev)
    f = R["filling"]["2026"]
    used = sum(n for s, n in f.items() if s != "absent")
    supplied = f["filled_earlier"] + f["filled_later"] + f["filled_other"] + f["overridden"]
    last = R["latest"]["2026"]
    c = next(r for r in R["consequence"]["2026"] if r["year"] == last)

    fig, ax = plt.subplots(figsize=(WIDTH_IN, WIDTH_IN * 0.86))
    boxes = []

    def box(x, y, w, h, text, edge=INK, face="white", fs=13.5, hatch=None):
        ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, facecolor=face,
                                   edgecolor=edge, linewidth=1.8, zorder=2, hatch=hatch))
        t = ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=3,
                    bbox=dict(facecolor=face, edgecolor="none", pad=1.5) if hatch else None)
        boxes.append((t, x, y, w, h))

    def arrow(x1, y1, x2, y2, col=INK):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.0), zorder=1)

    def note(x, y, text):
        t = ax.text(x, y, text, ha="left", va="center", fontsize=13, color=INK,
                    style="italic", zorder=3)
        return t

    X, W = 0.38, 0.74
    box(X, 0.94, W, 0.085, "A country's annual return to WHO:\n"
        "visits per patient, share hospitalised, days in hospital", fs=13)
    note(0.78, 0.94, f"{lo:.0f}–{hi:.0f}% of values identical to the\n"
                     "country's own previous year (Table 2)")
    arrow(X, 0.897, X, 0.832)
    box(X, 0.79, W, 0.085, "WHO's published country data,\nrelease after release")
    note(0.78, 0.79, f"{n_changed} of {n_pairs:,} values changed\nbetween releases (Table 1)")
    arrow(X, 0.747, X, 0.682)
    box(X, 0.64, W, 0.085, "WHO's finance pipeline fills each gap from\n"
        "the nearest year: up to 4 earlier, then 4 later")
    note(0.78, 0.64, f"{100 * supplied / used:.1f}% of the values used were\n"
                     f"supplied by WHO, {d3.WINDOW_START}–{last} (Table 3)")
    arrow(X, 0.597, X, 0.532)
    box(X, 0.47, W, 0.115, "Cost model, priced at WHO unit costs:\n"
        "bed-days = patients × share hospitalised × days\n"
        "visits = patients × visits per patient")
    arrow(X, 0.412, X, 0.347)
    box(X, 0.30, W, 0.085, f"Published TB funding, {last}: US$ {c['total'] / 1e9:.2f} billion,\n"
        f"of which care estimate US$ {c['ghs'] / 1e9:.2f} billion ({100 * c['ghs'] / c['total']:.1f}%)")
    shares = (("new inputs", c["new"], BLUE, None), ("restated inputs", c["restated"], ORANGE, "//"),
              ("WHO-supplied inputs", c["WHO-supplied"], GREY, "xx"))
    for x, (lab, val, col, hatch) in zip((0.05, 0.38, 0.71), shares):
        arrow(X, 0.257, x, 0.175, col)
        box(x, 0.12, 0.30, 0.10, f"{lab}\n{100 * val / c['ghs']:.1f}% of care,\n"
                                 f"US$ {val / 1e9:.2f} billion", edge=col, fs=13, hatch=hatch,
            face="white")
    ax.set_xlim(-0.14, 1.24)
    ax.set_ylim(0.04, 1.0)
    ax.axis("off")
    fig.canvas.draw()
    inv = ax.transData.inverted()
    for t, x, y, w, h in boxes:
        bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
        (x0, y0), (x1, y1) = inv.transform(bb.get_points())
        assert abs(x1 - x0) <= w * 0.97 and abs(y1 - y0) <= h * 0.97, (
            f"text overflows its box: {t.get_text()[:40]!r} "
            f"needs {abs(x1 - x0):.3f}x{abs(y1 - y0):.3f}, box is {w}x{h}")
    save(fig, "figure_b1_from_return_to_published_total.png")


def figure_b2() -> None:
    """Paper B: WHO's care estimate each year, split by where its inputs came
    from. Hatching, not colour alone, separates the classes in greyscale."""
    d3, R = _d3_results()
    last = R["latest"]["2026"]
    rows = [r for r in R["consequence"]["2026"] if d3.WINDOW_START <= r["year"] <= last]
    years = [r["year"] for r in rows]
    fig, ax = plt.subplots(figsize=(WIDTH_IN, WIDTH_IN * 0.52), layout="constrained")
    bottom = [0.0] * len(rows)
    for key, lab, col, hatch in (("new", "Inputs newly reported that year", BLUE, None),
                                 ("restated", "Inputs restated from the previous year", ORANGE, "//"),
                                 ("WHO-supplied", "Inputs supplied by WHO", GREY, "xx")):
        vals = [r[key] / 1e9 for r in rows]
        ax.bar(years, vals, bottom=bottom, color="white" if hatch else col, edgecolor=col,
               hatch=hatch, linewidth=1.6, label=lab, width=0.68, zorder=2)
        bottom = [b + v for b, v in zip(bottom, vals)]
    for y, r, top in zip(years, rows, bottom):
        ax.annotate(f"{100 * r['new'] / r['ghs']:.0f}%\nnew", (y, top), textcoords="offset points",
                    xytext=(0, 6), ha="center", va="bottom", fontsize=14, color=BLUE)
    ax.set_ylabel("WHO's care estimate, US$ billion", fontsize=14)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], fontsize=14)
    ax.set_ylim(0, max(bottom) * 1.32)
    ax.grid(axis="y", color="#ededed", linewidth=0.8, zorder=0)
    ax.legend(frameon=False, fontsize=14, loc="upper center", ncol=1,
              bbox_to_anchor=(0.5, 1.0))
    save(fig, "figure_b2_care_estimate_by_provenance.png")


if __name__ == "__main__":
    print(f"writing figures at {DPI} dpi:")
    figure_a1()
    figure_a2()
    figure_b2()
    figure_b1()
