# Mentor Brief: Current Analysis, RQs and Data-Use Boundaries

Date: 2026-06-10

This brief summarizes the current WildChat + LMSYS version of the analysis for discussion with mentors or external collaborators. It is written as a working analysis/RQ draft rather than as final manuscript prose.

## 1. Current Framing

Large language models are increasingly used during everyday work, but most empirical evidence about LLMs and learning comes from designed educational settings such as tutoring, feedback, question generation or classroom support. Our analysis asks whether everyday, naturalistic human--LLM conversations contain observable behavioural signatures of informal learning, even when users are not explicitly in a learning environment.

The core idea is to translate learning-science constructs into turn-level conversational signals. On the user side, we distinguish passive receipt, active uptake and constructive engagement. Constructive engagement is the strictest user-side proxy because it captures turns where users elaborate, test, revise, transfer or extend ideas. On the assistant side, we distinguish non-scaffolded reference responses from scaffolded support, and then decompose scaffolded support into support forms such as feedback, hinting, instructing, explaining, modelling and questioning.

The analysis is observational and associational. It does not claim durable learning gains or causal instructional effects. Instead, it asks whether everyday AI use contains measurable learning-oriented engagement, where that engagement is concentrated and how assistant scaffolding is locally coupled with constructive user participation.

## 2. Working Research Questions

RQ1. Presence and composition: Do everyday human--LLM conversations contain observable learning-oriented engagement, and what depth of engagement is most common?

RQ2. Contextual concentration: How does constructive engagement vary by user framing, task ecology and interaction depth?

RQ3. Scaffolding association: Are conversations with scaffolded assistant support associated with richer constructive participation, after accounting for observed conversation context?

RQ4. Optional extension beyond Sections 2.1--2.3: Which support forms are most aligned with constructive engagement, and is the support--engagement relationship strongest at the adjacent-turn scale or over longer within-conversation windows?

## 3. Current Methodology Status

The manuscript branch now uses two public conversational corpora and four task settings:

| Setting | Conversations | User turns | Assistant turns | Intentional conv. (%) | Scaffolded turns (%) | Cognitive overall (%) | Constructive (%) | Emotional (%) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| WildChat coding | 31,878 | 124,073 | 124,623 | 37.13 | 51.03 | 50.21 | 9.23 | 0.95 |
| WildChat writing | 39,534 | 163,705 | 164,824 | 25.80 | 23.53 | 16.34 | 2.22 | 0.57 |
| LMSYS coding | 31,879 | 106,312 | 104,431 | 41.54 | 29.11 | 45.28 | 5.43 | 0.90 |
| LMSYS writing | 21,023 | 77,906 | 76,279 | 20.64 | 19.43 | 15.30 | 1.53 | 0.21 |
| Total / pooled | 124,314 | 471,996 | 470,157 | 31.87 | 31.39 | 31.59 | 4.67 | 0.68 |

The current manuscript files have been updated so that Abstract, Introduction, Results, Methods and Appendix all describe the WildChat + LMSYS version rather than the earlier WildChat-only version.

The annotation pipeline remains the same Level 1--4 framework: task filtering, turn-level LLM-assisted annotation, parser checks, targeted post-processing and human verification. The latest manuscript treats labels as behavioural signatures, not as direct measurements of learning outcomes.

### Candidate public-corpus checks

The main manuscript currently uses LMSYS Chat-1M as the public replacement/replication corpus alongside WildChat. Other candidate corpora were checked with the same pipeline logic but are not folded into the main manuscript because their sampling frames differ too strongly from broad everyday public chat.

| Corpus | Current status | Filtered usable size | Main pattern | Recommendation |
| --- | --- | ---: | --- | --- |
| LMSYS Chat-1M | Completed and included in the manuscript | 31,879 coding; 21,023 writing conversations | Replicates the broad WildChat pattern: coding shows higher learning-oriented engagement than writing; scaffolded conversations are more constructive; local adjacent-turn coupling is positive but weaker in writing. | Main public replication corpus. |
| ShareChat strict-English | Completed strict-English check | 2,481 coding; 1,539 writing conversations | Constructive engagement remains materially higher than WildChat after strict language filtering: 15.17% in coding and 5.18% in writing, with stronger adjacent-turn lifts (+6.21 and +3.35 pp). This suggests the high constructive rate is not caused only by non-English content or missing post-processing, but by public-share selection and more engaged conversations. | Useful exploratory robustness corpus, but too small and selected for the main replacement analysis. |
| SWE-chat | Completed pipeline check | 1,536 coding; 3 writing conversations | Coding is a useful agentic software-engineering stress test, with 32.36% cognitive engagement and 19.45% scaffolded assistant turns. The writing side is essentially absent after filtering, so the corpus cannot support the paper's coding-versus-writing design. | Coding-specific appendix check only if needed; not a balanced main corpus. |
| ThoughtTrace | Completed/re-filtered check | 2 coding; 14 writing conversations | The retained sample is too small for stable descriptive, regression or temporal analyses; several regressions are singular or underpowered. | Do not use for main or appendix claims. |

This means the latest dataset update is not simply "more datasets in the paper." The defensible manuscript decision is to use WildChat plus LMSYS for the main evidence, and to keep ShareChat, SWE-chat and ThoughtTrace as internal feasibility checks unless reviewers specifically ask for broader corpus screening.

## 4. Findings for Sections 2.1--2.3

### Section 2.1: Everyday conversations contain learning-oriented engagement

