from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from compute_integrated_regression_stats import (
    FIG3_POISSON_COVARIATES,
    OUT,
    ROOT,
    _assistant_model_key,
    _f,
    _fit_grouped_binomial_cluster,
    _fit_logit_cluster,
    _fit_poisson_glm,
    _load_level2_rows,
)


MODEL_SOURCE_MIN_COUNT = 100
SECTION22_TERMS = [
    ("intentional_framing", "Intentional framing"),
    ("coding_task", "Coding task ecology"),
    ("length_4_6_user_turns", "4--6 user turns"),
    ("length_7plus_user_turns", "7+ user turns"),
]
SUPPORT_FORM_TERMS = [
    ("has_M1", "M1 feedback"),
    ("has_M2", "M2 hinting"),
    ("has_M3", "M3 instructing"),
    ("has_M4", "M4 explaining"),
    ("has_M5", "M5 modelling"),
    ("has_M6", "M6 questioning"),
]


def _p_value(coef: float, se: float) -> float:
    if se <= 0 or not math.isfinite(se):
        return float("nan")
    return math.erfc(abs(coef / se) / math.sqrt(2))


def _p_text(value: str | float) -> str:
    p = float(value)
    if p < 0.001:
        return "$<.001$"
    if not math.isfinite(p):
        return "--"
    return f"{p:.3f}".replace("0.", ".")


def _or_cell(row: dict[str, str], key: str = "estimate") -> str:
    return (
        f"{float(row[key]):.2f} "
        f"[{float(row['ci_low']):.2f}, {float(row['ci_high']):.2f}], "
        f"{_p_text(row['p_value'])}"
    )


def _model_source_levels(rows: list[dict[str, str]]) -> tuple[list[str], str, int]:
    counts = Counter(_assistant_model_key(row) for row in rows)
    recoverable = sorted([key for key in counts if key])
    eligible = sorted([key for key, count in counts.items() if key and count >= MODEL_SOURCE_MIN_COUNT])
    if not eligible:
        return [], "", len(recoverable)
    reference = eligible[0]
    return [key for key in eligible if key != reference], reference, len(recoverable)


def _add_fixed_effect_columns(
    names: list[str],
    rows: list[dict[str, str]],
    include_dataset: bool,
    include_model_source: bool,
) -> tuple[list[str], list[str], str, int]:
    model_levels: list[str] = []
    reference = ""
    recoverable_count = 0
    if include_dataset:
        names.extend(["dataset_LMSYS", "dataset_ShareChat"])
    if include_model_source:
        model_levels, reference, recoverable_count = _model_source_levels(rows)
        names.extend([f"model_source::{level}" for level in model_levels])
    return names, model_levels, reference, recoverable_count


def _fill_fixed_effect_columns(
    X: np.ndarray,
    i: int,
    row: dict[str, str],
    name_to_idx: dict[str, int],
) -> None:
    if "dataset_LMSYS" in name_to_idx:
        X[i, name_to_idx["dataset_LMSYS"]] = 1 if row["_dataset"] == "LMSYS" else 0
    if "dataset_ShareChat" in name_to_idx:
        X[i, name_to_idx["dataset_ShareChat"]] = 1 if row["_dataset"] == "ShareChat" else 0
    model_key = f"model_source::{_assistant_model_key(row)}"
    if model_key in name_to_idx:
        X[i, name_to_idx[model_key]] = 1


def _rate_count(row: dict[str, str], ratio_key: str, denominator_key: str) -> float:
    return _f(row, ratio_key) * _f(row, denominator_key)


