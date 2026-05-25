# Peer Feedback Triage and Validation Sources

This document records the local artifacts used to revise the manuscript in response to peer feedback about annotation reliability, examples, and claim boundaries. It intentionally does not reproduce API keys or raw private conversation text.

## Feedback Triage

The feedback is largely reasonable. The manuscript depends on turn-level labels, so the paper should show more than aggregate results: it should expose per-label agreement, prompt/model provenance, and representative label boundaries. This pass therefore added a per-label validation table and an operational example table to Methods.

The request for stronger causal identification is also reasonable as a concern, but the current completed artifacts support observational, covariate-adjusted and temporal-ordering claims rather than causal learning-gain claims. This pass tightened the Results, Methods, and Discussion language to distinguish local state-dependent coupling from cumulative uplift or causal learning effects.

The request for full confusion matrices, stratified validation by platform/domain/language, and formal sensitivity of substantive estimates to label error is only partly satisfied by current local artifacts. Disagreement CSVs and per-label positive counts exist for the validation sets; complete stratified validation and quantitative label-error perturbation analyses were not found in the latest project artifacts during this pass.

## Manuscript Changes In This Pass

Added `tables/table_label_examples.tex`.

Added `tables/table_label_validation.tex`.

Updated `sections/04-methods.tex` to include paraphrased label examples, validation-set sizes, per-label F1/MCC/Gwet AC1 summaries, user-turn update counts, and provenance language.

Updated `sections/02-results_updated.tex` and `sections/03-discussion.tex` to explicitly state that adjusted support--engagement estimates are associations and remain vulnerable to unobserved task/user/time-varying confounding.

## Latest Coding Validation Sources

Primary latest coding agreement rerun:

`/data/zixin/msra/shareable_project/verification/scripts/shareable_project/verification/rerun_outputs/sanity_3rounds_600plus_20260129/`

Key files:

`RUN_META.json`

`agreement_stats.csv`

Run metadata:

Run name: `sanity_3rounds_600plus_20260129`

Bundle: `../apply/coding/final_bundle_3rounds_600plus_20251222`

Tasks: 658 total, 643 after deduplication.

Human--human comparison used in the manuscript: `zixin_vs_Haotian_3rounds`.

Main human--human label agreement values used in `tables/table_label_validation.tex`:

| Label | Support | F1 | MCC | Gwet AC1 | Kappa | Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| A | 315 | 0.748 | 0.716 | 0.869 | 0.694 | 0.908 |
| C | 315 | 0.853 | 0.815 | 0.904 | 0.813 | 0.937 |
| P | 315 | 0.884 | 0.867 | 0.958 | 0.865 | 0.968 |
| E | 315 | 0.826 | 0.821 | 0.971 | 0.813 | 0.975 |
| S1 | 328 | 0.780 | 0.730 | 0.882 | 0.730 | 0.918 |
| S2 | 328 | 0.872 | 0.687 | 0.700 | 0.668 | 0.841 |
| M1 | 328 | 0.903 | 0.885 | 0.953 | 0.882 | 0.966 |
| M2 | 328 | 0.794 | 0.745 | 0.885 | 0.745 | 0.921 |
| M3 | 328 | 0.808 | 0.774 | 0.922 | 0.774 | 0.942 |
| M4 | 328 | 0.856 | 0.790 | 0.839 | 0.789 | 0.909 |
| M5 | 328 | 0.843 | 0.792 | 0.873 | 0.790 | 0.921 |
| M6 | 328 | 0.821 | 0.814 | 0.946 | 0.797 | 0.957 |

Note: `agreement_stats.csv` directly exports F1, kappa, accuracy, support, and positive counts. MCC and Gwet AC1 above were recomputed from the exported per-label support and positive counts.

Additional coding rerun checked:

`/data/zixin/msra/shareable_project/verification/rerun_outputs/sanity_combined_repicked200_new400_20260129/`

This rerun combines the repicked-200 and new-400 validation directories. It has 458 total tasks and 443 after deduplication. It is consistent with the three-round rerun but is not the main manuscript source because the three-round run is the fuller latest coding validation set.

Coding bundle provenance:

`/data/zixin/msra/shareable_project/verification/apply/coding/final_bundle_3rounds_600plus_20251222/README.md`

Coding prompt file:

`/data/zixin/msra/shareable_project/labeling_scripts/apply/coding/v12_prompt_builders.py`

Coding prompt version found in file:

`v21style_prompt_v5m`

## Latest Writing Validation Sources

Primary latest writing agreement directory:

`/data/zixin/msra/shareable_project/verification/apply/writing/verification_writing210_best_pipeline/`

Key files:

`AGREEMENT_RUN_INFO.md`

`PROMPT_FILE_INFO.md`

`agreement_revised_correct/agreement_stats_report.csv`

`agreement_revised_correct/*_disagreements/*.csv`

Run metadata from `AGREEMENT_RUN_INFO.md`:

