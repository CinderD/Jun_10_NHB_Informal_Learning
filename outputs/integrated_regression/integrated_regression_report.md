# Integrated Regression and Significance Report

Data scope: six main task settings: WildChat, LMSYS Chat and ShareChat coding/writing.

Model-label check: `chat_model` is complete for WildChat. LMSYS and ShareChat production columns are empty, but the conversation identifiers retain recoverable information: LMSYS contains model name and ShareChat contains public assistant/source family. The primary pooled model uses dataset fixed effects; a sensitivity replaces them with model/source fixed effects.

Claim-level consistency audit: Sections 2.1 and 2.2 are descriptive consistency claims over the six task settings. Inferential checks enter where the manuscript makes contrasts or model claims: Section 2.3 uses bootstrap CIs/p values for turn-weighted scaffolded versus reference contrasts, adjusted conversation-level models and an offset-rate sensitivity; Section 2.4 reports support-form CIs and between-stratum FDR-adjusted q values in the main figure; Section 2.5 uses conversation-cluster bootstrap CIs for adjacent-turn lifts and cluster-robust adjacent-turn regressions.

Section 2.2 conversation-level context check: a logistic regression predicting whether a conversation contains at least one constructive user turn includes user framing, task ecology, length bucket and dataset fixed effects. The model is a robustness check for systematic organization, not a causal estimate.

- Intentional framing: OR 3.028, 95% CI [2.926, 3.132], p=0.
- Coding task ecology: OR 1.888, 95% CI [1.714, 2.080], p=7.49305e-38.
- 4--6 user turns: OR 2.072, 95% CI [1.993, 2.154], p=2.27605e-295.
- 7+ user turns: OR 3.576, 95% CI [3.417, 3.743], p=0.

Section 2.2 constructive-rate sensitivity: a grouped-binomial logistic regression models constructive user-turn count out of total user turns with the same user framing, task ecology, length bucket and dataset fixed effects. This checks whether the length pattern is only an opportunity-count artifact from the any-constructive outcome.

- Intentional framing: OR 2.779, 95% CI [2.679, 2.883], p=0.
- Coding task ecology: OR 1.665, 95% CI [1.475, 1.880], p=1.82657e-16.
- 4--6 user turns: OR 1.134, 95% CI [1.092, 1.178], p=6.15766e-11.
- 7+ user turns: OR 1.063, 95% CI [1.015, 1.114], p=0.00984742.

Section 2.3 offset-rate sensitivity: the setting-specific Poisson model for constructive-turn counts was refitted with `offset(log(user_turns))` and quasi-Poisson scaled standard errors. This checks whether the scaffolded-support association is only a count-model specification artifact.

- WC coding: RR 1.570, 95% CI [1.471, 1.676], p=7.78715e-42.
- LMSYS coding: RR 1.465, 95% CI [1.379, 1.557], p=8.54994e-35.
- SC coding: RR 1.580, 95% CI [1.311, 1.905], p=1.5983e-06.
- WC writing: RR 1.356, 95% CI [1.257, 1.462], p=2.68522e-15.
- LMSYS writing: RR 1.703, 95% CI [1.497, 1.937], p=5.19063e-16.
- SC writing: RR 1.654, 95% CI [1.274, 2.147], p=0.000154645.

Integrated adjacent-turn logit outcome: whether the next user turn is constructive. Broad scaffolded-support models include scaffolded-support presence without M1-M6. Support-form decomposed models include broad scaffolded support plus M1-M6, so M coefficients describe form-level variation within scaffolded support. Standard errors are clustered by conversation.

Setting-level adjacent-turn models: separate model/source-adjusted regressions were fitted within each of the six task settings to check dataset-by-factor heterogeneity rather than relying only on pooled fixed effects. These outputs are exported to `setting_level_adjacent_turn_logit_model_source_fe.csv` and summarized in Supplementary Table C.

