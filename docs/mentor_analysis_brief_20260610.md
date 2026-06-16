# Mentor Brief: Multi-Corpus Public-Data Revision

Date: 2026-06-10

This brief summarizes the current public-data analysis for discussion with mentors or external collaborators. It is written as a working analysis/RQ draft rather than final manuscript prose. The main writing direction should not emphasize any single dataset. The stronger framing is that the core patterns are evaluated across multiple public conversational corpora, with WildChat, LMSYS Chat-1M and ShareChat strict-English as the main reportable evidence, and SWE-chat and ThoughtTrace as boundary checks.

## 1. Current Framing

Large language models are increasingly used during everyday work, but most empirical evidence about LLMs and learning comes from designed educational settings such as tutoring, feedback, question generation or classroom support. Our analysis asks whether everyday, naturalistic human-LLM conversations contain observable behavioural signatures of informal learning, even when users are not explicitly in a learning environment.

The core idea is to translate learning-science constructs into turn-level conversational signals. On the user side, we distinguish passive receipt, active uptake and constructive engagement. Constructive engagement is the strictest user-side proxy because it captures turns where users elaborate, test, revise, transfer or extend ideas. On the assistant side, we distinguish non-scaffolded reference responses from scaffolded support, and then decompose scaffolded support into support forms such as feedback, hinting, instructing, explaining, modelling and questioning.

The analysis is observational and associational. It does not claim durable learning gains or causal instructional effects. Instead, it asks whether everyday AI use contains measurable learning-oriented engagement, where that engagement is concentrated and how assistant scaffolding is locally coupled with constructive user participation across different public conversational corpora.

## 2. Working Research Questions

RQ1. Presence and composition: Do everyday human-LLM conversations contain observable learning-oriented engagement, and what depth of engagement is most common across public corpora?

RQ2. Contextual concentration: How does constructive engagement vary by user framing, task ecology and interaction depth?

RQ3. Scaffolding association: Are conversations with scaffolded assistant support associated with richer constructive participation, after accounting for observed conversation context?

RQ4. Cross-corpus robustness and limits: Which findings replicate across broad public-chat corpora, which findings are corpus-sensitive and what do specialized or highly selected corpora reveal about boundary conditions?

## 3. Current Methodology Status

The defensible public-data version should be organized around three public conversational corpora and six task settings:

| Setting | Conversations | User turns | Assistant turns | Intentional conv. (%) | Scaffolded turns (%) | Cognitive overall (%) | Constructive (%) | Emotional (%) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| WildChat coding | 31,878 | 124,073 | 124,623 | 37.13 | 51.03 | 50.21 | 9.23 | 0.95 |
| WildChat writing | 39,534 | 163,705 | 164,824 | 25.80 | 23.53 | 16.34 | 2.22 | 0.57 |
| LMSYS coding | 31,879 | 106,312 | 104,431 | 41.54 | 29.11 | 45.28 | 5.43 | 0.90 |
| LMSYS writing | 21,023 | 77,906 | 76,279 | 20.64 | 19.43 | 15.30 | 1.53 | 0.21 |
| ShareChat coding | 2,481 | 11,541 | 11,522 | 45.63 | 50.67 | 45.00 | 15.17 | 3.38 |
| ShareChat writing | 1,539 | 7,395 | 7,363 | 29.69 | 22.42 | 33.05 | 5.18 | 0.34 |
| Total / pooled | 128,334 | 490,932 | 489,042 | 32.11 | 31.71 | 31.93 | 4.93 | 0.74 |

The annotation pipeline remains the same Level 1-4 framework: task filtering, turn-level LLM-assisted annotation, parser checks, targeted post-processing and human verification. The latest manuscript should continue to treat labels as behavioural signatures, not as direct measurements of learning outcomes.

### Corpus Roles

The writing should not present the analysis as "WildChat plus LMSYS only." A cleaner structure is:

