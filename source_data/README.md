# Figure source data

This directory contains CSV source data for the manuscript's numeric main figures and Appendix C visual summary.

- `figure2_source_data.csv`: engagement composition, user-framing contrasts and conversation-length gradients.
- `figure3_source_data.csv`: scaffolded versus reference constructive ratios, adjusted model estimates, framing-stratified estimates and post-answer depth differences.
- `figure4_source_data.csv`: support-form constructive associations and Benjamini-Hochberg q values.
- `figure5_source_data.csv`: overall adjacent-turn probabilities with lift annotations, prior-state conditional probabilities, reverse scaffolded-support probabilities and focal prior-state x support-form odds ratios.
- `support_intent_form_profile_source_data.csv`: support-intent by support-form heatmap values and marginal bar values used in Fig. C1.
- `supplementary_support_supply_source_data.csv`: setting-level support-form supply values used to construct the Fig. C1 marginal support-form bars.
- `validation/`: human-confirmed validation metrics for user-framing, user-engagement and assistant scaffolding/support-form corpus-scale label audits. These files contain aggregate metrics and mismatch metadata, not raw conversation text.

Figure 1 is a conceptual framework figure and has no numeric source data. Supplementary table source files are stored under `tables/`, and regression/statistical output CSV files are stored under `outputs/integrated_regression/`.

Raw message text is not redistributed here. For reproduction from raw conversations, obtain the public corpora from their original releases and run the analysis code against the derived labelling pipeline outputs.
