from __future__ import annotations

import os
import csv
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-codex")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
SUPP_DIR = ROOT / "figures" / "supplementary"
SVG_DIR = ROOT / "figures_svg_editable" / "final_figures"
SOURCE_DIR = ROOT / "source_data"

COLORS = {
    "ink": "#17212B",
    "muted": "#5D6874",
    "grid": "#E5E9ED",
    "blue": "#2F5F83",
    "blue2": "#86AEC7",
    "teal": "#2E7C6B",
    "rose": "#B96B78",
    "rose_dark": "#8F4F5A",
    "grey": "#B8C4CF",
    "ref": "#8F9BA7",
}

plt.rcParams.update(
    {
        "font.family": "Nimbus Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.linewidth": 0.75,
    }
)


def save(fig: plt.Figure, stem: str) -> None:
    SUPP_DIR.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = SUPP_DIR / f"{stem}.pdf"
    svg_path = SVG_DIR / f"{stem}.svg"
    fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.025)
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.025)
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


def save_main(fig: plt.Figure, stem: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = FIG_DIR / f"{stem}.pdf"
    svg_path = SVG_DIR / f"{stem}.svg"
    fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.025)
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.025)
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


def _float(value: str) -> float:
    return float(value) if value not in {"", "nan", "None"} else np.nan


def make_around_first_scaffolded() -> None:
    order = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    rows = {}
    with open(SOURCE_DIR / "appendix_d_source_data.csv", newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["figure"] == "Appendix D1":
                rows[row["setting"]] = row

    settings = [s for s in order if s in rows]
    values = np.array([_float(rows[s]["estimate"]) for s in settings])
    ci = np.array([[_float(rows[s]["ci_low"]), _float(rows[s]["ci_high"])] for s in settings])
    y = np.arange(len(settings))
    colors = [COLORS["teal"] if v >= 0 else COLORS["rose"] for v in values]

    fig, ax = plt.subplots(figsize=(6.35, 3.15))
    ax.set_axisbelow(True)
    ax.axvline(0, color=COLORS["ref"], lw=0.9, ls=(0, (2.2, 2.2)), zorder=1)
    ax.barh(y, values, height=0.34, color=colors, edgecolor="white", linewidth=0.8, zorder=2)
    ax.errorbar(
        values,
        y,
        xerr=np.vstack([values - ci[:, 0], ci[:, 1] - values]),
        fmt="none",
        ecolor=COLORS["ink"],
        elinewidth=0.85,
        capsize=2.2,
        capthick=0.8,
        zorder=4,
    )
    for yi, val in zip(y, values):
        label_x = val + (0.18 if val >= 0 else -0.18)
        ax.text(
            label_x,
            yi,
            f"{val:+.1f} pp",
            ha="left" if val >= 0 else "right",
            va="center",
            fontsize=8.2,
            color=COLORS["ink"],
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.86, pad=0.12),
            zorder=5,
        )
    ax.set_yticks(y, settings)
    ax.invert_yaxis()
    ax.set_xlabel("After - before first scaffolded turn (pp)")
    ax.set_xlim(-5.3, 3.2)
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.75, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="both", labelsize=8.0)
    ax.text(-0.12, 1.05, "a", transform=ax.transAxes, fontsize=13, weight="bold")
    save(fig, "ExtendedDataFigure1_around_first_scaffolded")