| Corpus | Current status | Filtered usable size | Role in interpretation | Recommended manuscript use |
| --- | --- | ---: | --- | --- |
| WildChat | Completed | 31,878 coding; 39,534 writing conversations | Broad public-chat anchor corpus. It shows high coding-oriented engagement and clear scaffolded-support associations. | Main evidence. |
| LMSYS Chat-1M | Completed | 31,879 coding; 21,023 writing conversations | Broad public-chat replication corpus. It has lower scaffolded-support supply than WildChat, but still shows positive scaffolded-support associations with constructive participation. | Main evidence and cross-corpus replication. |
| ShareChat strict-English | Completed strict-English check | 2,481 coding; 1,539 writing conversations | Smaller and more selected because conversations are shared publicly, but it provides a useful third public-chat check. Constructive engagement is higher than in WildChat/LMSYS, suggesting a more engaged public-share ecology rather than a post-processing artefact. | Report as robustness evidence, preferably in the main results or a compact robustness section rather than only as an internal note. |
| SWE-chat | Completed clean pipeline rerun | 1,771 coding; 4 writing conversations | Useful coding-specific setting with agentic software-engineering interactions. The writing side is essentially absent, so it cannot support the coding-versus-writing design. | Report as a coding-specific setting; do not use the writing side. |
| ThoughtTrace | Completed all-LLM v3 filter, annotation and after-pipeline check | 56 coding; 61 writing conversations | Larger than the earlier v1/v2 check, but still too small and highly selected. S2 support is near-saturated in coding and very high in writing, leaving little non-scaffolded reference variation; several adjusted models show separation, non-convergence or unstable coefficients. | Internal feasibility/sanity check only, unless framed explicitly as a small specialized-corpus appendix. |

The latest ThoughtTrace all-LLM v3 report is at `/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0602_thoughttrace_replacement/user_turn_pipeline_min4_all_llm_v3/latest/user_llm_dynamics/large_analysis/user_llm_report_thoughttrace_v2.md`.

## 4. Important LMSYS Interpretation Check

The mentor concern about LMSYS is valid and should be handled explicitly. LMSYS has much lower assistant scaffolding supply than WildChat in coding, but its overall cognitive engagement does not drop in proportion. However, constructive engagement does drop.

| Setting | Scaffolded turns (%) | Cognitive overall (%) | Constructive (%) | Interpretation |
| --- | ---: | ---: | ---: | --- |
| WildChat coding | 51.03 | 50.21 | 9.23 | High scaffolding supply and high constructive engagement. |
| LMSYS coding | 29.11 | 45.28 | 5.43 | Much lower scaffolding supply; cognitive uptake remains relatively high, but constructive engagement is lower. |
| ShareChat coding | 50.67 | 45.00 | 15.17 | High scaffolding supply and very high constructive engagement, consistent with a selected high-engagement sharing ecology. |
| WildChat writing | 23.53 | 16.34 | 2.22 | Lower writing engagement and lower scaffolding than coding. |
| LMSYS writing | 19.43 | 15.30 | 1.53 | Similar overall cognitive engagement to WildChat writing, but lower constructive engagement. |
| ShareChat writing | 22.42 | 33.05 | 5.18 | Higher selected-engagement writing sample, with higher constructive engagement. |

This is not necessarily a contradiction. Cognitive engagement is broad and includes active uptake, so it can remain high even when assistant turns are less often scaffolded. Constructive engagement is stricter and appears more sensitive to the availability and timing of scaffolded support. The revised writing should therefore avoid implying that scaffolding simply raises all engagement. A more precise claim is that scaffolded support is most consistently associated with constructive participation, while overall cognitive uptake is also shaped by dataset ecology, task selection, user motivation and conversation length.

This explanation is also consistent with the temporal results: LMSYS writing has a positive conversation-level scaffolded-support association, but a small adjacent-turn lift compared with WildChat and ShareChat. That pattern suggests that some LMSYS engagement may be driven by broader conversation context rather than immediate local support.

## 5. Findings for Sections 2.1-2.3

### Section 2.1: Everyday conversations contain learning-oriented engagement

Across the pooled WildChat, LMSYS and ShareChat task settings, cognitive engagement appears in 31.9% of user turns, constructive engagement appears in 4.9% and emotional engagement is rare at 0.74%. This supports the claim that everyday human-LLM interaction often contains more than passive answer receipt, but the deeper constructive form is selective.

The cross-corpus pattern is more informative than a single pooled value:

| Task ecology | Constructive range across WildChat/LMSYS/ShareChat | Main interpretation |
| --- | ---: | --- |
| Coding-oriented conversations | 5.43-15.17% | Coding consistently elicits more constructive participation than writing, likely because debugging, constraints and executable tests make revision and explanation more visible. |
| Writing-oriented conversations | 1.53-5.18% | Writing has lower constructive engagement in broad corpora, but ShareChat shows that selected public-share writing interactions can still contain substantial constructive engagement. |

