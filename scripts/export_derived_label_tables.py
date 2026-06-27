#!/usr/bin/env python3
"""Export de-identified label-only tables for submission data sharing.

The exported files intentionally omit raw message text, original conversation
IDs, URLs, timestamps and user identifiers. They preserve the analytic labels
and aggregate fields needed to reproduce the manuscript figures, tables and
regression checks.
"""

from __future__ import annotations

import csv
import hashlib
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = Path("/data/zixin/msra/shareable_project/investigations/level_analysis/outputs")
OUT = ROOT / "derived_label_tables"
HASH_PREFIX = "nhb_informal_learning_label_release_v1:"


SETTINGS = [
    {
        "dataset": "WildChat",
        "task": "coding",
        "setting": "WildChat coding",
        "analysis_scope": "main_six_setting",
        "source_family": "wildchat",
        "source_artifact": "WildChat final production user-turn pipeline, 2026-04-11",
        "level2": BASE
        / "0410_wildchat_userturn_pipeline/latest/coding/wildchat_coding_level2/level2_reports/level2_metrics_20260411_212300.csv",
        "u2a": BASE
        / "0410_wildchat_userturn_pipeline/latest/coding/wildchat_coding_level3/level3_reports/level3_u2a_pairs_20260411_212559.csv",
        "a2u": BASE
        / "0410_wildchat_userturn_pipeline/latest/coding/wildchat_coding_level3/level3_reports/level3_a2u_pairs_20260411_212559.csv",
    },
    {
        "dataset": "WildChat",
        "task": "writing",
        "setting": "WildChat writing",
        "analysis_scope": "main_six_setting",
        "source_family": "wildchat",
        "source_artifact": "WildChat final production user-turn pipeline, 2026-04-11",
        "level2": BASE
        / "0410_wildchat_userturn_pipeline/latest/writing/wildchat_writing_level2/level2_reports/level2_metrics_20260411_212539.csv",
        "u2a": BASE
        / "0410_wildchat_userturn_pipeline/latest/writing/wildchat_writing_level3/level3_reports/level3_u2a_pairs_20260411_212622.csv",
        "a2u": BASE
        / "0410_wildchat_userturn_pipeline/latest/writing/wildchat_writing_level3/level3_reports/level3_a2u_pairs_20260411_212622.csv",
    },
    {
        "dataset": "LMSYS Chat",
        "task": "coding",
        "setting": "LMSYS coding",
        "analysis_scope": "main_six_setting",
        "source_family": "lmsys",
        "source_artifact": "LMSYS Chat final production user-turn pipeline, 2026-06-24",
        "level2": BASE
        / "0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/coding/lmsys_coding_level2/level2_reports/level2_metrics_20260624_121538.csv",
        "u2a": BASE
        / "0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/coding/lmsys_coding_level3/level3_reports/level3_u2a_pairs_20260624_121715.csv",
        "a2u": BASE
        / "0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/coding/lmsys_coding_level3/level3_reports/level3_a2u_pairs_20260624_121715.csv",
    },
    {
        "dataset": "LMSYS Chat",
        "task": "writing",
        "setting": "LMSYS writing",
        "analysis_scope": "main_six_setting",
        "source_family": "lmsys",
        "source_artifact": "LMSYS Chat final production user-turn pipeline, 2026-06-24",
        "level2": BASE
        / "0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/writing/lmsys_writing_level2/level2_reports/level2_metrics_20260624_121658.csv",
        "u2a": BASE
        / "0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/writing/lmsys_writing_level3/level3_reports/level3_u2a_pairs_20260624_121730.csv",
        "a2u": BASE
        / "0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/writing/lmsys_writing_level3/level3_reports/level3_a2u_pairs_20260624_121730.csv",
    },
    {
        "dataset": "ShareChat",
        "task": "coding",
        "setting": "ShareChat coding",
        "analysis_scope": "main_six_setting",
        "source_family": "sharechat",
        "source_artifact": "ShareChat strict-English final production user-turn pipeline, 2026-06-02",
        "level2": BASE
        / "0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/coding/sharechat_coding_level2/level2_reports/level2_metrics_20260602_125948.csv",
        "u2a": BASE
        / "0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/coding/sharechat_coding_level3/level3_reports/level3_u2a_pairs_20260602_130009.csv",
        "a2u": BASE
        / "0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/coding/sharechat_coding_level3/level3_reports/level3_a2u_pairs_20260602_130009.csv",
    },
    {
        "dataset": "ShareChat",
        "task": "writing",
        "setting": "ShareChat writing",
        "analysis_scope": "main_six_setting",
        "source_family": "sharechat",
        "source_artifact": "ShareChat strict-English final production user-turn pipeline, 2026-06-02",
        "level2": BASE
        / "0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/writing/sharechat_writing_level2/level2_reports/level2_metrics_20260602_130002.csv",
        "u2a": BASE
        / "0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/writing/sharechat_writing_level3/level3_reports/level3_u2a_pairs_20260602_130016.csv",
        "a2u": BASE
        / "0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/writing/sharechat_writing_level3/level3_reports/level3_a2u_pairs_20260602_130016.csv",
    },
]

