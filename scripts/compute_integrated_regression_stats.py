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


def _write_model_rows(
    output_name: str,
    scope: str,
    rows: list[dict[str, str]],
    include_dataset: bool,
    include_model: bool,
) -> tuple[float, int, int]:
    X, y, clusters, names = _make_design(
        rows,
        include_s2=True,
        include_support_forms=True,
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
        ("six public-chat settings, dataset FE", pooled, True, False),
        ("six public-chat settings, model/source FE", pooled, False, True),
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
                "broad S2 added after user/context controls",
                no_scaf_ll,
                no_scaf_k,
                s2_ll,
                s2_k,
                "Tests whether scaffolded-support presence adds signal before decomposing support form.",
            ),
            (
                "support forms M1-M6 added beyond broad S2",
                s2_ll,
                s2_k,
                full_ll,
                full_k,
                "Tests whether specific support forms explain additional signal beyond S2 presence.",
            ),
            (
                "full scaffolding block S2 plus M1-M6 added after user/context controls",
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


def compute_integrated_logit() -> None:
    pooled = _load_a2u_rows(wildchat_only=False)
    wild = _load_a2u_rows(wildchat_only=True)
    pooled_ll, pooled_n, pooled_k = _write_model_rows(
        "integrated_adjacent_turn_logit_pooled.csv",
        "six public-chat settings, dataset fixed effects",
        pooled,
        include_dataset=True,
        include_model=False,
    )
    pooled_model_ll, pooled_model_n, pooled_model_k = _write_model_rows(
        "integrated_adjacent_turn_logit_pooled_model_source_fe.csv",
        "six public-chat settings, model/source fixed effects",
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
                "scope": "six public-chat settings",
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
                "scope": "six public-chat settings",
                "comparison": "dataset fixed-effects baseline",
                "lr_chi2": "0",
                "df": "0",
                "p_value": "",
                "n_pairs": str(pooled_n),
                "notes": "Dataset fixed effects are retained as the primary pooled adjustment because ShareChat identifiers provide source family rather than exact model version.",
            }
        )


def write_tex_tables() -> None:
    pooled = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled.csv")))
    pooled_model = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled_model_source_fe.csv")))
    wild = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_wildchat_model_fe.csv")))
    blocks = list(csv.DictReader(open(OUT / "integrated_model_block_tests.csv")))
    scaf_blocks = list(csv.DictReader(open(OUT / "integrated_scaffolding_block_tests.csv")))
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
    by_pooled = {r["term"]: r for r in pooled}
    by_pooled_model = {r["term"]: r for r in pooled_model}
    by_wild = {r["term"]: r for r in wild}

    def cell(r: dict[str, str]) -> str:
        p = float(r["p_value"])
        ptxt = "$<.001$" if p < 0.001 else f"{p:.3f}".replace("0.", ".")
        return f"{float(r['odds_ratio']):.2f} [{float(r['ci_low']):.2f}, {float(r['ci_high']):.2f}], {ptxt}"

    table_path = ROOT / "tables" / "table_integrated_regression.tex"
    with open(table_path, "w") as f:
        f.write("\\begin{table*}[p]\n")
        f.write("\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\textbf{Integrated adjacent-turn regression combining user state, assistant scaffolding and model controls.} "
            "The outcome is whether the next user turn is constructive. Estimates are odds ratios with 95\\% confidence intervals and two-sided p values from conversation-cluster robust standard errors. The primary pooled model uses dataset fixed effects; the model/source sensitivity adds recoverable assistant model or source-family fixed effects.}\\label{tab:integrated_regression}\n"
        )
        f.write("\\setlength{\\tabcolsep}{4pt}\n\\renewcommand{\\arraystretch}{1.10}\n")
        f.write("\\resizebox{\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{lccc}\n\\toprule\n")
        f.write("Predictor & Pooled dataset FE & Pooled model/source FE & WildChat model FE \\\\\n\\midrule\n")
        for term, label in wanted:
            f.write(f"{label} & {cell(by_pooled[term])} & {cell(by_pooled_model[term])} & {cell(by_wild[term])} \\\\\n")
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
            "broad S2 added after user/context controls": "Broad S2 after user/context controls",
            "support forms M1-M6 added beyond broad S2": "M1--M6 forms beyond broad S2",
            "full scaffolding block S2 plus M1-M6 added after user/context controls": "Full scaffolding block after user/context controls",
        }
        for r in scaf_blocks:
            p = float(r["p_value"])
            ptxt = "$<.001$" if p < 0.001 else f"{p:.3f}".replace("0.", ".")
            f.write(
                f"{r['scope']} & {labels[r['comparison']]} & {float(r['lr_chi2']):.1f} ({r['df']}) & {ptxt} \\\\\n"
            )
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")

    contrasts = list(csv.DictReader(open(OUT / "key_percentage_lifts_significance.csv")))
    contrast_path = ROOT / "tables" / "table_key_contrast_significance.tex"
    compact = [r for r in contrasts if r["contrast"] in {"constructive_ratio_has_s2_minus_no_s2", "adjacent_next_constructive_s2_minus_s1"}]
    with open(contrast_path, "w") as f:
        f.write("\\begin{table*}[p]\n\\scriptsize\n\\centering\n")
        f.write(
            "\\caption{\\textbf{Uncertainty estimates for key percentage-point contrasts.} "
            "Constructive-ratio contrasts are conversation-bootstrap estimates weighted by user turns; adjacent-turn contrasts bootstrap conversations over assistant-to-user pairs. Percentage-point differences are the effect sizes reported in the main figures.}\\label{tab:key_contrast_significance}\n"
        )
        f.write("\\setlength{\\tabcolsep}{5pt}\n\\renewcommand{\\arraystretch}{1.10}\n")
        f.write("\\resizebox{\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{llccc}\n\\toprule\n")
        f.write("Setting & Contrast & Effect & 95\\% CI & p value \\\\\n\\midrule\n")
        for r in compact:
            label = "Has S2 $-$ no S2 constructive ratio" if r["contrast"].startswith("constructive") else "Adjacent S2 $-$ reference lift"
            p = float(r["p_value"])
            ptxt = "$<.001$" if p < 0.001 else f"{p:.3f}".replace("0.", ".")
            f.write(
                f"{r['setting']} & {label} & {float(r['estimate']):+.2f} pp & [{float(r['ci_low']):+.2f}, {float(r['ci_high']):+.2f}] & {ptxt} \\\\\n"
            )
        f.write("\\bottomrule\n\\end{tabular}%\n}\n\\end{table*}\n")