def make_intent_moderation() -> None:
    order = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    rows = {("intentional", s): None for s in order}
    rows.update({("unintentional", s): None for s in order})
    with open(SOURCE_DIR / "figure3_source_data.csv", newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["figure"] == "Figure 3" and row["panel"] == "c" and row["measure"] == "Poisson count ratio":
                rows[(row["group"], row["setting"])] = row

    y = np.arange(len(order))
    offset = 0.12
    groups = [
        ("intentional", -offset, COLORS["blue"], "Intentional"),
        ("unintentional", offset, COLORS["grey"], "Unintentional"),
    ]

    fig, ax = plt.subplots(figsize=(6.35, 3.35))
    ax.set_axisbelow(True)
    ax.axvline(1.0, color=COLORS["ref"], lw=0.9, ls=(0, (2.2, 2.2)), zorder=1)
    for group, dy, color, label in groups:
        vals = np.array([_float(rows[(group, s)]["estimate"]) for s in order])
        ci = np.array([[_float(rows[(group, s)]["ci_low"]), _float(rows[(group, s)]["ci_high"])] for s in order])
        yy = y + dy
        ax.errorbar(
            vals,
            yy,
            xerr=np.vstack([vals - ci[:, 0], ci[:, 1] - vals]),
            fmt="none",
            ecolor=color,
            elinewidth=0.85,
            capsize=2.2,
            capthick=0.8,
            zorder=3,
        )
        ax.scatter(vals, yy, s=30, color=color, edgecolor=COLORS["ink"], lw=0.45, label=label, zorder=4)
    ax.set_yticks(y, order)
    ax.invert_yaxis()
    ax.set_xlabel("Poisson count ratio for scaffolded support")
    ax.set_xlim(0.85, 3.12)
    ax.set_xticks([1.0, 1.5, 2.0, 2.5, 3.0])
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.75, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="both", labelsize=8.0)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.62, 1.16),
        frameon=False,
        ncol=2,
        handlelength=1.1,
        columnspacing=1.0,
    )
    ax.text(-0.12, 1.05, "a", transform=ax.transAxes, fontsize=13, weight="bold")
    save(fig, "ExtendedDataFigure2_intent_moderates_support_effect")