_REMOVED_BOUNDARY_SETTINGS = []
_UNUSED_REMOVED_BOUNDARY_SETTINGS = [
    {
        "dataset": "removed_boundary_corpus",
        "task": "coding",
        "setting": "removed boundary coding",
        "analysis_scope": "boundary_check",
        "source_family": "removed_boundary",
        "source_artifact": "removed boundary-check user-turn pipeline",
        "level2": BASE
        / "removed_boundary_level2.csv",
        "u2a": BASE
        / "removed_boundary_u2a.csv",
        "a2u": BASE
        / "removed_boundary_a2u.csv",
    },
    {
        "dataset": "removed_boundary_corpus",
        "task": "writing",
        "setting": "removed boundary writing",
        "analysis_scope": "boundary_check",
        "source_family": "removed_boundary",
        "source_artifact": "removed boundary-check user-turn pipeline",
        "level2": BASE
        / "removed_boundary_level2.csv",
        "u2a": BASE
        / "removed_boundary_u2a.csv",
        "a2u": BASE
        / "removed_boundary_a2u.csv",
    },
    {
        "dataset": "removed_boundary_corpus",
        "task": "coding",
        "setting": "removed boundary coding",
        "analysis_scope": "boundary_check",
        "source_family": "removed_boundary",
        "source_artifact": "removed boundary-check user-turn pipeline",
        "level2": BASE
        / "removed_boundary_level2.csv",
        "u2a": BASE
        / "removed_boundary_u2a.csv",
        "a2u": BASE
        / "removed_boundary_a2u.csv",
    },
    {
        "dataset": "removed_boundary_corpus",
        "task": "writing",
        "setting": "removed boundary writing",
        "analysis_scope": "boundary_check",
        "source_family": "removed_boundary",
        "source_artifact": "removed boundary-check user-turn pipeline",
        "level2": BASE
        / "removed_boundary_level2.csv",
        "u2a": BASE
        / "removed_boundary_u2a.csv",
        "a2u": BASE
        / "removed_boundary_a2u.csv",
    },
]


CONVERSATION_COLUMNS = [
    "dataset",
    "task",
    "setting",
    "analysis_scope",
    "conversation_id_hash",
    "source_family",
    "model_or_source_family",
    "learning_intent",
    "is_intentional",
    "task_domain",
    "language_flag",
    "is_english",
    "total_turns",
    "user_turns",
    "assistant_turns",
    "depth_after_first_answer",
    "has_scaffolded_support",
    "scaffolded_turn_count",
    "scaffolded_turn_ratio",
    "has_support_intent_I1",
    "has_support_intent_I2",
    "has_support_intent_I3",
    "has_M1_feedback",
    "has_M2_hinting",
    "has_M3_instructing",
    "has_M4_explaining",
    "has_M5_modelling",
    "has_M6_questioning",
    "emotional_user_turn_ratio",
    "cognitive_overall_user_turn_ratio",
    "passive_user_turn_ratio",
    "active_user_turn_ratio",
    "constructive_user_turn_ratio",
    "constructive_user_turn_count",
    "has_constructive_user_turn",
    "constructive_before_first_scaffold_ratio",
    "constructive_after_first_scaffold_ratio",
    "delta_constructive_after_first_scaffold",
    "has_error_marker",
    "persistence_after_failure",
    "constructive_after_error_ratio",
    "high_persistence",
]

U2A_COLUMNS = [
    "dataset",
    "task",
    "setting",
    "analysis_scope",
    "conversation_id_hash",
    "user_turn_id_hash",
    "user_turn_index",
    "source_family",
    "model_or_source_family",
    "learning_intent",
    "is_intentional",
    "task_domain",
    "language_flag",
    "is_english",
    "user_emotional",
    "user_cognitive_level",
    "user_is_constructive",
    "next_assistant_support_type",
    "next_assistant_is_scaffolded",
    "next_assistant_support_intent",
    "next_assistant_is_affective_support",
    "next_assistant_has_M1_feedback",
    "next_assistant_has_M2_hinting",
    "next_assistant_has_M3_instructing",
    "next_assistant_has_M4_explaining",
    "next_assistant_has_M5_modelling",
    "next_assistant_has_M6_questioning",
]

