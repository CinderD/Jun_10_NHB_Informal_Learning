from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-codex")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
SUPP_FIG_DIR = FIG_DIR / "supplementary"
SVG_DIR = ROOT / "figures_svg_editable" / "final_figures"


COLORS = {
    "ink": "#17212B",
    "muted": "#5D6874",
    "grid": "#E5E9ED",
    "blue": "#2F5F83",
    "blue2": "#86AEC7",
    "teal": "#2D8068",
    "teal2": "#89B9AA",
    "gold": "#B87923",
    "gold2": "#F3D79B",
    "rose": "#C86A78",
    "lav": "#7960A8",
    "pale": "#F8F6EF",
    "panel": "#FFFFFF",
    "line": "#D8DEE5",
    "grey": "#BFC7D5",
    "s1": "#B9C3CF",
    "s2": "#2E7C6B",
}

SETTING_COLORS = {
    "WC-Coding": "#2F5F83",
    "WC-Writing": "#86AEC7",
    "CP-Coding": "#C85D7A",
    "CP-Writing": "#E99A83",
}

plt.rcParams.update(
    {
        "font.family": "Nimbus Sans",
        "font.size": 9,
        "axes.titlesize": 11,
        "axes.labelsize": 9.5,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "legend.fontsize": 8.5,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.linewidth": 0.8,
    }
)


def _save(fig: plt.Figure, stem: str) -> None:
    _save_many(fig, [stem])


def _save_many(fig: plt.Figure, stems: list[str]) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    for stem in stems:
        svg_path = SVG_DIR / f"{stem}.svg"
        fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.025)
        fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.025)
        svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
    plt.close(fig)


def _save_supp(fig: plt.Figure, stem: str) -> None:
    SUPP_FIG_DIR.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = SVG_DIR / f"{stem}.svg"
    fig.savefig(SUPP_FIG_DIR / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.025)
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.025)
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n")
    plt.close(fig)


def _clean(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)


def _shadow_box(
    ax,
    xy,
    width,
    height,
    *,
    radius=0.018,
    face="white",
    edge="#D9E0E7",
    lw=0.9,
    shadow=True,
    alpha=1.0,
    zorder=2,
):
    x, y = xy
    if shadow:
        ax.add_patch(
            FancyBboxPatch(
                (x + 0.006, y - 0.007),
                width,
                height,
                boxstyle=f"round,pad=0.008,rounding_size={radius}",
                linewidth=0,
                facecolor="#000000",
                alpha=0.055,
                zorder=zorder - 1,
            )
        )
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        linewidth=lw,
        edgecolor=edge,
        facecolor=face,
        alpha=alpha,
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def _pill(ax, x, y, w, h, text, *, fc, ec=None, color=None, fs=7.5, weight="bold"):
    ec = ec or fc
    color = color or COLORS["ink"]
    _shadow_box(ax, (x, y), w, h, radius=h / 2.5, face=fc, edge=ec, lw=0.7, shadow=False, zorder=5)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color, weight=weight, zorder=6)


def _arrow(ax, xy1, xy2, *, color="#9AA7B3", lw=1.2, rad=0.0, ms=10, zorder=8):
    ax.add_patch(
        FancyArrowPatch(
            xy1,
            xy2,
            arrowstyle="-|>",
            mutation_scale=ms,
            linewidth=lw,
            color=color,
            connectionstyle=f"arc3,rad={rad}",
            zorder=zorder,
        )
    )


