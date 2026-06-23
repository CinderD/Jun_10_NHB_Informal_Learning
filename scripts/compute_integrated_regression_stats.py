from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "integrated_regression"
OUT.mkdir(parents=True, exist_ok=True)


LEVEL2 = {
    "WC coding": (
        "WildChat",
        "coding",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/latest/coding/wildchat_coding_level2/level2_reports/level2_metrics_20260411_212300.csv",
    ),
    "LMSYS coding": (
        "LMSYS",
        "coding",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/coding/lmsys_coding_level2/level2_reports/level2_metrics_20260609_152938.csv",
    ),
    "SC coding": (
        "ShareChat",
        "coding",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/coding/sharechat_coding_level2/level2_reports/level2_metrics_20260602_125948.csv",
    ),
    "WC writing": (
        "WildChat",
        "writing",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/latest/writing/wildchat_writing_level2/level2_reports/level2_metrics_20260411_212539.csv",
    ),
    "LMSYS writing": (
        "LMSYS",
        "writing",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/writing/lmsys_writing_level2/level2_reports/level2_metrics_20260609_153057.csv",
    ),
    "SC writing": (
        "ShareChat",
        "writing",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/writing/sharechat_writing_level2/level2_reports/level2_metrics_20260602_130002.csv",
    ),
}


LEVEL3_A2U = {
    "WC coding": (
        "WildChat",
        "coding",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/latest/coding/wildchat_coding_level3/level3_reports/level3_a2u_pairs_20260411_212559.csv",
    ),
    "LMSYS coding": (
        "LMSYS",
        "coding",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/coding/lmsys_coding_level3/level3_reports/level3_a2u_pairs_20260609_153113.csv",
    ),
    "SC coding": (
        "ShareChat",
        "coding",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/coding/sharechat_coding_level3/level3_reports/level3_a2u_pairs_20260602_130009.csv",
    ),
    "WC writing": (
        "WildChat",
        "writing",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/latest/writing/wildchat_writing_level3/level3_reports/level3_a2u_pairs_20260411_212622.csv",
    ),
    "LMSYS writing": (
        "LMSYS",
        "writing",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/writing/lmsys_writing_level3/level3_reports/level3_a2u_pairs_20260609_153128.csv",
    ),
    "SC writing": (
        "ShareChat",
        "writing",
        "/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/writing/sharechat_writing_level3/level3_reports/level3_a2u_pairs_20260602_130016.csv",
    ),
}


def _f(row: dict[str, str], key: str, default: float = 0.0) -> float:
    val = row.get(key, "")
    if val == "" or val is None:
        return default
    try:
        return float(val)
    except ValueError:
        return default


def _read_csv(path: str) -> list[dict[str, str]]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _two_sided_p_from_bootstrap(estimate: float, draws: np.ndarray) -> float:
    se = float(np.std(draws, ddof=1))
    if se == 0:
        return 0.0 if estimate != 0 else 1.0
    z = estimate / se
    return float(math.erfc(abs(z) / math.sqrt(2)))


def _bootstrap_diff(
    rows: list[dict[str, str]],
    numerator_key: str,
    denominator_key: str | None,
    group_key: str,
    value_key: str | None = None,
    n_boot: int = 1000,
    seed: int = 20260616,
) -> tuple[float, float, float, float]:
    rng = np.random.default_rng(seed)
    has = [r for r in rows if r[group_key] == "1"]
    ref = [r for r in rows if r[group_key] != "1"]

    def estimate(sample: list[dict[str, str]]) -> float:
        if value_key is not None:
            return float(np.mean([_f(r, value_key) for r in sample]))
        num = sum(_f(r, numerator_key) for r in sample)
        den = sum(_f(r, denominator_key or "") for r in sample)
        return num / den if den else 0.0

    point = estimate(has) - estimate(ref)
    draws = np.empty(n_boot)
    has_idx = np.arange(len(has))
    ref_idx = np.arange(len(ref))
    for i in range(n_boot):
        hs = [has[j] for j in rng.choice(has_idx, size=len(has_idx), replace=True)]
        rs = [ref[j] for j in rng.choice(ref_idx, size=len(ref_idx), replace=True)]
        draws[i] = estimate(hs) - estimate(rs)
    low, high = np.percentile(draws, [2.5, 97.5])
    return point, float(low), float(high), _two_sided_p_from_bootstrap(point, draws)


def compute_key_contrasts() -> None:
    rows_out: list[dict[str, str]] = []
    for setting, (_, _, path) in LEVEL2.items():
        rows = _read_csv(path)
        c_diff, c_low, c_high, c_p = _bootstrap_diff(rows, "Cog_C_count", "user_turns", "has_S2")
        d_diff, d_low, d_high, d_p = _bootstrap_diff(
            rows, "", None, "has_S2", value_key="depth_after_first_answer"
        )
        rows_out.append(
            {
                "setting": setting,
                "contrast": "constructive_ratio_has_s2_minus_no_s2",
                "estimate": f"{c_diff * 100:.4f}",
                "estimate_label": "percentage-point difference",
                "ci_low": f"{c_low * 100:.4f}",
                "ci_high": f"{c_high * 100:.4f}",
                "p_value": f"{c_p:.6g}",
                "effect_size": f"{c_diff * 100:.4f} pp",
                "method": "conversation bootstrap, weighted by user turns",
                "n_conversations": str(len(rows)),
            }
        )
        rows_out.append(
            {
                "setting": setting,
                "contrast": "post_answer_depth_has_s2_minus_no_s2",
                "estimate": f"{d_diff:.4f}",
                "estimate_label": "turn difference",
                "ci_low": f"{d_low:.4f}",
                "ci_high": f"{d_high:.4f}",
                "p_value": f"{d_p:.6g}",
                "effect_size": f"{d_diff:.4f} turns",
                "method": "conversation bootstrap",
                "n_conversations": str(len(rows)),
            }
        )

    for setting, (_, _, path) in LEVEL3_A2U.items():
        pairs = _read_csv(path)
        by_conv: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0, 0])
        for r in pairs:
            support = r.get("asst_Support_Type")
            if support not in {"S1", "S2"}:
                continue
            bucket = by_conv[r["conv_id"]]
            y = 1 if r.get("next_user_is_C") == "1" else 0
            if support == "S2":
                bucket[0] += y
                bucket[1] += 1
            else:
                bucket[2] += y
                bucket[3] += 1
        arr = np.asarray(list(by_conv.values()), dtype=float)

        def adj_est(sample: np.ndarray) -> float:
            p2 = sample[:, 0].sum() / sample[:, 1].sum()
            p1 = sample[:, 2].sum() / sample[:, 3].sum()
            return p2 - p1

        point = adj_est(arr)
        rng = np.random.default_rng(20260617)
        draws = np.empty(1000)
        idx = np.arange(arr.shape[0])
        for i in range(1000):
            draws[i] = adj_est(arr[rng.choice(idx, size=len(idx), replace=True)])
        low, high = np.percentile(draws, [2.5, 97.5])
        p = _two_sided_p_from_bootstrap(point, draws)
        rows_out.append(
            {
                "setting": setting,
                "contrast": "adjacent_next_constructive_s2_minus_s1",
                "estimate": f"{point * 100:.4f}",
                "estimate_label": "percentage-point difference",
                "ci_low": f"{low * 100:.4f}",
                "ci_high": f"{high * 100:.4f}",
                "p_value": f"{p:.6g}",
                "effect_size": f"{point * 100:.4f} pp",
                "method": "conversation-cluster bootstrap over A2U pairs",
                "n_conversations": str(arr.shape[0]),
            }
        )

    out_path = OUT / "key_percentage_lifts_significance.csv"
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        writer.writeheader()
        writer.writerows(rows_out)


def _sigmoid(eta: np.ndarray) -> np.ndarray:
    return np.where(eta >= 0, 1 / (1 + np.exp(-eta)), np.exp(eta) / (1 + np.exp(eta)))


def _fit_logit_cluster(
    X: np.ndarray,
    y: np.ndarray,
    clusters: list[str],
    names: list[str],
    max_iter: int = 80,
) -> tuple[np.ndarray, np.ndarray, float]:
    beta = np.zeros(X.shape[1])
    for _ in range(max_iter):
        eta = X @ beta
        p = np.clip(_sigmoid(eta), 1e-6, 1 - 1e-6)
        w = p * (1 - p)
        z = eta + (y - p) / w
        xtw = X.T * w
        h = xtw @ X
        # Tiny ridge only stabilizes rare dummy columns; reported SEs use the unpenalized bread below.
        step_beta = np.linalg.solve(h + np.eye(h.shape[0]) * 1e-8, xtw @ z)
        if np.max(np.abs(step_beta - beta)) < 1e-7:
            beta = step_beta
            break
        beta = step_beta

    p = np.clip(_sigmoid(X @ beta), 1e-6, 1 - 1e-6)
    w = p * (1 - p)
    bread = np.linalg.inv((X.T * w) @ X + np.eye(X.shape[1]) * 1e-8)
    meat = np.zeros((X.shape[1], X.shape[1]))
    scores = X * (y - p)[:, None]
    cluster_scores: dict[str, np.ndarray] = defaultdict(lambda: np.zeros(X.shape[1]))
    for cluster, score in zip(clusters, scores):
        cluster_scores[cluster] += score
    for score in cluster_scores.values():
        meat += np.outer(score, score)
    g = len(cluster_scores)
    n, k = X.shape
    correction = (g / (g - 1)) * ((n - 1) / (n - k)) if g > 1 and n > k else 1.0
    cov = bread @ meat @ bread * correction
    se = np.sqrt(np.maximum(np.diag(cov), 0))
    ll = float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return beta, se, ll


