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

`<local-msra-root>/shareable_project/verification/scripts/shareable_project/verification/rerun_outputs/sanity_3rounds_600plus_20260129/`

Key files:

`RUN_META.json`

`agreement_stats.csv`

Run metadata:

Run name: `sanity_3rounds_600plus_20260129`

Bundle: `../apply/coding/final_bundle_3rounds_600plus_20251222`

Tasks: 658 total, 643 after deduplication.

Human--human comparison used in the manuscript: two-reviewer comparison from the three-round coding audit.

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

`<local-msra-root>/shareable_project/verification/rerun_outputs/sanity_combined_repicked200_new400_20260129/`

This rerun combines the repicked-200 and new-400 validation directories. It has 458 total tasks and 443 after deduplication. It is consistent with the three-round rerun but is not the main manuscript source because the three-round run is the fuller latest coding validation set.

Coding bundle provenance:

`<local-msra-root>/shareable_project/verification/apply/coding/final_bundle_3rounds_600plus_20251222/README.md`

Coding prompt file:

`<local-msra-root>/shareable_project/labeling_scripts/apply/coding/v12_prompt_builders.py`

Coding prompt version found in file:

`v21style_prompt_v5m`

## Latest Writing Validation Sources

Primary latest writing agreement directory:

`<local-msra-root>/shareable_project/verification/apply/writing/verification_writing210_best_pipeline/`

Key files:

`AGREEMENT_RUN_INFO.md`

`PROMPT_FILE_INFO.md`

`agreement_revised_correct/agreement_stats_report.csv`

`agreement_revised_correct/*_disagreements/*.csv`

Run metadata from `AGREEMENT_RUN_INFO.md`:

Script: `verification/scripts/analyze_agreement_writing210_revised.py`

First human-review annotation artifact: retained locally.

Second human-review annotation artifact: retained locally.

LLM output: `verification/apply/writing/agreement_writing_20260123_prompt_r17_full/llm_with_turn_index__best_pipeline.json`

Tasks: `verification/apply/writing/agreement_writing_20260123_prompt_r17_full/task_order_writing_210.csv`

The best pipeline includes these post-processing stages:

`postprocess_llm_assistant_s2_recover.py`

`postprocess_llm_assistant_s2_details_heuristic.py`

`postprocess_llm_user_ca_strict_v3.py`

`postprocess_llm_user_cc_strict.py`

`postprocess_llm_user_emotional_strict.py`

Human--human comparison used in the manuscript: two-reviewer comparison using the final human-confirmed writing-210 labels.

Main writing label validation values used in `tables/table_label_validation.tex`:

| Label | Support | F1 | MCC | Gwet AC1 | Kappa | Accuracy |
|---|---:|---:|---:|---:|---:|---:|
| A | 90 | 0.732 | 0.685 | 0.811 | 0.657 | 0.878 |
| C | 90 | 0.885 | 0.827 | 0.859 | 0.826 | 0.922 |
| P | 90 | 0.800 | 0.812 | 0.988 | 0.795 | 0.989 |
| E | 90 | 0.800 | 0.788 | 0.975 | 0.788 | 0.978 |
| S1 | 120 | 0.710 | 0.671 | 0.903 | 0.667 | 0.925 |
| S2 | 120 | 0.971 | 0.796 | 0.934 | 0.795 | 0.950 |
| M1 | 120 | 0.889 | 0.799 | 0.802 | 0.798 | 0.900 |
| M2 | 120 | 0.820 | 0.704 | 0.708 | 0.694 | 0.850 |
| M3 | 120 | 0.714 | 0.665 | 0.859 | 0.655 | 0.900 |
| M4 | 120 | 0.839 | 0.699 | 0.701 | 0.699 | 0.850 |
| M5 | 120 | 0.938 | 0.915 | 0.945 | 0.915 | 0.967 |
| M6 | 120 | 0.963 | 0.959 | 0.990 | 0.958 | 0.992 |

Internal provenance artifacts:

`<local-msra-root>/shareable_project/verification/apply/writing/agreement_writing_20260123_prompt_r17_full/post_discussion_minimal/`

This folder retains the derived final human-confirmed file, the label-correction ledger and the recomputed agreement outputs. Original reviewer exports were not overwritten. The human-confirmed pass made 21 label-level updates: 9 for `C_A`, 5 for `S1`, 6 for `S2_Intent_I3` and 1 for `E`.

Writing prompt file:

`<local-msra-root>/shareable_project/labeling_scripts/apply/writing/v12_prompt_builders_writing_topic.py`

Writing prompt version found in file:

`v21style_prompt_v5m_writingtopic_r20260130_r60_intentlist_cp_cc_i3_refine_v10`

Model/config provenance:

`<local-msra-root>/shareable_project/verification/apply/writing/verification_writing210_best_pipeline/API_CONFIG_SUMMARY.md`

This file documents the deployment/model configuration used for the writing validation pipeline. The manuscript/source notes should not reproduce the API key contained in that local file.

