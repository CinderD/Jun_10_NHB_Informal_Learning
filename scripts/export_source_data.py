from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source_data"
STATS = ROOT / "outputs" / "integrated_regression"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def bh_fdr(pvals: list[float]) -> list[float]:
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    ranked = [pvals[i] for i in order]
    adjusted = [0.0] * len(pvals)
    running = 1.0
    m = float(len(pvals))
    for rank in range(len(ranked) - 1, -1, -1):
        running = min(running, ranked[rank] * m / (rank + 1))
        adjusted[order[rank]] = min(max(running, 0.0), 1.0)
    return adjusted


def figure2() -> None:
    labels = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    composition = {
        "Active": [80.4, 86.4, 62.0, 79.5, 82.7, 69.7],
        "Constructive": [18.4, 12.0, 33.7, 13.6, 10.0, 15.7],
        "Passive": [1.2, 1.6, 4.3, 6.9, 7.3, 14.6],
    }
    framing = {
        ("Cognitive", "intentional"): [76.6, 72.6, 73.8, 28.2, 28.2, 46.4],
        ("Cognitive", "unintentional"): [32.5, 25.3, 28.0, 10.5, 10.3, 24.9],
        ("Constructive", "intentional"): [13.1, 8.0, 22.0, 5.2, 3.5, 7.2],
        ("Constructive", "unintentional"): [5.7, 3.6, 9.2, 1.5, 1.0, 3.2],
    }
    depth = {
        "WC coding": [15.1, 28.6, 46.3],
        "LMSYS coding": [9.5, 20.5, 33.9],
        "SC coding": [27.8, 43.4, 61.3],
        "WC writing": [6.0, 9.2, 15.0],
        "LMSYS writing": [3.3, 6.3, 11.2],
        "SC writing": [7.6, 18.2, 31.3],
    }
    rows: list[dict[str, object]] = []
    for measure, values in composition.items():
        for setting, value in zip(labels, values):
            rows.append(
                {
                    "figure": "Figure 2",
                    "panel": "a",
                    "setting": setting,
                    "measure": measure,
                    "group": "cognitively engaged turns",
                    "estimate": value,
                    "unit": "percent",
                    "ci_low": "",
                    "ci_high": "",
                    "p_value": "",
                    "notes": "Composition denominator is cognitively engaged user turns.",
                }
            )
    for (measure, group), values in framing.items():
        for setting, value in zip(labels, values):
            rows.append(
                {
                    "figure": "Figure 2",
                    "panel": "b",
                    "setting": setting,
                    "measure": measure,
                    "group": group,
                    "estimate": value,
                    "unit": "percent of user turns",
                    "ci_low": "",
                    "ci_high": "",
                    "p_value": "",
                    "notes": "Intentional versus unintentional user framing.",
                }
            )
    for setting, values in depth.items():
        for bucket, value in zip(["2-3 user turns", "4-6 user turns", "7+ user turns"], values):
            rows.append(
                {
                    "figure": "Figure 2",
                    "panel": "c",
                    "setting": setting,
                    "measure": "conversation contains >=1 constructive user turn",
                    "group": bucket,
                    "estimate": value,
                    "unit": "percent of conversations",
                    "ci_low": "",
                    "ci_high": "",
                    "p_value": "",
                    "notes": "Conversation-level share by length bucket.",
                }
            )
    write_csv(OUT / "figure2_source_data.csv", rows)


