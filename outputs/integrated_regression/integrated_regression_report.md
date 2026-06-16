# Integrated Regression and Significance Report

Data scope: six main public-chat task settings: WildChat, LMSYS Chat-1M and ShareChat strict-English coding/writing. SWE-chat and ThoughtTrace are not included in the main pooled model.

Model-label check: `chat_model` is complete for WildChat. LMSYS and ShareChat production columns are empty, but the conversation identifiers retain recoverable information: LMSYS contains model name and ShareChat contains public assistant/source family. The primary pooled model uses dataset fixed effects; a sensitivity replaces them with model/source fixed effects.

Claim-level consistency audit: Sections 2.1 and 2.2 are descriptive consistency claims over the six public-chat settings. Inferential checks enter where the manuscript makes contrasts or model claims: Section 2.3 uses bootstrap CIs/p values for raw scaffolded versus reference contrasts and adjusted conversation-level models; Section 2.4 reports support-form CIs and between-stratum p values in the main figure; Section 2.5 uses conversation-cluster bootstrap CIs for adjacent-turn lifts and cluster-robust adjacent-turn regressions.

Integrated adjacent-turn logit outcome: whether the next user turn is constructive. Predictors include scaffolded support, prior user state, user framing, task, assistant-turn index, support means M1-M6 and dataset or model/source fixed effects. Standard errors are clustered by conversation.

Key pooled estimates with dataset fixed effects:

- scaffolded_support_S2: OR 0.944, 95% CI [0.871, 1.024], p=0.163539.
- prior_user_constructive: OR 8.237, 95% CI [7.811, 8.686], p=0.
- prior_user_active: OR 2.466, 95% CI [2.369, 2.567], p=0.
- prior_user_passive: OR 2.150, 95% CI [1.825, 2.533], p=5.53961e-20.
- intentional_framing: OR 1.370, 95% CI [1.315, 1.426], p=5.42609e-52.
- coding_task: OR 1.336, 95% CI [1.192, 1.498], p=6.69068e-07.
- M1: OR 0.793, 95% CI [0.735, 0.856], p=2.45376e-09.
- M4: OR 2.150, 95% CI [1.990, 2.323], p=4.93845e-84.
- M6: OR 0.817, 95% CI [0.720, 0.927], p=0.00166897.

Pooled model/source fixed-effect sensitivity:

- scaffolded_support_S2: OR 0.926, 95% CI [0.853, 1.004], p=0.0629577.
- prior_user_constructive: OR 7.944, 95% CI [7.529, 8.381], p=0.
- prior_user_active: OR 2.426, 95% CI [2.330, 2.526], p=0.
- prior_user_passive: OR 2.140, 95% CI [1.816, 2.522], p=1.09682e-19.
- intentional_framing: OR 1.392, 95% CI [1.336, 1.450], p=3.48144e-57.
- coding_task: OR 1.343, 95% CI [1.197, 1.506], p=4.887e-07.
- M1: OR 0.798, 95% CI [0.739, 0.862], p=8.46502e-09.
- M4: OR 2.124, 95% CI [1.965, 2.296], p=5.12837e-80.
- M6: OR 0.842, 95% CI [0.741, 0.956], p=0.00818913.

WildChat model-fixed-effect sensitivity:

- scaffolded_support_S2: OR 0.980, 95% CI [0.890, 1.080], p=0.689208.
- prior_user_constructive: OR 8.480, 95% CI [7.923, 9.075], p=0.
- intentional_framing: OR 1.370, 95% CI [1.301, 1.443], p=1.02296e-32.
- coding_task: OR 1.163, 95% CI [1.007, 1.343], p=0.0392409.
- M1: OR 0.742, 95% CI [0.675, 0.816], p=7.03029e-10.
- M4: OR 2.108, 95% CI [1.925, 2.308], p=1.9446e-58.
- M6: OR 1.077, 95% CI [0.925, 1.253], p=0.340153.

Model/source fixed-effect block in the pooled data: LR chi-square(41)=718.2, p=1.48635e-124. WildChat exact model fixed-effect block: LR chi-square(13)=553.2, p=7.04399e-110. Model/source labels add detectable heterogeneity. In the fully adjusted adjacent-turn model, the broad S2 indicator is not statistically distinguishable from the null after prior user state and specific support forms are included, whereas prior constructive/active state and M4 explaining remain large and statistically robust.

Consistency of key unadjusted contrasts:

- constructive_ratio_has_s2_minus_no_s2: 6/6 settings are positive; 6/6 have p<0.05.
- adjacent_next_constructive_s2_minus_s1: 6/6 settings are positive; 5/6 have p<0.05.

Nested scaffolding block tests:

- six public-chat settings, dataset FE; broad S2 added after user/context controls: LR chi-square(1)=585.0, p=3.11956e-129.
- six public-chat settings, dataset FE; support forms M1-M6 added beyond broad S2: LR chi-square(6)=895.1, p=4.21789e-190.
- six public-chat settings, dataset FE; full scaffolding block S2 plus M1-M6 added after user/context controls: LR chi-square(7)=1480.1, p=0.
- six public-chat settings, model/source FE; broad S2 added after user/context controls: LR chi-square(1)=509.5, p=7.99876e-113.
- six public-chat settings, model/source FE; support forms M1-M6 added beyond broad S2: LR chi-square(6)=827.9, p=1.42297e-175.
- six public-chat settings, model/source FE; full scaffolding block S2 plus M1-M6 added after user/context controls: LR chi-square(7)=1337.5, p=1.30888e-284.
- WildChat only, model FE; broad S2 added after user/context controls: LR chi-square(1)=418.6, p=5.0317e-93.
- WildChat only, model FE; support forms M1-M6 added beyond broad S2: LR chi-square(6)=519.4, p=5.63341e-109.
- WildChat only, model FE; full scaffolding block S2 plus M1-M6 added after user/context controls: LR chi-square(7)=937.9, p=3.08909e-198.

Prior-state by support-form interaction checks:

- six public-chat settings, dataset FE; prior state x M1-M6 block: LR chi-square(18)=308.6, p=8.33426e-55.
- six public-chat settings, model/source FE; prior state x M1-M6 block: LR chi-square(18)=300.2, p=4.43565e-53.
- WildChat only, model FE; prior state x M1-M6 block: LR chi-square(18)=186.0, p=6.27436e-30.

Pooled model/source FE, state-stratified selected support forms:

- prior constructive M1: OR 0.725, 95% CI [0.645, 0.815], p=6.74539e-08.
- prior constructive M4: OR 1.722, 95% CI [1.453, 2.041], p=3.45725e-10.
- prior active M1: OR 0.832, 95% CI [0.725, 0.954], p=0.00841487.
- prior active M4: OR 2.121, 95% CI [1.872, 2.404], p=4.16828e-32.
- prior passive M1: OR 2.161, 95% CI [1.157, 4.036], p=0.0156263.
- prior passive M4: OR 2.875, 95% CI [1.547, 5.344], p=0.000835472.