A2U_COLUMNS = [
    "dataset",
    "task",
    "setting",
    "analysis_scope",
    "conversation_id_hash",
    "assistant_turn_id_hash",
    "assistant_turn_index",
    "source_family",
    "model_or_source_family",
    "learning_intent",
    "is_intentional",
    "task_domain",
    "language_flag",
    "is_english",
    "assistant_support_type",
    "assistant_is_scaffolded",
    "assistant_support_intent",
    "assistant_has_M1_feedback",
    "assistant_has_M2_hinting",
    "assistant_has_M3_instructing",
    "assistant_has_M4_explaining",
    "assistant_has_M5_modelling",
    "assistant_has_M6_questioning",
    "previous_user_emotional",
    "previous_user_cognitive_level",
    "previous_user_is_constructive",
    "previous_user_is_error",
    "next_user_emotional",
    "next_user_cognitive_level",
    "next_user_is_constructive",
    "next_user_is_error",
]


def stable_hash(value: str) -> str:
    return hashlib.sha256((HASH_PREFIX + value).encode("utf-8")).hexdigest()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def flag(value: str) -> str:
    if value is None:
        return ""
    value = str(value).strip()
    if value == "":
        return ""
    if value.upper() in {"TRUE", "YES", "Y"}:
        return "1"
    if value.upper() in {"FALSE", "NO", "N"}:
        return "0"
    try:
        return "1" if float(value) != 0 else "0"
    except ValueError:
        return value


def model_or_family(raw_conv_id: str, chat_model: str, source_family: str) -> str:
    if chat_model:
        return chat_model
    parts = raw_conv_id.split("::")
    if source_family in {"lmsys", "sharechat"} and len(parts) >= 2:
        return parts[1]
    return ""


def task_domain(task: str) -> str:
    return "coding-oriented" if task == "coding" else "writing-oriented"


def base_fields(setting: dict[str, object], row: dict[str, str]) -> dict[str, str]:
    raw_id = row["conv_id"]
    return {
        "dataset": str(setting["dataset"]),
        "task": str(setting["task"]),
        "setting": str(setting["setting"]),
        "analysis_scope": str(setting["analysis_scope"]),
        "conversation_id_hash": stable_hash(raw_id),
        "source_family": str(setting["source_family"]),
        "model_or_source_family": model_or_family(
            raw_id, row.get("chat_model", ""), str(setting["source_family"])
        ),
        "learning_intent": row.get("learning_intent", ""),
        "is_intentional": flag(row.get("is_intentional", "")),
        "task_domain": task_domain(str(setting["task"])),
        "language_flag": row.get("language", ""),
        "is_english": flag(row.get("is_english", "")),
    }


def export_conversation(setting: dict[str, object]) -> tuple[list[dict[str, str]], set[str]]:
    rows = []
    allowed_conv_ids: set[str] = set()
    for row in read_rows(Path(setting["level2"])):
        allowed_conv_ids.add(row["conv_id"])
        out = base_fields(setting, row)
        out.update(
            {
                "total_turns": row.get("total_turns", ""),
                "user_turns": row.get("user_turns", ""),
                "assistant_turns": row.get("assistant_turns", ""),
                "depth_after_first_answer": row.get("depth_after_first_answer", ""),
                "has_scaffolded_support": flag(row.get("has_S2", "")),
                "scaffolded_turn_count": row.get("num_S2", ""),
                "scaffolded_turn_ratio": row.get("S2_ratio", ""),
                "has_support_intent_I1": flag(row.get("has_S2_I1", "")),
                "has_support_intent_I2": flag(row.get("has_S2_I2", "")),
                "has_support_intent_I3": flag(row.get("has_S2_I3", "")),
                "has_M1_feedback": flag(row.get("has_M1", "")),
                "has_M2_hinting": flag(row.get("has_M2", "")),
                "has_M3_instructing": flag(row.get("has_M3", "")),
                "has_M4_explaining": flag(row.get("has_M4", "")),
                "has_M5_modelling": flag(row.get("has_M5", "")),
                "has_M6_questioning": flag(row.get("has_M6", "")),
                "emotional_user_turn_ratio": row.get("Emo_ratio", ""),
                "cognitive_overall_user_turn_ratio": row.get("Cog_present_ratio", ""),
                "passive_user_turn_ratio": row.get("Cog_P_ratio", ""),
                "active_user_turn_ratio": row.get("Cog_A_ratio", ""),
                "constructive_user_turn_ratio": row.get("Cog_C_ratio", ""),
                "constructive_user_turn_count": row.get("Cog_C_count", ""),
                "has_constructive_user_turn": flag(row.get("has_Cog_C", "")),
                "constructive_before_first_scaffold_ratio": row.get("C_before_S2_ratio", ""),
                "constructive_after_first_scaffold_ratio": row.get("C_after_S2_ratio", ""),
                "delta_constructive_after_first_scaffold": row.get("delta_C_after_S2", ""),
                "has_error_marker": flag(row.get("has_error", "")),
                "persistence_after_failure": row.get("persistence_after_failure", ""),
                "constructive_after_error_ratio": row.get("C_after_error_ratio", ""),
                "high_persistence": flag(row.get("high_persistence", "")),
            }
        )
        rows.append(out)
    return rows, allowed_conv_ids