## User-Turn Final Check Sources

Final manual review directory:

`<local-msra-root>/labellingTool/public/data/user_turn_final_label_check/`

## User-Framing Validation Sources

Final human-verified user-framing audit:

Local audit artifact; public source-data release includes aggregate metrics only.

Metrics:

`source_data/validation/user_framing_validation_450_human_confirmed_metrics.csv`

Sampling design:

- 450 first user turns.
- 75 cases from each corpus-by-task setting: WildChat coding, WildChat writing, LMSYS Chat coding, LMSYS Chat writing, ShareChat coding and ShareChat writing.
- Each setting was positive-oversampled: 50 production-positive intentional-framing cases and 25 production-negative cases.

Key metrics against production labels:

| Group | n | Intentional F1 | MCC | Gwet AC1 |
|---|---:|---:|---:|---:|
| Overall | 450 | 0.857 | 0.677 | 0.671 |
| Coding | 225 | 0.924 | 0.791 | 0.820 |
| Writing | 225 | 0.779 | 0.589 | 0.517 |
| WildChat | 150 | 0.839 | 0.670 | 0.636 |
| LMSYS Chat | 150 | 0.795 | 0.585 | 0.542 |
| ShareChat | 150 | 0.928 | 0.799 | 0.828 |

Interpretation:

This audit fills the earlier gap in which the writing-210 learning-intent check had no positive human cases. Because the audit intentionally oversampled production-positive cases, it validates the user-framing label boundary but should not be used to estimate population prevalence.

## Assistant Production-Label Validation Sources

Human-confirmed assistant-side production-label audit:

`<local-msra-root>/labellingTool/public/data/assistant_production_validation_180_20260629_codex_prefilled.json`

Metrics:

`<local-msra-root>/labellingTool/public/data/assistant_production_validation_results/assistant_production_validation_per_label_metrics.csv`

Sampling design:

- 180 assistant turns.
- 30 cases from each corpus-by-task setting.
- Scaffolded-support and support-form positives were deliberately oversampled.

Key overall metrics against production labels:

| Label | F1 | MCC | Gwet AC1 |
|---|---:|---:|---:|
| Scaffolding | 0.912 | 0.590 | 0.791 |
| M1 feedback | 0.938 | 0.918 | 0.945 |
| M2 hinting | 0.909 | 0.880 | 0.930 |
| M3 instructing | 0.717 | 0.600 | 0.715 |
| M4 explaining | 0.883 | 0.772 | 0.747 |
| M5 modelling | 0.724 | 0.631 | 0.642 |
| M6 questioning | 0.691 | 0.675 | 0.873 |

Interpretation:

The audit validates assistant scaffolded-support and support-form label boundaries. Because it intentionally oversampled positive support labels, it should not be used to estimate population prevalence.

Files:

`review_wildchat_pc_final_coding_review_100_2026-03-28.json`

`review_wildchat_pc_final_writing_review_100_2026-03-28.json`

Each file contains 100 reviewed WildChat user-turn examples after the update pass. The review records include the LLM label, human verdict, bad-data flag, and relabel notes.

WildChat user-turn update reports:

`<local-msra-root>/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/reports/user_turn_round2_final_coding_report.json`

`<local-msra-root>/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/reports/user_turn_round2_final_writing_report.json`

Coding update pass:

31,879 conversations scanned; 3,801 candidates found and processed; 1,815 updates applied.

Writing update pass:

39,534 conversations scanned; 165 candidates found and processed; 21 updates applied.

## Disagreement and Error Inspection

Writing disagreement CSVs are available under:

`<local-msra-root>/shareable_project/verification/apply/writing/verification_writing210_best_pipeline/agreement_revised_correct/`

Subdirectories include:

`human_review_pair_disagreements/`

`human_review_vs_llm_disagreements/`

`second_human_review_vs_llm_disagreements/`

`llm_vs_consensus_disagreements/`

These files provide per-label disagreement case indices for error inspection. They do not by themselves include full confusion-matrix tables in manuscript-ready form.

## Result and Robustness Output Sources

Main refreshed Level 1--4 outputs:

`<local-msra-root>/shareable_project/investigations/level_analysis/outputs/0406_latest/`

Key files include:

`CONCLUSIONS_0406_updated.md`

`wildchat_pipeline_0406.log`

`plot_figures_0406.log`

`copilot_final_results_0406.zip`

Figure and table data sources for the current result figures:

`<local-msra-root>/shareable_project/investigations/level_analysis/outputs/0419_nhb_spec_figures/`

WildChat model snapshot/family robustness outputs:

`<local-msra-root>/shareable_project/investigations/level_analysis/outputs/0420_wildchat_modeltype_figures/`

## Figure Source Note

The manuscript currently compiles from PDF figures in `figures/`. The editable SVG versions of all five final manuscript figures are present in:

`figures_svg_editable/final_figures/`