def make_figure1() -> None:
    fig, ax = plt.subplots(figsize=(7.7, 4.45))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    _clean(ax)
    ax.set_facecolor("white")

    ax.text(
        0.035,
        0.955,
        "From everyday LLM use to evidence about informal learning",
        ha="left",
        va="center",
        fontsize=12.0,
        weight="bold",
        color=COLORS["ink"],
    )
    ax.text(
        0.035,
        0.918,
        "A behavioural framework linking task ecology, turn-level codes and multi-scale association tests.",
        ha="left",
        va="center",
        fontsize=7.5,
        color=COLORS["muted"],
    )

    # Three major cards.
    left = (0.035, 0.105, 0.285, 0.750)
    mid = (0.360, 0.105, 0.305, 0.750)
    right = (0.705, 0.105, 0.260, 0.750)
    for x, y, w, h in [left, mid, right]:
        _shadow_box(ax, (x, y), w, h, radius=0.018, face="white", edge="#D8E0E7", lw=0.85, shadow=False)

    def card_header(x, y, label, title, subtitle):
        ax.add_patch(Circle((x + 0.033, y + 0.700), 0.014, facecolor="#F1F4F7", edgecolor="#C9D3DD", lw=0.6, zorder=4))
        ax.text(x + 0.033, y + 0.700, label, fontsize=7.2, weight="bold", color=COLORS["ink"], ha="center", va="center", zorder=5)
        ax.text(x + 0.057, y + 0.702, title, fontsize=8.3, weight="bold", color=COLORS["ink"], ha="left", va="center")
        ax.text(x + 0.026, y + 0.632, subtitle, fontsize=6.1, color=COLORS["muted"], ha="left", linespacing=1.15)

    card_header(left[0], left[1], "a", "Interaction ecology", "Natural conversations in public\nchat corpora.")
    card_header(mid[0], mid[1], "b", "Turn-level labels", "Adjacent turns coded as observable\nbehavioural signals.")
    card_header(right[0], right[1], "c", "Inference scales", "Shared labels support descriptive,\nassociational and temporal analyses.")

    # Left card: clean 2-by-2 ecology matrix plus user framing.
    ax.text(0.064, 0.665, "Platform x task setting", fontsize=7.2, weight="bold", color=COLORS["muted"])
    matrix_x, matrix_y = 0.064, 0.420
    cell_w, cell_h = 0.103, 0.085
    for row, platform in enumerate(["WildChat", "LMSYS"]):
        ax.text(matrix_x - 0.003, matrix_y + (1 - row) * cell_h + 0.034, platform, fontsize=6.6, color=COLORS["muted"], ha="right", va="center")
    for col, task in enumerate(["Coding", "Writing"]):
        ax.text(matrix_x + col * cell_w + cell_w / 2, matrix_y + 2 * cell_h + 0.025, task, fontsize=6.6, color=COLORS["muted"], ha="center")
    for row in range(2):
        for col in range(2):
            fc = "#E2F1F7" if col == 0 else "#F4F0FA"
            ec = "#B5D5E2" if col == 0 else "#D1C5E5"
            _shadow_box(
                ax,
                (matrix_x + col * cell_w, matrix_y + (1 - row) * cell_h),
                cell_w - 0.012,
                cell_h - 0.014,
                radius=0.010,
                face=fc,
                edge=ec,
                lw=0.7,
                shadow=False,
            )
    _shadow_box(ax, (0.071, 0.265), 0.210, 0.060, radius=0.014, face="#FFF7E6", edge="#E5BA65", lw=0.7, shadow=False)
    ax.text(0.086, 0.302, "User framing", fontsize=6.9, weight="bold", color=COLORS["gold"])
    ax.text(0.086, 0.280, "Intentional or unintentional learning context", fontsize=6.2, color=COLORS["ink"])
    _shadow_box(ax, (0.071, 0.165), 0.210, 0.052, radius=0.014, face="#FAFBFC", edge="#DFE5EA", lw=0.6, shadow=False)
    ax.text(0.086, 0.192, "Task settings define contextual contrasts.", fontsize=6.4, color=COLORS["muted"], ha="left", va="center")

    # Middle card: timeline.
    for x, label, sub, fc, ec, col in [
        (0.388, "User t-1", "prior state", "#E6F3F8", "#A9C8D7", COLORS["blue"]),
        (0.494, "Assistant t", "support", "#FFF0CE", "#E4B45C", COLORS["gold"]),
        (0.600, "User t+1", "uptake", "#E6F3F8", "#A9C8D7", COLORS["blue"]),
    ]:
        _shadow_box(ax, (x, 0.657), 0.082, 0.076, radius=0.014, face=fc, edge=ec, lw=0.75, shadow=False)
        ax.text(x + 0.010, 0.702, label, fontsize=6.4, weight="bold", color=col)
        ax.text(x + 0.010, 0.676, sub, fontsize=6.1, color=COLORS["ink"], linespacing=1.03)
    _arrow(ax, (0.470, 0.695), (0.494, 0.695), lw=0.9, ms=7, color="#65717C")
    _arrow(ax, (0.576, 0.695), (0.600, 0.695), lw=0.9, ms=7, color="#65717C")

    ax.text(0.390, 0.590, "User codes", fontsize=7.2, weight="bold", color=COLORS["blue"])
    for i, (letter, desc, fc) in enumerate(
        [("A", "active", "#DAECF6"), ("C", "constructive", "#BFE5DD"), ("P", "passive", "#EDF2F6")]
    ):
        cy = 0.545 - i * 0.053
        ax.add_patch(Circle((0.407, cy), 0.014, facecolor=fc, edgecolor="#8CB6CC", linewidth=0.7))
        ax.text(0.407, cy, letter, ha="center", va="center", fontsize=6.4, weight="bold", color=COLORS["blue"])
        ax.text(0.432, cy, desc, ha="left", va="center", fontsize=6.4, color=COLORS["ink"])

    ax.text(0.522, 0.590, "Assistant codes", fontsize=7.2, weight="bold", color=COLORS["gold"], ha="left")
    _pill(ax, 0.522, 0.528, 0.065, 0.032, "reference", fc="#F7F9FB", ec="#C7D0DA", color=COLORS["muted"], fs=5.9)
    _pill(ax, 0.597, 0.528, 0.068, 0.032, "scaffold", fc="#FFF0CE", ec="#E4B45C", color=COLORS["gold"], fs=5.7)
    ax.text(0.522, 0.482, "Support forms", fontsize=6.8, weight="bold", color=COLORS["gold"])
    for i, lab in enumerate(["M1 feedback", "M2 hint", "M3 instruct", "M4 explain", "M5 model", "M6 question"]):
        col = i % 2
        row = i // 2
        _pill(
            ax,
            0.522 + col * 0.073,
            0.445 - row * 0.038,
            0.067,
            0.026,
            lab,
            fc="#FFFBF2",
            ec="#E7C582",
            color=COLORS["ink"],
            fs=5.25,
            weight="normal",
        )
    _shadow_box(ax, (0.392, 0.165), 0.235, 0.052, radius=0.014, face="#FAFBFC", edge="#DFE5EA", lw=0.6, shadow=False)
    ax.text(
        0.405,
        0.192,
        "Labels are behavioural signatures, not outcomes.",
        fontsize=6.3,
        color=COLORS["muted"],
        ha="left",
        va="center",
    )

    # Right card: evidence modules.
    modules = [
        (0.728, 0.620, "#E7F2F7", "#BCD6E2", "Prevalence", "Engagement signatures\nacross settings.", "bars"),
        (0.728, 0.455, "#FFF0CE", "#E8C679", "Support association", "Scaffolding aligned with\nconstructive participation.", "network"),
        (0.728, 0.290, "#F0EAF7", "#D2C6E4", "Local coupling", "Scaffolding predicts\nnext-turn engagement.", "couple"),
    ]
    for x, y, fc, ec, title, desc, icon in modules:
        _shadow_box(ax, (x, y), 0.212, 0.112, radius=0.014, face=fc, edge=ec, lw=0.7, shadow=False)
        ax.text(x + 0.070, y + 0.082, title, fontsize=6.35, weight="bold", color=COLORS["ink"])
        ax.text(x + 0.070, y + 0.043, desc, fontsize=5.2, color=COLORS["muted"], linespacing=1.08)
        if icon == "bars":
            for j, bh in enumerate([0.055, 0.040, 0.026]):
                ax.add_patch(Rectangle((x + 0.023 + j * 0.018, y + 0.028), 0.010, bh, facecolor="#5A8EAA", edgecolor="none"))
            ax.plot([x + 0.016, x + 0.068], [y + 0.026, y + 0.026], color="#7FA6BA", lw=0.8)
        elif icon == "network":
            pts = [(x + 0.030, y + 0.067), (x + 0.055, y + 0.083), (x + 0.060, y + 0.045), (x + 0.038, y + 0.035)]
            for p1, p2 in [(pts[0], pts[1]), (pts[0], pts[2]), (pts[0], pts[3]), (pts[2], pts[1])]:
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#C79B4A", lw=0.9)
            for p in pts:
                ax.add_patch(Circle(p, 0.009, facecolor="#A8792D", edgecolor="white", lw=0.5))
        else:
            xs = [x + 0.024, x + 0.045, x + 0.066]
            for xx in xs:
                ax.add_patch(Circle((xx, y + 0.067), 0.010, facecolor="#F6F2FB", edgecolor=COLORS["lav"], lw=0.7))
            _arrow(ax, (xs[0] + 0.010, y + 0.067), (xs[1] - 0.010, y + 0.067), lw=0.8, ms=6, color=COLORS["lav"])
            _arrow(ax, (xs[1] + 0.010, y + 0.067), (xs[2] - 0.010, y + 0.067), lw=0.8, ms=6, color=COLORS["lav"])
            ax.text(x + 0.019, y + 0.028, "Scaf. -> C", fontsize=6.1, weight="bold", color=COLORS["lav"])

    _arrow(ax, (0.322, 0.500), (0.358, 0.500), color="#A7B2BC", lw=1.2, ms=10)
    _arrow(ax, (0.668, 0.500), (0.705, 0.500), color="#A7B2BC", lw=1.2, ms=10)

    _save(fig, "fig1_analytic_framework_final")


