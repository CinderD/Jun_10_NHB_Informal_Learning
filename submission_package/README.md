# Submission Data Package

This package contains derived, non-raw data files sufficient to verify the manuscript's aggregate figures, tables and statistical summaries.

## Contents

- `source_data/`: numeric source data for the main figures and selected supplementary figures.
- `derived_label_tables/`: de-identified conversation-level and adjacent-turn label-only tables for the six main public-chat task settings.
- `statistical_outputs/integrated_regression/`: regression, bootstrap, confidence-interval and p-value outputs used in the manuscript and appendix.
- `statistical_outputs/support_intent/`: support-intent prevalence and contrast summaries.
- `tables/`: LaTeX table source files included in the manuscript and appendix.
- `docs/numeric_consistency_checks.csv`: automated checks comparing figure source data with statistical output files.
- `MANIFEST.csv`: file list with SHA-256 checksums.

## Scope

The package intentionally excludes raw message text, original conversation identifiers, URLs, timestamps, user identifiers, linked user histories, API keys and files from archived `previous/` folders. Raw public corpora should be obtained from their original providers under their own licences and terms.

## Notes For Submission

Figure 1 is conceptual and has no numeric source-data file. Main numeric figures are covered by `source_data/figure2_source_data.csv` through `source_data/figure5_source_data.csv`. Supplementary tables and model checks are covered by the table source files and statistical output CSVs. The label-only tables are organized by dataset and task; see `derived_label_tables/README.md` for schemas, row counts and identifier handling.
