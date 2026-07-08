from __future__ import annotations

import csv
import os
from collections import defaultdict
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-cache")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source_data" / "wildchat_model_family_robustness_source_data.csv"
SUPP_FIG_DIR = ROOT / "figures" / "supplementary"
SVG_DIR = ROOT / "figures_svg_editable" / "final_figures"

FAMILY_ORDER = ["GPT-3.5", "GPT-4", "GPT-4o", "GPT-4.1-mini"]
TASKS = [
    ("coding", "#2F5F83", -0.14, "Coding"),
    ("writing", "#C86A78", 0.14, "Writing"),
]

COLORS = {
    "ink": "#17212B",
    "muted": "#5D6874",
    "grid": "#E5E9ED",
    "line": "#D8DEE5",
    "ref": "#8F9BA7",
}

PANELS = [
    ("a", "Cognitive engagement", "cognitive engagement prevalence", "Cognitive engagement (%)", (0, 60), [0, 20, 40, 60], None, True),
    ("b", "Support association", "adjusted support association", "Poisson count ratio", (0.7, 3.25), [1.0, 1.5, 2.0, 2.5, 3.0], 1.0, False),
    ("c", "Adjacent-turn lift", "adjacent-turn constructive lift", "Next-turn constructive lift (pp)", (-1.0, 7.0), [0, 2, 4, 6], 0.0, False),
]

plt.rcParams.update(
    {
        "font.family": "Nimbus Sans",
        "font.size": 9,
        "axes.titlesize": 10.5,
        "axes.labelsize": 9.2,
        "xtick.labelsize": 8.2,
        "ytick.labelsize": 8.2,
        "legend.fontsize": 8.2,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.linewidth": 0.75,
    }
)


def _read_rows() -> list[dict[str, str]]:
    with open(SOURCE, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _save(fig: plt.Figure, stem: str) -> None:
    SUPP_FIG_DIR.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = SUPP_FIG_DIR / f"{stem}.pdf"
    svg_path = SVG_DIR / f"{stem}.svg"
    fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.025)
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.025)
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


def _group(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, list[float] | float]]:
    grouped: dict[tuple[str, str, str], dict[str, list[float] | float]] = defaultdict(lambda: {"snapshots": [], "summary": np.nan})
    for row in rows:
        key = (row["metric"], row["model_family"], row["task"])
        value = float(row["estimate"])
        if row["level"] == "model snapshot":
            grouped[key]["snapshots"].append(value)
        elif row["level"] == "family summary":
            grouped[key]["summary"] = value
    return grouped


def _draw_panel(
    ax: plt.Axes,
    grouped: dict[tuple[str, str, str], dict[str, list[float] | float]],
    letter: str,
    title: str,
    metric: str,
    xlabel: str,
    xlim: tuple[float, float],
    xticks: list[float],
    refline: float | None,
    show_ylabels: bool,
) -> None:
    y = np.arange(len(FAMILY_ORDER))
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.7, zorder=0)
    if refline is not None:
        ax.axvline(refline, color=COLORS["ref"], lw=0.9, ls=(0, (2.2, 2.2)), zorder=1)

    for family_index, family in enumerate(FAMILY_ORDER):
        for task, color, offset, _label in TASKS:
            vals = np.asarray(grouped[(metric, family, task)]["snapshots"], dtype=float)
            summary = float(grouped[(metric, family, task)]["summary"])
            yy = family_index + offset
            if vals.size:
                ax.plot([vals.min(), vals.max()], [yy, yy], color=COLORS["line"], lw=1.0, zorder=1)
                jitter = np.linspace(-0.035, 0.035, vals.size) if vals.size > 1 else np.array([0.0])
                ax.scatter(vals, yy + jitter, s=14, color=color, alpha=0.26, edgecolor="none", zorder=2)
            ax.scatter(summary, yy, marker="D", s=42, color=color, edgecolor="white", linewidth=0.7, zorder=4)

    ax.set_yticks(y, FAMILY_ORDER)
    if not show_ylabels:
        ax.set_yticklabels([])
        ax.tick_params(axis="y", length=0)
    ax.invert_yaxis()
    ax.set_xlim(*xlim)
    ax.set_xticks(xticks)
    ax.set_xlabel(xlabel)
    ax.set_title(title, loc="left", pad=7, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="both", length=3)
    ax.text(-0.15, 1.05, letter, transform=ax.transAxes, fontsize=13, weight="bold")


def main() -> None:
    rows = _read_rows()
    grouped = _group(rows)
    fig, axes = plt.subplots(1, 3, figsize=(7.45, 3.05), gridspec_kw={"wspace": 0.24})
    for ax, panel in zip(axes, PANELS):
        _draw_panel(ax, grouped, *panel)

    handles = [
        Line2D([0], [0], marker="D", color="none", markerfacecolor="#2F5F83", markeredgecolor="white", markersize=6.4, label="Coding family summary"),
        Line2D([0], [0], marker="D", color="none", markerfacecolor="#C86A78", markeredgecolor="white", markersize=6.4, label="Writing family summary"),
        Line2D([0], [0], marker="o", color=COLORS["line"], markerfacecolor=COLORS["line"], markeredgecolor="none", markersize=4.2, label="Individual model snapshots"),
    ]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.56, 0.99), ncol=3, frameon=False, columnspacing=1.05, handletextpad=0.45)
    fig.text(
        0.12,
        0.045,
        "Small points show user-facing WildChat model snapshots within each family; diamonds show coarse family summaries.",
        ha="left",
        va="bottom",
        fontsize=7.4,
        color=COLORS["muted"],
    )
    fig.subplots_adjust(left=0.12, right=0.99, top=0.76, bottom=0.25)
    _save(fig, "SupplementaryFigure_WildChatModelFamilyRobustness")


if __name__ == "__main__":
    main()
