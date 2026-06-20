# Integrated Regression and Significance Report

Data scope: six main task settings: WildChat, LMSYS Chat and ShareChat coding/writing. SWE-chat and ThoughtTrace are not included in the main pooled model.

Model-label check: `chat_model` is complete for WildChat. LMSYS and ShareChat production columns are empty, but the conversation identifiers retain recoverable information: LMSYS contains model name and ShareChat contains public assistant/source family. The primary pooled model uses dataset fixed effects; a sensitivity replaces them with model/source fixed effects.

Claim-level consistency audit: Sections 2.1 and 2.2 are descriptive consistency claims over the six task settings. Inferential checks enter where the manuscript makes contrasts or model claims: Section 2.3 uses bootstrap CIs/p values for turn-weighted scaffolded versus reference contrasts and adjusted conversation-level models; Section 2.4 reports support-form CIs and between-stratum FDR-adjusted q values in the main figure; Section 2.5 uses conversation-cluster bootstrap CIs for adjacent-turn lifts and cluster-robust adjacent-turn regressions.

Section 2.2 conversation-level context check: a logistic regression predicting whether a conversation contains at least one constructive user turn includes user framing, task ecology, length bucket and dataset fixed effects. The model is a robustness check for systematic organization, not a causal estimate.

- Intentional framing: OR 3.029, 95% CI [2.927, 3.134], p=0.
- Coding task ecology: OR 1.887, 95% CI [1.713, 2.079], p=9.82466e-38.
- 4--6 user turns: OR 2.069, 95% CI [1.990, 2.151], p=2.1066e-293.
- 7+ user turns: OR 3.576, 95% CI [3.417, 3.743], p=0.

Integrated adjacent-turn logit outcome: whether the next user turn is constructive. Broad S2 models include scaffolded-support presence without M1-M6. Support-form decomposed models include broad S2 plus M1-M6, so M coefficients describe form-level variation within scaffolded support. Standard errors are clustered by conversation.

Setting-level adjacent-turn models: separate model/source-adjusted regressions were fitted within each of the six task settings to check dataset-by-factor heterogeneity rather than relying only on pooled fixed effects. These outputs are exported to `setting_level_adjacent_turn_logit_model_source_fe.csv` and summarized in Supplementary Table C.

- Setting-level scaffolded_support_S2: OR>1 in 6/6 settings; p<0.05 in 4/6 settings.
- Setting-level prior_user_constructive: OR>1 in 6/6 settings; p<0.05 in 6/6 settings.
- Setting-level M1: OR>1 in 4/6 settings; p<0.05 in 4/6 settings.
- Setting-level M4: OR>1 in 6/6 settings; p<0.05 in 4/6 settings.
- Setting-level M6: OR>1 in 2/6 settings; p<0.05 in 3/6 settings.

Key pooled estimates with dataset fixed effects. S2 and user/context rows come from broad S2 models; M rows come from support-form decomposed models:

- scaffolded_support_S2: OR 1.496, 95% CI [1.444, 1.550], p=8.81018e-110.
- prior_user_constructive: OR 8.899, 95% CI [8.449, 9.374], p=0.
- prior_user_active: OR 2.619, 95% CI [2.518, 2.724], p=0.
- prior_user_passive: OR 2.066, 95% CI [1.754, 2.432], p=3.33229e-18.
- intentional_framing: OR 1.403, 95% CI [1.348, 1.460], p=2.82583e-61.
- coding_task: OR 1.373, 95% CI [1.223, 1.541], p=8.26508e-08.
- M1: OR 0.793, 95% CI [0.735, 0.856], p=2.45376e-09.
- M4: OR 2.150, 95% CI [1.990, 2.323], p=4.93845e-84.
- M6: OR 0.817, 95% CI [0.720, 0.927], p=0.00166897.

Pooled model/source fixed-effect sensitivity:

