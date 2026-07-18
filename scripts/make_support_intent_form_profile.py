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
from matplotlib.colors import LinearSegmentedColormap


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "support_intent"
SOURCE_DIR = ROOT / "source_data"
SUPP_DIR = ROOT / "figures" / "supplementary"
SVG_DIR = ROOT / "figures_svg_editable" / "final_figures"

CROSSWALK = OUT / "support_intent_form_crosswalk.csv"
SUPPLY = SOURCE_DIR / "supplementary_support_supply_source_data.csv"
SOURCE_OUT = SOURCE_DIR / "support_intent_form_profile_source_data.csv"

DATASETS = [
    ("WC", "WildChat", ["WC coding", "WC writing"]),
    ("LMSYS", "LMSYS Chat", ["LMSYS coding", "LMSYS writing"]),
    ("SC", "ShareChat", ["SC coding", "SC writing"]),
]
INTENTS = [
    ("I1", "I1\nmeta"),
    ("I2", "I2\ncog."),
    ("I3", "I3\naff."),
]
FORMS = [
    ("M1", "M1\nfeedback"),
    ("M2", "M2\nhinting"),
    ("M3", "M3\ninstructing"),
    ("M4", "M4\nexplaining"),
    ("M5", "M5\nmodelling"),
    ("M6", "M6\nquestioning"),
]

COLORS = {
    "ink": "#17212B",
    "muted": "#5D6874",
    "grid": "#E5E9ED",
    "line": "#D8DEE5",
    "blue": "#2F5F83",
    "blue_light": "#88B2CC",
    "teal": "#2E7C6B",
    "gold": "#B87923",
}

CMAP = LinearSegmentedColormap.from_list(
    "support_teal",
    ["#F4FAF7", "#D4EEE4", "#9BD6BE", "#4EA987", "#1F735F"],
)

