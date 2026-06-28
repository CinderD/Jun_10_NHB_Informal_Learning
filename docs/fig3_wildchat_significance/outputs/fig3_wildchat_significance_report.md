# Figure 3 WildChat Significance Report

## Data Files Used
- WC coding: `<local-msra-root>/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/latest/coding/wildchat_coding_level2/level2_reports/level2_metrics_20260411_212300.csv`
- WC writing: `<local-msra-root>/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/latest/writing/wildchat_writing_level2/level2_reports/level2_metrics_20260411_212539.csv`
- WC coding production report used for formula verification: `<local-msra-root>/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/latest/coding/wildchat_coding_level2/level2_reports/level2_report_20260411_212300.md`
- WC writing production report used for formula verification: `<local-msra-root>/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/latest/writing/wildchat_writing_level2/level2_reports/level2_report_20260411_212539.md`

## Filter Applied
- Source scope: task-specific WildChat level-2 production CSVs only.
- Included task settings: `WC coding` and `WC writing`.
- Excluded source scope: all non-WildChat files and rows.
- User-framing strata: `learning_intent == INTENTIONAL` and `learning_intent == UNINTENTIONAL`.

## Model Formulas
- Adjusted Poisson: `Cog_C_count ~ has_S2 + is_intentional + is_coding_topic + total_turns + Emo_ratio + has_error + persistence_after_failure + high_persistence`.
- Adjusted logit: `has_Cog_C ~ has_S2 + is_intentional + is_coding_topic + total_turns`.
- Stratified Poisson used for the CSV/Figure 3c candidate: `Cog_C_count ~ has_S2 + is_coding_topic + total_turns + Emo_ratio + has_error + persistence_after_failure + high_persistence` within each user-framing stratum. This follows the requested rule of using the Figure 3b Poisson covariates while omitting user framing.
- Offsets: none in the production reports; none were added here.
- SE method for adjusted models: standard model SE, nonrobust, matching the production report covariance type.
- CI method for raw contrasts: 5,000-draw conversation-level bootstrap for mean differences.
- P-value method for raw contrasts: two-sided Mann-Whitney U test, matching the existing comparative-analysis convention.

## Reproduction Check
| Estimate | Target | Recomputed | Status |
|---|---:|---:|---|
| WC coding Poisson RR | 1.852 | 1.852 | matches rounding |
| WC coding Logit OR | 1.761 | 1.761 | matches rounding |
| WC writing Poisson RR | 1.569 | 1.569 | matches rounding |
| WC writing Logit OR | 1.437 | 1.437 | matches rounding |
| WC coding intentional Poisson RR | 1.800 | 1.968 | differs from provided target |
| WC coding unintentional Poisson RR | 1.500 | 1.633 | near target |
| WC writing intentional Poisson RR | 2.900 | 1.579 | differs from provided target |
| WC writing unintentional Poisson RR | 1.100 | 1.567 | differs from provided target |

The adjusted Figure 3b estimates reproduce the current production point estimates. The user-framing stratified Poisson estimates use the requested same-as-Figure-3b-minus-framing specification, but do not reproduce the provided rounded targets for `WC writing`; the recomputed results are 1.579 and 1.567, not 2.9 and 1.1.

As a cross-check, the 0410 production report's own stratified summary uses the same formula except it omits `high_persistence`; that variant gives 1.980 and 1.636 for coding, and 1.583 and 1.567 for writing. The discrepancy with the provided 2.9/1.1 targets therefore is not caused by the `high_persistence` choice.

## Estimates
| Panel | Task | Metric | Estimate | 95% CI | p | n |
|---|---|---|---:|---:|---:|---:|
| a | WC coding | raw contrast | 3.98 pp | [3.57, 4.39] | 3.02e-109 | 31878 |
| a | WC writing | raw contrast | 1.26 pp | [1.05, 1.46] | 2.41e-88 | 39534 |

| Panel | Task | Metric | Estimate | 95% CI | p | n |
|---|---|---|---:|---:|---:|---:|
| b | WC coding | Poisson RR | 1.852 | [1.749, 1.961] | 1.25e-98 | 31878 |
| b | WC coding | Logit OR | 1.761 | [1.635, 1.896] | 1.39e-50 | 31878 |
| b | WC writing | Poisson RR | 1.569 | [1.463, 1.682] | 1.38e-36 | 39534 |
| b | WC writing | Logit OR | 1.437 | [1.328, 1.555] | 2.51e-19 | 39534 |

| Panel | Task | Framing | Metric | Estimate | 95% CI | p | n |
|---|---|---:|---|---:|---:|---:|---:|
| c | WC coding | intentional | Poisson RR | 1.968 | [1.802, 2.149] | 3.94e-51 | 11837 |
| c | WC coding | unintentional | Poisson RR | 1.633 | [1.513, 1.763] | 4.12e-36 | 20041 |
| c | WC writing | intentional | Poisson RR | 1.579 | [1.427, 1.748] | 9.01e-19 | 10201 |
| c | WC writing | unintentional | Poisson RR | 1.567 | [1.422, 1.726] | 1.10e-19 | 29333 |

| Panel | Task | Metric | Estimate | 95% CI | p | n |
|---|---|---|---:|---:|---:|---:|
| d | WC coding | raw contrast | 2.23 | [2.11, 2.34] | <1e-300 | 31878 |
| d | WC writing | raw contrast | 3.13 | [2.95, 3.31] | <1e-300 | 39534 |

| Panel | Task | Metric | Estimate | 95% CI | p | n |
|---|---|---|---:|---:|---:|---:|
| appendix | WC coding | raw contrast | 45.58 pp | [42.02, 49.23] | 1.26e-41 | 31878 |

## Statistical Distinguishability
- Raw constructive-ratio contrasts are distinguishable from zero in both WildChat task settings.
- Adjusted Poisson RR and logit OR estimates are distinguishable from the null value of 1 in both task settings.
- User-framing stratified Poisson RR estimates are distinguishable from the null value of 1 in all four strata under the production model.
- Post-answer depth differences are distinguishable from zero in both task settings.
- The appendix persistence contrast reproduces the current figure metric and is distinguishable from zero.

## Quality Checks
- Generated CSV, report and editable figure text were checked for removed source labels and deprecated wording; no matches were found.
- The updated Figure 3 PDF text boxes were checked for obvious label overlap after generation.

## Warnings
- The persistence output that matches the current figure uses `persistence_after_failure` as a conversation-level metric with zeros for conversations without detected breakdowns. This reproduces 0.895 versus 0.440 after scaling, but the source column is count-like rather than a failure-case-only binary probability.
- All model formulas use observed covariates only. These outputs support associational claims, not causal interpretation.