def _assistant_model_key(row: dict[str, str]) -> str:
    explicit = (row.get("chat_model") or "").strip()
    if explicit:
        return f"{row.get('_dataset', 'unknown')}::{explicit}"
    parts = (row.get("conv_id") or "").split("::")
    if len(parts) >= 3 and parts[1]:
        # LMSYS stores the model in conv_id; ShareChat stores the public assistant/source
        # family (for example chatgpt/perplexity), not a precise model version.
        return f"{row.get('_dataset', 'unknown')}::{parts[1]}"
    return ""


def _make_design(
    rows: list[dict[str, str]],
    include_s2: bool = True,
    include_support_forms: bool = True,
    include_dataset: bool = True,
    include_model: bool = False,
) -> tuple[np.ndarray, np.ndarray, list[str], list[str]]:
    names = [
        "Intercept",
        "prior_user_constructive",
        "prior_user_active",
        "prior_user_passive",
        "prior_user_emotional",
        "prior_user_error",
        "intentional_framing",
        "coding_task",
        "log_assistant_turn_index",
    ]
    if include_s2:
        names.insert(1, "scaffolded_support_S2")
    if include_support_forms:
        names.extend([f"M{i}" for i in range(1, 7)])
    if include_dataset:
        names.extend(["dataset_LMSYS", "dataset_ShareChat"])
    model_levels: list[str] = []
    if include_model:
        counts = Counter(_assistant_model_key(r) for r in rows)
        model_levels = sorted([m for m, c in counts.items() if m and c >= 100])
        if model_levels:
            ref = model_levels[0]
            model_levels = [m for m in model_levels if m != ref]
            names.extend([f"model_{m}" for m in model_levels])

    X = np.zeros((len(rows), len(names)), dtype=float)
    y = np.zeros(len(rows), dtype=float)
    clusters = []
    name_to_idx = {name: i for i, name in enumerate(names)}
    for i, r in enumerate(rows):
        X[i, name_to_idx["Intercept"]] = 1
        if include_s2:
            X[i, name_to_idx["scaffolded_support_S2"]] = 1 if r.get("asst_Support_Type") == "S2" else 0
        lvl = r.get("prev_user_Cognitive_level") or "NA"
        X[i, name_to_idx["prior_user_constructive"]] = 1 if lvl == "C" else 0
        X[i, name_to_idx["prior_user_active"]] = 1 if lvl == "A" else 0
        X[i, name_to_idx["prior_user_passive"]] = 1 if lvl == "P" else 0
        X[i, name_to_idx["prior_user_emotional"]] = _f(r, "prev_user_Emotional")
        X[i, name_to_idx["prior_user_error"]] = _f(r, "prev_user_is_error")
        X[i, name_to_idx["intentional_framing"]] = _f(r, "is_intentional")
        X[i, name_to_idx["coding_task"]] = _f(r, "is_coding_topic")
        X[i, name_to_idx["log_assistant_turn_index"]] = math.log1p(_f(r, "asst_turn_index"))
        if include_support_forms:
            for j in range(1, 7):
                X[i, name_to_idx[f"M{j}"]] = _f(r, f"asst_has_M{j}")
        if include_dataset:
            X[i, name_to_idx["dataset_LMSYS"]] = 1 if r["_dataset"] == "LMSYS" else 0
            X[i, name_to_idx["dataset_ShareChat"]] = 1 if r["_dataset"] == "ShareChat" else 0
        if include_model:
            m = _assistant_model_key(r)
            key = f"model_{m}"
            if key in name_to_idx:
                X[i, name_to_idx[key]] = 1
        y[i] = _f(r, "next_user_is_C")
        clusters.append(r["conv_id"])
    return X, y, clusters, names


PRIOR_STATES = [
    ("constructive", "C", "prior constructive"),
    ("active", "A", "prior active"),
    ("passive", "P", "prior passive"),
]


def _make_interaction_design(
    rows: list[dict[str, str]],
    include_dataset: bool,
    include_model: bool,
) -> tuple[np.ndarray, np.ndarray, list[str], list[str]]:
    base_x, y, clusters, names = _make_design(
        rows,
        include_s2=True,
        include_support_forms=True,
        include_dataset=include_dataset,
        include_model=include_model,
    )
    interaction_names = [f"prior_{state}_x_M{j}" for state, _, _ in PRIOR_STATES for j in range(1, 7)]
    X = np.zeros((base_x.shape[0], base_x.shape[1] + len(interaction_names)), dtype=float)
    X[:, : base_x.shape[1]] = base_x
    for i, r in enumerate(rows):
        lvl = r.get("prev_user_Cognitive_level") or ""
        offset = base_x.shape[1]
        for state, code, _ in PRIOR_STATES:
            for j in range(1, 7):
                X[i, offset] = _f(r, f"asst_has_M{j}") if lvl == code else 0.0
                offset += 1
    return X, y, clusters, names + interaction_names


def _load_a2u_rows(wildchat_only: bool = False) -> list[dict[str, str]]:
    rows = []
    for setting, (dataset, task, path) in LEVEL3_A2U.items():
        if wildchat_only and dataset != "WildChat":
            continue
        for r in _read_csv(path):
            if r.get("asst_Support_Type") not in {"S1", "S2"}:
                continue
            r["_setting"] = setting
            r["_dataset"] = dataset
            r["_task"] = task
            rows.append(r)
    return rows


def _load_level2_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for setting, (dataset, task, path) in LEVEL2.items():
        for r in _read_csv(path):
            r["_setting"] = setting
            r["_dataset"] = dataset
            r["_task"] = task
            rows.append(r)
    return rows


def _make_constructive_context_design(
    rows: list[dict[str, str]],
) -> tuple[np.ndarray, np.ndarray, list[str], list[str]]:
    names = [
        "Intercept",
        "intentional_framing",
        "coding_task",
        "length_4_6_user_turns",
        "length_7plus_user_turns",
        "dataset_LMSYS",
        "dataset_ShareChat",
    ]
    X = np.zeros((len(rows), len(names)), dtype=float)
    y = np.zeros(len(rows), dtype=float)
    clusters: list[str] = []
    name_to_idx = {name: i for i, name in enumerate(names)}
    for i, r in enumerate(rows):
        user_turns = _f(r, "user_turns")
        X[i, name_to_idx["Intercept"]] = 1
        X[i, name_to_idx["intentional_framing"]] = _f(r, "is_intentional")
        X[i, name_to_idx["coding_task"]] = _f(r, "is_coding_topic")
        X[i, name_to_idx["length_4_6_user_turns"]] = 1 if 4 <= user_turns <= 6 else 0
        X[i, name_to_idx["length_7plus_user_turns"]] = 1 if user_turns >= 7 else 0
        X[i, name_to_idx["dataset_LMSYS"]] = 1 if r["_dataset"] == "LMSYS" else 0
        X[i, name_to_idx["dataset_ShareChat"]] = 1 if r["_dataset"] == "ShareChat" else 0
        y[i] = _f(r, "has_Cog_C")
        clusters.append(r["conv_id"])
    return X, y, clusters, names


def _make_constructive_rate_design(
    rows: list[dict[str, str]],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str], list[str]]:
    X, _, clusters, names = _make_constructive_context_design(rows)
    successes = np.asarray([_f(r, "Cog_C_count") for r in rows], dtype=float)
    trials = np.asarray([max(_f(r, "user_turns"), 1.0) for r in rows], dtype=float)
    successes = np.minimum(successes, trials)
    return X, successes, trials, clusters, names


def _fit_grouped_binomial_cluster(
    X: np.ndarray,
    successes: np.ndarray,
    trials: np.ndarray,
    clusters: list[str],
    max_iter: int = 80,
) -> tuple[np.ndarray, np.ndarray, float]:
    beta = np.zeros(X.shape[1])
    y_rate = successes / trials
    for _ in range(max_iter):
        eta = X @ beta
        p = np.clip(_sigmoid(eta), 1e-6, 1 - 1e-6)
        w = trials * p * (1 - p)
        z = eta + (y_rate - p) / (p * (1 - p))
        xtw = X.T * w
        h = xtw @ X
        step_beta = np.linalg.solve(h + np.eye(h.shape[0]) * 1e-8, xtw @ z)
        if np.max(np.abs(step_beta - beta)) < 1e-7:
            beta = step_beta
            break
        beta = step_beta

    p = np.clip(_sigmoid(X @ beta), 1e-6, 1 - 1e-6)
    w = trials * p * (1 - p)
    bread = np.linalg.inv((X.T * w) @ X + np.eye(X.shape[1]) * 1e-8)
    scores = X * (successes - trials * p)[:, None]
    meat = np.zeros((X.shape[1], X.shape[1]))
    cluster_scores: dict[str, np.ndarray] = defaultdict(lambda: np.zeros(X.shape[1]))
    for cluster, score in zip(clusters, scores):
        cluster_scores[cluster] += score
    for score in cluster_scores.values():
        meat += np.outer(score, score)
    g = len(cluster_scores)
    n, k = X.shape
    correction = (g / (g - 1)) * ((n - 1) / (n - k)) if g > 1 and n > k else 1.0
    cov = bread @ meat @ bread * correction
    se = np.sqrt(np.maximum(np.diag(cov), 0))
    ll = float(
        np.sum(successes * np.log(p) + (trials - successes) * np.log(1 - p))
    )
    return beta, se, ll