- Setting-level scaffolded_support_S2: OR>1 in 6/6 settings; p<0.05 in 4/6 settings.
- Setting-level prior_user_constructive: OR>1 in 6/6 settings; p<0.05 in 6/6 settings.
- Setting-level M1: OR>1 in 4/6 settings; p<0.05 in 4/6 settings.
- Setting-level M4: OR>1 in 6/6 settings; p<0.05 in 4/6 settings.
- Setting-level M6: OR>1 in 2/6 settings; p<0.05 in 3/6 settings.

Key pooled estimates with dataset fixed effects. Scaffolded-support and user/context rows come from broad scaffolded-support models; M rows come from support-form decomposed models:

- scaffolded_support_S2: OR 1.495, 95% CI [1.443, 1.549], p=1.1673e-109.
- prior_user_constructive: OR 8.904, 95% CI [8.453, 9.379], p=0.
- prior_user_active: OR 2.618, 95% CI [2.518, 2.723], p=0.
- prior_user_passive: OR 2.075, 95% CI [1.763, 2.443], p=1.65002e-18.
- intentional_framing: OR 1.402, 95% CI [1.346, 1.459], p=5.02918e-61.
- coding_task: OR 1.369, 95% CI [1.220, 1.537], p=9.78613e-08.
- M1: OR 0.792, 95% CI [0.734, 0.855], p=2.20746e-09.
- M4: OR 2.150, 95% CI [1.990, 2.323], p=4.73013e-84.
- M6: OR 0.816, 95% CI [0.720, 0.926], p=0.00158038.

Pooled model/source fixed-effect sensitivity:

- scaffolded_support_S2: OR 1.466, 95% CI [1.415, 1.519], p=7.29052e-100.
- prior_user_constructive: OR 8.552, 95% CI [8.114, 9.014], p=0.
- prior_user_active: OR 2.567, 95% CI [2.467, 2.671], p=0.
- prior_user_passive: OR 2.071, 95% CI [1.760, 2.438], p=2.11854e-18.
- intentional_framing: OR 1.423, 95% CI [1.367, 1.481], p=2.23372e-66.
- coding_task: OR 1.373, 95% CI [1.223, 1.542], p=8.50092e-08.
- M1: OR 0.797, 95% CI [0.738, 0.861], p=7.49698e-09.
- M4: OR 2.124, 95% CI [1.965, 2.296], p=4.65553e-80.
- M6: OR 0.841, 95% CI [0.740, 0.955], p=0.00774421.

WildChat model-fixed-effect sensitivity:

- scaffolded_support_S2: OR 1.555, 95% CI [1.486, 1.627], p=1.2114e-81.
- prior_user_constructive: OR 9.112, 95% CI [8.526, 9.738], p=0.
- intentional_framing: OR 1.400, 95% CI [1.330, 1.474], p=1.32561e-37.
- coding_task: OR 1.213, 95% CI [1.050, 1.401], p=0.00852337.
- M1: OR 0.742, 95% CI [0.675, 0.816], p=7.03029e-10.
- M4: OR 2.108, 95% CI [1.925, 2.308], p=1.9446e-58.
- M6: OR 1.077, 95% CI [0.925, 1.253], p=0.340153.

Model/source fixed-effect block in the pooled data: LR chi-square(41)=714.4, p=8.95719e-124. WildChat exact model fixed-effect block: LR chi-square(13)=553.2, p=7.04399e-110. Model/source labels add detectable heterogeneity. Broad scaffolded support remains positive in the broad support model, while the decomposed models show that support-form variation, especially M4 explaining, carries additional local signal.

Consistency of key unadjusted contrasts:

- constructive_ratio_has_s2_minus_no_s2: 6/6 settings are positive; 6/6 have p<0.05.
- post_answer_depth_has_s2_minus_no_s2: 6/6 settings are positive; 6/6 have p<0.05.
- adjacent_next_constructive_s2_minus_s1: 6/6 settings are positive; 5/6 have p<0.05.