Figure implication: if figures are updated, the main Figure 2 should include WildChat, LMSYS and ShareChat where space allows, or use WildChat/LMSYS in the main panel with ShareChat as a labelled robustness inset. The caption should avoid framing the paper as a two-dataset analysis if the text claims three corpora.

### Section 2.2: Constructive engagement is shaped by framing, task ecology and depth

Constructive engagement is higher when users explicitly frame the interaction as learning-oriented or exploratory. The intentional versus unintentional contrast appears in cognitive engagement and constructive engagement across the broad corpora and is especially visible in coding-oriented settings.

Coding-oriented conversations show higher constructive engagement than writing-oriented conversations across WildChat, LMSYS and ShareChat. The best explanation is not that coding is inherently "more educational," but that coding tasks make uncertainty, failure and revision more externally visible through errors, constraints, tests and debugging loops. Writing tasks can often be resolved through direct drafting or editing without requiring users to articulate the underlying rationale.

Interaction depth also matters descriptively. The share of conversations with at least one constructive turn increases with conversation length in the main corpora. This should be interpreted as an opportunity structure for constructive participation, not as causal evidence that longer conversations automatically produce learning.

### Section 2.3: Scaffolded conversations show richer constructive participation

The support-engagement association is positive across WildChat, LMSYS and ShareChat, but the strength and temporal form vary by corpus and task. This is exactly why the writing should emphasize cross-corpus convergence in the direction of association, while being transparent about corpus-sensitive magnitudes.

| Setting | Constructive ratio, Has S2 / No S2 | Difference (pp) | Post-answer depth diff. (turns) | Poisson RR | Logit OR | Adjacent-turn lift (pp) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| WildChat coding | 0.094 / 0.055 | +3.9 | +2.23 | 1.852 | 1.761 | +2.67 |
| LMSYS coding | 0.059 / 0.039 | +2.0 | +1.43 | 1.626 | 1.542 | +2.01 |
| ShareChat coding | 0.167 / 0.092 | +7.5 | +3.36 | 1.893 | 2.140 | +6.21 |
| WildChat writing | 0.032 / 0.020 | +1.2 | +3.13 | 1.569 | 1.437 | +1.12 |
| LMSYS writing | 0.022 / 0.010 | +1.2 | +2.10 | 1.985 | 1.764 | +0.26 |
| ShareChat writing | 0.058 / 0.032 | +2.6 | +3.39 | 2.491 | 1.757 | +3.35 |

Adjusted models remain positive across all six reportable settings, suggesting that scaffolded-support presence is not fully explained by measured user framing, task ecology and interaction depth. The interpretation remains associational because scaffolding is not randomized and may be elicited by task complexity, user motivation or previous interaction state.

The revised main claim should be:

Scaffolded assistant support is most consistently associated with constructive engagement, the strictest user-side behavioural signature of learning-oriented participation. The association is visible across multiple public corpora, but its magnitude depends on corpus ecology and task context.

The revised main claim should not be:

Scaffolding always increases overall engagement, or every corpus shows the same local temporal coupling.

## 6. Boundary Checks From SWE-chat and ThoughtTrace

SWE-chat coding can be reported as a coding-specific setting, while ThoughtTrace should remain a small feasibility check.

| Corpus | Useful observation | Limitation |
| --- | --- | --- |
| SWE-chat coding | 1,771 coding conversations; 35.77% cognitive engagement; 17.34% constructive engagement; 17.74% scaffolded assistant turns; scaffolded conversations have higher constructive ratios than non-scaffolded conversations (0.207 vs 0.121). | Only 4 writing conversations after filtering, so it cannot support coding-versus-writing comparisons. It is an agentic software-engineering corpus, not broad public chat. |
| ThoughtTrace all-LLM v3 | 56 coding and 61 writing conversations after the updated all-LLM filter. Coding has high cognitive engagement (64.54%) and S2 turns are very frequent (85.71%). | Sample is small and scaffolded support is near-saturated, especially in coding. There is too little non-scaffolded reference variation for stable adjusted associations. |

These checks can be described as corpus screening or boundary-condition analyses. They should not drive the main RQ narrative unless the paper explicitly adds a small appendix section on specialized corpora.

## 7. Data-Use and Compliance Points to Clarify

This is not a legal opinion, but these are the analysis boundaries we can communicate clearly:

- We do not use private Copilot data in this branch.
- We report aggregate turn-level and conversation-level statistics rather than raw conversation excerpts.
- Examples in the manuscript should be de-identified and paraphrased rather than copied verbatim from logs.
- We do not link conversations into user histories.
- We do not estimate longitudinal user-level trajectories.
- Temporal analyses are within-conversation turn-order analyses, such as adjacent assistant-to-user or user-to-assistant pairs.
- The study does not infer user demographics, identity, expertise or durable learning outcomes.
- Data-use review should confirm whether each public corpus license or usage guideline allows aggregate behavioural analysis and LLM-assisted annotation for research publication.

The likely sensitive point is not longitudinal tracking, because the current temporal analysis is not longitudinal across users. The more important compliance question is whether aggregate analysis of public conversational logs, after filtering and paraphrased reporting, is allowed under the relevant dataset usage guidelines.

## 8. Suggested Short Note to Collaborators

We are revising the public-data version so that the core results are framed across public conversational corpora rather than around a single dataset. The main reportable evidence comes from WildChat, LMSYS Chat-1M, ShareChat strict-English and SWE-chat coding. ThoughtTrace was processed with the same pipeline but is better treated as a boundary check because it is small with near-saturated scaffolding.

The first result is that everyday LLM conversations contain observable learning-oriented engagement: across the six WildChat/LMSYS/ShareChat task settings, cognitive engagement appears in about 31.9% of user turns, while the stricter constructive form appears in about 4.9%. Constructive engagement is concentrated in intentional, coding-oriented and longer exchanges.

The second result is that scaffolded assistant support is associated with richer constructive participation across all six reportable settings. LMSYS is important because it has lower scaffolded-support supply than WildChat, while overall cognitive engagement does not decline proportionally. This should be interpreted as evidence that scaffolding is most tightly connected to constructive engagement, not to all forms of cognitive uptake. Overall cognitive uptake is broader and can be shaped by task selection, user motivation and dataset ecology.

For data-use review, the key question is whether aggregate behavioural analysis of these public conversational datasets is compliant with the relevant usage guidelines. The current analysis should be easier to defend than longitudinal user analysis because it does not link conversations across users or estimate user-level trajectories; all temporal claims are confined to within-conversation ordering.

## 9. Source Reports to Attach or Show

- WildChat report: `/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0410_wildchat_userturn_pipeline/latest/user_llm_dynamics/large_analysis/user_llm_report_wildchat_v2.md`
- LMSYS report: `/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0530_lmsys_chat_1m_replacement/user_turn_pipeline_min4/latest/user_llm_dynamics/large_analysis/user_llm_report_lmsys_v2.md`
- ShareChat strict-English report: `/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0529_sharechat_replacement/user_turn_pipeline_min4_english_strict/latest/user_llm_dynamics/large_analysis/user_llm_report_sharechat_v2.md`
- SWE-chat clean rerun report: `/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0615_swe_chat_clean_rerun/user_turn_pipeline_min4/latest/user_llm_dynamics/large_analysis/user_llm_report_swe_chat_v2.md`
- ThoughtTrace all-LLM v3 report: `/data/zixin/msra/shareable_project/investigations/level_analysis/outputs/0602_thoughttrace_replacement/user_turn_pipeline_min4_all_llm_v3/latest/user_llm_dynamics/large_analysis/user_llm_report_thoughttrace_v2.md`

## 10. Files Currently Relevant in the Paper Repo

- Main compiled PDF: `sn-article.pdf`
- Dataset overview: `tables/table3.tex`
- Support association summary: `tables/table4.tex`
- Figure 1 framework: `figures/figure_1_all_wild_lmsys.png`
- Figure 2 engagement ecology: `figures/fig_engagement_ecology_compact_final.pdf`
- Figure 3 support association: `figures/fig_support_association_wild_lmsys_with_ci.pdf`
- Figure 4 support forms and supply: `figures/fig_support_form_supply_compact_final_v2.pdf`
- Figure 5 temporal coupling: `figures/fig_temporal_coupling_scale_compact_final_v5.pdf`
- Figure 6 temporal estimand schematic: `figures/figure5_temporal_schematic_refined.pdf`

These repo files still appear to be mostly WildChat + LMSYS oriented. If the paper text is revised to foreground WildChat, LMSYS and ShareChat together, the figures and tables should be updated accordingly or explicitly described as main-plus-robustness displays.