Script: `verification/scripts/analyze_agreement_writing210_revised.py`

Zixin annotations: `verification/apply/writing/agreement_writing_20260123_prompt_r17_full/annotated_zixin.json`

Haotian annotations: `verification/apply/writing/agreement_writing_20260123_prompt_r17_full/annotated_haotian.json`

LLM output: `verification/apply/writing/agreement_writing_20260123_prompt_r17_full/llm_with_turn_index__best_pipeline.json`

Tasks: `verification/apply/writing/agreement_writing_20260123_prompt_r17_full/task_order_writing_210.csv`

The best pipeline includes these post-processing stages:

`postprocess_llm_assistant_s2_recover.py`

`postprocess_llm_assistant_s2_details_heuristic.py`

`postprocess_llm_user_ca_strict_v3.py`

`postprocess_llm_user_cc_strict.py`

`postprocess_llm_user_emotional_strict.py`

Human--human comparison used in the manuscript: `zixin_vs_Haotian`.

Main human--human label agreement values used in `tables/table_label_validation.tex`:

| Label | Support | F1 | MCC | Gwet AC1 | Kappa | Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| A | 90 | 0.375 | 0.376 | 0.686 | 0.289 | 0.778 |
| C | 90 | 0.885 | 0.827 | 0.859 | 0.826 | 0.922 |
| P | 90 | 0.800 | 0.812 | 0.988 | 0.795 | 0.989 |
| E | 90 | 0.667 | 0.654 | 0.963 | 0.649 | 0.967 |
| S1 | 120 | 0.462 | 0.429 | 0.855 | 0.403 | 0.883 |
| S2 | 120 | 0.971 | 0.796 | 0.934 | 0.795 | 0.950 |
| M1 | 120 | 0.889 | 0.799 | 0.802 | 0.798 | 0.900 |
| M2 | 120 | 0.820 | 0.704 | 0.708 | 0.694 | 0.850 |
| M3 | 120 | 0.714 | 0.665 | 0.859 | 0.655 | 0.900 |
| M4 | 120 | 0.839 | 0.699 | 0.701 | 0.699 | 0.850 |
| M5 | 120 | 0.938 | 0.915 | 0.945 | 0.915 | 0.967 |
| M6 | 120 | 0.963 | 0.959 | 0.990 | 0.958 | 0.992 |

Writing prompt file:

`/data/zixin/msra/shareable_project/labeling_scripts/apply/writing/v12_prompt_builders_writing_topic.py`

Writing prompt version found in file:

`v21style_prompt_v5m_writingtopic_r20260130_r60_intentlist_cp_cc_i3_refine_v10`

Model/config provenance:

`/data/zixin/msra/shareable_project/verification/apply/writing/verification_writing210_best_pipeline/API_CONFIG_SUMMARY.md`

This file documents the deployment/model configuration used for the writing validation pipeline. The manuscript/source notes should not reproduce the API key contained in that local file.

## User-Turn Final Check Sources

Final manual review directory:

`/data/zixin/msra/labellingTool/public/data/user_turn_final_label_check/`

Files:

`review_wildchat_pc_final_coding_review_100_2026-03-28.json`

`review_wildchat_pc_final_writing_review_100_2026-03-28.json`

Each file contains 100 reviewed WildChat user-turn examples after the update pass. The review records include the LLM label, human verdict, bad-data flag, and relabel notes.

WildChat user-turn update reports:

`/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/reports/user_turn_round2_final_coding_report.json`

`/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/reports/user_turn_round2_final_writing_report.json`

Coding update pass:

31,879 conversations scanned; 3,801 candidates found and processed; 1,815 updates applied.

Writing update pass:

39,534 conversations scanned; 165 candidates found and processed; 21 updates applied.

## Disagreement and Error Inspection

Writing disagreement CSVs are available under:

`/data/zixin/msra/shareable_project/verification/apply/writing/verification_writing210_best_pipeline/agreement_revised_correct/`

Subdirectories include:

`zixin_vs_haotian_disagreements/`

`zixin_vs_llm_disagreements/`

`haotian_vs_llm_disagreements/`

`llm_vs_consensus_disagreements/`

These files provide per-label disagreement case indices for error inspection. They do not by themselves include full confusion-matrix tables in manuscript-ready form.

## Result and Robustness Output Sources

Main refreshed Level 1--4 outputs:

`/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0406_latest/`

Key files include:

`CONCLUSIONS_0406_updated.md`

`wildchat_pipeline_0406.log`

`plot_figures_0406.log`

`copilot_final_results_0406.zip`

Figure and table data sources for the current result figures:

`/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0419_nhb_spec_figures/`

WildChat model snapshot/family robustness outputs:

`/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0420_wildchat_modeltype_figures/`

## Figure Source Note

The manuscript currently compiles from PDF figures in `figures/`. The editable SVG versions of all five final manuscript figures are present in:

`figures_svg_editable/final_figures/`