plt.rcParams.update(
    {
        "font.family": "Nimbus Sans",
        "font.size": 8.5,
        "axes.titlesize": 10,
        "axes.labelsize": 8.8,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 8.0,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.linewidth": 0.75,
    }
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _form_col(form: str, suffix: str) -> str:
    labels = {
        "M1": "feedback",
        "M2": "hinting",
        "M3": "instructing",
        "M4": "explaining",
        "M5": "modelling",
        "M6": "questioning",
    }
    return f"{form}_{labels[form]}_{suffix}"


def _setting_s2(cross_rows: list[dict[str, str]]) -> dict[str, float]:
    s2 = {}
    for row in cross_rows:
        s2.setdefault(row["setting"], float(row["scaffolded_turns"]))
    return s2


def _aggregate() -> dict[str, dict[str, object]]:
    cross_rows = _read_csv(CROSSWALK)
    supply_rows = _read_csv(SUPPLY)
    s2_by_setting = _setting_s2(cross_rows)
    cross_by_dataset = defaultdict(list)
    for row in cross_rows:
        for key, _label, settings in DATASETS:
            if row["setting"] in settings:
                cross_by_dataset[key].append(row)
                break

    supply_by_setting_form = {
        (row["setting"], row["support_form"].split()[0]): float(row["estimate"])
        for row in supply_rows
    }

    out: dict[str, dict[str, object]] = {}
    for key, label, settings in DATASETS:
        dataset_rows = cross_by_dataset[key]
        total_s2 = sum(s2_by_setting[s] for s in settings)

        intent_turns = {intent: 0.0 for intent, _ in INTENTS}
        cross_counts = {(intent, form): 0.0 for intent, _ in INTENTS for form, _ in FORMS}
        for row in dataset_rows:
            intent = row["support_intent"]
            intent_turns[intent] += float(row["intent_turns"])
            for form, _form_label in FORMS:
                cross_counts[(intent, form)] += float(row[_form_col(form, "count")])

        heatmap = np.zeros((len(INTENTS), len(FORMS)), dtype=float)
        for i, (intent, _intent_label) in enumerate(INTENTS):
            denom = intent_turns[intent]
            for j, (form, _form_label) in enumerate(FORMS):
                heatmap[i, j] = 100 * cross_counts[(intent, form)] / denom if denom else np.nan

        intent_share = np.array(
            [100 * intent_turns[intent] / total_s2 if total_s2 else np.nan for intent, _ in INTENTS],
            dtype=float,
        )

        form_share = []
        for form, _form_label in FORMS:
            count = 0.0
            for setting in settings:
                pct = supply_by_setting_form[(setting, form)]
                count += pct * s2_by_setting[setting] / 100
            form_share.append(100 * count / total_s2 if total_s2 else np.nan)

        out[key] = {
            "label": label,
            "settings": settings,
            "total_s2": total_s2,
            "heatmap": heatmap,
            "intent_share": intent_share,
            "form_share": np.array(form_share, dtype=float),
        }
    return out


def _write_source_data(data: dict[str, dict[str, object]]) -> None:
    rows = []
    for key, payload in data.items():
        label = str(payload["label"])
        heatmap = payload["heatmap"]
        form_share = payload["form_share"]
        intent_share = payload["intent_share"]
        for i, (intent, intent_label) in enumerate(INTENTS):
            rows.append(
                {
                    "figure": "Fig. C1",
                    "dataset": label,
                    "panel_element": "right intent bar",
                    "support_intent": intent,
                    "support_form": "",
                    "estimate": f"{intent_share[i]:.6f}",
                    "unit": "percent of scaffolded assistant turns",
                    "notes": "Support-intent labels are non-exclusive.",
                }
            )
            for j, (form, form_label) in enumerate(FORMS):
                rows.append(
                    {
                        "figure": "Fig. C1",
                        "dataset": label,
                        "panel_element": "intent-by-form heatmap",
                        "support_intent": intent,
                        "support_form": form,
                        "estimate": f"{heatmap[i, j]:.6f}",
                        "unit": "percent of turns with the intent label",
                        "notes": "Cells condition on scaffolded assistant turns containing the row support-intent label; labels are non-exclusive.",
                    }
                )
        for j, (form, form_label) in enumerate(FORMS):
            rows.append(
                {
                    "figure": "Fig. C1",
                    "dataset": label,
                    "panel_element": "top support-form bar",
                    "support_intent": "",
                    "support_form": form,
                    "estimate": f"{form_share[j]:.6f}",
                    "unit": "percent of scaffolded assistant turns",
                    "notes": "Support-form labels are non-exclusive.",
                }
            )
    SOURCE_OUT.parent.mkdir(parents=True, exist_ok=True)
    with SOURCE_OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _clean_spines(ax: plt.Axes) -> None:
    ax.spines[["top", "right"]].set_visible(False)


def _draw_dataset(fig: plt.Figure, spec, payload: dict[str, object], letter: str) -> None:
    sub = spec.subgridspec(
        2,
        2,
        height_ratios=[0.62, 1.0],
        width_ratios=[1.0, 0.36],
        hspace=0.08,
        wspace=0.06,
    )
    ax_top = fig.add_subplot(sub[0, 0])
    ax_heat = fig.add_subplot(sub[1, 0])
    ax_side = fig.add_subplot(sub[1, 1])

    label = str(payload["label"])
    heatmap = payload["heatmap"]
    form_share = payload["form_share"]
    intent_share = payload["intent_share"]

    x = np.arange(len(FORMS))
    ax_top.set_axisbelow(True)
    ax_top.bar(x, form_share, color=COLORS["blue_light"], edgecolor="none", linewidth=0.0, width=0.78, zorder=2)
    for xi, val in zip(x, form_share):
        ax_top.text(xi, val + 2.2, f"{val:.0f}", ha="center", va="bottom", fontsize=6.8, color=COLORS["ink"])
    ax_top.set_ylim(0, max(100, np.nanmax(form_share) + 12))
    ax_top.set_yticks([0, 50, 100])
    ax_top.set_yticklabels(["0", "50", "100"], fontsize=6.7, color=COLORS["muted"])
    ax_top.set_xticks([])
    ax_top.grid(axis="y", color=COLORS["grid"], linewidth=0.65, zorder=0)
    _clean_spines(ax_top)
    ax_top.spines["bottom"].set_visible(False)
    ax_top.set_title(label, loc="left", pad=2, fontsize=10.2, fontweight="bold", color=COLORS["ink"])
    ax_top.text(-0.13, 1.08, letter, transform=ax_top.transAxes, fontsize=13, weight="bold", color=COLORS["ink"])
    ax_top.text(
        0.99,
        1.05,
        "M1-M6 share of scaffolded turns (%)",
        transform=ax_top.transAxes,
        ha="right",
        va="bottom",
        fontsize=7.0,
        color=COLORS["muted"],
    )

    im = ax_heat.imshow(heatmap, cmap=CMAP, vmin=0, vmax=100, aspect="auto")
    ax_heat.set_xticks(np.arange(len(FORMS)), [label for _form, label in FORMS])
    ax_heat.set_yticks(np.arange(len(INTENTS)), [label for _intent, label in INTENTS])
    ax_heat.tick_params(axis="x", length=0, pad=4)
    ax_heat.tick_params(axis="y", length=0, pad=4)
    for i in range(len(INTENTS)):
        for j in range(len(FORMS)):
            val = heatmap[i, j]
            color = "white" if val >= 58 else COLORS["ink"]
            ax_heat.text(j, i, f"{val:.0f}", ha="center", va="center", fontsize=7.4, color=color)
    ax_heat.set_xticks(np.arange(-0.5, len(FORMS), 1), minor=True)
    ax_heat.set_yticks(np.arange(-0.5, len(INTENTS), 1), minor=True)
    ax_heat.grid(which="minor", color="#FFFFFF", linewidth=1.0)
    ax_heat.tick_params(which="minor", bottom=False, left=False)
    for spine in ax_heat.spines.values():
        spine.set_color(COLORS["line"])
        spine.set_linewidth(0.8)
    ax_heat.set_xlabel("Support form", labelpad=6)
    ax_heat.set_ylabel("Support intent", labelpad=6)

    y = np.arange(len(INTENTS))
    ax_side.set_axisbelow(True)
    ax_side.barh(y, intent_share, color="#D7AA5C", edgecolor="none", linewidth=0.0, height=0.62, zorder=2)
    for yi, val in zip(y, intent_share):
        ax_side.text(val + 2.3, yi, f"{val:.0f}", ha="left", va="center", fontsize=6.8, color=COLORS["ink"])
    ax_side.set_xlim(0, max(100, np.nanmax(intent_share) + 14))
    ax_side.set_ylim(len(INTENTS) - 0.5, -0.5)
    ax_side.set_yticks([])
    ax_side.set_xticks([0, 50, 100])
    ax_side.set_xticklabels(["0", "50", "100"], fontsize=6.7, color=COLORS["muted"])
    ax_side.grid(axis="x", color=COLORS["grid"], linewidth=0.65, zorder=0)
    _clean_spines(ax_side)
    ax_side.set_xlabel("I1-I3 share\nof scaffolded\nturns (%)", labelpad=6, fontsize=7.0, color=COLORS["muted"])
    return im


def make_figure() -> None:
    data = _aggregate()
    _write_source_data(data)

    fig = plt.figure(figsize=(7.55, 8.35))
    gs = fig.add_gridspec(3, 1, hspace=0.54)
    ims = []
    for row, (key, _label, _settings) in enumerate(DATASETS):
        ims.append(_draw_dataset(fig, gs[row, 0], data[key], chr(ord("a") + row)))

    cax = fig.add_axes([0.26, 0.055, 0.48, 0.017])
    cbar = fig.colorbar(ims[-1], cax=cax, orientation="horizontal")
    cbar.set_ticks([0, 25, 50, 75, 100])
    cbar.ax.tick_params(labelsize=7.2, length=2.5)
    cbar.ax.xaxis.set_label_position("top")
    cbar.set_label("% within row intent", fontsize=7.5, color=COLORS["muted"], labelpad=3)
    fig.text(
        0.05,
        0.008,
        "Intent and support-form labels are non-exclusive; values need not sum to 100%. Bars are percentages of scaffolded assistant turns.",
        ha="left",
        va="bottom",
        fontsize=7.4,
        color=COLORS["muted"],
    )
    fig.subplots_adjust(left=0.11, right=0.96, top=0.975, bottom=0.145)

    SUPP_DIR.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = SUPP_DIR / "SupplementaryFigure_SupportIntentFormProfile.pdf"
    svg_path = SVG_DIR / "SupplementaryFigure_SupportIntentFormProfile.svg"
    fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.025)
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.025)
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


if __name__ == "__main__":
    make_figure()