Nested scaffolding block tests:

- six task settings, dataset FE; broad scaffolded support added after user/context controls: LR chi-square(1)=584.6, p=3.72994e-129.
- six task settings, dataset FE; support-form descriptors M1-M6 added within scaffolded support: LR chi-square(6)=896.7, p=1.92283e-190.
- six task settings, dataset FE; full scaffolding block plus M1-M6 added after user/context controls: LR chi-square(7)=1481.3, p=0.
- six task settings, model/source FE; broad scaffolded support added after user/context controls: LR chi-square(1)=509.7, p=7.24738e-113.
- six task settings, model/source FE; support-form descriptors M1-M6 added within scaffolded support: LR chi-square(6)=829.8, p=5.52223e-176.
- six task settings, model/source FE; full scaffolding block plus M1-M6 added after user/context controls: LR chi-square(7)=1339.6, p=4.60016e-285.
- WildChat only, model FE; broad scaffolded support added after user/context controls: LR chi-square(1)=418.6, p=5.0317e-93.
- WildChat only, model FE; support-form descriptors M1-M6 added within scaffolded support: LR chi-square(6)=519.4, p=5.63341e-109.
- WildChat only, model FE; full scaffolding block plus M1-M6 added after user/context controls: LR chi-square(7)=937.9, p=3.08909e-198.

Prior-state by support-form interaction checks:

- six task settings, dataset FE; prior state x M1-M6 block: LR chi-square(18)=305.4, p=3.72548e-54.
- six task settings, model/source FE; prior state x M1-M6 block: LR chi-square(18)=297.3, p=1.69029e-52.
- WildChat only, model FE; prior state x M1-M6 block: LR chi-square(18)=186.0, p=6.27436e-30.

Pooled model/source FE, state-stratified support forms:

- prior constructive scaffolded_support_S2: OR 0.938, 95% CI [0.778, 1.130], p=0.49987.
- prior constructive M1: OR 0.724, 95% CI [0.645, 0.814], p=6.2191e-08.
- prior constructive M2: OR 0.905, 95% CI [0.789, 1.038], p=0.154979.
- prior constructive M3: OR 0.924, 95% CI [0.811, 1.053], p=0.235731.
- prior constructive M4: OR 1.721, 95% CI [1.452, 2.039], p=3.5963e-10.
- prior constructive M5: OR 0.810, 95% CI [0.705, 0.931], p=0.00305086.
- prior constructive M6: OR 0.946, 95% CI [0.716, 1.249], p=0.694143.
- prior active scaffolded_support_S2: OR 0.701, 95% CI [0.614, 0.801], p=1.46317e-07.
- prior active M1: OR 0.831, 95% CI [0.725, 0.953], p=0.00805331.
- prior active M2: OR 1.143, 95% CI [1.025, 1.274], p=0.0160466.
- prior active M3: OR 0.983, 95% CI [0.892, 1.082], p=0.721853.
- prior active M4: OR 2.127, 95% CI [1.877, 2.410], p=2.40933e-32.
- prior active M5: OR 0.829, 95% CI [0.758, 0.906], p=3.43384e-05.
- prior active M6: OR 0.751, 95% CI [0.606, 0.931], p=0.00901202.
- prior passive scaffolded_support_S2: OR 0.700, 95% CI [0.331, 1.483], p=0.35183.
- prior passive M1: OR 2.164, 95% CI [1.159, 4.041], p=0.0153442.
- prior passive M2: OR 1.791, 95% CI [0.952, 3.372], p=0.0707934.
- prior passive M3: OR 1.521, 95% CI [0.674, 3.432], p=0.312153.
- prior passive M4: OR 2.880, 95% CI [1.552, 5.347], p=0.000801455.
- prior passive M5: OR 0.456, 95% CI [0.201, 1.037], p=0.06116.
- prior passive M6: OR 2.192, 95% CI [1.124, 4.274], p=0.0213349.