- scaffolded_support_S2: OR 1.466, 95% CI [1.415, 1.519], p=7.9874e-100.
- prior_user_constructive: OR 8.545, 95% CI [8.108, 9.006], p=0.
- prior_user_active: OR 2.566, 95% CI [2.467, 2.670], p=0.
- prior_user_passive: OR 2.061, 95% CI [1.750, 2.427], p=4.36728e-18.
- intentional_framing: OR 1.424, 95% CI [1.368, 1.482], p=1.1906e-66.
- coding_task: OR 1.376, 95% CI [1.225, 1.546], p=7.26524e-08.
- M1: OR 0.798, 95% CI [0.739, 0.862], p=8.46502e-09.
- M4: OR 2.124, 95% CI [1.965, 2.296], p=5.12837e-80.
- M6: OR 0.842, 95% CI [0.741, 0.956], p=0.00818913.

WildChat model-fixed-effect sensitivity:

- scaffolded_support_S2: OR 1.555, 95% CI [1.486, 1.627], p=1.2114e-81.
- prior_user_constructive: OR 9.112, 95% CI [8.526, 9.738], p=0.
- intentional_framing: OR 1.400, 95% CI [1.330, 1.474], p=1.32561e-37.
- coding_task: OR 1.213, 95% CI [1.050, 1.401], p=0.00852337.
- M1: OR 0.742, 95% CI [0.675, 0.816], p=7.03029e-10.
- M4: OR 2.108, 95% CI [1.925, 2.308], p=1.9446e-58.
- M6: OR 1.077, 95% CI [0.925, 1.253], p=0.340153.

Model/source fixed-effect block in the pooled data: LR chi-square(41)=718.2, p=1.48635e-124. WildChat exact model fixed-effect block: LR chi-square(13)=553.2, p=7.04399e-110. Model/source labels add detectable heterogeneity. Broad S2 remains positive in the broad support model, while the decomposed models show that support-form variation, especially M4 explaining, carries additional local signal.

Consistency of key unadjusted contrasts:

- constructive_ratio_has_s2_minus_no_s2: 6/6 settings are positive; 6/6 have p<0.05.
- adjacent_next_constructive_s2_minus_s1: 6/6 settings are positive; 5/6 have p<0.05.

Nested scaffolding block tests:

- six task settings, dataset FE; broad S2 added after user/context controls: LR chi-square(1)=585.0, p=3.11956e-129.
- six task settings, dataset FE; support-form descriptors M1-M6 added within scaffolded support: LR chi-square(6)=895.1, p=4.21789e-190.
- six task settings, dataset FE; full scaffolding block S2 plus M1-M6 added after user/context controls: LR chi-square(7)=1480.1, p=0.
- six task settings, model/source FE; broad S2 added after user/context controls: LR chi-square(1)=509.5, p=7.99876e-113.
- six task settings, model/source FE; support-form descriptors M1-M6 added within scaffolded support: LR chi-square(6)=827.9, p=1.42297e-175.
- six task settings, model/source FE; full scaffolding block S2 plus M1-M6 added after user/context controls: LR chi-square(7)=1337.5, p=1.30888e-284.
- WildChat only, model FE; broad S2 added after user/context controls: LR chi-square(1)=418.6, p=5.0317e-93.
- WildChat only, model FE; support-form descriptors M1-M6 added within scaffolded support: LR chi-square(6)=519.4, p=5.63341e-109.
- WildChat only, model FE; full scaffolding block S2 plus M1-M6 added after user/context controls: LR chi-square(7)=937.9, p=3.08909e-198.

Prior-state by support-form interaction checks:

- six task settings, dataset FE; prior state x M1-M6 block: LR chi-square(18)=308.6, p=8.33426e-55.
- six task settings, model/source FE; prior state x M1-M6 block: LR chi-square(18)=300.2, p=4.43565e-53.
- WildChat only, model FE; prior state x M1-M6 block: LR chi-square(18)=186.0, p=6.27436e-30.

Pooled model/source FE, state-stratified selected support forms:

- prior constructive M1: OR 0.725, 95% CI [0.645, 0.815], p=6.74539e-08.
- prior constructive M4: OR 1.722, 95% CI [1.453, 2.041], p=3.45725e-10.
- prior active M1: OR 0.832, 95% CI [0.725, 0.954], p=0.00841487.
- prior active M4: OR 2.121, 95% CI [1.872, 2.404], p=4.16828e-32.
- prior passive M1: OR 2.161, 95% CI [1.157, 4.036], p=0.0156263.
- prior passive M4: OR 2.875, 95% CI [1.547, 5.344], p=0.000835472.
