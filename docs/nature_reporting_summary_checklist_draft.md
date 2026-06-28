# Nature Reporting Summary and Editorial Checklist Draft

This draft is intended to support completion of the Nature Portfolio Reporting Summary and related editorial policy checklist. It summarizes information already reported in the manuscript, Supplementary Information, source-data release and code archive.

## Study Design

This is a secondary observational analysis of public human-LLM conversation corpora. The study does not assign treatments, recruit participants, randomize exposure, or measure individual-level learning outcomes. It characterizes aggregate turn-level and conversation-level behavioural signatures of learning-oriented engagement in naturalistic human-LLM interaction.

The analysed corpora are WildChat, LMSYS Chat-1M and ShareChat. The final analytic sample contains 128,569 conversations, 491,685 user turns and 489,785 assistant turns across six task settings: WildChat coding, WildChat writing, LMSYS Chat coding, LMSYS Chat writing, ShareChat coding and ShareChat writing.

## Sampling and Filtering

All records were selected by corpus-level processing rules rather than by participant recruitment. The filtering pipeline is documented in Supplementary Table A1.

WildChat uses refreshed task-filter outputs from the public WildChat-4.8M release. Retained conversations had at least four message turns and passed English-oriented semantic coding or writing filters.

LMSYS Chat starts from 1,000,000 public source conversations. The pipeline retained 777,453 English conversations, then 236,372 English conversations with at least four turns, then applied the same semantic task filters. The final analytic sample contains 32,114 coding and 21,023 writing conversations.

ShareChat starts from five final-language-filtered public CSV files containing 1,199,899 message rows and 129,584 platform-url conversations after local conversion. After role normalization, minimum-turn filtering, semantic task filtering and strict-English screening, the final analytic sample contains 2,481 coding and 1,539 writing conversations.

No statistical power calculation was used because the study analyses all conversations passing the documented corpus filters rather than a prospective experimental sample.

## Data Exclusions

Exclusions were based on documented corpus conversion and filtering rules: non-target-language records, conversations below the minimum-turn screen, conversations failing semantic coding/writing filters, ShareChat conversations failing the strict-English screen and records missing required downstream analytic fields. Exclusion counts and retained counts are reported in Supplementary Table A1 and provenance artifacts in Supplementary Table A2.

No exclusions were based on observed outcome direction.

## Annotation and Measurement

The unit of annotation is the conversational turn. User turns were labelled for passive, active, constructive and emotional engagement. Assistant turns were labelled for scaffolded support versus non-scaffolded reference responses, plus support-intent labels and support-form labels for scaffolded turns.

Production labels were generated using LLM-assisted annotation with parser checks, documented rule-based post-processing and human validation. Coding-oriented annotation used the V12 coding prompt. Writing-oriented annotation used the writing-topic V12 prompt. Per-conversation metadata record schema, prompt version, deployment name and API version. Supplementary Section A.3 reports model/provider, prompt, temperature, retry policy and post-processing details.

Human validation was used to quantify label reliability and identify boundary cases. Coding validation combined 658 task turns and 643 turns after deduplication. Writing validation used 210 reviewed conversations with final human labels. A separate positive-oversampled user-framing audit reviewed 450 first user turns across the six corpus-by-task settings. Agreement metrics are reported with per-label F1, Matthews correlation coefficient and Gwet's AC1.

The labels are interpreted as observable behavioural signatures, not direct measures of learning gain, prior knowledge, motivation, learner identity or durable skill development.

## Statistical Analyses

Descriptive analyses report proportions, turn-weighted ratios and conversation-level summaries within the six task settings.

Conversation-level scaffolded-support associations use turn-weighted constructive-ratio contrasts, Poisson generalized linear models for constructive-turn counts and logistic models for any constructive turn. Primary Poisson models use raw constructive-turn counts with conversation length as a covariate; offset-rate and quasi-Poisson sensitivities are reported in the Supplementary Information.