def compute_section21_model_source_breakdown(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = _assistant_model_key(row)
        if key:
            grouped[(row["_setting"], key)].append(row)

    detail_rows: list[dict[str, str]] = []
    for (setting, model_source), subset in sorted(grouped.items()):
        if len(subset) < MODEL_SOURCE_MIN_COUNT:
            continue
        user_turns = sum(_f(row, "user_turns") for row in subset)
        assistant_turns = sum(_f(row, "assistant_turns") for row in subset)
        if user_turns <= 0 or assistant_turns <= 0:
            continue
        passive = sum(_rate_count(row, "Cog_P_ratio", "user_turns") for row in subset)
        active = sum(_rate_count(row, "Cog_A_ratio", "user_turns") for row in subset)
        constructive = sum(_f(row, "Cog_C_count") for row in subset)
        emotional = sum(_rate_count(row, "Emo_ratio", "user_turns") for row in subset)
        scaffolded = sum(_f(row, "num_S2") for row in subset)
        cognitive = passive + active + constructive
        detail_rows.append(
            {
                "section": "2.1",
                "setting": setting,
                "dataset": subset[0]["_dataset"],
                "task": subset[0]["_task"],
                "model_source": model_source,
                "n_conversations": str(len(subset)),
                "user_turns": f"{int(user_turns)}",
                "assistant_turns": f"{int(assistant_turns)}",
                "passive_pct_user_turns": f"{passive / user_turns * 100:.4f}",
                "active_pct_user_turns": f"{active / user_turns * 100:.4f}",
                "constructive_pct_user_turns": f"{constructive / user_turns * 100:.4f}",
                "cognitive_overall_pct_user_turns": f"{cognitive / user_turns * 100:.4f}",
                "emotional_expression_pct_user_turns": f"{emotional / user_turns * 100:.4f}",
                "scaffolded_pct_assistant_turns": f"{scaffolded / assistant_turns * 100:.4f}",
                "notes": "Model/source levels are shown when at least 100 conversations are available within the setting; WildChat uses chat_model, LMSYS uses model recovered from conversation identifiers and ShareChat uses public assistant/source family.",
            }
        )

    summary_rows: list[dict[str, str]] = []
    by_setting: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in detail_rows:
        by_setting[row["setting"]].append(row)
    for setting, subset in sorted(by_setting.items()):
        def vals(key: str) -> list[float]:
            return [float(row[key]) for row in subset]

        summary_rows.append(
            {
                "section": "2.1",
                "setting": setting,
                "n_model_source_levels_ge_100_conversations": str(len(subset)),
                "cognitive_overall_min_pct": f"{min(vals('cognitive_overall_pct_user_turns')):.2f}",
                "cognitive_overall_median_pct": f"{float(np.median(vals('cognitive_overall_pct_user_turns'))):.2f}",
                "cognitive_overall_max_pct": f"{max(vals('cognitive_overall_pct_user_turns')):.2f}",
                "constructive_min_pct": f"{min(vals('constructive_pct_user_turns')):.2f}",
                "constructive_median_pct": f"{float(np.median(vals('constructive_pct_user_turns'))):.2f}",
                "constructive_max_pct": f"{max(vals('constructive_pct_user_turns')):.2f}",
                "scaffolded_min_pct": f"{min(vals('scaffolded_pct_assistant_turns')):.2f}",
                "scaffolded_median_pct": f"{float(np.median(vals('scaffolded_pct_assistant_turns'))):.2f}",
                "scaffolded_max_pct": f"{max(vals('scaffolded_pct_assistant_turns')):.2f}",
                "notes": "Ranges summarize model/source levels with at least 100 conversations within each setting; full rows are exported in section21_model_source_engagement_breakdown.csv.",
            }
        )

    for path, out_rows in [
        (OUT / "section21_model_source_engagement_breakdown.csv", detail_rows),
        (OUT / "section21_model_source_engagement_summary.csv", summary_rows),
    ]:
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), lineterminator="\n")
            writer.writeheader()
            writer.writerows(out_rows)
    return detail_rows, summary_rows


def _make_section22_design(
    rows: list[dict[str, str]],
    include_dataset: bool,
    include_model_source: bool,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str], list[str], str, int]:
    names = [
        "Intercept",
        "intentional_framing",
        "coding_task",
        "length_4_6_user_turns",
        "length_7plus_user_turns",
    ]
    names, _, reference, recoverable_count = _add_fixed_effect_columns(
        names, rows, include_dataset, include_model_source
    )
    X = np.zeros((len(rows), len(names)), dtype=float)
    any_c = np.zeros(len(rows), dtype=float)
    successes = np.zeros(len(rows), dtype=float)
    trials = np.zeros(len(rows), dtype=float)
    clusters: list[str] = []
    name_to_idx = {name: idx for idx, name in enumerate(names)}
    for i, row in enumerate(rows):
        user_turns = _f(row, "user_turns")
        X[i, name_to_idx["Intercept"]] = 1
        X[i, name_to_idx["intentional_framing"]] = _f(row, "is_intentional")
        X[i, name_to_idx["coding_task"]] = _f(row, "is_coding_topic")
        X[i, name_to_idx["length_4_6_user_turns"]] = 1 if 4 <= user_turns <= 6 else 0
        X[i, name_to_idx["length_7plus_user_turns"]] = 1 if user_turns >= 7 else 0
        _fill_fixed_effect_columns(X, i, row, name_to_idx)
        any_c[i] = _f(row, "has_Cog_C")
        trials[i] = max(user_turns, 1.0)
        successes[i] = min(_f(row, "Cog_C_count"), trials[i])
        clusters.append(row["conv_id"])
    return X, any_c, successes, trials, clusters, names, reference, recoverable_count