def figure3() -> None:
    labels = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    no_s2 = [5.5626, 3.9665, 8.9800, 1.7372, 1.0692, 3.4391]
    has_s2 = [10.1265, 6.4707, 16.3192, 2.7293, 2.1567, 6.6385]
    depth_diff = [2.2259, 1.4214, 3.3617, 3.1268, 2.0999, 3.3848]
    depth_ci = [(2.1065, 2.3468), (1.3362, 1.5160), (2.6850, 4.0114), (2.9593, 3.3027), (1.9063, 2.2810), (1.9213, 4.6377)]
    depth_p = [1.70734e-300, 4.12801e-207, 3.11658e-23, 5.16574e-261, 1.6131e-107, 1.01313e-06]
    pois = [1.852129, 1.621977, 1.892754, 1.568604, 1.985056, 2.491434]
    pois_ci = [(1.748968, 1.961375), (1.531958, 1.717285), (1.605713, 2.231107), (1.462784, 1.682078), (1.759494, 2.239534), (1.970588, 3.149944)]
    logit = [1.760538, 1.543781, 2.140210, 1.436974, 1.764222, 1.756637]
    logit_ci = [(1.634771, 1.895981), (1.439886, 1.655173), (1.690000, 2.710000), (1.328000, 1.555000), (1.539000, 2.022000), (1.280000, 2.411000)]
    strat_int = [1.967756, 1.671692, 2.113730, 1.579301, 2.333909, 1.854075]
    strat_int_ci = [(1.801625, 2.149207), (1.552075, 1.800528), (1.679535, 2.660174), (1.427233, 1.747571), (1.886383, 2.887607), (1.235605, 2.782114)]
    strat_unint = [1.633274, 1.582937, 1.680661, 1.566670, 1.841921, 2.234555]
    strat_unint_ci = [(1.512785, 1.763359), (1.447858, 1.730617), (1.327630, 2.127566), (1.421943, 1.726128), (1.585813, 2.139391), (1.675959, 2.979332)]
    rows: list[dict[str, object]] = []
    for setting, ref, scaf in zip(labels, no_s2, has_s2):
        for group, value in [("non-scaffolded reference", ref), ("scaffolded support", scaf)]:
            rows.append(
                {
                    "figure": "Figure 3",
                    "panel": "a",
                    "setting": setting,
                    "measure": "turn-weighted constructive ratio",
                    "group": group,
                    "estimate": value,
                    "unit": "percent",
                    "ci_low": "",
                    "ci_high": "",
                    "p_value": "",
                    "notes": "Group ratio is total constructive user turns divided by total user turns.",
                }
            )
    adjusted = {
        (r["setting"], r["model_type"]): r
        for r in read_csv(STATS / "fig3_adjusted_model_significance.csv")
    }
    for setting, value, ci in zip(labels, pois, pois_ci):
        r = adjusted[(setting, "Poisson RR")]
        rows.append({"figure": "Figure 3", "panel": "b", "setting": setting, "measure": "Poisson count ratio", "group": "scaffolded support", "estimate": r["estimate"], "unit": "ratio", "ci_low": r["ci_low"], "ci_high": r["ci_high"], "p_value": r["p_value"], "notes": "Model-based 95% CI and two-sided p value."})
    for setting, value, ci in zip(labels, logit, logit_ci):
        r = adjusted[(setting, "Logit OR")]
        rows.append({"figure": "Figure 3", "panel": "b", "setting": setting, "measure": "Logit odds ratio", "group": "scaffolded support", "estimate": r["estimate"], "unit": "odds ratio", "ci_low": r["ci_low"], "ci_high": r["ci_high"], "p_value": r["p_value"], "notes": "Model-based 95% CI and two-sided p value."})
    stratified = {
        (r["setting"], r["user_framing"]): r
        for r in read_csv(STATS / "fig3_user_framing_stratified_poisson_significance.csv")
    }
    for group, values, cis in [("intentional", strat_int, strat_int_ci), ("unintentional", strat_unint, strat_unint_ci)]:
        for setting, value, ci in zip(labels, values, cis):
            r = stratified[(setting, group)]
            rows.append({"figure": "Figure 3", "panel": "c", "setting": setting, "measure": "Poisson count ratio", "group": group, "estimate": r["estimate"], "unit": "ratio", "ci_low": r["ci_low"], "ci_high": r["ci_high"], "p_value": r["p_value"], "notes": "User-framing stratified model; model-based 95% CI and two-sided p value."})
    for setting, value, ci, p_value in zip(labels, depth_diff, depth_ci, depth_p):
        rows.append({"figure": "Figure 3", "panel": "d", "setting": setting, "measure": "post-answer depth difference", "group": "scaffolded minus reference", "estimate": value, "unit": "turns", "ci_low": ci[0], "ci_high": ci[1], "p_value": p_value, "notes": "Conversation-level bootstrap estimate."})
    write_csv(OUT / "figure3_source_data.csv", rows)