def make_figure2() -> None:
    labels = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    active = np.array([80.4, 86.4, 62.0, 79.5, 82.7, 69.7])
    constructive = np.array([18.4, 12.0, 33.7, 13.6, 10.0, 15.7])
    passive = np.array([1.2, 1.6, 4.3, 6.9, 7.3, 14.6])
    cog_intent = np.array([76.6, 72.6, 73.8, 28.2, 28.2, 46.4])
    cog_unintent = np.array([32.5, 25.3, 28.0, 10.5, 10.3, 24.9])
    con_intent = np.array([13.1, 8.0, 22.0, 5.2, 3.5, 7.2])
    con_unintent = np.array([5.7, 3.6, 9.2, 1.5, 1.0, 3.2])
    depth = {
        "WC coding": [0.151, 0.286, 0.463],
        "LMSYS coding": [0.095, 0.205, 0.339],
        "SC coding": [0.278, 0.434, 0.613],
        "WC writing": [0.060, 0.092, 0.150],
        "LMSYS writing": [0.033, 0.063, 0.112],
        "SC writing": [0.076, 0.182, 0.313],
    }

    fig = plt.figure(figsize=(7.85, 4.95))
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1.22, 0.76], width_ratios=[1.12, 1.18], hspace=0.74, wspace=0.42)
    axa = fig.add_subplot(gs[0, 0])
    gs_b = gs[0, 1].subgridspec(1, 2, wspace=0.28)
    axb1 = fig.add_subplot(gs_b[0, 0])
    axb2 = fig.add_subplot(gs_b[0, 1])
    axc = fig.add_subplot(gs[1, :])

    y = np.arange(len(labels))
    axa.barh(y, constructive, color=COLORS["teal"], edgecolor="white", linewidth=0.8, height=0.60, label="Constructive")
    axa.barh(y, active, left=constructive, color="#9DC4D5", edgecolor="white", linewidth=0.8, height=0.60, label="Active")
    axa.barh(y, passive, left=constructive + active, color="#D7DADF", edgecolor="white", linewidth=0.8, height=0.60, label="Passive")
    for i in range(len(labels)):
        axa.text(constructive[i] / 2, i, f"{constructive[i]:.1f}", ha="center", va="center", fontsize=8.0, color="white")
        axa.text(constructive[i] + active[i] / 2, i, f"{active[i]:.1f}", ha="center", va="center", fontsize=8.0, color=COLORS["ink"])
    axa.set_yticks(y, labels)
    axa.invert_yaxis()
    axa.set_xlim(0, 100)
    axa.set_xlabel("Share of cognitively engaged turns (%)")
    axa.set_title("")
    axa.grid(axis="x", color=COLORS["grid"], linewidth=0.8)
    axa.set_axisbelow(True)
    axa.spines[["top", "right", "left"]].set_visible(False)
    axa.tick_params(axis="y", length=0, pad=2)

    comp_handles = [
        Rectangle((0, 0), 1, 1, facecolor=COLORS["teal"], edgecolor=COLORS["ink"], linewidth=0.55),
        Rectangle((0, 0), 1, 1, facecolor="#8BB8CC", edgecolor=COLORS["ink"], linewidth=0.55),
        Rectangle((0, 0), 1, 1, facecolor="#DADADA", edgecolor=COLORS["ink"], linewidth=0.55),
    ]

    def intent_dumbbell(ax, left_vals, right_vals, title, xlim, show_y=False):
        yy = np.arange(len(labels))
        for i, name in enumerate(labels):
            ax.plot([left_vals[i], right_vals[i]], [i, i], color="#C7D0D8", lw=2.0, zorder=1)
            ax.scatter(left_vals[i], i, s=38, color=COLORS["grey"], edgecolor="white", linewidth=0.7, zorder=3)
            ax.scatter(right_vals[i], i, s=38, color="#2D71B8", edgecolor="white", linewidth=0.7, zorder=3)
            ax.text(right_vals[i] + xlim[1] * 0.035, i, f"+{right_vals[i] - left_vals[i]:.1f}", fontsize=7.2, ha="left", va="center", color=COLORS["ink"])
        ax.set_yticks(yy, labels if show_y else [])
        ax.invert_yaxis()
        ax.set_xlim(*xlim)
        ax.set_title(title, loc="center", pad=7, fontsize=8.6, weight="bold")
        ax.set_xlabel("User-turn rate (%)", fontsize=7.5)
        ax.grid(axis="x", color=COLORS["grid"], linewidth=0.8)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0, pad=2)
        ax.tick_params(axis="x", labelsize=7.5)

    intent_dumbbell(axb1, cog_unintent, cog_intent, "Cognitive", (0, 86), show_y=True)
    intent_dumbbell(axb2, con_unintent, con_intent, "Constructive", (0, 25.5), show_y=False)
    intent_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor="#2D71B8", markeredgecolor="white", markersize=5.6),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS["grey"], markeredgecolor="white", markersize=5.6),
    ]

    depth_matrix = np.array(list(depth.values()))
    cmap = LinearSegmentedColormap.from_list("depth", ["#F3F6F6", "#A8C8D7", "#2F5F83"])
    axc.imshow(depth_matrix, cmap=cmap, norm=Normalize(0.03, 0.62), aspect="auto")
    axc.set_xticks(np.arange(3), ["2-3\nuser turns", "4-6\nuser turns", "7+\nuser turns"], fontsize=8.0)
    axc.set_yticks(np.arange(len(labels)), labels)
    axc.set_xlabel("Conversation length", fontweight="bold", labelpad=3)
    axc.set_ylabel("Setting", labelpad=5)
    axc.set_title("")
    axc.set_xticks(np.arange(-0.5, 3, 1), minor=True)
    axc.set_yticks(np.arange(-0.5, len(labels), 1), minor=True)
    axc.grid(which="minor", color="white", linewidth=1.2)
    axc.tick_params(axis="both", which="both", length=0)
    for sp in axc.spines.values():
        sp.set_visible(False)
    for i in range(depth_matrix.shape[0]):
        for j in range(depth_matrix.shape[1]):
            val = depth_matrix[i, j]
            axc.text(j, i, f"{val * 100:.1f}%", ha="center", va="center", fontsize=8.3, color="white" if val > 0.30 else COLORS["ink"])
    for tick in axc.get_xticklabels():
        tick.set_fontweight("bold")
    fig.subplots_adjust(left=0.105, right=0.985, top=0.805, bottom=0.165)
    top_row_y = max(axa.get_position().y1, axb1.get_position().y1, axb2.get_position().y1) + 0.080
    top_legend_y = top_row_y - 0.040
    a_center = (axa.get_position().x0 + axa.get_position().x1) / 2
    b_center = (axb1.get_position().x0 + axb2.get_position().x1) / 2
    c_center = (axc.get_position().x0 + axc.get_position().x1) / 2
    c_title_y = axc.get_position().y1 + 0.048
    fig.text(axa.get_position().x0 - 0.030, top_row_y, "a", fontsize=14, weight="bold", ha="right", va="center")
    fig.text(a_center, top_row_y, "Engagement composition", fontsize=9.3, weight="bold", ha="center", va="center", color=COLORS["ink"])
    fig.text(axb1.get_position().x0 - 0.030, top_row_y, "b", fontsize=14, weight="bold", ha="right", va="center")
    fig.text(b_center, top_row_y, "Explicit user framing", fontsize=9.3, weight="bold", ha="center", va="center", color=COLORS["ink"])
    fig.text(axc.get_position().x0 - 0.020, c_title_y, "c", fontsize=14, weight="bold", ha="right", va="center")
    fig.text(c_center, c_title_y, "Conversations with ≥1 constructive turn", fontsize=9.3, weight="bold", ha="center", va="center", color=COLORS["ink"])
    fig.legend(comp_handles, ["Constructive", "Active", "Passive"], loc="center", bbox_to_anchor=(a_center, top_legend_y), ncol=3, frameon=False, handlelength=1.0, columnspacing=0.75, fontsize=7.6)
    fig.legend(intent_handles, ["Intent.", "Unintent."], loc="center", bbox_to_anchor=(b_center, top_legend_y), ncol=2, frameon=False, fontsize=7.3, handletextpad=0.2, columnspacing=0.8)
    fig.text(0.985, 0.030, "WC, WildChat; LMSYS, LMSYS Chat; SC, ShareChat.", ha="right", fontsize=7.6, color=COLORS["muted"])

    _save(fig, "fig_engagement_ecology_compact_final")