def compute_section22_model_source_sensitivity(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out_rows: list[dict[str, str]] = []
    specs = [
        ("dataset FE", True, False),
        ("model/source FE", False, True),
    ]
    for adjustment, include_dataset, include_model_source in specs:
        X, any_c, successes, trials, clusters, names, reference, recoverable_count = _make_section22_design(
            rows, include_dataset, include_model_source
        )
        beta, se, ll = _fit_logit_cluster(X, any_c, clusters, names)
        beta_rate, se_rate, ll_rate = _fit_grouped_binomial_cluster(X, successes, trials, clusters)
        for outcome, coef, coef_se, log_likelihood, extra in [
            (
                "any constructive turn",
                beta,
                se,
                ll,
                {
                    "n_user_turns": "",
                    "n_constructive_turns": "",
                    "formula": (
                        "has_Cog_C ~ user framing + task ecology + length bucket + "
                        f"{'dataset fixed effects' if include_dataset else 'model/source fixed effects'}"
                    ),
                    "se_type": "conversation-robust sandwich",
                },
            ),
            (
                "constructive-turn rate",
                beta_rate,
                se_rate,
                ll_rate,
                {
                    "n_user_turns": f"{int(trials.sum())}",
                    "n_constructive_turns": f"{int(successes.sum())}",
                    "formula": (
                        "Cog_C_count out of user_turns ~ user framing + task ecology + length bucket + "
                        f"{'dataset fixed effects' if include_dataset else 'model/source fixed effects'}"
                    ),
                    "se_type": "conversation-robust sandwich",
                },
            ),
        ]:
            for name, b, s in zip(names, coef, coef_se):
                p = _p_value(float(b), float(s))
                out_rows.append(
                    {
                        "section": "2.2",
                        "outcome": outcome,
                        "adjustment": adjustment,
                        "term": name,
                        "label": dict(SECTION22_TERMS).get(name, name),
                        "coef_log_odds": f"{float(b):.6f}",
                        "se": f"{float(s):.6f}",
                        "z": f"{float(b) / float(s):.6f}" if s > 0 else "",
                        "p_value": f"{p:.6g}",
                        "estimate_type": "odds ratio",
                        "estimate": f"{math.exp(float(b)):.6f}",
                        "ci_low": f"{math.exp(float(b) - 1.96 * float(s)):.6f}",
                        "ci_high": f"{math.exp(float(b) + 1.96 * float(s)):.6f}",
                        "n_conversations": str(len(rows)),
                        "n_user_turns": extra["n_user_turns"],
                        "n_constructive_turns": extra["n_constructive_turns"],
                        "log_likelihood": f"{log_likelihood:.6f}",
                        "model_source_reference": reference,
                        "n_recoverable_model_source_levels": str(recoverable_count),
                        "n_model_source_fixed_effects": str(sum(1 for n in names if n.startswith("model_source::"))),
                        "formula": extra["formula"],
                        "se_type": extra["se_type"],
                        "notes": "Model/source sensitivity replaces dataset fixed effects with recoverable model or source-family indicators; model/source labels are observational metadata.",
                    }
                )
    path = OUT / "section22_model_source_sensitivity.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(out_rows)
    return out_rows


def _make_section23_design(
    rows: list[dict[str, str]],
    include_dataset: bool,
    include_model_source: bool,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str], list[str], str, int]:
    names = ["Intercept", "has_S2"] + FIG3_POISSON_COVARIATES
    names, _, reference, recoverable_count = _add_fixed_effect_columns(
        names, rows, include_dataset, include_model_source
    )
    X = np.zeros((len(rows), len(names)), dtype=float)
    count_y = np.zeros(len(rows), dtype=float)
    any_y = np.zeros(len(rows), dtype=float)
    offset = np.zeros(len(rows), dtype=float)
    clusters: list[str] = []
    name_to_idx = {name: idx for idx, name in enumerate(names)}
    for i, row in enumerate(rows):
        X[i, name_to_idx["Intercept"]] = 1
        X[i, name_to_idx["has_S2"]] = _f(row, "has_S2")
        for covariate in FIG3_POISSON_COVARIATES:
            X[i, name_to_idx[covariate]] = _f(row, covariate)
        _fill_fixed_effect_columns(X, i, row, name_to_idx)
        count_y[i] = _f(row, "Cog_C_count")
        any_y[i] = _f(row, "has_Cog_C")
        offset[i] = math.log(max(_f(row, "user_turns"), 1.0))
        clusters.append(row["conv_id"])
    return X, count_y, any_y, offset, clusters, names, reference, recoverable_count