Across the pooled WildChat + LMSYS corpus, cognitive engagement appears in 31.6% of user turns, constructive engagement appears in 4.7% and emotional engagement is rare at 0.68%. This supports the claim that everyday human--LLM interaction often contains more than passive answer receipt, but the deeper constructive form is selective.

Figure to show: `figures/fig_engagement_ecology_compact_final.pdf`

Main visual point: active uptake dominates cognitively engaged turns across all four settings, while constructive engagement remains a smaller but stable component.

### Section 2.2: Constructive engagement is shaped by framing, task ecology and depth

Constructive engagement is higher when users explicitly frame the interaction as learning-oriented or exploratory. The intentional versus unintentional contrast appears in both cognitive engagement and constructive engagement.

Coding-oriented conversations show higher cognitive and constructive engagement than writing-oriented conversations in both datasets. A plausible interpretation is that coding tasks make uncertainty, failure and revision more externally visible through errors, constraints and executable tests, whereas writing tasks can often be resolved through direct drafting or editing without requiring users to articulate the underlying rationale.

Interaction depth also matters descriptively. The share of conversations with at least one constructive turn increases monotonically with conversation length, from 0.033--0.151 in 2--3-turn conversations to 0.112--0.463 in conversations with seven or more turns. We interpret this as an opportunity structure for constructive participation, not as causal evidence that longer conversations automatically produce learning.

Figure to show: `figures/fig_engagement_ecology_compact_final.pdf`, especially panels b and c.

### Section 2.3: Scaffolded conversations show richer constructive participation

Conversations containing at least one scaffolded assistant turn show higher constructive participation than conversations without scaffolded support in all four task settings.

| Setting | Constructive ratio, Has S2 / No S2 | Difference (pp) | Post-answer depth diff. (turns) | Poisson RR | Logit OR |
| --- | ---: | ---: | ---: | ---: | ---: |
| WildChat coding | 0.094 / 0.055 | +3.9 | +2.23 | 1.852 | 1.761 |
| LMSYS coding | 0.059 / 0.039 | +2.0 | +1.43 | 1.626 | 1.542 |
| WildChat writing | 0.032 / 0.020 | +1.2 | +3.13 | 1.569 | 1.437 |
| LMSYS writing | 0.022 / 0.010 | +1.2 | +2.10 | 1.985 | 1.764 |

Adjusted models remain positive across all four settings, suggesting that scaffolded-support presence is not fully explained by measured user framing, task ecology and interaction depth. The interpretation remains associational because scaffolding is not randomized and may be elicited by task complexity or user motivation.

Figure to show: `figures/fig_support_association_wild_lmsys_with_ci.pdf`

Main visual point: scaffolded conversations are more constructive and deeper, and adjusted association estimates remain above 1 across settings.

## 5. Data-Use and Compliance Points to Clarify

This is not a legal opinion, but these are the analysis boundaries we can communicate clearly:

- We do not use private Copilot data in this branch.
- We report aggregate turn-level and conversation-level statistics rather than raw conversation excerpts.
- Examples in the manuscript are de-identified and paraphrased rather than copied verbatim from logs.
- We do not link conversations into user histories.
- We do not estimate longitudinal user-level trajectories.
- Temporal analyses are within-conversation turn-order analyses, such as adjacent assistant-to-user or user-to-assistant pairs.
- The study does not infer user demographics, identity, expertise or durable learning outcomes.
- Data-use review should confirm whether each public corpus license or usage guideline allows aggregate behavioural analysis and LLM-assisted annotation for research publication.

The likely sensitive point is not longitudinal tracking, because the current temporal analysis is not longitudinal across users. The more important compliance question is whether aggregate analysis of public conversational logs, after filtering and paraphrased reporting, is allowed under the relevant dataset usage guidelines.

## 6. Suggested Short Note to Collaborators

We are currently using a WildChat + LMSYS version of the analysis. The methodology has been updated to use a shared Level 1--4 annotation pipeline across four task settings: WildChat coding, WildChat writing, LMSYS coding and LMSYS writing. The main analysis remains observational and aggregate. We do not use Copilot data, do not reproduce raw conversation text and do not track users longitudinally.

The first set of results shows that everyday LLM conversations contain observable learning-oriented engagement: cognitive engagement appears in about 31.6% of user turns, while the stricter constructive form appears in 4.7%. Constructive engagement is concentrated in intentional, coding-oriented and longer exchanges. A second set of results shows that scaffolded assistant support is associated with richer constructive participation across all four task settings, with positive raw contrasts and positive adjusted Poisson/logit associations. These analyses support an interpretation of everyday LLM use as a site of potential informal learning, while remaining careful not to claim causal learning gains.

For data-use review, the key question is whether aggregate behavioural analysis of these public conversational datasets is compliant with the relevant usage guidelines. The current analysis should be easier to defend than longitudinal user analysis because it does not link conversations across users or estimate user-level trajectories; all temporal claims are confined to within-conversation ordering.

## 7. Files to Attach or Show

- Main compiled PDF: `sn-article.pdf`
- Dataset overview: `tables/table3.tex`
- Support association summary: `tables/table4.tex`
- Figure 1 framework: `figures/figure_1_all_wild_lmsys.png`
- Figure 2 engagement ecology: `figures/fig_engagement_ecology_compact_final.pdf`
- Figure 3 support association: `figures/fig_support_association_wild_lmsys_with_ci.pdf`
- Figure 4 support forms and supply: `figures/fig_support_form_supply_compact_final_v2.pdf`
- Figure 5 temporal coupling: `figures/fig_temporal_coupling_scale_compact_final_v5.pdf`
- Figure 6 temporal estimand schematic: `figures/figure5_temporal_schematic_refined.pdf`
