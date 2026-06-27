# Submission Readiness Audit

Date: 2026-06-28

## Scope

This audit checks the current manuscript and derived-data package against Nature Portfolio-style submission expectations for data availability, code availability, ethics disclosure, competing interests, author contributions, figure source data and reproducibility materials.

## Current Package

- `submission_package/source_data/` contains numeric source data for the main numeric figures and selected supplementary figures.
- `submission_package/derived_label_tables/` contains de-identified conversation-level and adjacent-turn label-only tables for WildChat, LMSYS Chat and ShareChat.
- `submission_package/statistical_outputs/integrated_regression/` contains regression, bootstrap, confidence-interval, p-value and sensitivity outputs used in the manuscript and appendix.
- `submission_package/statistical_outputs/support_intent/` contains support-intent prevalence and contrast summaries.
- `submission_package/tables/` contains the LaTeX source for manuscript and appendix tables.
- `submission_package/docs/numeric_consistency_checks.csv` records automated row-level checks comparing figure source data with the corresponding statistical output files.
- `submission_package/MANIFEST.csv` records SHA-256 checksums for packaged files.
- `submission_package_20260628.zip` is a zipped copy of the package.

The package excludes raw message text, user identifiers, linked user histories, API keys and archived `previous/` folders. Raw public corpora should be obtained from their original providers under their own licences and terms.

## Automated Checks

- Active LaTeX dependency check: all active `\input`, `\include` and `\includegraphics` targets were present.
- Active citation check: all 53 active citation keys were present in `sn-bibliography.bib`.
- Active reference metadata check: active article, conference, book and chapter references had a DOI, URL or ISBN after cleanup.
- Numeric source-data check: 18/18 row-level checks passed in `numeric_consistency_checks.csv`.
- Derived label-table check: conversation counts, user-turn counts and assistant-turn counts matched Table 1 for all six main task settings.
- Derived label-table leakage scan found no raw message-text fields, original conversation identifiers, URLs, timestamps, API-key strings, internal absolute paths or archived Copilot labels.
- Figure 3 panel b source data matched `outputs/integrated_regression/fig3_adjusted_model_significance.csv`.
- Figure 3 panel c source data matched `outputs/integrated_regression/fig3_user_framing_stratified_poisson_significance.csv`.
- Figure 5 panel a source data matched `outputs/integrated_regression/key_percentage_lifts_significance.csv`.
- Active-source wording scan found no remaining active occurrences of `Copilot`, `CP coding`, `CP writing`, `direct-response`, `S1 direct`, `four matched settings`, `four dataset-by-task settings`, `matched settings`, `strictest`, `stricter level`, `stricter constructive` or `measured user status`.
- LaTeX compilation completed successfully with `latexmk -pdf -interaction=nonstopmode -halt-on-error sn-article.tex`.

## Table 1 Verification

The Table 1 total counts were rechecked from the displayed setting rows: 128,569 conversations, 491,685 user turns and 489,785 assistant turns. Weighted pooled values recomputed from rounded row displays matched the table to rounding precision for user intent, scaffolded support, cognitive engagement and constructive engagement. The emotional-engagement pooled value recomputed from rounded displayed rows is 0.75%, whereas the table reports 0.74%; this is consistent with using unrounded underlying row values rather than the rounded table display.

## Nature-Facing Materials Present

- Data availability statement: present in `sections/06-declarations.tex`.
- Code availability statement: present in `sections/06-declarations.tex`.
- Ethics statement: present in `sections/06-declarations.tex`.
- Competing interests: present in `sections/06-declarations.tex`.
- Author contributions: present, but final author initials and role allocation remain a team-level item.
- Acknowledgements and funding: present, but final funder names and grant numbers remain a team-level item.
- LLM use statement: present in `sections/06-declarations.tex`.
- Reporting summary / editorial checklist note: present in `sections/06-declarations.tex`.
- Figure source data statement: present in `sections/06-declarations.tex`.

## Remaining Manual Items Before Submission

- Mint and insert the final archival DOI/accession for the derived-data deposit.
- Mint and insert the final archival DOI/accession for the code release.
- Replace the author-contribution placeholder with final CRediT initials and roles.
- Replace the acknowledgements/funding placeholder with final funder names, grant numbers and acknowledgements.
- Insert the exact IRB/exemption identifier if the team has one; otherwise keep the secondary-analysis ethics statement and confirm it matches institutional requirements.
- Decide whether the final journal upload should use the modular Overleaf source or a flattened single `.tex` file with embedded bibliography, depending on the journal production instructions.
- Confirm whether the final source-data package should also include rendered figure PDFs/SVGs in addition to numeric source-data CSVs.

## Notes

The current submission package is a derived-data and source-data package, not a raw-data redistribution. This is intentional because the project uses public conversation corpora released by third parties and the manuscript should avoid redistributing raw message text or user-level traces.