def make_figure3() -> None:
    labels = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    poisson_color = COLORS["s2"]
    logit_color = COLORS["blue"]
    intentional_color = COLORS["blue"]
    unintentional_color = COLORS["grey"]
    # Turn-weighted constructive user-turn ratios within conversations with
    # versus without scaffolded support. These match Supplementary Table C6.
    no_s2 = np.array([5.5626, 3.9665, 8.9800, 1.7372, 1.0692, 3.4391])
    has_s2 = np.array([10.1265, 6.4707, 16.3192, 2.7293, 2.1567, 6.6385])
    depth_diff = np.array([2.23, 1.42, 3.36, 3.13, 2.10, 3.38])
    pois = np.array([1.852, 1.622, 1.893, 1.569, 1.985, 2.491])
    logit = np.array([1.761, 1.544, 2.140, 1.437, 1.764, 1.757])
    pois_ci = np.array(
        [
            [1.749, 1.961],
            [1.532, 1.717],
            [1.606, 2.231],
            [1.463, 1.682],
            [1.759, 2.240],
            [1.971, 3.150],
        ]
    )
    logit_ci = np.array(
        [
            [1.635, 1.896],
            [1.440, 1.655],
            [1.690, 2.710],
            [1.328, 1.555],
            [1.539, 2.022],
            [1.280, 2.411],
        ]
    )
    strat_intentional = np.array([1.968, 1.672, 2.114, 1.579, 2.334, 1.857])
    strat_unintentional = np.array([1.633, 1.583, 1.681, 1.567, 1.842, 2.235])
    strat_intentional_ci = np.array(
        [
            [1.802, 2.149],
            [1.552, 1.801],
            [1.680, 2.660],
            [1.427, 1.748],
            [1.886, 2.888],
            [1.236, 2.782],
        ]
    )
    strat_unintentional_ci = np.array(
        [
            [1.513, 1.763],
            [1.448, 1.731],
            [1.328, 2.128],
            [1.422, 1.726],
            [1.586, 2.139],
            [1.676, 2.979],
        ]
    )

    fig = plt.figure(figsize=(7.85, 5.65))
    gs = GridSpec(2, 2, figure=fig, width_ratios=[1.04, 1.16], height_ratios=[1.0, 0.88], wspace=0.42, hspace=0.74)
    axa = fig.add_subplot(gs[0, 0])
    axb = fig.add_subplot(gs[0, 1])
    axc = fig.add_subplot(gs[1, 0])
    axd = fig.add_subplot(gs[1, 1])

    def dumbbell(ax, left, right, ylabels, title, xlabel, xlim, diff_fmt="{:+.1f}", scale=1, value_fmt="{:.1f}"):
        y = np.arange(len(ylabels))
        for i in range(len(ylabels)):
            ax.plot([left[i], right[i]], [i, i], color="#B9C2CB", lw=2.4, zorder=1)
            ax.scatter(left[i], i, s=58, color=COLORS["s1"], edgecolor="white", linewidth=0.8, zorder=3)
            ax.scatter(right[i], i, s=58, color=COLORS["s2"], edgecolor="white", linewidth=0.8, zorder=3)
            left_label_y = i + 0.27 if i < len(ylabels) - 1 else i - 0.27
            ax.text(left[i], left_label_y, value_fmt.format(left[i]), fontsize=7.3, ha="center", va="center", color=COLORS["muted"])
            ax.text(right[i], i - 0.27, value_fmt.format(right[i]), fontsize=7.3, ha="center", va="center", color=COLORS["ink"])
            ax.text(right[i] + (xlim[1] - xlim[0]) * 0.04, i, diff_fmt.format((right[i] - left[i]) * scale), fontsize=8.3, ha="left", va="center", color=COLORS["ink"])
        ax.set_yticks(y, ylabels)
        ax.invert_yaxis()
        ax.set_ylim(len(ylabels) - 0.55, -0.85)
        ax.set_xlim(*xlim)
        ax.set_title("")
        ax.set_xlabel(xlabel)
        ax.grid(axis="x", color=COLORS["grid"], lw=0.8)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0, pad=2)

    dumbbell(axa, no_s2, has_s2, labels, "Conversation-level constructive ratio", "Constructive user turns (%)", (0, 18.8))
    a_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS["s1"], markeredgecolor=COLORS["ink"], markersize=6.5),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS["s2"], markeredgecolor=COLORS["ink"], markersize=6.5),
    ]

    y = np.arange(len(labels))
    axb.axvline(1.0, color=COLORS["ink"], lw=1.0)
    for i in range(len(labels)):
        axb.errorbar(
            pois[i],
            i - 0.12,
            xerr=np.array([[pois[i] - pois_ci[i, 0]], [pois_ci[i, 1] - pois[i]]]),
            fmt="none",
            ecolor=COLORS["s2"],
            elinewidth=0.8,
            capsize=2.0,
            capthick=0.8,
            zorder=2,
        )
        axb.errorbar(
            logit[i],
            i + 0.12,
            xerr=np.array([[logit[i] - logit_ci[i, 0]], [logit_ci[i, 1] - logit[i]]]),
            fmt="none",
            ecolor=logit_color,
            elinewidth=0.8,
            capsize=2.0,
            capthick=0.8,
            zorder=2,
        )
        axb.scatter(pois[i], i - 0.12, s=48, color=poisson_color, edgecolor="white", linewidth=0.7, zorder=3)
        axb.scatter(logit[i], i + 0.12, s=48, color=logit_color, edgecolor="white", linewidth=0.7, zorder=3)
        axb.text(min(max(pois_ci[i, 1], logit_ci[i, 1]) + 0.045, 3.22), i, f"{pois[i]:.2f} / {logit[i]:.2f}", va="center", fontsize=7.5, color=COLORS["ink"])
    axb.set_yticks(y, labels)
    axb.invert_yaxis()
    axb.set_ylim(len(labels) - 0.55, -0.85)
    axb.set_xlim(0.94, 3.30)
    axb.set_title("")
    axb.set_xlabel("Association estimate")
    axb.grid(axis="x", color=COLORS["grid"], lw=0.8)
    axb.spines[["top", "right", "left"]].set_visible(False)
    axb.tick_params(axis="y", length=0, pad=2)
    b_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS["s2"], markersize=6.5),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=logit_color, markersize=6.5),
    ]

    yc = np.arange(len(labels))
    axc.axvline(1.0, color=COLORS["ink"], lw=1.0)
    for i in range(len(labels)):
        axc.errorbar(
            strat_intentional[i],
            i - 0.12,
            xerr=np.array([[strat_intentional[i] - strat_intentional_ci[i, 0]], [strat_intentional_ci[i, 1] - strat_intentional[i]]]),
            fmt="none",
            ecolor=intentional_color,
            elinewidth=0.8,
            capsize=2.0,
            capthick=0.8,
            zorder=2,
        )
        axc.errorbar(
            strat_unintentional[i],
            i + 0.12,
            xerr=np.array([[strat_unintentional[i] - strat_unintentional_ci[i, 0]], [strat_unintentional_ci[i, 1] - strat_unintentional[i]]]),
            fmt="none",
            ecolor=unintentional_color,
            elinewidth=0.8,
            capsize=2.0,
            capthick=0.8,
            zorder=2,
        )
        axc.scatter(strat_intentional[i], i - 0.12, s=48, color=intentional_color, edgecolor="white", linewidth=0.7, zorder=3)
        axc.scatter(strat_unintentional[i], i + 0.12, s=48, color=unintentional_color, edgecolor="white", linewidth=0.7, zorder=3)
        axc.text(
            min(max(strat_intentional_ci[i, 1], strat_unintentional_ci[i, 1]) + 0.045, 3.22),
            i,
            f"{strat_intentional[i]:.2f} / {strat_unintentional[i]:.2f}",
            va="center",
            fontsize=7.5,
            color=COLORS["ink"],
        )
    axc.set_yticks(yc, labels)
    axc.invert_yaxis()
    axc.set_ylim(len(labels) - 0.55, -0.85)
    axc.set_xlim(0.94, 3.30)
    axc.set_title("")
    axc.set_xlabel("Poisson count ratio (intentional / unintentional)")
    axc.grid(axis="x", color=COLORS["grid"], lw=0.8)
    axc.spines[["top", "right", "left"]].set_visible(False)
    axc.tick_params(axis="y", length=0, pad=2)
    c_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=intentional_color, markersize=6.5),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=unintentional_color, markersize=6.5),
    ]

    y_depth = np.arange(len(labels))
    axd.axvline(0, color=COLORS["ink"], lw=0.9)
    axd.barh(y_depth, depth_diff, color=COLORS["s2"], edgecolor="white", linewidth=0.8, height=0.56)
    for i, val in enumerate(depth_diff):
        axd.text(val + 0.08, i, f"+{val:.2f}", va="center", ha="left", fontsize=8.2, color=COLORS["ink"])
    axd.set_yticks(y_depth, labels)
    axd.invert_yaxis()
    axd.set_ylim(len(labels) - 0.55, -0.85)
    axd.set_xlim(0, 3.85)
    axd.set_title("")
    axd.set_xlabel("Scaffolded - reference (turns)")
    axd.grid(axis="x", color=COLORS["grid"], lw=0.8)
    axd.spines[["top", "right", "left"]].set_visible(False)
    axd.tick_params(axis="y", length=0, pad=2)

    fig.text(0.985, 0.030, "WC, WildChat; LMSYS, LMSYS Chat; SC, ShareChat.", ha="right", fontsize=7.6, color=COLORS["muted"])
    fig.subplots_adjust(left=0.115, right=0.985, top=0.790, bottom=0.140, hspace=0.86, wspace=0.42)
    top_title_y = max(axa.get_position().y1, axb.get_position().y1) + 0.065
    bottom_title_y = max(axc.get_position().y1, axd.get_position().y1) + 0.065

    def add_panel_header(ax, label, title, y):
        pos = ax.get_position()
        fig.text(pos.x0 - 0.020, y, label, fontsize=14, weight="bold", ha="right", va="center")
        fig.text((pos.x0 + pos.x1) / 2, y, title, fontsize=9.3, weight="bold", ha="center", va="center", color=COLORS["ink"])

    add_panel_header(axa, "a", "Conversation-level constructive ratio", top_title_y)
    add_panel_header(axb, "b", "Adjusted association models", top_title_y)
    add_panel_header(axc, "c", "Framing-stratified association", bottom_title_y)
    add_panel_header(axd, "d", "Post-answer depth", bottom_title_y)
    top_legend_y = max(axa.get_position().y1, axb.get_position().y1) + 0.028
    bottom_legend_y = max(axc.get_position().y1, axd.get_position().y1) + 0.028
    fig.legend(a_handles, ["Ref.", "Scaffolded"], loc="center", bbox_to_anchor=((axa.get_position().x0 + axa.get_position().x1) / 2, top_legend_y), ncol=2, frameon=False, fontsize=8.0, handletextpad=0.3, columnspacing=0.9)
    fig.legend(b_handles, ["Poisson count ratio", "Logit OR"], loc="center", bbox_to_anchor=((axb.get_position().x0 + axb.get_position().x1) / 2, top_legend_y), ncol=2, frameon=False, fontsize=8.0, handletextpad=0.3, columnspacing=0.9)
    fig.legend(c_handles, ["Intent.", "Unintent."], loc="center", bbox_to_anchor=((axc.get_position().x0 + axc.get_position().x1) / 2, bottom_legend_y), ncol=2, frameon=False, fontsize=7.8, handletextpad=0.3, columnspacing=0.65)

    _save_many(fig, ["fig_support_association_compact_final_v2", "fig_support_association_wild_lmsys_with_ci"])