def write_report() -> None:
    pooled = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled.csv")))
    pooled_model = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_pooled_model_source_fe.csv")))
    wild = list(csv.DictReader(open(OUT / "integrated_adjacent_turn_logit_wildchat_model_fe.csv")))
    blocks = list(csv.DictReader(open(OUT / "integrated_model_block_tests.csv")))
    scaf_blocks = list(csv.DictReader(open(OUT / "integrated_scaffolding_block_tests.csv")))
    pooled_block = blocks[0]
    wild_block = blocks[1]
    by_pooled = {r["term"]: r for r in pooled}
    by_pooled_model = {r["term"]: r for r in pooled_model}
    by_wild = {r["term"]: r for r in wild}
    contrasts = list(csv.DictReader(open(OUT / "key_percentage_lifts_significance.csv")))
    with open(OUT / "integrated_regression_report.md", "w") as f:
        f.write("# Integrated Regression and Significance Report\n\n")
        f.write("Data scope: six main public-chat task settings: WildChat, LMSYS Chat-1M and ShareChat strict-English coding/writing. SWE-chat and ThoughtTrace are not included in the main pooled model.\n\n")
        f.write("Model-label check: `chat_model` is complete for WildChat. LMSYS and ShareChat production columns are empty, but the conversation identifiers retain recoverable information: LMSYS contains model name and ShareChat contains public assistant/source family. The primary pooled model uses dataset fixed effects; a sensitivity replaces them with model/source fixed effects.\n\n")
        f.write("Integrated adjacent-turn logit outcome: whether the next user turn is constructive. Predictors include scaffolded support, prior user state, user framing, task, assistant-turn index, support means M1-M6 and dataset or model/source fixed effects. Standard errors are clustered by conversation.\n\n")
        f.write("Key pooled estimates with dataset fixed effects:\n\n")
        for term in ["scaffolded_support_S2", "prior_user_constructive", "prior_user_active", "prior_user_passive", "intentional_framing", "coding_task", "M1", "M4", "M6"]:
            r = by_pooled[term]
            f.write(f"- {term}: OR {float(r['odds_ratio']):.3f}, 95% CI [{float(r['ci_low']):.3f}, {float(r['ci_high']):.3f}], p={r['p_value']}.\n")
        f.write("\nPooled model/source fixed-effect sensitivity:\n\n")
        for term in ["scaffolded_support_S2", "prior_user_constructive", "prior_user_active", "prior_user_passive", "intentional_framing", "coding_task", "M1", "M4", "M6"]:
            r = by_pooled_model[term]
            f.write(f"- {term}: OR {float(r['odds_ratio']):.3f}, 95% CI [{float(r['ci_low']):.3f}, {float(r['ci_high']):.3f}], p={r['p_value']}.\n")
        f.write("\nWildChat model-fixed-effect sensitivity:\n\n")
        for term in ["scaffolded_support_S2", "prior_user_constructive", "intentional_framing", "coding_task", "M1", "M4", "M6"]:
            r = by_wild[term]
            f.write(f"- {term}: OR {float(r['odds_ratio']):.3f}, 95% CI [{float(r['ci_low']):.3f}, {float(r['ci_high']):.3f}], p={r['p_value']}.\n")
        f.write(
            f"\nModel/source fixed-effect block in the pooled data: LR chi-square({pooled_block['df']})={float(pooled_block['lr_chi2']):.1f}, p={pooled_block['p_value']}. "
            f"WildChat exact model fixed-effect block: LR chi-square({wild_block['df']})={float(wild_block['lr_chi2']):.1f}, p={wild_block['p_value']}. "
            "Model/source labels add detectable heterogeneity. In the fully adjusted adjacent-turn model, the broad S2 indicator is not statistically distinguishable from the null after prior user state and specific support forms are included, whereas prior constructive/active state and M4 explaining remain large and statistically robust.\n\n"
        )
        f.write("Consistency of key unadjusted contrasts:\n\n")
        for contrast in ["constructive_ratio_has_s2_minus_no_s2", "adjacent_next_constructive_s2_minus_s1"]:
            sub = [r for r in contrasts if r["contrast"] == contrast]
            positive = sum(float(r["estimate"]) > 0 for r in sub)
            significant = sum(float(r["p_value"]) < 0.05 for r in sub)
            f.write(f"- {contrast}: {positive}/{len(sub)} settings are positive; {significant}/{len(sub)} have p<0.05.\n")
        f.write("\nNested scaffolding block tests:\n\n")
        for r in scaf_blocks:
            f.write(
                f"- {r['scope']}; {r['comparison']}: LR chi-square({r['df']})={float(r['lr_chi2']):.1f}, p={r['p_value']}.\n"
            )


def main() -> None:
    compute_key_contrasts()
    compute_integrated_logit()
    write_tex_tables()
    write_report()


if __name__ == "__main__":
    main()