def figure4() -> None:
    forms = ["M1 feedback", "M2 hinting", "M3 instructing", "M4 explaining", "M5 modelling", "M6 questioning"]
    settings = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    groups = [
        ("a", "intentional", [14.68, 3.74, -2.77, 6.67, 0.13, -4.81], [13.53, 2.81, -3.44, 6.02, -0.56, -5.56], [15.83, 4.67, -2.10, 7.31, 0.82, -4.07], [1.77e-30, 6.23e-05, 3.99e-06, 3.86e-24, 2.01e-02, 9.34e-18]),
        ("a", "unintentional", [6.67, 1.62, -1.04, 3.04, 1.08, -1.28], [5.94, 1.16, -1.34, 2.76, 0.68, -1.59], [7.41, 2.09, -0.74, 3.32, 1.48, -0.96], [1.77e-30, 6.23e-05, 3.99e-06, 3.86e-24, 2.01e-02, 9.34e-18]),
        ("b", "coding", [12.35, 2.99, 1.59, 4.03, -0.59, -3.96], [11.38, 2.34, 1.05, 3.56, -1.05, -4.41], [13.33, 3.64, 2.13, 4.49, -0.13, -3.52], [3.93e-02, 9.41e-01, 1.23e-45, 4.33e-01, 4.95e-44, 3.71e-23]),
        ("b", "writing", [10.93, 3.02, -3.38, 4.30, 6.67, -0.84], [10.00, 2.36, -3.80, 3.80, 5.76, -1.27], [11.87, 3.69, -2.95, 4.80, 7.59, -0.42], [3.93e-02, 9.41e-01, 1.23e-45, 4.33e-01, 4.95e-44, 3.71e-23]),
    ]
    supply = {
        "M1 feedback": [8.8, 4.4, 13.3, 16.6, 11.3, 24.2],
        "M2 hinting": [14.7, 7.6, 12.7, 9.6, 10.9, 23.2],
        "M3 instructing": [29.7, 9.7, 25.7, 59.2, 52.3, 22.9],
        "M4 explaining": [84.0, 76.7, 81.2, 29.5, 26.9, 45.2],
        "M5 modelling": [23.9, 16.5, 18.4, 15.0, 10.3, 23.5],
        "M6 questioning": [6.9, 13.9, 18.6, 6.9, 13.4, 38.1],
    }
    q_by_panel = {"a": bh_fdr(groups[0][5]), "b": bh_fdr(groups[2][5])}
    rows: list[dict[str, object]] = []
    for panel, group, values, lows, highs, pvals in groups:
        for i, form in enumerate(forms):
            rows.append(
                {
                    "figure": "Figure 4",
                    "panel": panel,
                    "setting": "pooled six settings",
                    "measure": "constructive association",
                    "group": group,
                    "support_form": form,
                    "estimate": values[i],
                    "unit": "percentage-point difference",
                    "ci_low": lows[i],
                    "ci_high": highs[i],
                    "p_value_for_between_stratum_contrast": pvals[i],
                    "q_value_bh_fdr": q_by_panel[panel][i],
                    "notes": "Support forms are non-exclusive; q values are Benjamini-Hochberg adjusted within each displayed six-form family.",
                }
            )
    write_csv(OUT / "figure4_source_data.csv", rows)

    supply_rows: list[dict[str, object]] = []
    for form, values in supply.items():
        for setting, value in zip(settings, values):
            supply_rows.append(
                {
                    "figure": "Supplementary Figure D3",
                    "panel": "",
                    "setting": setting,
                    "measure": "support-form supply within scaffolded assistant turns",
                    "group": "scaffolded assistant turns",
                    "support_form": form,
                    "estimate": value,
                    "unit": "percent",
                    "ci_low": "",
                    "ci_high": "",
                    "p_value_for_between_stratum_contrast": "",
                    "q_value_bh_fdr": "",
                    "notes": "Support-form labels are non-exclusive and rows do not sum to 100%.",
                }
            )
    write_csv(OUT / "supplementary_support_supply_source_data.csv", supply_rows)