Temporal analyses use adjacent assistant-to-user and user-to-assistant turn pairs. Adjacent-turn confidence intervals use 1,000 conversation-cluster bootstrap resamples to account for multiple turn pairs within conversations.

Support-form comparisons report effect sizes with confidence intervals and Benjamini-Hochberg false-discovery-rate adjustment within each displayed six-form comparison family.

Integrated adjacent-turn regressions include user-state features, assistant-scaffolding features, adjacent-turn context and dataset or recoverable model/source fixed effects. These models are reported as robustness and decomposition analyses rather than causal estimates.

## Randomization and Blinding

Randomization is not applicable because the study is observational and uses public conversation logs. Assistant scaffolding and user engagement were observed rather than assigned.

Blinding is not applicable to experimental treatment allocation. Human validation was used to compare annotated labels against human-reviewed labels and adjudicated label boundaries; validation samples were not used as a separate source of outcome measurement in the main analyses.

## Replication and Robustness

The main descriptive and associational patterns are reported across six corpus-by-task settings rather than a single pooled corpus. Additional checks include setting-level models, pooled models with dataset fixed effects, model/source fixed-effect sensitivity where recoverable, offset-rate sensitivity for Poisson models, grouped-binomial constructive-rate sensitivity and WildChat model-snapshot robustness figures.

The study does not claim causal replication or randomized treatment effects.

## Data Availability

Raw public conversation data should be obtained from the original data providers and used under their dataset licences and terms. The manuscript does not redistribute raw message text, user identifiers or linked user histories.

Derived data sufficient to verify reported aggregate figures, tables and statistical summaries are archived on Zenodo at https://doi.org/10.5281/zenodo.20995946 and in the GitHub repository https://github.com/CinderD/Informal-learning-in-everyday-human-LLM-interaction at tag v0.1.0, commit 31e10cfea930.

The release includes numeric source data for main figures, de-identified analytic labels without raw message text, table source files, confidence intervals, p values, FDR q values, model-output summaries, provenance documentation and SHA-256 checksums.

## Code Availability

Custom code used to export source data and de-identified label tables, compute statistical analyses and generate figures and tables is archived with the derived-data release on Zenodo and in the GitHub repository listed above. The repository excludes API keys, raw message text and files that cannot be redistributed under the original corpus terms. Reproducing the full annotation pipeline from raw conversations requires user-provided API credentials and access to the raw public corpora from their original sources.

## Ethics and Privacy

The study is a secondary analysis of public naturalistic human-LLM conversation datasets. The authors did not recruit participants, intervene in conversations, contact users, or attempt to identify users. Analyses are reported at aggregate turn or conversation level. Manuscript examples are paraphrased rather than copied from raw logs.

Institution-specific ethics or IRB determination details should be entered in the journal submission system according to the authors' confirmed institutional record.

## Competing Interests

The manuscript states that H.L. and X.X. are employees of Microsoft Research Asia and that the remaining authors declare no competing interests.

## AI and LLM Use

LLMs were objects of study and were also used as annotation and writing-assistance tools. Production labels were generated with LLM-assisted workflows and checked through parser rules, documented rule-based post-processing and human validation. LLM-based tools also assisted with code drafting, debugging, workflow organization and language editing. No LLM or AI tool is listed as an author, and the authors take responsibility for the final manuscript, analyses and interpretation.

## Figure Source Data

Numeric source data for the main figures are provided in `source_data/figure2_source_data.csv`, `source_data/figure3_source_data.csv`, `source_data/figure4_source_data.csv` and `source_data/figure5_source_data.csv`. Figure 1 is a conceptual framework figure and has no numeric source data. Supplementary table and regression source files are provided in `tables/` and `outputs/integrated_regression/`.

## Items for Final Author Confirmation

Author-order-specific CRediT contributions, grant numbers, acknowledgements and the institution-specific ethics or IRB reference should be confirmed by the authors before submission. These are author metadata items rather than analysis reproducibility gaps.