FIG3_POISSON_COVARIATES = [
    "is_intentional",
    "is_coding_topic",
    "total_turns",
    "Emo_ratio",
    "has_error",
    "persistence_after_failure",
    "high_persistence",
]


def _make_fig3_poisson_design(
    rows: list[dict[str, str]],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    names = ["Intercept", "has_S2"] + FIG3_POISSON_COVARIATES
    X = np.zeros((len(rows), len(names)), dtype=float)
    y = np.zeros(len(rows), dtype=float)
    offset = np.zeros(len(rows), dtype=float)
    name_to_idx = {name: i for i, name in enumerate(names)}
    for i, r in enumerate(rows):
        X[i, name_to_idx["Intercept"]] = 1
        X[i, name_to_idx["has_S2"]] = _f(r, "has_S2")
        for covariate in FIG3_POISSON_COVARIATES:
            X[i, name_to_idx[covariate]] = _f(r, covariate)
        y[i] = _f(r, "Cog_C_count")
        offset[i] = math.log(max(_f(r, "user_turns"), 1.0))
    return X, y, offset, names


def _fit_poisson_glm(
    X: np.ndarray,
    y: np.ndarray,
    offset: np.ndarray | None = None,
    max_iter: int = 100,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float, int]:
    if offset is None:
        offset = np.zeros(len(y), dtype=float)
    exposure = np.exp(offset)
    beta = np.zeros(X.shape[1], dtype=float)
    beta[0] = math.log(max(float(y.sum() / exposure.sum()), 1e-8))

    for _ in range(max_iter):
        eta = np.clip(offset + X @ beta, -30, 30)
        mu = np.exp(eta)
        gradient = X.T @ (y - mu)
        hessian = (X.T * mu) @ X
        step = np.linalg.solve(hessian + np.eye(hessian.shape[0]) * 1e-8, gradient)
        beta = beta + step
        if float(np.max(np.abs(step))) < 1e-9:
            break

    eta = np.clip(offset + X @ beta, -30, 30)
    mu = np.exp(eta)
    hessian = (X.T * mu) @ X
    bread = np.linalg.inv(hessian + np.eye(hessian.shape[0]) * 1e-8)
    model_se = np.sqrt(np.maximum(np.diag(bread), 0))

    scores = X * (y - mu)[:, None]
    meat = scores.T @ scores
    n, k = X.shape
    hc1_correction = n / (n - k) if n > k else 1.0
    hc1_cov = bread @ meat @ bread * hc1_correction
    hc1_se = np.sqrt(np.maximum(np.diag(hc1_cov), 0))

    pearson = float(np.sum((y - mu) ** 2 / np.clip(mu, 1e-8, None)))
    df_resid = n - k
    dispersion = pearson / df_resid if df_resid > 0 else float("nan")
    return beta, model_se, hc1_se, dispersion, pearson, df_resid


def compute_fig3_offset_rate_sensitivity() -> None:
    out_rows: list[dict[str, str]] = []
    formula = (
        "Cog_C_count ~ has_S2 + is_intentional + is_coding_topic + total_turns + "
        "Emo_ratio + has_error + persistence_after_failure + high_persistence + offset(log(user_turns))"
    )
    covariates = "has_S2; " + "; ".join(FIG3_POISSON_COVARIATES)
    for setting, (_, _, path) in LEVEL2.items():
        rows = _read_csv(path)
        X, y, offset, names = _make_fig3_poisson_design(rows)
        beta, model_se, hc1_se, dispersion, pearson, df_resid = _fit_poisson_glm(X, y, offset)
        se_specs = [
            ("model_based", model_se),
            ("HC1_sandwich", hc1_se),
            ("quasi_poisson_scaled", model_se * math.sqrt(dispersion)),
        ]
        idx = names.index("has_S2")
        for se_type, se_vec in se_specs:
            b = float(beta[idx])
            s = float(se_vec[idx])
            z = b / s if s > 0 else float("nan")
            p = math.erfc(abs(z) / math.sqrt(2)) if s > 0 else float("nan")
            out_rows.append(
                {
                    "setting": setting,
                    "outcome": "constructive-turn count per user turn",
                    "formula": formula,
                    "offset": "log(user_turns)",
                    "term": "has_S2",
                    "estimate_rr": f"{math.exp(b):.6f}",
                    "ci_low": f"{math.exp(b - 1.96 * s):.6f}",
                    "ci_high": f"{math.exp(b + 1.96 * s):.6f}",
                    "p_value": f"{p:.6g}",
                    "se_type": se_type,
                    "pearson_dispersion": f"{dispersion:.4f}",
                    "pearson_chi2": f"{pearson:.4f}",
                    "df_resid": str(df_resid),
                    "n_conversations": str(len(rows)),
                    "n_user_turns": f"{int(sum(max(_f(r, 'user_turns'), 1.0) for r in rows))}",
                    "n_constructive_turns": f"{int(sum(_f(r, 'Cog_C_count') for r in rows))}",
                    "covariates": covariates,
                    "notes": "Section 2.3 sensitivity; same setting-specific covariates as the primary Poisson count model, with user turns represented as the exposure offset.",
                }
            )
    with open(OUT / "fig3_poisson_offset_rate_sensitivity.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)


def compute_constructive_context_logit() -> None:
    rows = _load_level2_rows()
    X, y, clusters, names = _make_constructive_context_design(rows)
    beta, se, ll = _fit_logit_cluster(X, y, clusters, names)
    label_map = {
        "intentional_framing": "Intentional framing",
        "coding_task": "Coding task ecology",
        "length_4_6_user_turns": "4--6 user turns",
        "length_7plus_user_turns": "7+ user turns",
        "dataset_LMSYS": "LMSYS Chat",
        "dataset_ShareChat": "ShareChat",
    }
    formula = "any constructive user turn ~ user framing + task ecology + length bucket + dataset fixed effects"
    out_rows: list[dict[str, str]] = []
    for name, b, s in zip(names, beta, se):
        z = b / s if s > 0 else float("nan")
        p = math.erfc(abs(z) / math.sqrt(2)) if s > 0 else float("nan")
        out_rows.append(
            {
                "term": name,
                "label": label_map.get(name, "Intercept"),
                "coef_log_odds": f"{b:.6f}",
                "cluster_robust_se": f"{s:.6f}",
                "z": f"{z:.6f}",
                "p_value": f"{p:.6g}",
                "odds_ratio": f"{math.exp(b):.6f}",
                "ci_low": f"{math.exp(b - 1.96 * s):.6f}",
                "ci_high": f"{math.exp(b + 1.96 * s):.6f}",
                "n_conversations": str(len(rows)),
                "log_likelihood": f"{ll:.6f}",
                "formula": formula,
                "reference": "unintentional framing, writing task, 2--3 user turns, WildChat",
                "se_type": "conversation-robust sandwich",
                "notes": "Section 2.2 robustness check; estimates are associational and do not identify causal effects.",
            }
        )
    with open(OUT / "constructive_context_logit.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)

    Xr, successes, trials, clusters, names = _make_constructive_rate_design(rows)
    beta, se, ll = _fit_grouped_binomial_cluster(Xr, successes, trials, clusters)
    formula = "constructive user-turn count out of user turns ~ user framing + task ecology + length bucket + dataset fixed effects"
    rate_rows: list[dict[str, str]] = []
    for name, b, s in zip(names, beta, se):
        z = b / s if s > 0 else float("nan")
        p = math.erfc(abs(z) / math.sqrt(2)) if s > 0 else float("nan")
        rate_rows.append(
            {
                "term": name,
                "label": label_map.get(name, "Intercept"),
                "coef_log_odds": f"{b:.6f}",
                "conversation_robust_se": f"{s:.6f}",
                "z": f"{z:.6f}",
                "p_value": f"{p:.6g}",
                "odds_ratio": f"{math.exp(b):.6f}",
                "ci_low": f"{math.exp(b - 1.96 * s):.6f}",
                "ci_high": f"{math.exp(b + 1.96 * s):.6f}",
                "n_conversations": str(len(rows)),
                "n_user_turns": f"{int(trials.sum())}",
                "n_constructive_turns": f"{int(successes.sum())}",
                "log_likelihood_without_constants": f"{ll:.6f}",
                "formula": formula,
                "reference": "unintentional framing, writing task, 2--3 user turns, WildChat",
                "se_type": "conversation-robust sandwich",
                "notes": "Section 2.2 rate sensitivity; grouped-binomial model uses user turns as the denominator to reduce the mechanical opportunity effect in any-constructive outcomes.",
            }
        )
    with open(OUT / "constructive_rate_context_logit.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rate_rows[0].keys()))
        writer.writeheader()
        writer.writerows(rate_rows)


def _write_model_rows(
    output_name: str,
    scope: str,
    rows: list[dict[str, str]],
    include_dataset: bool,
    include_model: bool,
    include_support_forms: bool = True,
) -> tuple[float, int, int]:
    X, y, clusters, names = _make_design(
        rows,
        include_s2=True,
        include_support_forms=include_support_forms,
        include_dataset=include_dataset,
        include_model=include_model,
    )
    beta, se, ll = _fit_logit_cluster(X, y, clusters, names)
    out_rows = []
    for name, b, s in zip(names, beta, se):
        z = b / s if s > 0 else float("nan")
        p = math.erfc(abs(z) / math.sqrt(2)) if s > 0 else float("nan")
        out_rows.append(
            {
                "scope": scope,
                "term": name,
                "coef_log_odds": f"{b:.6f}",
                "cluster_robust_se": f"{s:.6f}",
                "z": f"{z:.6f}",
                "p_value": f"{p:.6g}",
                "odds_ratio": f"{math.exp(b):.6f}",
                "ci_low": f"{math.exp(b - 1.96 * s):.6f}",
                "ci_high": f"{math.exp(b + 1.96 * s):.6f}",
                "n_pairs": str(len(rows)),
                "n_conversations": str(len(set(clusters))),
                "log_likelihood": f"{ll:.6f}",
                "se_type": "conversation-cluster robust sandwich",
            }
        )
    with open(OUT / output_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)
    return ll, len(rows), X.shape[1]


SETTING_LEVEL_TERMS = [
    ("scaffolded_support_S2", "Scaffolded support"),
    ("prior_user_constructive", "Prior user constructive"),
    ("prior_user_active", "Prior user active"),
    ("prior_user_passive", "Prior user passive"),
    ("intentional_framing", "Intentional framing"),
    ("M1", "M1 feedback"),
    ("M2", "M2 hinting"),
    ("M3", "M3 instructing"),
    ("M4", "M4 explaining"),
    ("M5", "M5 modelling"),
    ("M6", "M6 questioning"),
]


def _write_setting_level_models(rows: list[dict[str, str]]) -> None:
    out_rows: list[dict[str, str]] = []
    for setting in LEVEL3_A2U:
        sub = [r for r in rows if r["_setting"] == setting]
        specs = [
            (
                "broad_s2_only",
                "Broad scaffolded-support model",
                ["scaffolded_support_S2", "prior_user_constructive", "prior_user_active", "prior_user_passive", "intentional_framing"],
                False,
            ),
            (
                "support_form_decomposed",
                "Support-form model",
                ["M1", "M2", "M3", "M4", "M5", "M6"],
                True,
            ),
        ]
        for model_spec, model_label, terms, include_support_forms in specs:
            X, y, clusters, names = _make_design(
                sub,
                include_s2=True,
                include_support_forms=include_support_forms,
                include_dataset=False,
                include_model=True,
            )
            beta, se, ll = _fit_logit_cluster(X, y, clusters, names)
            model_fe_count = sum(1 for name in names if name.startswith("model_"))
            label_by_term = dict(SETTING_LEVEL_TERMS)
            for term in terms:
                if term not in names:
                    continue
                idx = names.index(term)
                b = float(beta[idx])
                s = float(se[idx])
                z = b / s if s > 0 else float("nan")
                p = math.erfc(abs(z) / math.sqrt(2)) if s > 0 else float("nan")
                out_rows.append(
                    {
                        "setting": setting,
                        "model_spec": model_spec,
                        "model_label": model_label,
                        "term": term,
                        "label": label_by_term[term],
                        "coef_log_odds": f"{b:.6f}",
                        "cluster_robust_se": f"{s:.6f}",
                        "z": f"{z:.6f}",
                        "p_value": f"{p:.6g}",
                        "odds_ratio": f"{math.exp(b):.6f}",
                        "ci_low": f"{math.exp(b - 1.96 * s):.6f}",
                        "ci_high": f"{math.exp(b + 1.96 * s):.6f}",
                        "n_pairs": str(len(sub)),
                        "n_conversations": str(len(set(clusters))),
                        "model_source_fe_count": str(model_fe_count),
                        "log_likelihood": f"{ll:.6f}",
                        "se_type": "conversation-cluster robust sandwich",
                        "notes": "Broad scaffolded support is estimated without M1-M6; support-form coefficients are estimated in the decomposed model with broad scaffolded support and co-occurring forms included.",
                    }
                )
    with open(OUT / "setting_level_adjacent_turn_logit_model_source_fe.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)


def _fit_logit_for_block_test(
    rows: list[dict[str, str]],
    include_dataset: bool,
    include_model: bool,
    include_s2: bool,
    include_support_forms: bool,
) -> tuple[float, int, int]:
    X, y, clusters, names = _make_design(
        rows,
        include_s2=include_s2,
        include_support_forms=include_support_forms,
        include_dataset=include_dataset,
        include_model=include_model,
    )
    _, _, ll = _fit_logit_cluster(X, y, clusters, names)
    return ll, X.shape[1], len(rows)


def _write_scaffolding_block_tests(
    pooled: list[dict[str, str]],
    wild: list[dict[str, str]],
) -> None:
    specs = [
        ("six task settings, dataset FE", pooled, True, False),
        ("six task settings, model/source FE", pooled, False, True),
        ("WildChat only, model FE", wild, False, True),
    ]
    out_rows: list[dict[str, str]] = []
    for scope, rows, include_dataset, include_model in specs:
        no_scaf_ll, no_scaf_k, n_pairs = _fit_logit_for_block_test(
            rows, include_dataset, include_model, include_s2=False, include_support_forms=False
        )
        s2_ll, s2_k, _ = _fit_logit_for_block_test(
            rows, include_dataset, include_model, include_s2=True, include_support_forms=False
        )
        full_ll, full_k, _ = _fit_logit_for_block_test(
            rows, include_dataset, include_model, include_s2=True, include_support_forms=True
        )
        comparisons = [
            (
                "broad scaffolded support added after user/context controls",
                no_scaf_ll,
                no_scaf_k,
                s2_ll,
                s2_k,
                "Tests whether scaffolded-support presence adds signal before decomposing support form.",
            ),
            (
                "support-form descriptors M1-M6 added within scaffolded support",
                s2_ll,
                s2_k,
                full_ll,
                full_k,
                "Tests whether nested support-form descriptors add signal among scaffolded turns after the broad scaffolded-support contrast is represented.",
            ),
            (
                "full scaffolding block plus M1-M6 added after user/context controls",
                no_scaf_ll,
                no_scaf_k,
                full_ll,
                full_k,
                "Tests the joint contribution of scaffolding features after user state, task/framing, turn index and fixed effects.",
            ),
        ]
        for comparison, reduced_ll, reduced_k, full_model_ll, full_model_k, notes in comparisons:
            lr = 2 * (full_model_ll - reduced_ll)
            df = full_model_k - reduced_k
            p = float(stats.chi2.sf(lr, df)) if df > 0 else float("nan")
            out_rows.append(
                {
                    "scope": scope,
                    "comparison": comparison,
                    "lr_chi2": f"{lr:.6f}",
                    "df": str(df),
                    "p_value": f"{p:.6g}",
                    "n_pairs": str(n_pairs),
                    "notes": notes,
                }
            )
    with open(OUT / "integrated_scaffolding_block_tests.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)


def _write_prior_state_support_form_checks(
    pooled: list[dict[str, str]],
    wild: list[dict[str, str]],
) -> None:
    specs = [
        ("six task settings, dataset FE", pooled, True, False),
        ("six task settings, model/source FE", pooled, False, True),
        ("WildChat only, model FE", wild, False, True),
    ]
    block_rows: list[dict[str, str]] = []
    coef_rows: list[dict[str, str]] = []
    strat_rows: list[dict[str, str]] = []
    for scope, rows, include_dataset, include_model in specs:
        reduced_x, y, clusters, reduced_names = _make_design(
            rows,
            include_s2=True,
            include_support_forms=True,
            include_dataset=include_dataset,
            include_model=include_model,
        )
        _, _, reduced_ll = _fit_logit_cluster(reduced_x, y, clusters, reduced_names)
        full_x, y_full, clusters_full, full_names = _make_interaction_design(
            rows,
            include_dataset=include_dataset,
            include_model=include_model,
        )
        beta, se, full_ll = _fit_logit_cluster(full_x, y_full, clusters_full, full_names)
        lr = 2 * (full_ll - reduced_ll)
        df = len(full_names) - len(reduced_names)
        p = float(stats.chi2.sf(lr, df)) if df > 0 else float("nan")
        block_rows.append(
            {
                "scope": scope,
                "comparison": "prior user state x support forms M1-M6 added beyond main effects",
                "lr_chi2": f"{lr:.6f}",
                "df": str(df),
                "p_value": f"{p:.6g}",
                "n_pairs": str(len(rows)),
                "n_conversations": str(len(set(clusters_full))),
                "notes": "Tests whether support-form coefficients vary by immediately preceding user engagement state.",
            }
        )
        for name, b, s in zip(full_names, beta, se):
            if "_x_M" not in name:
                continue
            z = b / s if s > 0 else float("nan")
            pv = math.erfc(abs(z) / math.sqrt(2)) if s > 0 else float("nan")
            coef_rows.append(
                {
                    "scope": scope,
                    "term": name,
                    "coef_log_odds": f"{b:.6f}",
                    "cluster_robust_se": f"{s:.6f}",
                    "z": f"{z:.6f}",
                    "p_value": f"{pv:.6g}",
                    "odds_ratio_multiplier": f"{math.exp(b):.6f}",
                    "ci_low": f"{math.exp(b - 1.96 * s):.6f}",
                    "ci_high": f"{math.exp(b + 1.96 * s):.6f}",
                    "n_pairs": str(len(rows)),
                    "n_conversations": str(len(set(clusters_full))),
                    "se_type": "conversation-cluster robust sandwich",
                }
            )

        for state, code, state_label in PRIOR_STATES:
            sub = [r for r in rows if (r.get("prev_user_Cognitive_level") or "") == code]
            if len(sub) < 500:
                continue
            X, ys, cls, names = _make_design(
                sub,
                include_s2=True,
                include_support_forms=True,
                include_dataset=include_dataset,
                include_model=include_model,
            )
            b2, s2, ll2 = _fit_logit_cluster(X, ys, cls, names)
            for term in ["scaffolded_support_S2", "M1", "M2", "M3", "M4", "M5", "M6"]:
                if term not in names:
                    continue
                idx = names.index(term)
                b = float(b2[idx])
                s = float(s2[idx])
                z = b / s if s > 0 else float("nan")
                pv = math.erfc(abs(z) / math.sqrt(2)) if s > 0 else float("nan")
                strat_rows.append(
                    {
                        "scope": scope,
                        "prior_user_state": state_label,
                        "term": term,
                        "coef_log_odds": f"{b:.6f}",
                        "cluster_robust_se": f"{s:.6f}",
                        "z": f"{z:.6f}",
                        "p_value": f"{pv:.6g}",
                        "odds_ratio": f"{math.exp(b):.6f}",
                        "ci_low": f"{math.exp(b - 1.96 * s):.6f}",
                        "ci_high": f"{math.exp(b + 1.96 * s):.6f}",
                        "n_pairs": str(len(sub)),
                        "n_conversations": str(len(set(cls))),
                        "log_likelihood": f"{ll2:.6f}",
                        "se_type": "conversation-cluster robust sandwich",
                    }
                )

    with open(OUT / "prior_state_support_form_interaction_block_tests.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(block_rows[0].keys()))
        writer.writeheader()
        writer.writerows(block_rows)
    with open(OUT / "prior_state_support_form_interaction_coefficients.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(coef_rows[0].keys()))
        writer.writeheader()
        writer.writerows(coef_rows)
    with open(OUT / "prior_state_stratified_support_form_logit.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(strat_rows[0].keys()))
        writer.writeheader()
        writer.writerows(strat_rows)


def compute_integrated_logit() -> None:
    pooled = _load_a2u_rows(wildchat_only=False)
    wild = _load_a2u_rows(wildchat_only=True)
    _write_setting_level_models(pooled)
    _write_model_rows(
        "integrated_adjacent_turn_logit_pooled_broad_s2.csv",
        "six task settings, dataset fixed effects, broad scaffolded support only",
        pooled,
        include_dataset=True,
        include_model=False,
        include_support_forms=False,
    )
    _write_model_rows(
        "integrated_adjacent_turn_logit_pooled_model_source_fe_broad_s2.csv",
        "six task settings, model/source fixed effects, broad scaffolded support only",
        pooled,
        include_dataset=False,
        include_model=True,
        include_support_forms=False,
    )
    _write_model_rows(
        "integrated_adjacent_turn_logit_wildchat_model_fe_broad_s2.csv",
        "WildChat only, model fixed effects, broad scaffolded support only",
        wild,
        include_dataset=False,
        include_model=True,
        include_support_forms=False,
    )
    pooled_ll, pooled_n, pooled_k = _write_model_rows(
        "integrated_adjacent_turn_logit_pooled.csv",
        "six task settings, dataset fixed effects",
        pooled,
        include_dataset=True,
        include_model=False,
    )
    pooled_model_ll, pooled_model_n, pooled_model_k = _write_model_rows(
        "integrated_adjacent_turn_logit_pooled_model_source_fe.csv",
        "six task settings, model/source fixed effects",
        pooled,
        include_dataset=False,
        include_model=True,
    )
    wild_nomodel_ll, _, wild_nomodel_k = _write_model_rows(
        "integrated_adjacent_turn_logit_wildchat_no_model_fe.csv",
        "WildChat only, no model fixed effects",
        wild,
        include_dataset=False,
        include_model=False,
    )
    wild_model_ll, wild_n, wild_model_k = _write_model_rows(
        "integrated_adjacent_turn_logit_wildchat_model_fe.csv",
        "WildChat only, model fixed effects",
        wild,
        include_dataset=False,
        include_model=True,
    )
    _write_scaffolding_block_tests(pooled, wild)
    _write_prior_state_support_form_checks(pooled, wild)
    lr = 2 * (wild_model_ll - wild_nomodel_ll)
    df = wild_model_k - wild_nomodel_k
    p = float(stats.chi2.sf(lr, df)) if df > 0 else float("nan")
    pooled_model_lr = 2 * (pooled_model_ll - pooled_ll)
    pooled_model_df = pooled_model_k - pooled_k
    pooled_model_p = float(stats.chi2.sf(pooled_model_lr, pooled_model_df)) if pooled_model_df > 0 else float("nan")
    with open(OUT / "integrated_model_block_tests.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "scope",
                "comparison",
                "lr_chi2",
                "df",
                "p_value",
                "n_pairs",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerow(
            {
                "scope": "six task settings",
                "comparison": "model/source fixed effects added beyond dataset fixed effects",
                "lr_chi2": f"{pooled_model_lr:.6f}",
                "df": str(pooled_model_df),
                "p_value": f"{pooled_model_p:.6g}",
                "n_pairs": str(pooled_model_n),
                "notes": "WildChat uses chat_model; LMSYS model and ShareChat assistant/source family are recovered from conversation identifiers.",
            }
        )
        writer.writerow(
            {
                "scope": "WildChat only",
                "comparison": "model fixed effects added to integrated adjacent-turn logit",
                "lr_chi2": f"{lr:.6f}",
                "df": str(df),
                "p_value": f"{p:.6g}",
                "n_pairs": str(wild_n),
                "notes": "WildChat uses exact chat_model labels retained in the production outputs.",
            }
        )
        writer.writerow(
            {
                "scope": "six task settings",
                "comparison": "dataset fixed-effects baseline",
                "lr_chi2": "0",
                "df": "0",
                "p_value": "",
                "n_pairs": str(pooled_n),
                "notes": "Dataset fixed effects are retained as the primary pooled adjustment because ShareChat identifiers provide source family rather than exact model version.",
            }
        )


def write_tex_tables() -> None:
    context_rows = list(csv.DictReader(open(OUT / "constructive_context_logit.csv")))
    rate_context_rows = list(csv.DictReader(open(OUT / "constructive_rate_context_logit.csv")))
    fig3_offset_rows = list(csv.DictReader(open(OUT / "fig3_poisson_offset_rate_sensitivity.csv")))
    pooled_broad = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled_broad_s2.csv")))
    pooled_model_broad = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled_model_source_fe_broad_s2.csv")))
    wild_broad = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_wildchat_model_fe_broad_s2.csv")))
    pooled = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled.csv")))
    pooled_model = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled_model_source_fe.csv")))
    wild = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_wildchat_model_fe.csv")))
    setting_level = list(csv.DictReader(open(OUT / "setting_level_adjacent_turn_logit_model_source_fe.csv")))
    blocks = list(csv.DictReader(open(OUT / "integrated_model_block_tests.csv")))
    scaf_blocks = list(csv.DictReader(open(OUT / "integrated_scaffolding_block_tests.csv")))
    state_form_blocks = list(csv.DictReader(open(OUT / "prior_state_support_form_interaction_block_tests.csv")))
    state_form_strat = list(csv.DictReader(open(OUT / "prior_state_stratified_support_form_logit.csv")))
    pooled_block = blocks[0]
    wild_block = blocks[1]

    wanted = [
        ("scaffolded_support_S2", "Scaffolded support"),
        ("prior_user_constructive", "Prior user constructive"),
        ("prior_user_active", "Prior user active"),
        ("prior_user_passive", "Prior user passive"),
        ("intentional_framing", "Intentional framing"),
        ("coding_task", "Coding task"),
        ("M1", "M1 feedback"),
        ("M4", "M4 explaining"),
        ("M6", "M6 questioning"),
    ]
    by_pooled_broad = {r["term"]: r for r in pooled_broad}
    by_pooled_model_broad = {r["term"]: r for r in pooled_model_broad}
    by_wild_broad = {r["term"]: r for r in wild_broad}
    by_pooled_full = {r["term"]: r for r in pooled}
    by_pooled_model_full = {r["term"]: r for r in pooled_model}
    by_wild_full = {r["term"]: r for r in wild}
    settings = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    by_setting_term = {(r["setting"], r["term"]): r for r in setting_level}

    def cell(r: dict[str, str]) -> str:
        p = float(r["p_value"])
        ptxt = "$<.001$" if p < 0.001 else f"{p:.3f}".replace("0.", ".")
        return f"{float(r['odds_ratio']):.2f} [{float(r['ci_low']):.2f}, {float(r['ci_high']):.2f}], {ptxt}"

    def rr_cell(r: dict[str, str]) -> str:
        p = float(r["p_value"])
        ptxt = "$<.001$" if p < 0.001 else f"{p:.3f}".replace("0.", ".")
        return f"{float(r['estimate_rr']):.2f} [{float(r['ci_low']):.2f}, {float(r['ci_high']):.2f}], {ptxt}"

    def compact_cell(r: dict[str, str]) -> str:
        p = float(r["p_value"])
        ptxt = "$<.001$" if p < 0.001 else f"{p:.3f}".replace("0.", ".")
        return f"\\makecell{{{float(r['odds_ratio']):.2f} [{float(r['ci_low']):.2f}, {float(r['ci_high']):.2f}]\\\\{ptxt}}}"

    def normalized_scope(scope: str) -> str:
        return scope.replace("six public-chat settings", "six task settings")

    context_path = ROOT / "tables" / "table_constructive_context_logit.tex"
    with open(context_path, "w") as f:
        f.write("\\begin{table*}[p]\n\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\textbf{Conversation-level context model for constructive engagement.} "
            "The outcome is whether a conversation contains at least one constructive user turn. "
            "The logistic regression includes user framing, task ecology, conversation-length bucket and dataset fixed effects. "
            "Cells report odds ratios with 95\\% confidence intervals and two-sided p values from conversation-robust standard errors. "
            "The reference category is unintentional framing, writing-oriented task, 2--3 user turns and WildChat.}\\label{tab:constructive_context_logit}\n"
        )
        f.write("\\setlength{\\tabcolsep}{6pt}\n\\renewcommand{\\arraystretch}{1.08}\n")
        f.write("\\resizebox{0.82\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{lc}\n\\toprule\n")
        f.write("Predictor & OR [95\\% CI], p value \\\\\n\\midrule\n")
        for term in [
            "intentional_framing",
            "coding_task",
            "length_4_6_user_turns",
            "length_7plus_user_turns",
            "dataset_LMSYS",
            "dataset_ShareChat",
        ]:
            r = next(row for row in context_rows if row["term"] == term)
            f.write(f"{r['label']} & {cell(r)} \\\\\n")
        n = int(next(row for row in context_rows if row["term"] == "Intercept")["n_conversations"])
        f.write("\\midrule\n")
        f.write(f"Conversations & {n:,} \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")

    rate_context_path = ROOT / "tables" / "table_constructive_rate_context_logit.tex"
    with open(rate_context_path, "w") as f:
        f.write("\\begin{table*}[p]\n\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\textbf{Conversation-level constructive-rate sensitivity model.} "
            "The outcome is the number of constructive user turns out of total user turns in each conversation, modelled with a grouped-binomial logistic regression. "
            "The model includes user framing, task ecology, conversation-length bucket and dataset fixed effects, using user-turn counts as denominators to reduce the mechanical opportunity effect in any-constructive-turn outcomes. "
            "Cells report odds ratios with 95\\% confidence intervals and two-sided p values from conversation-robust standard errors. "
            "The reference category is unintentional framing, writing-oriented task, 2--3 user turns and WildChat.}\\label{tab:constructive_rate_context_logit}\n"
        )
        f.write("\\setlength{\\tabcolsep}{6pt}\n\\renewcommand{\\arraystretch}{1.08}\n")
        f.write("\\resizebox{0.86\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{lc}\n\\toprule\n")
        f.write("Predictor & OR [95\\% CI], p value \\\\\n\\midrule\n")
        for term in [
            "intentional_framing",
            "coding_task",
            "length_4_6_user_turns",
            "length_7plus_user_turns",
            "dataset_LMSYS",
            "dataset_ShareChat",
        ]:
            r = next(row for row in rate_context_rows if row["term"] == term)
            f.write(f"{r['label']} & {cell(r)} \\\\\n")
        first = next(row for row in rate_context_rows if row["term"] == "Intercept")
        f.write("\\midrule\n")
        f.write(f"Conversations & {int(first['n_conversations']):,} \\\\\n")
        f.write(f"User turns & {int(first['n_user_turns']):,} \\\\\n")
        f.write(f"Constructive user turns & {int(first['n_constructive_turns']):,} \\\\\n")
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")

    offset_rate_path = ROOT / "tables" / "table_fig3_offset_rate_sensitivity.tex"
    with open(offset_rate_path, "w") as f:
        f.write("\\begin{table*}[p]\n\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\textbf{Offset-rate sensitivity for scaffolded-support Poisson models.} "
            "The primary Fig.~\\ref{fig:s2_conversation_association}b Poisson model uses raw constructive-turn counts with conversation length entered as a covariate. "
            "As a rate sensitivity, this table refits the same setting-specific mean model with \\texttt{offset(log(user\\_turns))}. "
            "Cells report the scaffolded-support rate ratio with 95\\% confidence intervals and two-sided p values using quasi-Poisson scaled standard errors.}\\label{tab:fig3_offset_rate_sensitivity}\n"
        )
        f.write("\\setlength{\\tabcolsep}{5pt}\n\\renewcommand{\\arraystretch}{1.08}\n")
        f.write("\\resizebox{0.92\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{lccc}\n\\toprule\n")
        f.write("Setting & Offset rate ratio [95\\% CI], p value & Pearson dispersion & Conversations \\\\\n\\midrule\n")
        for setting in ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]:
            r = next(row for row in fig3_offset_rows if row["setting"] == setting and row["se_type"] == "quasi_poisson_scaled")
            f.write(
                f"{setting} & {rr_cell(r)} & {float(r['pearson_dispersion']):.2f} & {int(r['n_conversations']):,} \\\\\n"
            )
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")

    setting_table_path = ROOT / "tables" / "table_setting_level_adjacent_models.tex"
    with open(setting_table_path, "w") as f:
        f.write("\\begin{table*}[p]\n\\tiny\n\\centering\n")
        f.write(
            "\\caption{\\textbf{Setting-level integrated adjacent-turn models.} "
            "Each column reports a separate within-setting logistic regression for whether the next user turn is constructive. "
            "The scaffolded-support row comes from a broad scaffolded-support model. Support-form rows come from a decomposed model that includes broad scaffolded-support presence and co-occurring M1--M6 forms, so form coefficients compare variation within scaffolded support rather than replacing the broad scaffolded-support contrast. "
            "All models include prior user state, intentional framing, assistant-turn index and recoverable model/source fixed effects where available. "
            "Cells report odds ratios with 95\\% confidence intervals and two-sided p values from conversation-cluster robust standard errors.}\\label{tab:setting_level_adjacent_models}\n"
        )
        f.write("\\setlength{\\tabcolsep}{3pt}\n\\renewcommand{\\arraystretch}{1.12}\n")
        f.write("\\resizebox{\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{lcccccc}\n\\toprule\n")
        f.write("Predictor & WC coding & LMSYS coding & SC coding & WC writing & LMSYS writing & SC writing \\\\\n\\midrule\n")
        first_rows = {setting: next(r for r in setting_level if r["setting"] == setting) for setting in settings}
        f.write("A2U pairs & " + " & ".join(f"{int(first_rows[s]['n_pairs']):,}" for s in settings) + " \\\\\n")
        f.write("Conversations & " + " & ".join(f"{int(first_rows[s]['n_conversations']):,}" for s in settings) + " \\\\\n")
        f.write("Model/source FE count & " + " & ".join(first_rows[s]["model_source_fe_count"] for s in settings) + " \\\\\n\\midrule\n")
        for term, label in SETTING_LEVEL_TERMS:
            f.write(
                label
                + " & "
                + " & ".join(compact_cell(by_setting_term[(setting, term)]) for setting in settings)
                + " \\\\\n"
            )
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")

    table_path = ROOT / "tables" / "table_integrated_regression.tex"
    with open(table_path, "w") as f:
        f.write("\\begin{table*}[p]\n")
        f.write("\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\textbf{Integrated adjacent-turn regression combining user state, assistant scaffolding and model controls.} "
            "The outcome is whether the next user turn is constructive. The scaffolded-support row is estimated in a broad scaffolded-support model; M1, M4 and M6 rows are estimated in a decomposed support-form model that includes broad scaffolded-support presence and co-occurring support forms. Estimates are odds ratios with 95\\% confidence intervals and two-sided p values from conversation-cluster robust standard errors. The primary pooled model uses dataset fixed effects; the model/source sensitivity adds recoverable assistant model or source-family fixed effects.}\\label{tab:integrated_regression}\n"
        )
        f.write("\\setlength{\\tabcolsep}{4pt}\n\\renewcommand{\\arraystretch}{1.10}\n")
        f.write("\\resizebox{\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{lccc}\n\\toprule\n")
        f.write("Predictor & Pooled dataset FE & Pooled model/source FE & WildChat model FE \\\\\n\\midrule\n")
        for term, label in wanted:
            if term in {"M1", "M4", "M6"}:
                row_pooled = by_pooled_full[term]
                row_pooled_model = by_pooled_model_full[term]
                row_wild = by_wild_full[term]
            else:
                row_pooled = by_pooled_broad[term]
                row_pooled_model = by_pooled_model_broad[term]
                row_wild = by_wild_broad[term]
            f.write(f"{label} & {cell(row_pooled)} & {cell(row_pooled_model)} & {cell(row_wild)} \\\\\n")
        f.write("\\midrule\n")
        f.write(
            f"Model/source block & Reference & LR $\\chi^2_{{{pooled_block['df']}}}={float(pooled_block['lr_chi2']):.1f}$, $p<.001$ & LR $\\chi^2_{{{wild_block['df']}}}={float(wild_block['lr_chi2']):.1f}$, $p<.001$ \\\\\n"
        )
        f.write("\\bottomrule\n\\end{tabular}%\n}\n")
        f.write("\\end{table*}\n")

    block_table_path = ROOT / "tables" / "table_integrated_scaffolding_block_tests.tex"
    with open(block_table_path, "w") as f:
        f.write("\\begin{table*}[p]\n\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\textbf{Incremental contribution of scaffolding features in integrated adjacent-turn models.} "
            "Likelihood-ratio block tests compare nested logistic regressions for whether the next user turn is constructive. "
            "All models include prior user state, user framing, task ecology, assistant-turn index and the indicated dataset or model/source fixed effects.}\\label{tab:integrated_scaffolding_block_tests}\n"
        )
        f.write("\\setlength{\\tabcolsep}{4pt}\n\\renewcommand{\\arraystretch}{1.08}\n")
        f.write("\\resizebox{\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{llcc}\n\\toprule\n")
        f.write("Scope & Added feature block & LR $\\chi^2$ (df) & p value \\\\\n\\midrule\n")
        labels = {
            "broad scaffolded support added after user/context controls": "Broad scaffolded support after user/context controls",
            "support-form descriptors M1-M6 added within scaffolded support": "M1--M6 descriptors within scaffolded support",
            "full scaffolding block plus M1-M6 added after user/context controls": "Full scaffolding block after user/context controls",
        }
        for r in scaf_blocks:
            p = float(r["p_value"])
            ptxt = "$<.001$" if p < 0.001 else f"{p:.3f}".replace("0.", ".")
            f.write(
                f"{normalized_scope(r['scope'])} & {labels[r['comparison']]} & {float(r['lr_chi2']):.1f} ({r['df']}) & {ptxt} \\\\\n"
            )
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")

    state_form_path = ROOT / "tables" / "table_prior_state_support_form_interactions.tex"
    by_scope_state_term = {
        (normalized_scope(r["scope"]), r["prior_user_state"], r["term"]): r
        for r in state_form_strat
        if normalized_scope(r["scope"]) == "six task settings, model/source FE"
    }

    def or_cell(r: dict[str, str]) -> str:
        p = float(r["p_value"])
        ptxt = "$<.001$" if p < 0.001 else f"{p:.3f}".replace("0.", ".")
        return f"{float(r['odds_ratio']):.2f} [{float(r['ci_low']):.2f}, {float(r['ci_high']):.2f}], {ptxt}"

    with open(state_form_path, "w") as f:
        f.write("\\begin{table*}[p]\n\\small\n\\centering\n")
        f.write(
            "\\caption{\\textbf{Prior user state and support form jointly structure adjacent-turn constructive engagement.} "
            "The first panel reports likelihood-ratio tests adding prior-state $\\times$ M1--M6 interactions to the integrated adjacent-turn logistic model. "
            "The second panel reports pooled model/source fixed-effect estimates for selected support forms within each prior user state. Estimates are odds ratios with 95\\% confidence intervals and two-sided p values from conversation-cluster robust standard errors.}\\label{tab:prior_state_support_form_interactions}\n"
        )
        f.write("\\setlength{\\tabcolsep}{5pt}\n\\renewcommand{\\arraystretch}{1.14}\n")
        f.write("\\begin{tabularx}{\\textwidth}{>{\\raggedright\\arraybackslash}p{0.20\\textwidth}>{\\raggedright\\arraybackslash}p{0.22\\textwidth}>{\\raggedright\\arraybackslash}p{0.23\\textwidth}>{\\raggedright\\arraybackslash}X}\n\\toprule\n")
        f.write("Panel & Scope / prior state & Term or test & Estimate \\\\\n\\midrule\n")
        for r in state_form_blocks:
            p = float(r["p_value"])
            ptxt = "$<.001$" if p < 0.001 else f"{p:.3f}".replace("0.", ".")
            f.write(
                f"Interaction block & {normalized_scope(r['scope'])} & Prior state $\\times$ M1--M6 & LR $\\chi^2_{{{r['df']}}}={float(r['lr_chi2']):.1f}$, {ptxt} \\\\\n"
            )
        f.write("\\midrule\n")
        for state_label in ["prior constructive", "prior active", "prior passive"]:
            for term, label in [("M1", "M1 feedback"), ("M4", "M4 explaining")]:
                r = by_scope_state_term[("six task settings, model/source FE", state_label, term)]
                f.write(
                    f"State-stratified model/source FE & {state_label} & {label} & {or_cell(r)} \\\\\n"
                )
        f.write("\\bottomrule\n\\end{tabularx}\n\\end{table*}\n")

    contrasts = list(csv.DictReader(open(OUT / "key_percentage_lifts_significance.csv")))
    contrast_path = ROOT / "tables" / "table_key_contrast_significance.tex"
    compact_contrasts = {
        "constructive_ratio_has_s2_minus_no_s2",
        "post_answer_depth_has_s2_minus_no_s2",
        "adjacent_next_constructive_s2_minus_s1",
    }
    compact = [r for r in contrasts if r["contrast"] in compact_contrasts]
    with open(contrast_path, "w") as f:
        f.write("\\begin{table*}[p]\n\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\textbf{Uncertainty estimates for key support--engagement contrasts.} "
            "Constructive-ratio contrasts are turn-weighted conversation-bootstrap estimates, with ratios computed as total constructive user turns divided by total user turns within scaffolded versus non-scaffolded conversation groups. Post-answer depth contrasts use conversation-level bootstrap resampling. Adjacent-turn contrasts bootstrap conversations over assistant-to-user pairs. Percentage-point and turn differences are the effect sizes reported in the main figures.}\\label{tab:key_contrast_significance}\n"
        )
        f.write("\\setlength{\\tabcolsep}{5pt}\n\\renewcommand{\\arraystretch}{1.10}\n")
        f.write("\\resizebox{\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{llccc}\n\\toprule\n")
        f.write("Setting & Contrast & Effect & 95\\% CI & p value \\\\\n\\midrule\n")
        for r in compact:
            if r["contrast"] == "constructive_ratio_has_s2_minus_no_s2":
                label = "Scaffolded $-$ reference constructive ratio"
                unit = "pp"
            elif r["contrast"] == "post_answer_depth_has_s2_minus_no_s2":
                label = "Scaffolded $-$ reference post-answer depth"
                unit = "turns"
            else:
                label = "Adjacent scaffolded $-$ reference lift"
                unit = "pp"
            p = float(r["p_value"])
            ptxt = "$<.001$" if p < 0.001 else f"{p:.3f}".replace("0.", ".")
            f.write(
                f"{r['setting']} & {label} & {float(r['estimate']):+.2f} {unit} & [{float(r['ci_low']):+.2f}, {float(r['ci_high']):+.2f}] & {ptxt} \\\\\n"
            )
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")


def write_report() -> None:
    context_rows = list(csv.DictReader(open(OUT / "constructive_context_logit.csv")))
    rate_context_rows = list(csv.DictReader(open(OUT / "constructive_rate_context_logit.csv")))
    fig3_offset_rows = list(csv.DictReader(open(OUT / "fig3_poisson_offset_rate_sensitivity.csv")))
    pooled_broad = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled_broad_s2.csv")))
    pooled_model_broad = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled_model_source_fe_broad_s2.csv")))
    wild_broad = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_wildchat_model_fe_broad_s2.csv")))
    pooled = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled.csv")))
    pooled_model = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled_model_source_fe.csv")))
    wild = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_wildchat_model_fe.csv")))
    setting_level = list(csv.DictReader(open(OUT / "setting_level_adjacent_turn_logit_model_source_fe.csv")))
    blocks = list(csv.DictReader(open(OUT / "integrated_model_block_tests.csv")))
    scaf_blocks = list(csv.DictReader(open(OUT / "integrated_scaffolding_block_tests.csv")))
    state_form_blocks = list(csv.DictReader(open(OUT / "prior_state_support_form_interaction_block_tests.csv")))
    state_form_strat = list(csv.DictReader(open(OUT / "prior_state_stratified_support_form_logit.csv")))
    pooled_block = blocks[0]
    wild_block = blocks[1]
    by_pooled_broad = {r["term"]: r for r in pooled_broad}
    by_pooled_model_broad = {r["term"]: r for r in pooled_model_broad}
    by_wild_broad = {r["term"]: r for r in wild_broad}
    by_pooled_full = {r["term"]: r for r in pooled}
    by_pooled_model_full = {r["term"]: r for r in pooled_model}
    by_wild_full = {r["term"]: r for r in wild}
    contrasts = list(csv.DictReader(open(OUT / "key_percentage_lifts_significance.csv")))
    def normalized_scope(scope: str) -> str:
        return scope.replace("six public-chat settings", "six task settings")

    with open(OUT / "integrated_regression_report.md", "w") as f:
        f.write("# Integrated Regression and Significance Report\n\n")
        f.write("Data scope: six main task settings: WildChat, LMSYS Chat and ShareChat coding/writing. SWE-chat and ThoughtTrace are not included in the main pooled model.\n\n")
        f.write("Model-label check: `chat_model` is complete for WildChat. LMSYS and ShareChat production columns are empty, but the conversation identifiers retain recoverable information: LMSYS contains model name and ShareChat contains public assistant/source family. The primary pooled model uses dataset fixed effects; a sensitivity replaces them with model/source fixed effects.\n\n")
        f.write("Claim-level consistency audit: Sections 2.1 and 2.2 are descriptive consistency claims over the six task settings. Inferential checks enter where the manuscript makes contrasts or model claims: Section 2.3 uses bootstrap CIs/p values for turn-weighted scaffolded versus reference contrasts, adjusted conversation-level models and an offset-rate sensitivity; Section 2.4 reports support-form CIs and between-stratum FDR-adjusted q values in the main figure; Section 2.5 uses conversation-cluster bootstrap CIs for adjacent-turn lifts and cluster-robust adjacent-turn regressions.\n\n")
        f.write("Section 2.2 conversation-level context check: a logistic regression predicting whether a conversation contains at least one constructive user turn includes user framing, task ecology, length bucket and dataset fixed effects. The model is a robustness check for systematic organization, not a causal estimate.\n\n")
        for term in ["intentional_framing", "coding_task", "length_4_6_user_turns", "length_7plus_user_turns"]:
            r = next(row for row in context_rows if row["term"] == term)
            f.write(f"- {r['label']}: OR {float(r['odds_ratio']):.3f}, 95% CI [{float(r['ci_low']):.3f}, {float(r['ci_high']):.3f}], p={r['p_value']}.\n")
        f.write("\n")
        f.write("Section 2.2 constructive-rate sensitivity: a grouped-binomial logistic regression models constructive user-turn count out of total user turns with the same user framing, task ecology, length bucket and dataset fixed effects. This checks whether the length pattern is only an opportunity-count artifact from the any-constructive outcome.\n\n")
        for term in ["intentional_framing", "coding_task", "length_4_6_user_turns", "length_7plus_user_turns"]:
            r = next(row for row in rate_context_rows if row["term"] == term)
            f.write(f"- {r['label']}: OR {float(r['odds_ratio']):.3f}, 95% CI [{float(r['ci_low']):.3f}, {float(r['ci_high']):.3f}], p={r['p_value']}.\n")
        f.write("\n")
        f.write("Section 2.3 offset-rate sensitivity: the setting-specific Poisson model for constructive-turn counts was refitted with `offset(log(user_turns))` and quasi-Poisson scaled standard errors. This checks whether the scaffolded-support association is only a count-model specification artifact.\n\n")
        for setting in ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]:
            r = next(row for row in fig3_offset_rows if row["setting"] == setting and row["se_type"] == "quasi_poisson_scaled")
            f.write(f"- {setting}: RR {float(r['estimate_rr']):.3f}, 95% CI [{float(r['ci_low']):.3f}, {float(r['ci_high']):.3f}], p={r['p_value']}.\n")
        f.write("\n")
        f.write("Integrated adjacent-turn logit outcome: whether the next user turn is constructive. Broad scaffolded-support models include scaffolded-support presence without M1-M6. Support-form decomposed models include broad scaffolded support plus M1-M6, so M coefficients describe form-level variation within scaffolded support. Standard errors are clustered by conversation.\n\n")
        f.write("Setting-level adjacent-turn models: separate model/source-adjusted regressions were fitted within each of the six task settings to check dataset-by-factor heterogeneity rather than relying only on pooled fixed effects. These outputs are exported to `setting_level_adjacent_turn_logit_model_source_fe.csv` and summarized in Supplementary Table C.\n\n")
        for term in ["scaffolded_support_S2", "prior_user_constructive", "M1", "M4", "M6"]:
            sub = [r for r in setting_level if r["term"] == term]
            positive = sum(float(r["odds_ratio"]) > 1 for r in sub)
            significant = sum(float(r["p_value"]) < 0.05 for r in sub)
            f.write(f"- Setting-level {term}: OR>1 in {positive}/{len(sub)} settings; p<0.05 in {significant}/{len(sub)} settings.\n")
        f.write("\n")
        f.write("Key pooled estimates with dataset fixed effects. Scaffolded-support and user/context rows come from broad scaffolded-support models; M rows come from support-form decomposed models:\n\n")
        for term in ["scaffolded_support_S2", "prior_user_constructive", "prior_user_active", "prior_user_passive", "intentional_framing", "coding_task", "M1", "M4", "M6"]:
            r = by_pooled_full[term] if term in {"M1", "M4", "M6"} else by_pooled_broad[term]
            f.write(f"- {term}: OR {float(r['odds_ratio']):.3f}, 95% CI [{float(r['ci_low']):.3f}, {float(r['ci_high']):.3f}], p={r['p_value']}.\n")
        f.write("\nPooled model/source fixed-effect sensitivity:\n\n")
        for term in ["scaffolded_support_S2", "prior_user_constructive", "prior_user_active", "prior_user_passive", "intentional_framing", "coding_task", "M1", "M4", "M6"]:
            r = by_pooled_model_full[term] if term in {"M1", "M4", "M6"} else by_pooled_model_broad[term]
            f.write(f"- {term}: OR {float(r['odds_ratio']):.3f}, 95% CI [{float(r['ci_low']):.3f}, {float(r['ci_high']):.3f}], p={r['p_value']}.\n")
        f.write("\nWildChat model-fixed-effect sensitivity:\n\n")
        for term in ["scaffolded_support_S2", "prior_user_constructive", "intentional_framing", "coding_task", "M1", "M4", "M6"]:
            r = by_wild_full[term] if term in {"M1", "M4", "M6"} else by_wild_broad[term]
            f.write(f"- {term}: OR {float(r['odds_ratio']):.3f}, 95% CI [{float(r['ci_low']):.3f}, {float(r['ci_high']):.3f}], p={r['p_value']}.\n")
        f.write(
            f"\nModel/source fixed-effect block in the pooled data: LR chi-square({pooled_block['df']})={float(pooled_block['lr_chi2']):.1f}, p={pooled_block['p_value']}. "
            f"WildChat exact model fixed-effect block: LR chi-square({wild_block['df']})={float(wild_block['lr_chi2']):.1f}, p={wild_block['p_value']}. "
            "Model/source labels add detectable heterogeneity. Broad scaffolded support remains positive in the broad support model, while the decomposed models show that support-form variation, especially M4 explaining, carries additional local signal.\n\n"
        )
        f.write("Consistency of key unadjusted contrasts:\n\n")
        for contrast in [
            "constructive_ratio_has_s2_minus_no_s2",
            "post_answer_depth_has_s2_minus_no_s2",
            "adjacent_next_constructive_s2_minus_s1",
        ]:
            sub = [r for r in contrasts if r["contrast"] == contrast]
            positive = sum(float(r["estimate"]) > 0 for r in sub)
            significant = sum(float(r["p_value"]) < 0.05 for r in sub)
            f.write(f"- {contrast}: {positive}/{len(sub)} settings are positive; {significant}/{len(sub)} have p<0.05.\n")
        f.write("\nNested scaffolding block tests:\n\n")
        for r in scaf_blocks:
            f.write(
                f"- {normalized_scope(r['scope'])}; {r['comparison']}: LR chi-square({r['df']})={float(r['lr_chi2']):.1f}, p={r['p_value']}.\n"
            )
        f.write("\nPrior-state by support-form interaction checks:\n\n")
        for r in state_form_blocks:
            f.write(
                f"- {normalized_scope(r['scope'])}; prior state x M1-M6 block: LR chi-square({r['df']})={float(r['lr_chi2']):.1f}, p={r['p_value']}.\n"
            )
        f.write("\nPooled model/source FE, state-stratified selected support forms:\n\n")
        for r in state_form_strat:
            if r["scope"] != "six task settings, model/source FE" or r["term"] not in {"M1", "M4"}:
                continue
            f.write(
                f"- {r['prior_user_state']} {r['term']}: OR {float(r['odds_ratio']):.3f}, 95% CI [{float(r['ci_low']):.3f}, {float(r['ci_high']):.3f}], p={r['p_value']}.\n"
            )


def main() -> None:
    compute_key_contrasts()
    compute_fig3_offset_rate_sensitivity()
    compute_constructive_context_logit()
    compute_integrated_logit()
    write_tex_tables()
    write_report()


if __name__ == "__main__":
    main()