def figure5() -> None:
    order = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    adjacent = {
        r["setting"]: r
        for r in read_csv(STATS / "key_percentage_lifts_significance.csv")
        if r["contrast"] == "adjacent_next_constructive_s2_minus_s1"
    }
    cond = {
        "prior constructive": {"WC coding": (26.0563, 30.0682), "LMSYS coding": (21.9201, 24.1834), "SC coding": (32.24, 36.75), "WC writing": (6.0528, 12.3195), "LMSYS writing": (11.4618, 9.0909), "SC writing": (22.91, 25.74)},
        "prior active": {"WC coding": (9.6341, 11.7894), "LMSYS coding": (6.1476, 8.3811), "SC coding": (14.45, 17.51), "WC writing": (1.9286, 2.5838), "LMSYS writing": (2.1687, 2.0536), "SC writing": (6.24, 7.46)},
        "prior passive": {"WC coding": (12.9630, 15.0327), "LMSYS coding": (7.3482, 13.8462), "SC coding": (9.23, 28.77), "WC writing": (2.1182, 3.5857), "LMSYS writing": (2.2831, 4.7619), "SC writing": (1.38, 9.33)},
    }
    next_s2 = {
        "WC coding": [65.5, 50.7, 29.5],
        "LMSYS coding": [40.3, 26.0, 17.2],
        "SC coding": [66.3, 53.7, 43.7],
        "WC writing": [37.8, 43.2, 18.8],
        "LMSYS writing": [34.2, 31.2, 12.1],
        "SC writing": [39.6, 29.3, 26.5],
    }
    form_or = {
        "M1 feedback": [(0.7250, 0.6451, 0.8148), (0.8319, 0.7254, 0.9539), (2.1609, 1.1570, 4.0359)],
        "M4 explaining": [(1.7221, 1.4532, 2.0406), (2.1213, 1.8721, 2.4036), (2.8755, 1.5473, 5.3435)],
    }
    rows: list[dict[str, object]] = []
    for setting in order:
        r = adjacent[setting]
        rows.append({"figure": "Figure 5", "panel": "a", "setting": setting, "measure": "next-turn constructive lift", "group": "scaffolded minus reference", "estimate": r["estimate"], "unit": "percentage-point difference", "ci_low": r["ci_low"], "ci_high": r["ci_high"], "p_value": r["p_value"], "n_conversations": r["n_conversations"], "notes": "Conversation-cluster bootstrap CI and two-sided p value over assistant-to-user pairs."})
    for state, vals in cond.items():
        for setting, (ref, scaf) in vals.items():
            rows.append({"figure": "Figure 5", "panel": "b", "setting": setting, "measure": "P(next constructive turn)", "group": f"{state}: non-scaffolded reference", "estimate": ref, "unit": "percent", "ci_low": "", "ci_high": "", "notes": ""})
            rows.append({"figure": "Figure 5", "panel": "b", "setting": setting, "measure": "P(next constructive turn)", "group": f"{state}: scaffolded support", "estimate": scaf, "unit": "percent", "ci_low": "", "ci_high": "", "notes": ""})
    for setting, values in next_s2.items():
        for state, value in zip(["prior constructive", "prior active", "prior passive"], values):
            rows.append({"figure": "Figure 5", "panel": "c", "setting": setting, "measure": "P(next assistant scaffolded)", "group": state, "estimate": value, "unit": "percent", "ci_low": "", "ci_high": "", "notes": ""})
    for form, values in form_or.items():
        for state, (estimate, low, high) in zip(["prior constructive", "prior active", "prior passive"], values):
            rows.append({"figure": "Figure 5", "panel": "d", "setting": "pooled model/source FE", "measure": "adjusted odds ratio for next constructive turn", "group": state, "support_form": form, "estimate": estimate, "unit": "odds ratio", "ci_low": low, "ci_high": high, "notes": "Focal support forms selected from Section 2.4 conversation-level form patterns."})
    write_csv(OUT / "figure5_source_data.csv", rows)


def readme() -> None:
    text = """# Figure source data

This directory contains CSV source data for the manuscript's numeric main figures.

- `figure2_source_data.csv`: engagement composition, user-framing contrasts and conversation-length gradients.
- `figure3_source_data.csv`: scaffolded versus reference constructive ratios, adjusted model estimates, framing-stratified estimates and post-answer depth differences.
- `figure4_source_data.csv`: support-form constructive associations and Benjamini-Hochberg q values.
- `figure5_source_data.csv`: adjacent-turn lifts, prior-state conditional probabilities, reverse scaffolded-support probabilities and focal prior-state x support-form odds ratios.
- `appendix_d_source_data.csv`: six-setting around-first-scaffold contrasts used in Supplementary Figure D1. Supplementary Figure D2 reads the framing-stratified estimates from `figure3_source_data.csv`.
- `supplementary_support_supply_source_data.csv`: support-form supply profiles used in Supplementary Figure D3.

Figure 1 is a conceptual framework figure and has no numeric source data. Supplementary table source files are stored under `tables/`, and regression/statistical output CSV files are stored under `outputs/integrated_regression/`.

Raw message text is not redistributed here. For reproduction from raw conversations, obtain the public corpora from their original releases and run the analysis code against the derived labelling pipeline outputs.
"""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "README.md").write_text(text)


def main() -> None:
    figure2()
    figure3()
    figure4()
    figure5()
    readme()


if __name__ == "__main__":
    main()
