from __future__ import annotations

import csv
import json
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "support_intent"
OUT.mkdir(parents=True, exist_ok=True)
ANALYSIS_OUTPUTS_ROOT = Path(
    os.environ.get("MSRA_ANALYSIS_OUTPUTS_ROOT", ROOT / "data" / "level_analysis" / "outputs")
)

SETTINGS = {
    "WC coding": {
        "task": "coding",
        "level2": ANALYSIS_OUTPUTS_ROOT / "0410_wildchat_userturn_pipeline/latest/coding/wildchat_coding_level2/level2_reports/level2_metrics_20260411_212300.csv",
        "conversations": ANALYSIS_OUTPUTS_ROOT / "0410_wildchat_userturn_pipeline/user_turn_round2_final_coding/conversations",
    },
    "LMSYS coding": {
        "task": "coding",
        "level2": ANALYSIS_OUTPUTS_ROOT / "0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/coding/lmsys_coding_level2/level2_reports/level2_metrics_20260624_121538.csv",
        "conversations": ANALYSIS_OUTPUTS_ROOT / "0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/user_turn_round2_final_coding/conversations",
    },
    "SC coding": {
        "task": "coding",
        "level2": ANALYSIS_OUTPUTS_ROOT / "0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/coding/sharechat_coding_level2/level2_reports/level2_metrics_20260602_125948.csv",
        "conversations": ANALYSIS_OUTPUTS_ROOT / "0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/user_turn_round2_final_coding_english/conversations",
    },
    "WC writing": {
        "task": "writing",
        "level2": ANALYSIS_OUTPUTS_ROOT / "0410_wildchat_userturn_pipeline/latest/writing/wildchat_writing_level2/level2_reports/level2_metrics_20260411_212539.csv",
        "conversations": ANALYSIS_OUTPUTS_ROOT / "0410_wildchat_userturn_pipeline/user_turn_round2_final_writing/conversations",
    },
    "LMSYS writing": {
        "task": "writing",
        "level2": ANALYSIS_OUTPUTS_ROOT / "0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/writing/lmsys_writing_level2/level2_reports/level2_metrics_20260624_121658.csv",
        "conversations": ANALYSIS_OUTPUTS_ROOT / "0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/user_turn_round2_final_writing/conversations",
    },
    "SC writing": {
        "task": "writing",
        "level2": ANALYSIS_OUTPUTS_ROOT / "0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/writing/sharechat_writing_level2/level2_reports/level2_metrics_20260602_130002.csv",
        "conversations": ANALYSIS_OUTPUTS_ROOT / "0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/user_turn_round2_final_writing_english/conversations",
    },
}

INTENTS = {
    "I1": "metacognitive",
    "I2": "cognitive",
    "I3": "affective",
}

FORMS = {
    "M1": "feedback",
    "M2": "hinting",
    "M3": "instructing",
    "M4": "explaining",
    "M5": "modelling",
    "M6": "questioning",
}