def _append_section23_rows(
    out_rows: list[dict[str, str]],
    adjustment: str,
    term: str,
    estimate_type: str,
    model_type: str,
    coef: float,
    se: float,
    p: float,
    rows: list[dict[str, str]],
    names: list[str],
    reference: str,
    recoverable_count: int,
    log_likelihood: str,
    dispersion: str,
    formula: str,
    se_type: str,
) -> None:
    out_rows.append(
        {
            "section": "2.3",
            "model_type": model_type,
            "adjustment": adjustment,
            "term": term,
            "label": "Scaffolded support",
            "coef": f"{coef:.6f}",
            "se": f"{se:.6f}",
            "z": f"{coef / se:.6f}" if se > 0 else "",
            "p_value": f"{p:.6g}",
            "estimate_type": estimate_type,
            "estimate": f"{math.exp(coef):.6f}",
            "ci_low": f"{math.exp(coef - 1.96 * se):.6f}",
            "ci_high": f"{math.exp(coef + 1.96 * se):.6f}",
            "n_conversations": str(len(rows)),
            "n_user_turns": f"{int(sum(max(_f(row, 'user_turns'), 1.0) for row in rows))}",
            "n_constructive_turns": f"{int(sum(_f(row, 'Cog_C_count') for row in rows))}",
            "pearson_dispersion": dispersion,
            "log_likelihood": log_likelihood,
            "model_source_reference": reference,
            "n_recoverable_model_source_levels": str(recoverable_count),
            "n_model_source_fixed_effects": str(sum(1 for n in names if n.startswith("model_source::"))),
            "formula": formula,
            "se_type": se_type,
            "notes": "Pooled Section 2.3 sensitivity; model/source sensitivity replaces dataset fixed effects with recoverable model or source-family indicators.",
        }
    )