def _support_supply_profile() -> tuple[list[str], list[str], np.ndarray]:
    mean_cols = ["M1", "M2", "M3", "M4", "M5", "M6"]
    settings = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    # Rows are support forms; columns follow the six displayed task settings.
    supply = np.array(
        [
            [8.8, 4.4, 13.3, 16.6, 11.3, 24.2],
            [14.7, 7.6, 12.7, 9.6, 10.9, 23.2],
            [29.7, 9.7, 25.7, 59.2, 52.3, 22.9],
            [84.0, 76.7, 81.2, 29.5, 26.9, 45.2],
            [23.9, 16.5, 18.4, 15.0, 10.3, 23.5],
            [6.9, 13.9, 18.6, 6.9, 13.4, 38.1],
        ]
    )
    return mean_cols, settings, supply


def make_figure4() -> None:
    rows = ["M1\nfeedback", "M2\nhint", "M3\ninstruct", "M4\nexplain", "M5\nmodel", "M6\nquestion"]
    # Estimates compare scaffolded conversations containing each non-exclusive
    # support form with scaffolded conversations without that form, using the
    # constructive ratio. Values are pooled over the six task settings
    # and stratified by the indicated conversational context.
    intentional_effect = np.array([14.68, 3.74, -2.77, 6.67, 0.13, -4.81])
    intentional_low = np.array([13.53, 2.81, -3.44, 6.02, -0.56, -5.56])
    intentional_high = np.array([15.83, 4.67, -2.10, 7.31, 0.82, -4.07])
    unintentional_effect = np.array([6.67, 1.62, -1.04, 3.04, 1.08, -1.28])
    unintentional_low = np.array([5.94, 1.16, -1.34, 2.76, 0.68, -1.59])
    unintentional_high = np.array([7.41, 2.09, -0.74, 3.32, 1.48, -0.96])
    framing_p = np.array([1.77e-30, 6.23e-05, 3.99e-06, 3.86e-24, 2.01e-02, 9.34e-18])

    coding_effect = np.array([12.35, 2.99, 1.59, 4.03, -0.59, -3.96])
    coding_low = np.array([11.38, 2.34, 1.05, 3.56, -1.05, -4.41])
    coding_high = np.array([13.33, 3.64, 2.13, 4.49, -0.13, -3.52])
    writing_effect = np.array([10.93, 3.02, -3.38, 4.30, 6.67, -0.84])
    writing_low = np.array([10.00, 2.36, -3.80, 3.80, 5.76, -1.27])
    writing_high = np.array([11.87, 3.69, -2.95, 4.80, 7.59, -0.42])
    task_p = np.array([3.93e-02, 9.41e-01, 1.23e-45, 4.33e-01, 4.95e-44, 3.71e-23])

    fig = plt.figure(figsize=(7.45, 3.55))
    gs = fig.add_gridspec(1, 2, wspace=0.25)
    ax_framing = fig.add_subplot(gs[0, 0])
    ax_task = fig.add_subplot(gs[0, 1])

    centers = np.arange(len(rows))
    ylim = (-9.4, 21.0)
    y_span = ylim[1] - ylim[0]
    panel_title_kwargs = dict(loc="left", pad=10, fontsize=9.4, fontweight="bold")

    def _style_support_axis(ax: plt.Axes, title: str) -> None:
        ax.axhline(0, color=COLORS["ink"], linewidth=0.9, zorder=1)
        ax.grid(axis="y", color=COLORS["grid"], linewidth=0.75, zorder=0)
        ax.set_ylim(*ylim)
        ax.set_xlim(centers[0] - 0.62, centers[-1] + 0.62)
        ax.set_xticks(centers, rows)
        ax.set_title(title, **panel_title_kwargs)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(axis="x", length=0, pad=5, labelsize=7.5)
        ax.tick_params(axis="y", labelsize=7.6)

    def _bh_fdr(pvals: np.ndarray) -> np.ndarray:
        pvals = np.asarray(pvals, dtype=float)
        order = np.argsort(pvals)
        ranked = pvals[order]
        m = float(len(pvals))
        adjusted_ranked = ranked * m / (np.arange(len(pvals)) + 1)
        adjusted_ranked = np.minimum.accumulate(adjusted_ranked[::-1])[::-1]
        adjusted = np.empty_like(adjusted_ranked)
        adjusted[order] = np.clip(adjusted_ranked, 0, 1)
        return adjusted

    def _q_label(q: float) -> str:
        if q < 0.001:
            return "q<.001"
        return f"q={q:.3f}".replace("0.", ".")

    framing_q = _bh_fdr(framing_p)
    task_q = _bh_fdr(task_p)

    def _draw_bracket(ax: plt.Axes, x0: float, x1: float, y: float, label: str, color: str, above: bool) -> None:
        tick = y_span * 0.010
        if above:
            ys = [y - tick, y, y, y - tick]
            va = "bottom"
            text_y = y + y_span * 0.010
        else:
            ys = [y + tick, y, y, y + tick]
            va = "top"
            text_y = y - y_span * 0.010
        ax.plot([x0, x0, x1, x1], ys, color=color, linewidth=0.95, zorder=5)
        ax.text(
            (x0 + x1) / 2,
            text_y,
            label,
            ha="center",
            va=va,
            fontsize=5.9,
            color=color,
            fontweight="bold",
            linespacing=0.92,
            zorder=6,
        )

    def _draw_grouped_support_panel(
        ax: plt.Axes,
        first_label: str,
        second_label: str,
        first_vals: np.ndarray,
        first_low: np.ndarray,
        first_high: np.ndarray,
        second_vals: np.ndarray,
        second_low: np.ndarray,
        second_high: np.ndarray,
        qvals: np.ndarray,
        title: str,
    ) -> None:
        offsets = np.array([-0.17, 0.17])
        width = 0.29
        specs = [
            (first_label, first_vals, first_low, first_high, COLORS["blue"], offsets[0]),
            (second_label, second_vals, second_low, second_high, COLORS["grey"], offsets[1]),
        ]
        for label, vals, lows, highs, color, offset in specs:
            xpos = centers + offset
            ax.bar(xpos, vals, width=width, color=color, edgecolor="white", linewidth=0.65, zorder=2, label=label)
            ax.errorbar(
                xpos,
                vals,
                yerr=np.vstack([vals - lows, highs - vals]),
                fmt="none",
                ecolor=COLORS["ink"],
                elinewidth=0.78,
                capsize=1.8,
                capthick=0.78,
                zorder=3,
            )
            for xi, val in zip(xpos, vals):
                if val >= 0:
                    y_text = val + 0.43
                    va = "bottom"
                else:
                    y_text = val - 0.43
                    va = "top"
                ax.text(xi, y_text, f"{val:+.1f}", ha="center", va=va, fontsize=5.45, color=COLORS["ink"], zorder=4)

        for i in range(len(centers)):
            delta = first_vals[i] - second_vals[i]
            shown_delta = 0.0 if abs(delta) < 0.05 else delta
            color = COLORS["muted"] if abs(delta) < 0.05 else ("#1B7A4B" if delta >= 0 else "#B4443E")
            above = max(first_high[i], second_high[i]) >= abs(min(first_low[i], second_low[i]))
            if above:
                y = max(first_high[i], second_high[i]) + y_span * 0.075
            else:
                y = min(first_low[i], second_low[i]) - y_span * 0.052
            _draw_bracket(
                ax,
                centers[i] + offsets[0],
                centers[i] + offsets[1],
                y,
                f"Δ={shown_delta:+.1f}\n{_q_label(qvals[i])}",
                color,
                above,
            )

        _style_support_axis(ax, title)
        ax.legend(loc="upper right", frameon=False, ncol=2, fontsize=7.0, handlelength=0.9, columnspacing=0.75)

    _draw_grouped_support_panel(
        ax_framing,
        "Intentional",
        "Unintentional",
        intentional_effect,
        intentional_low,
        intentional_high,
        unintentional_effect,
        unintentional_low,
        unintentional_high,
        framing_q,
        "Constructive association by user framing",
    )
    ax_framing.set_ylabel("Constructive engagement difference (pp)")
    ax_framing.text(-0.15, 1.12, "a", transform=ax_framing.transAxes, fontsize=14, weight="bold")

    _draw_grouped_support_panel(
        ax_task,
        "Coding",
        "Writing",
        coding_effect,
        coding_low,
        coding_high,
        writing_effect,
        writing_low,
        writing_high,
        task_q,
        "Constructive association by task ecology",
    )
    ax_task.set_ylabel("")
    ax_task.text(-0.13, 1.12, "b", transform=ax_task.transAxes, fontsize=14, weight="bold")

    fig.subplots_adjust(left=0.085, right=0.985, top=0.78, bottom=0.185)
    fig.text(0.985, 0.040, "Support-form labels are non-exclusive; q values are Benjamini-Hochberg FDR-adjusted.", ha="right", fontsize=7.5, color=COLORS["muted"])
    _save(fig, "fig_support_form_supply_compact_final_v2")