def _read_csv(path: str | Path) -> list[dict[str, str]]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _f(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    if value in ("", None):
        return 0.0
    return float(value)


def _contains_intent(value: object, intent: str) -> bool:
    if isinstance(value, list):
        return any(_contains_intent(v, intent) for v in value)
    if isinstance(value, dict):
        return any(_contains_intent(v, intent) for v in value.values())
    return bool(re.search(rf"\b{intent}\b", str(value)))


def _assistant_turn_intents(message: dict) -> set[str]:
    analysis = message.get("v21_analysis") or message.get("analysis") or {}
    support_type = str(analysis.get("Support_Type", analysis.get("support_type", ""))).upper()
    if "S2" not in support_type:
        return set()

    details = analysis.get("S2_Details") or analysis.get("s2_details") or {}
    raw_intent = (
        details.get("Intent")
        or details.get("intent")
        or analysis.get("S2_Intent")
        or analysis.get("s2_intent")
        or ""
    )
    return {intent for intent in INTENTS if _contains_intent(raw_intent, intent)}


def _assistant_turn_labels(message: dict) -> tuple[set[str], set[str]]:
    analysis = message.get("v21_analysis") or message.get("analysis") or {}
    support_type = str(analysis.get("Support_Type", analysis.get("support_type", ""))).upper()
    if "S2" not in support_type:
        return set(), set()

    details = analysis.get("S2_Details") or analysis.get("s2_details") or {}
    raw_intent = (
        details.get("Intent")
        or details.get("intent")
        or analysis.get("S2_Intent")
        or analysis.get("s2_intent")
        or ""
    )
    raw_means = (
        details.get("Means")
        or details.get("means")
        or analysis.get("S2_Means")
        or analysis.get("s2_means")
        or ""
    )
    intents = {intent for intent in INTENTS if _contains_intent(raw_intent, intent)}
    forms = {form for form in FORMS if _contains_intent(raw_means, form)}
    return intents, forms


def _count_s2_turns(conv_dir: str | Path) -> tuple[int, dict[str, int]]:
    s2_turns = 0
    intent_turns = {intent: 0 for intent in INTENTS}
    for path in Path(conv_dir).glob("*.json"):
        with open(path) as f:
            data = json.load(f)
        for message in data.get("Messages", data.get("messages", [])):
            if str(message.get("role", "")).lower() != "assistant":
                continue
            intents = _assistant_turn_intents(message)
            if intents:
                s2_turns += 1
                for intent in intents:
                    intent_turns[intent] += 1
    return s2_turns, intent_turns


def _support_intent_form_rows() -> list[dict[str, object]]:
    output = []
    for setting, cfg in SETTINGS.items():
        s2_turns = 0
        intent_turns = {intent: 0 for intent in INTENTS}
        form_turns = {form: 0 for form in FORMS}
        cross_turns = {(intent, form): 0 for intent in INTENTS for form in FORMS}

        for path in Path(cfg["conversations"]).glob("*.json"):
            with open(path) as f:
                data = json.load(f)
            for message in data.get("Messages", data.get("messages", [])):
                if str(message.get("role", "")).lower() != "assistant":
                    continue
                intents, forms = _assistant_turn_labels(message)
                if not intents:
                    continue
                s2_turns += 1
                for intent in intents:
                    intent_turns[intent] += 1
                for form in forms:
                    form_turns[form] += 1
                for intent in intents:
                    for form in forms:
                        cross_turns[(intent, form)] += 1

        for intent, intent_label in INTENTS.items():
            row: dict[str, object] = {
                "setting": setting,
                "task": cfg["task"],
                "support_intent": intent,
                "support_intent_label": intent_label,
                "scaffolded_turns": s2_turns,
                "intent_turns": intent_turns[intent],
                "intent_share_pct": 100 * intent_turns[intent] / s2_turns if s2_turns else float("nan"),
            }
            for form, form_label in FORMS.items():
                count = cross_turns[(intent, form)]
                row[f"{form}_{form_label}_count"] = count
                row[f"{form}_{form_label}_pct_of_scaffolded"] = 100 * count / s2_turns if s2_turns else float("nan")
                row[f"{form}_{form_label}_pct_within_intent"] = (
                    100 * count / intent_turns[intent] if intent_turns[intent] else float("nan")
                )
            output.append(row)
    return output


def _setting_rows() -> list[dict[str, object]]:
    output = []
    for setting, cfg in SETTINGS.items():
        rows = _read_csv(cfg["level2"])
        s2_turns, intent_turns = _count_s2_turns(cfg["conversations"])
        scaffolded_rows = [row for row in rows if _f(row, "has_S2") > 0]

        for intent, label in INTENTS.items():
            flag = f"has_S2_{intent}"
            with_rows = [row for row in scaffolded_rows if _f(row, flag) > 0]
            without_rows = [row for row in scaffolded_rows if _f(row, flag) <= 0]

            with_c = sum(_f(row, "Cog_C_count") for row in with_rows)
            with_u = sum(_f(row, "user_turns") for row in with_rows)
            without_c = sum(_f(row, "Cog_C_count") for row in without_rows)
            without_u = sum(_f(row, "user_turns") for row in without_rows)
            with_ratio = 100 * with_c / with_u if with_u else float("nan")
            without_ratio = 100 * without_c / without_u if without_u else float("nan")

            output.append(
                {
                    "setting": setting,
                    "task": cfg["task"],
                    "intent": intent,
                    "label": label,
                    "s2_turns": s2_turns,
                    "intent_s2_turns": intent_turns[intent],
                    "intent_s2_turn_prevalence_pct": 100 * intent_turns[intent] / s2_turns if s2_turns else float("nan"),
                    "scaffolded_conversations": len(scaffolded_rows),
                    "conv_with_intent": len(with_rows),
                    "conv_without_intent": len(without_rows),
                    "constructive_count_with_intent": with_c,
                    "user_turns_with_intent": with_u,
                    "constructive_count_without_intent": without_c,
                    "user_turns_without_intent": without_u,
                    "constructive_ratio_with_intent_pct": with_ratio,
                    "constructive_ratio_without_intent_pct": without_ratio,
                    "difference_pp": with_ratio - without_ratio,
                }
            )
    return output


def _summary_rows(setting_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    scopes = [
        ("pooled", lambda row: True),
        ("coding", lambda row: row["task"] == "coding"),
        ("writing", lambda row: row["task"] == "writing"),
    ]
    for scope, predicate in scopes:
        scoped = [row for row in setting_rows if predicate(row)]
        for intent, label in INTENTS.items():
            intent_rows = [row for row in scoped if row["intent"] == intent]
            s2_turns = sum(float(row["s2_turns"]) for row in intent_rows)
            intent_s2_turns = sum(float(row["intent_s2_turns"]) for row in intent_rows)
            with_c = sum(float(row["constructive_count_with_intent"]) for row in intent_rows)
            with_u = sum(float(row["user_turns_with_intent"]) for row in intent_rows)
            without_c = sum(float(row["constructive_count_without_intent"]) for row in intent_rows)
            without_u = sum(float(row["user_turns_without_intent"]) for row in intent_rows)
            with_ratio = 100 * with_c / with_u if with_u else float("nan")
            without_ratio = 100 * without_c / without_u if without_u else float("nan")
            rows.append(
                {
                    "scope": scope,
                    "intent": intent,
                    "label": label,
                    "s2_turn_prevalence_pct": 100 * intent_s2_turns / s2_turns if s2_turns else float("nan"),
                    "constructive_ratio_with_intent_pct": with_ratio,
                    "constructive_ratio_without_intent_pct": without_ratio,
                    "difference_pp": with_ratio - without_ratio,
                    "conv_with_intent": int(sum(float(row["conv_with_intent"]) for row in intent_rows)),
                    "conv_without_intent": int(sum(float(row["conv_without_intent"]) for row in intent_rows)),
                }
            )
    return rows


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _fmt(value: object, digits: int = 1, plus: bool = False) -> str:
    numeric = float(value)
    prefix = "+" if plus and numeric > 0 else ""
    return f"{prefix}{numeric:.{digits}f}"


def _write_tex(path: Path, rows: list[dict[str, object]]) -> None:
    order = [
        ("pooled", "Pooled"),
        ("coding", "Coding"),
        ("writing", "Writing"),
    ]
    by_key = {(row["scope"], row["intent"]): row for row in rows}
    lines = [
        r"\begin{table*}[p]",
        r"\centering",
        r"\scriptsize",
        r"\caption{\textbf{Support-intent labels are dominated by cognitive support.} Scaffolded assistant turns can receive metacognitive (\texttt{I1}), cognitive (\texttt{I2}) or affective (\texttt{I3}) intent labels. Scaffolded-turn prevalence reports the share of scaffolded assistant turns containing each intent label. Constructive ratios compare scaffolded conversations containing at least one assistant turn with the intent label with scaffolded conversations without that intent label, using turn-weighted constructive user-turn ratios. Intent labels can co-occur, and affective intent is sparse, so these contrasts are interpreted descriptively.}",
        r"\label{tab:support_intent_summary}",
        r"\begin{adjustbox}{max width=\textwidth}",
        r"\begin{tabular}{@{}llrrrrl@{}}",
        r"\toprule",
        r"Scope & Intent label & Scaffolded turns (\%) & With intent (\%) & Without intent (\%) & Diff. (pp) & Conv. with / without \\",
        r"\midrule",
    ]
    for scope_idx, (scope, label_scope) in enumerate(order):
        if scope_idx:
            lines.append(r"\addlinespace")
        for intent, label in INTENTS.items():
            row = by_key[(scope, intent)]
            lines.append(
                f"{label_scope} & \\texttt{{{intent}}} {label} & "
                f"{_fmt(row['s2_turn_prevalence_pct'])} & "
                f"{_fmt(row['constructive_ratio_with_intent_pct'])} & "
                f"{_fmt(row['constructive_ratio_without_intent_pct'])} & "
                f"{_fmt(row['difference_pp'], plus=True)} & "
                f"{int(row['conv_with_intent']):,} / {int(row['conv_without_intent']):,} \\\\"
            )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{adjustbox}",
            r"\end{table*}",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def _write_crosswalk_tex(path: Path, rows: list[dict[str, object]]) -> None:
    order = ["WC coding", "LMSYS coding", "SC coding", "WC writing", "LMSYS writing", "SC writing"]
    display_names = {
        "WC coding": "WildChat coding",
        "LMSYS coding": "LMSYS Chat coding",
        "SC coding": "ShareChat coding",
        "WC writing": "WildChat writing",
        "LMSYS writing": "LMSYS Chat writing",
        "SC writing": "ShareChat writing",
    }
    by_setting = {setting: [row for row in rows if row["setting"] == setting] for setting in order}
    lines = [
        r"\begin{table*}[p]",
        r"\centering",
        r"\scriptsize",
        r"\caption{\textbf{Support-intent by support-form crosswalk.} Rows are support-intent labels within each task setting. Intent share reports the percentage of scaffolded assistant turns with the intent label. Cells report the percentage of turns with that intent label that also contain each support-form label. Intent and support-form labels are non-exclusive, so rows do not sum to 100\%.}",
        r"\label{tab:support_intent_form_crosswalk}",
        r"\begin{adjustbox}{max width=\textwidth}",
        r"\begin{tabular}{@{}llrrrrrrr@{}}",
        r"\toprule",
        r"Setting & Intent & Intent share (\%) & M1 feedback & M2 hinting & M3 instructing & M4 explaining & M5 modelling & M6 questioning \\",
        r"\midrule",
    ]
    for setting_idx, setting in enumerate(order):
        if setting_idx:
            lines.append(r"\addlinespace")
        for row in by_setting[setting]:
            intent = str(row["support_intent"])
            label = str(row["support_intent_label"])
            lines.append(
                f"{display_names[setting]} & \\texttt{{{intent}}} {label} & "
                f"{_fmt(row['intent_share_pct'])} & "
                f"{_fmt(row['M1_feedback_pct_within_intent'])} & "
                f"{_fmt(row['M2_hinting_pct_within_intent'])} & "
                f"{_fmt(row['M3_instructing_pct_within_intent'])} & "
                f"{_fmt(row['M4_explaining_pct_within_intent'])} & "
                f"{_fmt(row['M5_modelling_pct_within_intent'])} & "
                f"{_fmt(row['M6_questioning_pct_within_intent'])} \\\\"
            )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{adjustbox}",
            r"\end{table*}",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> None:
    setting_rows = _setting_rows()
    summary_rows = _summary_rows(setting_rows)
    crosswalk_rows = _support_intent_form_rows()
    _write_csv(OUT / "support_intent_setting_level.csv", setting_rows)
    _write_csv(OUT / "support_intent_summary.csv", summary_rows)
    _write_csv(OUT / "support_intent_form_crosswalk.csv", crosswalk_rows)
    _write_tex(ROOT / "tables" / "table_support_intent_summary.tex", summary_rows)
    _write_crosswalk_tex(ROOT / "tables" / "table_support_intent_form_crosswalk.tex", crosswalk_rows)


if __name__ == "__main__":
    main()