def make_temporal_coupling() -> None:
    settings = ["WC coding", "WC writing"]
    lift = np.array([2.6756, 1.1281])
    lift_ci = np.array([[2.2904, 3.0607], [0.9487, 1.3075]])
    before_after = np.array([1.4, -4.2])
    before_after_ci = np.array([[0.9496, 1.7999], [-4.6790, -3.8188]])

    state_rows = [
        ("prior constructive", "WC coding", 26.0563, 24.5124, 27.6619, 30.0682, 28.8784, 31.2854),
        ("prior constructive", "WC writing", 6.0528, 5.0744, 7.2055, 12.3195, 10.5635, 14.3206),
        ("prior active", "WC coding", 9.6341, 9.2175, 10.0673, 11.7894, 11.3335, 12.2611),
        ("prior active", "WC writing", 1.9286, 1.6596, 2.2403, 2.5838, 2.2383, 2.9809),
        ("prior passive", "WC coding", 12.9630, 9.4704, 17.4946, 15.0327, 10.2307, 21.5475),
        ("prior passive", "WC writing", 2.1182, 1.3602, 3.2845, 3.5857, 1.8977, 6.6729),
    ]
    next_s2 = np.array([[65.4814, 50.7089, 29.5189], [37.7753, 43.1958, 18.7938]])

    ref_color = COLORS["grey"]
    scaf_color = COLORS["teal"]
    ref_err = "#7E8B97"
    scaf_err = "#2F6F61"

    def xerr(value: float, low: float, high: float) -> np.ndarray:
        return np.array([[value - low], [high - value]])

    fig = plt.figure(figsize=(7.45, 4.95))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.04, 0.82], width_ratios=[0.94, 1.34, 1.10], hspace=0.76, wspace=0.66)
    axa = fig.add_subplot(gs[0, 0])
    axb = fig.add_subplot(gs[0, 1:])
    axc = fig.add_subplot(gs[1, :2])
    axd = fig.add_subplot(gs[1, 2])

    y = np.arange(len(settings))
    axa.barh(y, lift, height=0.28, color=scaf_color, edgecolor="none", zorder=2)
    axa.errorbar(lift, y, xerr=np.vstack([lift - lift_ci[:, 0], lift_ci[:, 1] - lift]), fmt="none", ecolor=COLORS["ink"], elinewidth=0.75, capsize=2.1, capthick=0.75, zorder=4)
    for i, val in enumerate(lift):
        axa.text(val - 0.12, i, f"{val:+.1f} pp", va="center", ha="right", fontsize=7.3, color="white", bbox=dict(facecolor=scaf_color, edgecolor="none", pad=0.15), zorder=5)
    axa.axvline(0, color=COLORS["ink"], lw=0.9)
    axa.set_yticks(y, settings)
    axa.set_ylim(len(settings) - 0.45, -0.55)
    axa.set_xlim(-0.25, 3.35)
    axa.set_xlabel("Next-turn constructive lift (pp)")
    axa.set_title("Overall adjacent-turn\ncontrast", loc="left", pad=7, fontsize=9.2, fontweight="bold")
    axa.grid(axis="x", color=COLORS["grid"], lw=0.65)
    axa.spines[["top", "right"]].set_visible(False)
    axa.tick_params(axis="both", labelsize=7.2)
    axa.text(-0.24, 1.08, "a", transform=axa.transAxes, fontsize=13, weight="bold")

    b_y = np.array([5.0, 4.25, 2.95, 2.20, 0.90, 0.15])
    b_labels = ["coding", "writing", "coding", "writing", "coding", "writing"]
    group_centres = [4.625, 2.575, 0.525]
    group_labels = ["prior\nconstructive", "prior\nactive", "prior\npassive"]
    axb.axvline(0, color=COLORS["grid"], lw=0.8, zorder=0)
    for idx, (state, setting, s1, s1_low, s1_high, s2, s2_low, s2_high) in enumerate(state_rows):
        yy = b_y[idx]
        axb.plot([s1, s2], [yy, yy], color="#CDD4DB", lw=1.0, zorder=1)
        axb.errorbar(s1, yy - 0.07, xerr=xerr(s1, s1_low, s1_high), fmt="none", ecolor=ref_err, elinewidth=0.7, capsize=1.7, capthick=0.7, zorder=2)
        axb.errorbar(s2, yy + 0.07, xerr=xerr(s2, s2_low, s2_high), fmt="none", ecolor=scaf_err, elinewidth=0.7, capsize=1.7, capthick=0.7, zorder=2)
        axb.scatter(s1, yy - 0.07, s=23, color=ref_color, edgecolor=COLORS["ink"], lw=0.45, zorder=3)
        axb.scatter(s2, yy + 0.07, s=23, color=scaf_color, edgecolor=COLORS["ink"], lw=0.45, zorder=3)
        axb.text(min(s2 + 1.0, 34.0), yy + 0.07, f"{s2 - s1:+.1f} pp", va="center", fontsize=6.8, color=COLORS["ink"], bbox=dict(facecolor="white", edgecolor="none", alpha=0.88, pad=0.10), zorder=5)
    for yc, label in zip(group_centres, group_labels):
        axb.text(-5.7, yc, label, ha="right", va="center", fontsize=7.2, color=COLORS["muted"], fontweight="bold", clip_on=False)
    for sep in [3.58, 1.48]:
        axb.axhline(sep, color=COLORS["grid"], lw=0.75, zorder=0)
    axb.set_yticks(b_y, b_labels)
    axb.set_ylim(-0.45, 5.55)
    axb.set_xlim(0, 35)
    axb.set_xticks([0, 10, 20, 30])
    axb.set_xlabel("P(next constructive turn) (%)")
    axb.set_title("Adjacent-turn contrast by prior user state", loc="left", pad=7, fontsize=9.2, fontweight="bold")
    axb.grid(axis="x", color=COLORS["grid"], lw=0.65)
    axb.spines[["top", "right"]].set_visible(False)
    axb.tick_params(axis="both", labelsize=7.0)
    axb.text(-0.20, 1.08, "b", transform=axb.transAxes, fontsize=13, weight="bold")
    axb.legend(
        [
            Line2D([0], [0], marker="o", linestyle="None", markerfacecolor=ref_color, markeredgecolor=COLORS["ink"], markeredgewidth=0.45, markersize=5.0),
            Line2D([0], [0], marker="o", linestyle="None", markerfacecolor=scaf_color, markeredgecolor=COLORS["ink"], markeredgewidth=0.45, markersize=5.0),
        ],
        ["non-scaffolded reference", "scaffolded support"],
        loc="upper right",
        bbox_to_anchor=(1.00, 1.36),
        frameon=False,
        ncol=2,
        handletextpad=0.35,
        columnspacing=0.8,
        fontsize=7.0,
    )

    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("s2", ["#F4F7F6", "#A8C8BD", "#2F7C68"])
    axc.imshow(next_s2, cmap=cmap, norm=matplotlib.colors.Normalize(0, 75), aspect="auto")
    axc.set_xticks(np.arange(3), ["prior\nconstructive", "prior\nactive", "prior\npassive"])
    axc.set_yticks(np.arange(len(settings)), settings)
    axc.set_title("P(next assistant scaffolded | prior user state)", loc="left", pad=6, fontsize=9.2, fontweight="bold")
    axc.set_xticks(np.arange(-0.5, 3, 1), minor=True)
    axc.set_yticks(np.arange(-0.5, len(settings), 1), minor=True)
    axc.grid(which="minor", color="white", linewidth=1.1)
    axc.tick_params(axis="both", which="both", length=0)
    axc.tick_params(axis="both", labelsize=7.4)
    for sp in axc.spines.values():
        sp.set_visible(False)
    for i in range(next_s2.shape[0]):
        for j in range(next_s2.shape[1]):
            val = next_s2[i, j]
            axc.text(j, i, f"{val:.1f}%", ha="center", va="center", fontsize=7.6, color="white" if val > 50 else COLORS["ink"])
    axc.text(-0.10, 1.08, "c", transform=axc.transAxes, fontsize=13, weight="bold")

    d_colors = [scaf_color if val >= 0 else COLORS["rose"] for val in before_after]
    axd.barh(y, before_after, height=0.28, color=d_colors, edgecolor="none", zorder=2)
    for i, val in enumerate(before_after):
        axd.errorbar(val, y[i], xerr=xerr(val, before_after_ci[i, 0], before_after_ci[i, 1]), fmt="none", ecolor=COLORS["ink"], elinewidth=0.75, capsize=2.1, capthick=0.75, zorder=4)
        label_x = val + 0.18 if val >= 0 else val + 0.25
        axd.text(label_x, i, f"{val:+.1f} pp", va="center", ha="left", fontsize=7.3, bbox=dict(facecolor="white", edgecolor="none", alpha=0.88, pad=0.12), zorder=5)
    axd.axvline(0, color=COLORS["ink"], lw=0.9)
    axd.set_yticks(y, settings)
    axd.set_ylim(len(settings) - 0.45, -0.55)
    axd.set_xlim(-5.05, 2.05)
    axd.set_xlabel("After - before first scaffolded turn (pp)")
    axd.set_title("Coarse within-conversation contrast", loc="left", pad=6, fontsize=9.2, fontweight="bold")
    axd.grid(axis="x", color=COLORS["grid"], lw=0.65)
    axd.spines[["top", "right"]].set_visible(False)
    axd.tick_params(axis="both", labelsize=7.4)
    axd.text(-0.12, 1.08, "d", transform=axd.transAxes, fontsize=13, weight="bold")

    fig.subplots_adjust(left=0.110, right=0.985, top=0.840, bottom=0.140)
    fig.text(0.50, 0.038, "WC = WildChat. Error bars show 95% CI where displayed; numbers report scaffolded - reference differences.", ha="center", fontsize=6.8, color=COLORS["muted"])
    save_main(fig, "fig_temporal_coupling_scale_compact_final_v5")


def main() -> None:
    make_around_first_scaffolded()
    make_intent_moderation()


if __name__ == "__main__":
    main()