def make_support_supply_supplement() -> None:
    mean_cols, settings, supply = _support_supply_profile()
    cmap_s = LinearSegmentedColormap.from_list("supply", ["#F3F6F6", "#B8C9D2", "#2E5F7F"])
    fig, ax_supply = plt.subplots(figsize=(7.15, 2.85))
    data = supply.T
    ax_supply.imshow(data, cmap=cmap_s, norm=Normalize(0, 84), aspect="auto")
    ax_supply.set_xticks(np.arange(len(mean_cols)), mean_cols)
    ax_supply.set_yticks(np.arange(len(settings)), settings)
    ax_supply.set_title("Support-form supply within scaffolded assistant turns (%)", loc="left", pad=8, fontsize=9.4, fontweight="bold")
    ax_supply.tick_params(axis="both", length=0)
    ax_supply.set_xticks(np.arange(-0.5, len(mean_cols), 1), minor=True)
    ax_supply.set_yticks(np.arange(-0.5, len(settings), 1), minor=True)
    ax_supply.grid(which="minor", color="white", linewidth=1.1)
    ax_supply.tick_params(which="minor", bottom=False, left=False)
    for sp in ax_supply.spines.values():
        sp.set_visible(False)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            txt_color = "white" if val > 68 else COLORS["ink"]
            ax_supply.text(j, i, f"{val:.1f}", ha="center", va="center", fontsize=7.8, color=txt_color)
    fig.subplots_adjust(left=0.145, right=0.985, top=0.82, bottom=0.18)
    fig.text(0.985, 0.030, "WC, WildChat; LMSYS, LMSYS Chat; SC, ShareChat. Support-form labels are non-exclusive.", ha="right", fontsize=7.4, color=COLORS["muted"])
    _save_supp(fig, "SupplementaryFigure_SupportSupplyProfile")