def export_u2a(setting: dict[str, object], allowed_conv_ids: set[str]) -> list[dict[str, str]]:
    rows = []
    for row in read_rows(Path(setting["u2a"])):
        raw_id = row["conv_id"]
        if raw_id not in allowed_conv_ids:
            continue
        out = base_fields(setting, row)
        out.update(
            {
                "user_turn_id_hash": stable_hash(f"{raw_id}:user:{row.get('user_turn_index', '')}"),
                "user_turn_index": row.get("user_turn_index", ""),
                "user_emotional": flag(row.get("user_Emotional", "")),
                "user_cognitive_level": row.get("user_Cognitive_level", ""),
                "user_is_constructive": flag(row.get("user_is_C", "")),
                "next_assistant_support_type": row.get("next_asst_Support_Type", ""),
                "next_assistant_is_scaffolded": flag(row.get("next_asst_is_S2", "")),
                "next_assistant_support_intent": row.get("next_asst_S2_Intent", ""),
                "next_assistant_is_affective_support": flag(row.get("next_asst_is_I3", "")),
                "next_assistant_has_M1_feedback": flag(row.get("next_asst_has_M1", "")),
                "next_assistant_has_M2_hinting": flag(row.get("next_asst_has_M2", "")),
                "next_assistant_has_M3_instructing": flag(row.get("next_asst_has_M3", "")),
                "next_assistant_has_M4_explaining": flag(row.get("next_asst_has_M4", "")),
                "next_assistant_has_M5_modelling": flag(row.get("next_asst_has_M5", "")),
                "next_assistant_has_M6_questioning": flag(row.get("next_asst_has_M6", "")),
            }
        )
        rows.append(out)
    return rows


def export_a2u(setting: dict[str, object], allowed_conv_ids: set[str]) -> list[dict[str, str]]:
    rows = []
    for row in read_rows(Path(setting["a2u"])):
        raw_id = row["conv_id"]
        if raw_id not in allowed_conv_ids:
            continue
        support_type = row.get("asst_Support_Type", "")
        out = base_fields(setting, row)
        out.update(
            {
                "assistant_turn_id_hash": stable_hash(
                    f"{raw_id}:assistant:{row.get('asst_turn_index', '')}"
                ),
                "assistant_turn_index": row.get("asst_turn_index", ""),
                "assistant_support_type": support_type,
                "assistant_is_scaffolded": "1" if support_type == "S2" else "0" if support_type else "",
                "assistant_support_intent": row.get("asst_S2_Intent", ""),
                "assistant_has_M1_feedback": flag(row.get("asst_has_M1", "")),
                "assistant_has_M2_hinting": flag(row.get("asst_has_M2", "")),
                "assistant_has_M3_instructing": flag(row.get("asst_has_M3", "")),
                "assistant_has_M4_explaining": flag(row.get("asst_has_M4", "")),
                "assistant_has_M5_modelling": flag(row.get("asst_has_M5", "")),
                "assistant_has_M6_questioning": flag(row.get("asst_has_M6", "")),
                "previous_user_emotional": flag(row.get("prev_user_Emotional", "")),
                "previous_user_cognitive_level": row.get("prev_user_Cognitive_level", ""),
                "previous_user_is_constructive": flag(row.get("prev_user_is_C", "")),
                "previous_user_is_error": flag(row.get("prev_user_is_error", "")),
                "next_user_emotional": flag(row.get("next_user_Emotional", "")),
                "next_user_cognitive_level": row.get("next_user_Cognitive_level", ""),
                "next_user_is_constructive": flag(row.get("next_user_is_C", "")),
                "next_user_is_error": flag(row.get("next_user_is_error", "")),
            }
        )
        rows.append(out)
    return rows