def compute_section23_model_source_sensitivity(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out_rows: list[dict[str, str]] = []
    for adjustment, include_dataset, include_model_source in [
        ("dataset FE", True, False),
        ("model/source FE", False, True),
    ]:
        X, count_y, any_y, offset, clusters, names, reference, recoverable_count = _make_section23_design(
            rows, include_dataset, include_model_source
        )
        idx = names.index("has_S2")
        fixed_effect_text = "dataset fixed effects" if include_dataset else "model/source fixed effects"

        beta_count, _, hc1_se, dispersion, _, _ = _fit_poisson_glm(X, count_y, None)
        b = float(beta_count[idx])
        s = float(hc1_se[idx])
        _append_section23_rows(
            out_rows,
            adjustment,
            "has_S2",
            "Poisson count ratio",
            "Poisson count",
            b,
            s,
            _p_value(b, s),
            rows,
            names,
            reference,
            recoverable_count,
            "",
            f"{dispersion:.4f}",
            "Cog_C_count ~ has_S2 + conversation context + " + fixed_effect_text,
            "HC1 sandwich",
        )

        beta_logit, se_logit, ll_logit = _fit_logit_cluster(X, any_y, clusters, names)
        b = float(beta_logit[idx])
        s = float(se_logit[idx])
        _append_section23_rows(
            out_rows,
            adjustment,
            "has_S2",
            "logit odds ratio",
            "Logit any constructive",
            b,
            s,
            _p_value(b, s),
            rows,
            names,
            reference,
            recoverable_count,
            f"{ll_logit:.6f}",
            "",
            "has_Cog_C ~ has_S2 + conversation context + " + fixed_effect_text,
            "conversation-robust sandwich",
        )

        beta_offset, model_se_offset, _, dispersion_offset, _, _ = _fit_poisson_glm(X, count_y, offset)
        quasi_se = model_se_offset * math.sqrt(dispersion_offset)
        b = float(beta_offset[idx])
        s = float(quasi_se[idx])
        _append_section23_rows(
            out_rows,
            adjustment,
            "has_S2",
            "offset rate ratio",
            "Poisson offset rate",
            b,
            s,
            _p_value(b, s),
            rows,
            names,
            reference,
            recoverable_count,
            "",
            f"{dispersion_offset:.4f}",
            "Cog_C_count ~ has_S2 + conversation context + " + fixed_effect_text + " + offset(log(user_turns))",
            "quasi-Poisson scaled model SE",
        )

    path = OUT / "section23_model_source_sensitivity.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(out_rows)
    return out_rows


def _make_section24_design(
    rows: list[dict[str, str]],
    include_dataset: bool,
    include_model_source: bool,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str], list[str], str, int, list[dict[str, str]]]:
    scaffolded_rows = [row for row in rows if _f(row, "has_S2") > 0]
    names = [
        "Intercept",
        "has_M1",
        "has_M2",
        "has_M3",
        "has_M4",
        "has_M5",
        "has_M6",
        "intentional_framing",
        "coding_task",
        "length_4_6_user_turns",
        "length_7plus_user_turns",
    ]
    names, _, reference, recoverable_count = _add_fixed_effect_columns(
        names, scaffolded_rows, include_dataset, include_model_source
    )
    X = np.zeros((len(scaffolded_rows), len(names)), dtype=float)
    successes = np.zeros(len(scaffolded_rows), dtype=float)
    trials = np.zeros(len(scaffolded_rows), dtype=float)
    clusters: list[str] = []
    name_to_idx = {name: idx for idx, name in enumerate(names)}
    for i, row in enumerate(scaffolded_rows):
        user_turns = _f(row, "user_turns")
        X[i, name_to_idx["Intercept"]] = 1
        for support_key, _ in SUPPORT_FORM_TERMS:
            X[i, name_to_idx[support_key]] = _f(row, support_key)
        X[i, name_to_idx["intentional_framing"]] = _f(row, "is_intentional")
        X[i, name_to_idx["coding_task"]] = _f(row, "is_coding_topic")
        X[i, name_to_idx["length_4_6_user_turns"]] = 1 if 4 <= user_turns <= 6 else 0
        X[i, name_to_idx["length_7plus_user_turns"]] = 1 if user_turns >= 7 else 0
        _fill_fixed_effect_columns(X, i, row, name_to_idx)
        trials[i] = max(user_turns, 1.0)
        successes[i] = min(_f(row, "Cog_C_count"), trials[i])
        clusters.append(row["conv_id"])
    return X, successes, trials, clusters, names, reference, recoverable_count, scaffolded_rows