def make_figure5() -> None:
    order = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    keys = order
    # 95% CIs were recalculated from the same A2U pair files and level-2
    # conversation metrics that produce the point estimates.
    lift = np.array([2.6756, 2.0051, 6.21, 1.1281, 0.2666, 3.35])
    lift_ci = np.array(
        [
            [2.2904, 3.0607],
            [1.5400, 2.5000],
            [np.nan, np.nan],
            [0.9487, 1.3075],
            [0.0200, 0.5200],
            [np.nan, np.nan],
        ]
    )
    cond = {
        "prior constructive": {
            "WC coding": (26.0563, 30.0682),
            "LMSYS coding": (21.9201, 24.1834),
            "SC coding": (32.24, 36.75),
            "WC writing": (6.0528, 12.3195),
            "LMSYS writing": (11.4618, 9.0909),
            "SC writing": (22.91, 25.74),
        },
        "prior active": {
            "WC coding": (9.6341, 11.7894),
            "LMSYS coding": (6.1476, 8.3811),
            "SC coding": (14.45, 17.51),
            "WC writing": (1.9286, 2.5838),
            "LMSYS writing": (2.1687, 2.0536),
            "SC writing": (6.24, 7.46),
        },
        "prior passive": {
            "WC coding": (12.9630, 15.0327),
            "LMSYS coding": (7.3482, 13.8462),
            "SC coding": (9.23, 28.77),
            "WC writing": (2.1182, 3.5857),
            "LMSYS writing": (2.2831, 4.7619),
            "SC writing": (1.38, 9.33),
        },
    }
    cond_ci = {
        "prior constructive": {
            "WC coding": ((24.5124, 27.6619), (28.8784, 31.2854)),
            "LMSYS coding": ((20.2489, 23.5914), (22.0800, 26.2868)),
            "SC coding": ((np.nan, np.nan), (np.nan, np.nan)),
            "WC writing": ((5.0744, 7.2055), (10.5635, 14.3206)),
            "LMSYS writing": ((8.9170, 14.0066), (6.0877, 12.0942)),
            "SC writing": ((np.nan, np.nan), (np.nan, np.nan)),
        },
        "prior active": {
            "WC coding": ((9.2175, 10.0673), (11.3335, 12.2611)),
            "LMSYS coding": ((5.8291, 6.4661), (7.7615, 9.0006)),
            "SC coding": ((np.nan, np.nan), (np.nan, np.nan)),
            "WC writing": ((1.6596, 2.2403), (2.2383, 2.9809)),
            "LMSYS writing": ((1.7641, 2.5732), (1.4846, 2.6227)),
            "SC writing": ((np.nan, np.nan), (np.nan, np.nan)),
        },
        "prior passive": {
            "WC coding": ((9.4704, 17.4946), (10.2307, 21.5475)),
            "LMSYS coding": ((4.4575, 10.2389), (5.4496, 22.2427)),
            "SC coding": ((np.nan, np.nan), (np.nan, np.nan)),
            "WC writing": ((1.3602, 3.2845), (1.8977, 6.6729)),
            "LMSYS writing": ((0.8843, 3.6819), (-0.4968, 10.0206)),
            "SC writing": ((np.nan, np.nan), (np.nan, np.nan)),
        },
    }
    next_s2 = np.array(
        [
            [65.5, 50.7, 29.5],
            [40.3, 26.0, 17.2],
            [66.3, 53.7, 43.7],
            [37.8, 43.2, 18.8],
            [34.2, 31.2, 12.1],
            [39.6, 29.3, 26.5],
        ]
    )
    form_states = ["prior constructive", "prior active", "prior passive"]
    form_or = {
        "M1 feedback": np.array([0.7250, 0.8319, 2.1609]),
        "M4 explaining": np.array([1.7221, 2.1213, 2.8755]),
    }
    form_ci = {
        "M1 feedback": np.array([[0.6451, 0.8148], [0.7254, 0.9539], [1.1570, 4.0359]]),
        "M4 explaining": np.array([[1.4532, 2.0406], [1.8721, 2.4036], [1.5473, 5.3435]]),
    }

    ref_color = "#B8C4CF"
    ref_err = "#7E8B97"
    scaf_color = COLORS["s2"]
    scaf_err = "#2F6F61"
    rose = "#B96B78"
    rose_err = "#8F4F5A"
    guide = "#CDD4DB"
    feedback_color = "#A8753D"
    explaining_color = "#4E7896"

    def _pp(val: float) -> str:
        return f"{val:+.1f}".replace("-", "−") + " pp"

    def _xerr(value: float, ci: tuple[float, float]) -> np.ndarray:
        return np.array([[value - ci[0]], [ci[1] - value]])

    def _has_ci(ci) -> bool:
        return not np.isnan(np.asarray(ci, dtype=float)).any()

    fig = plt.figure(figsize=(7.85, 6.15))
    gs = GridSpec(
        2,
        4,
        figure=fig,
        height_ratios=[1.0, 0.98],
        width_ratios=[1.10, 0.93, 0.93, 0.93],
        hspace=1.04,
        wspace=0.64,
    )
    axa = fig.add_subplot(gs[0, 0])
    axs_b = [fig.add_subplot(gs[0, i]) for i in range(1, 4)]
    axc = fig.add_subplot(gs[1, 0:2])
    axd_m1 = fig.add_subplot(gs[1, 2])
    axd_m4 = fig.add_subplot(gs[1, 3], sharey=axd_m1)

    y = np.arange(len(order))
    axa.barh(y, lift, height=0.30, color=scaf_color, edgecolor="none", zorder=2)
    valid_lift_ci = ~np.isnan(lift_ci).any(axis=1)
    if valid_lift_ci.any():
        axa.errorbar(
            lift[valid_lift_ci],
            y[valid_lift_ci],
            xerr=np.vstack([lift[valid_lift_ci] - lift_ci[valid_lift_ci, 0], lift_ci[valid_lift_ci, 1] - lift[valid_lift_ci]]),
            fmt="none",
            ecolor="#0D1822",
            elinewidth=1.10,
            capsize=3.0,
            capthick=1.05,
            zorder=6,
        )
    axa.scatter(lift, y, s=26, color=scaf_color, edgecolor=COLORS["ink"], lw=0.50, zorder=7)
    for i, val in enumerate(lift):
        label_x = val + 0.18
        label_ha = "left"
        if val > 5.5:
            label_x = val - 0.18
            label_ha = "right"
        axa.text(
            min(label_x, 7.48),
            i,
            _pp(val),
            va="center",
            ha=label_ha,
            fontsize=7.3,
            color=COLORS["ink"],
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.92, pad=0.10),
            zorder=8,
        )
    axa.set_yticks(y, order)
    axa.invert_yaxis()
    axa.set_xlim(0, 7.75)
    axa.set_xlabel("Next-turn constructive lift (pp)")
    axa.grid(axis="x", color=COLORS["grid"], lw=0.65)
    axa.spines[["top", "right"]].set_visible(False)
    axa.spines["left"].set_linewidth(0.9)
    axa.tick_params(axis="both", labelsize=7.4)

    for ax, (title, vals) in zip(axs_b, cond.items()):
        for i, name in enumerate(keys):
            s1, s2 = vals[name]
            ref_y = i - 0.075
            scaf_y = i + 0.075
            ref_ci, scaf_ci = cond_ci[title][name]
            ax.plot([s1, s2], [ref_y, scaf_y], color=guide, lw=0.9, zorder=1)
            if _has_ci(ref_ci):
                ax.errorbar(s1, ref_y, xerr=_xerr(s1, ref_ci), fmt="none", ecolor=ref_err, elinewidth=0.7, capsize=1.7, capthick=0.7, zorder=2)
            if _has_ci(scaf_ci):
                ax.errorbar(s2, scaf_y, xerr=_xerr(s2, scaf_ci), fmt="none", ecolor=scaf_err, elinewidth=0.7, capsize=1.7, capthick=0.7, zorder=2)
            ax.scatter(s1, ref_y, s=24, color=ref_color, edgecolor=COLORS["ink"], lw=0.45, zorder=3)
            ax.scatter(s2, scaf_y, s=24, color=scaf_color, edgecolor=COLORS["ink"], lw=0.45, zorder=3)
            dx = s2 - s1
            if dx >= 0:
                x_label = min(s2 + 0.95, 37.0)
                text_y = scaf_y
            else:
                x_label = min(max(s1, s2) + 1.35, 37.0)
                text_y = scaf_y + 0.18
            ax.text(
                x_label,
                text_y,
                _pp(dx),
                va="center",
                ha="left",
                fontsize=6.8,
                color=COLORS["ink"],
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.86, pad=0.12),
                zorder=5,
            )
        ax.set_title(title, pad=3, fontsize=8.1)
        ax.set_yticks(y)
        ax.set_yticklabels(order if ax is axs_b[0] else [])
        ax.invert_yaxis()
        ax.set_xlim(0, 38.5)
        ax.set_xticks([0, 10, 20, 30])
        ax.grid(axis="x", color=COLORS["grid"], lw=0.65)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(axis="both", labelsize=7.0)

    legend_handles = [
        Line2D([0], [0], marker="o", linestyle="None", markerfacecolor=ref_color, markeredgecolor=COLORS["ink"], markeredgewidth=0.45, markersize=5.0),
        Line2D([0], [0], marker="o", linestyle="None", markerfacecolor=scaf_color, markeredgecolor=COLORS["ink"], markeredgewidth=0.45, markersize=5.0),
    ]

    cmap = LinearSegmentedColormap.from_list("s2", ["#F4F7F6", "#A8C8BD", "#2F7C68"])
    axc.imshow(next_s2, cmap=cmap, norm=Normalize(0, 75), aspect="auto")
    axc.set_xticks(np.arange(3), ["prior\nconstructive", "prior\nactive", "prior\npassive"])
    axc.set_yticks(np.arange(len(order)), order)
    axc.set_xticks(np.arange(-0.5, 3, 1), minor=True)
    axc.set_yticks(np.arange(-0.5, len(order), 1), minor=True)
    axc.grid(which="minor", color="white", linewidth=1.1)
    axc.tick_params(axis="both", which="both", length=0)
    axc.tick_params(axis="both", labelsize=7.4)
    for sp in axc.spines.values():
        sp.set_visible(False)
    for i in range(next_s2.shape[0]):
        for j in range(next_s2.shape[1]):
            val = next_s2[i, j]
            axc.text(j, i, f"{val:.1f}%", ha="center", va="center", fontsize=7.6, color="white" if val > 50 else COLORS["ink"])

    y2 = np.arange(len(form_states))
    form_specs = [
        (axd_m1, "M1 feedback", feedback_color, True),
        (axd_m4, "M4 explaining", explaining_color, False),
    ]
    for ax, label, color, show_y in form_specs:
        vals = form_or[label]
        ci = form_ci[label]
        ax.errorbar(
            vals,
            y2,
            xerr=np.vstack([vals - ci[:, 0], ci[:, 1] - vals]),
            fmt="none",
            ecolor=color,
            elinewidth=0.8,
            capsize=2.2,
            capthick=0.8,
            zorder=3,
        )
        ax.scatter(vals, y2, s=27, color=color, edgecolor=COLORS["ink"], lw=0.45, zorder=4)
        for x, yv in zip(vals, y2):
            label_x = min(x + 0.13, 5.22)
            ax.text(
                label_x,
                yv,
                f"{x:.2f}",
                va="center",
                ha="left",
                fontsize=7.1,
                color=COLORS["ink"],
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.90, pad=0.12),
                zorder=5,
            )
        ax.set_xlim(0.20, 5.55)
        ax.set_xticks([1, 3, 5])
        ax.set_xlabel("Adjusted OR")
        ax.set_title(label, pad=4, fontsize=8.0, fontweight="bold", color=color)
        ax.set_axisbelow(True)
        ax.grid(axis="x", color=COLORS["grid"], lw=0.58, zorder=0)
        ax.axvline(1, color="#6F7D89", lw=1.05, ls=(0, (3.0, 2.0)), zorder=2)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(axis="both", labelsize=7.3)
        ax.tick_params(axis="y", pad=1.2)
        if show_y:
            ax.set_yticks(y2, ["prior\nconstructive", "prior\nactive", "prior\npassive"])
        else:
            ax.tick_params(axis="y", left=False, labelleft=False)
    axd_m1.invert_yaxis()

    fig.subplots_adjust(left=0.105, right=0.985, top=0.815, bottom=0.135)
    top_panel_y = max(axa.get_position().y1, axs_b[0].get_position().y1)
    top_header_y = top_panel_y + 0.044
    bottom_header_y = max(axc.get_position().y1, axd_m1.get_position().y1) + 0.040

    def _panel_header(ax, label, title, y_pos, label_dx=0.035):
        pos = ax.get_position()
        fig.text(pos.x0 - label_dx, y_pos, label, ha="left", va="bottom", fontsize=13, fontweight="bold", color=COLORS["ink"])
        fig.text(pos.x0, y_pos + 0.002, title, ha="left", va="bottom", fontsize=9.2, fontweight="bold", color=COLORS["ink"])

    _panel_header(axa, "a", "Overall adjacent-turn lift", top_header_y)
    _panel_header(axc, "c", "P(next assistant scaffolded | prior user state)", bottom_header_y)
    _panel_header(axd_m1, "d", "Support-form signal by prior state", bottom_header_y, label_dx=0.045)

    b_left = axs_b[0].get_position().x0
    b_right = axs_b[-1].get_position().x1
    b_center = (b_left + b_right) / 2
    b_bottom = min(ax.get_position().y0 for ax in axs_b)
    fig.text(b_left - 0.042, top_header_y, "b", ha="left", va="bottom", fontsize=13, fontweight="bold", color=COLORS["ink"])
    fig.text(b_center, top_header_y + 0.002, "Adjacent-turn contrast by prior user state", ha="center", va="bottom", fontsize=9.2, fontweight="bold", color=COLORS["ink"])
    fig.legend(
        legend_handles,
        ["non-scaffolded reference", "scaffolded support"],
        loc="center",
        bbox_to_anchor=(b_center, b_bottom - 0.045),
        frameon=False,
        ncol=2,
        handletextpad=0.4,
        columnspacing=0.75,
        fontsize=7.0,
    )
    fig.text(b_center, b_bottom - 0.080, "P(next constructive turn) (%)", ha="center", fontsize=8.0)

    fig.text(
        0.50,
        0.038,
        "WC = WildChat; LMSYS = LMSYS Chat; SC = ShareChat. Error bars show 95% CI where displayed; panel d reports pooled model/source FE odds ratios.",
        ha="center",
        fontsize=6.8,
        color=COLORS["muted"],
    )
    _save(fig, "fig_temporal_coupling_scale_compact_final_v5")


def main() -> None:
    make_figure2()
    make_figure3()
    make_figure4()
    make_support_supply_supplement()
    make_figure5()


if __name__ == "__main__":
    main()