def dataset_slug(name: str) -> str:
    return name.lower().replace(" ", "_")


def write_readme(summary_rows: list[dict[str, str]]) -> None:
    rows_text = "\n".join(
        f"| {r['dataset']} | {r['task']} | {r['analysis_scope']} | {r['conversations']} | {r['user_to_assistant_pairs']} | {r['assistant_to_user_pairs']} |"
        for r in summary_rows
    )
    text = f"""# Derived Label Tables

These files provide de-identified analytic labels for the manuscript's main public-chat task settings. They are intended to complement the aggregate figure source data and statistical-output files.

## Scope

- Included main corpora: WildChat, LMSYS Chat and ShareChat strict-English.
- Included tasks: coding-oriented and writing-oriented conversations.
- Excluded data: raw message text, original conversation identifiers, URLs, timestamps, user identifiers, linked user histories and API credentials.
- Identifier handling: `conversation_id_hash` and turn-level hashes use SHA-256 over `{HASH_PREFIX}<raw id or raw id + role + turn index>`.
- Raw public corpora must still be obtained from the original providers under their own licences and terms.

## Files

Each dataset folder contains:

- `conversation_labels.csv`: one row per analytic conversation, with conversation-level user engagement, assistant scaffolding and contextual labels.
- `user_to_assistant_pair_labels.csv`: one row per user turn that can be paired with the next assistant turn, with the user-side label and next assistant support labels.
- `assistant_to_user_pair_labels.csv`: one row per assistant turn that can be paired with a surrounding user state and next user outcome, with support labels and adjacent user engagement labels.

## Row Counts

| Dataset | Task | Scope | Conversations | User-to-assistant pairs | Assistant-to-user pairs |
|---|---|---|---:|---:|---:|
{rows_text}

## Notes

The adjacent-pair files are not a complete raw turn dump. They preserve the analytic turn-pair units used in the temporal and adjacent-turn models. Conversation-level counts in `conversation_labels.csv` retain the full user-turn and assistant-turn totals used for Table 1 and conversation-level analyses.
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")


def write_summary(summary_rows: list[dict[str, str]]) -> None:
    write_rows(
        OUT / "derived_label_tables_summary.csv",
        [
            "dataset",
            "task",
            "setting",
            "analysis_scope",
            "conversations",
            "user_turns",
            "assistant_turns",
            "user_to_assistant_pairs",
            "assistant_to_user_pairs",
            "source_artifact",
        ],
        summary_rows,
    )


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True, exist_ok=True)
    summary_rows: list[dict[str, str]] = []
    for setting in SETTINGS[:6]:
        for key in ["level2", "u2a", "a2u"]:
            if not Path(setting[key]).exists():
                raise FileNotFoundError(setting[key])
        dataset_dir = OUT / dataset_slug(str(setting["dataset"])) / str(setting["task"])
        conv, allowed_conv_ids = export_conversation(setting)
        u2a = export_u2a(setting, allowed_conv_ids)
        a2u = export_a2u(setting, allowed_conv_ids)
        write_rows(dataset_dir / "conversation_labels.csv", CONVERSATION_COLUMNS, conv)
        write_rows(dataset_dir / "user_to_assistant_pair_labels.csv", U2A_COLUMNS, u2a)
        write_rows(dataset_dir / "assistant_to_user_pair_labels.csv", A2U_COLUMNS, a2u)
        summary_rows.append(
            {
                "dataset": str(setting["dataset"]),
                "task": str(setting["task"]),
                "setting": str(setting["setting"]),
                "analysis_scope": str(setting["analysis_scope"]),
                "conversations": str(len(conv)),
                "user_turns": str(sum(int(float(r["user_turns"])) for r in conv)),
                "assistant_turns": str(sum(int(float(r["assistant_turns"])) for r in conv)),
                "user_to_assistant_pairs": str(len(u2a)),
                "assistant_to_user_pairs": str(len(a2u)),
                "source_artifact": str(setting["source_artifact"]),
            }
        )
    write_summary(summary_rows)
    write_readme(summary_rows)
    print(f"Wrote derived label tables to {OUT}")
    for row in summary_rows:
        print(
            row["setting"],
            "conversations=", row["conversations"],
            "u2a_pairs=", row["user_to_assistant_pairs"],
            "a2u_pairs=", row["assistant_to_user_pairs"],
        )


if __name__ == "__main__":
    main()