def compute_section24_support_form_model_source_sensitivity(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out_rows: list[dict[str, str]] = []
    for adjustment, include_dataset, include_model_source in [
        ("dataset FE", True, False),
        ("model/source FE", False, True),
    ]:
        X, successes, trials, clusters, names, reference, recoverable_count, scaffolded_rows = _make_section24_design(
            rows, include_dataset, include_model_source
        )
        beta, se, ll = _fit_grouped_binomial_cluster(X, successes, trials, clusters)
        fixed_effect_text = "dataset fixed effects" if include_dataset else "model/source fixed effects"
        for support_key, label in SUPPORT_FORM_TERMS:
            idx = names.index(support_key)
            b = float(beta[idx])
            s = float(se[idx])
            p = _p_value(b, s)
            out_rows.append(
                {
                    "section": "2.4",
                    "model_type": "grouped-binomial constructive-turn rate",
                    "adjustment": adjustment,
                    "term": support_key,
                    "label": label,
                    "coef_log_odds": f"{b:.6f}",
                    "se": f"{s:.6f}",
                    "z": f"{b / s:.6f}" if s > 0 else "",
                    "p_value": f"{p:.6g}",
                    "estimate_type": "odds ratio",
                    "estimate": f"{math.exp(b):.6f}",
                    "ci_low": f"{math.exp(b - 1.96 * s):.6f}",
                    "ci_high": f"{math.exp(b + 1.96 * s):.6f}",
                    "n_conversations": str(len(scaffolded_rows)),
                    "n_user_turns": f"{int(trials.sum())}",
                    "n_constructive_turns": f"{int(successes.sum())}",
                    "log_likelihood": f"{ll:.6f}",
                    "model_source_reference": reference,
                    "n_recoverable_model_source_levels": str(recoverable_count),
                    "n_model_source_fixed_effects": str(sum(1 for n in names if n.startswith("model_source::"))),
                    "formula": (
                        "Cog_C_count out of user_turns ~ M1 + M2 + M3 + M4 + M5 + M6 + "
                        "user framing + task ecology + length bucket + " + fixed_effect_text
                    ),
                    "se_type": "conversation-robust sandwich",
                    "notes": "Pooled Section 2.4 sensitivity restricted to conversations containing scaffolded support; support-form labels are non-exclusive and entered jointly.",
                }
            )
    path = OUT / "section24_support_form_model_source_sensitivity.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(out_rows)
    return out_rows


def write_section22_table(rows: list[dict[str, str]]) -> None:
    by_key = {(row["outcome"], row["adjustment"], row["term"]): row for row in rows}
    path = ROOT / "tables" / "table_section22_model_source_sensitivity.tex"
    with open(path, "w") as f:
        f.write("\\begin{table*}[p]\n\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\revise{\\textbf{Model/source sensitivity for Section~2.2 context models.} "
            "The dataset fixed-effect models match the context models reported for Section~2.2. "
            "The model/source sensitivity replaces dataset fixed effects with recoverable assistant-model or source-family indicators. "
            "Model/source levels with at least 100 conversations are represented as fixed-effect indicators; rarer levels are absorbed into the reference category. "
            "Cells report odds ratios with 95\\% confidence intervals and two-sided p values from conversation-robust standard errors.}}\\label{tab:section22_model_source_sensitivity}\n"
        )
        f.write("\\setlength{\\tabcolsep}{5pt}\n\\renewcommand{\\arraystretch}{1.10}\n")
        f.write("\\resizebox{0.92\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{llcc}\n\\toprule\n")
        f.write("Outcome & Predictor & Dataset FE & Model/source FE \\\\\n\\midrule\n")
        first = True
        for outcome, outcome_label in [
            ("any constructive turn", "Any constructive turn"),
            ("constructive-turn rate", "Constructive-turn rate"),
        ]:
            for term, label in SECTION22_TERMS:
                panel = outcome_label if first or term == SECTION22_TERMS[0][0] else ""
                first = False
                f.write(
                    f"{panel} & {label} & "
                    f"{_or_cell(by_key[(outcome, 'dataset FE', term)])} & "
                    f"{_or_cell(by_key[(outcome, 'model/source FE', term)])} \\\\\n"
                )
            f.write("\\midrule\n")
        n = int(next(row for row in rows if row["adjustment"] == "dataset FE")["n_conversations"])
        model_fe = int(next(row for row in rows if row["adjustment"] == "model/source FE")["n_model_source_fixed_effects"])
        f.write(f"Conversations & & {n:,} & {n:,} \\\\\n")
        f.write(f"Model/source fixed effects & & -- & {model_fe} \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")


def write_section21_table(rows: list[dict[str, str]]) -> None:
    path = ROOT / "tables" / "table_section21_model_source_breakdown.tex"
    with open(path, "w") as f:
        f.write("\\begin{table*}[p]\n\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\revise{\\textbf{Model/source breakdown for Section~2.1 descriptive engagement measures.} "
            "Ranges summarize recoverable assistant-model or source-family levels with at least 100 conversations within each task setting. "
            "The full model/source rows, including passive, active, constructive, overall cognitive engagement, emotional expression and scaffolded-support percentages, are exported in the source CSV.}}\\label{tab:section21_model_source_breakdown}\n"
        )
        f.write("\\setlength{\\tabcolsep}{4pt}\n\\renewcommand{\\arraystretch}{1.10}\n")
        f.write("\\resizebox{0.94\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{lcccc}\n\\toprule\n")
        f.write("Setting & Model/source levels & Cognitive overall, \\% & Constructive, \\% & Scaffolded support, \\% \\\\\n\\midrule\n")
        for row in rows:
            f.write(
                f"{row['setting']} & {row['n_model_source_levels_ge_100_conversations']} & "
                f"{row['cognitive_overall_min_pct']}--{row['cognitive_overall_max_pct']} "
                f"(median {row['cognitive_overall_median_pct']}) & "
                f"{row['constructive_min_pct']}--{row['constructive_max_pct']} "
                f"(median {row['constructive_median_pct']}) & "
                f"{row['scaffolded_min_pct']}--{row['scaffolded_max_pct']} "
                f"(median {row['scaffolded_median_pct']}) \\\\\n"
            )
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")


def write_section23_table(rows: list[dict[str, str]]) -> None:
    by_key = {(row["model_type"], row["adjustment"]): row for row in rows}
    path = ROOT / "tables" / "table_section23_model_source_sensitivity.tex"
    with open(path, "w") as f:
        f.write("\\begin{table*}[p]\n\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\revise{\\textbf{Model/source sensitivity for Section~2.3 scaffolded-support models.} "
            "Pooled sensitivity models compare dataset fixed effects with recoverable assistant-model or source-family fixed effects. "
            "Model/source levels with at least 100 conversations are represented as fixed-effect indicators; rarer levels are absorbed into the reference category. "
            "Rows report the scaffolded-support coefficient from models predicting constructive-turn counts, any constructive turn and constructive-turn rate. "
            "These checks supplement the main setting-level estimates in Fig.~\\ref{fig:s2_conversation_association}b and Table~\\ref{tab:support_engagement_summary}.}}\\label{tab:section23_model_source_sensitivity}\n"
        )
        f.write("\\setlength{\\tabcolsep}{5pt}\n\\renewcommand{\\arraystretch}{1.10}\n")
        f.write("\\resizebox{0.86\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{lcc}\n\\toprule\n")
        f.write("Model & Dataset FE & Model/source FE \\\\\n\\midrule\n")
        for model_type, label in [
            ("Poisson count", "Poisson count ratio"),
            ("Logit any constructive", "Logit odds ratio"),
            ("Poisson offset rate", "Offset rate ratio"),
        ]:
            f.write(
                f"{label} & {_or_cell(by_key[(model_type, 'dataset FE')])} & "
                f"{_or_cell(by_key[(model_type, 'model/source FE')])} \\\\\n"
            )
        n = int(rows[0]["n_conversations"])
        model_fe = int(next(row for row in rows if row["adjustment"] == "model/source FE")["n_model_source_fixed_effects"])
        f.write("\\midrule\n")
        f.write(f"Conversations & {n:,} & {n:,} \\\\\n")
        f.write(f"Model/source fixed effects & -- & {model_fe} \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")


def write_section24_table(rows: list[dict[str, str]]) -> None:
    by_key = {(row["adjustment"], row["term"]): row for row in rows}
    path = ROOT / "tables" / "table_section24_support_form_model_source_sensitivity.tex"
    with open(path, "w") as f:
        f.write("\\begin{table*}[p]\n\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\revise{\\textbf{Model/source sensitivity for Section~2.4 support-form models.} "
            "The sensitivity is restricted to conversations containing scaffolded support and enters the six non-exclusive support-form indicators jointly. "
            "Cells report odds ratios for constructive-turn rate with 95\\% confidence intervals and two-sided p values from conversation-robust standard errors. "
            "This model/source check complements, but does not replace, the descriptive percentage-point support-form contrasts in Fig.~\\ref{fig:support_form_supply}.}}\\label{tab:section24_support_form_model_source_sensitivity}\n"
        )
        f.write("\\setlength{\\tabcolsep}{5pt}\n\\renewcommand{\\arraystretch}{1.10}\n")
        f.write("\\resizebox{0.82\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{lcc}\n\\toprule\n")
        f.write("Support form & Dataset FE & Model/source FE \\\\\n\\midrule\n")
        for term, label in SUPPORT_FORM_TERMS:
            f.write(
                f"{label} & {_or_cell(by_key[('dataset FE', term)])} & "
                f"{_or_cell(by_key[('model/source FE', term)])} \\\\\n"
            )
        n = int(rows[0]["n_conversations"])
        model_fe = int(next(row for row in rows if row["adjustment"] == "model/source FE")["n_model_source_fixed_effects"])
        f.write("\\midrule\n")
        f.write(f"Scaffolded conversations & {n:,} & {n:,} \\\\\n")
        f.write(f"Model/source fixed effects & -- & {model_fe} \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")


def main() -> None:
    rows = _load_level2_rows()
    _, section21_summary = compute_section21_model_source_breakdown(rows)
    section22 = compute_section22_model_source_sensitivity(rows)
    section23 = compute_section23_model_source_sensitivity(rows)
    section24 = compute_section24_support_form_model_source_sensitivity(rows)
    write_section21_table(section21_summary)
    write_section22_table(section22)
    write_section23_table(section23)
    write_section24_table(section24)


if __name__ == "__main__":
    main()
