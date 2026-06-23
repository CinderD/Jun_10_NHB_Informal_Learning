# Reference audit, 2026-06-24

Scope: active references cited by `sn-article.tex`, `sections/*.tex` and `tables/*.tex`.

Checks performed:
- Parsed active `\cite{...}` commands after excluding commented lines.
- Verified that all 57 active citation keys are defined in `sn-bibliography.bib`.
- Queried Crossref title matches for missing or incomplete DOI metadata.
- Queried the arXiv API for arXiv-only corpus and preprint references.
- Rebuilt the manuscript with `sn-nature.bst` and checked `sn-article.blg` for BibTeX warnings.

Main updates:
- Added formal DOI metadata for peer-reviewed or proceedings references where Crossref returned high-confidence matches, including ACM CHI/L@S/CSCW papers, PNAS, QJE, BJET, Educational Psychologist, Review of Educational Research, Studies in Continuing Education and Educational Psychology Review.
- Updated Terzimehic et al. from an arXiv preprint entry to the formal Computers and Education: Artificial Intelligence article with DOI `10.1016/j.caeai.2026.100634`.
- Added arXiv DOI metadata for arXiv-only public-corpus and preprint references: WildChat, LMSYS-Chat-1M, ShareChat, Handa et al., Tutor CoPilot, SWE-chat, ThoughtTrace and Neagu et al.
- Added stable URL metadata for Schugurensky (2000) and Baker et al. (2008), where no high-confidence DOI was found.
- Added ISBN metadata for Agresti (2013) and McCullagh & Nelder (1989), where no DOI was used.
- Protected acronyms and proper names in BibTeX titles, including AI, LLM, ChatGPT, WildChat, LMSYS-Chat-1M, ShareChat, SWE-chat, ThoughtTrace, ICAP, RCT and T4.

Remaining non-DOI entries:
- Agresti (2013), `Categorical Data Analysis`: book reference, ISBN included.
- McCullagh & Nelder (1989), `Generalized Linear Models`: book reference, ISBN included.
- Schugurensky (2000), NALL working paper: stable institutional handle included.
- Baker et al. (2008), Journal of Interactive Learning Research: stable LearnTechLib page included.

Validation outcome:
- Active citation keys: 57.
- Undefined citation keys: 0.
- Active entries without DOI, arXiv eprint, URL or ISBN: 0.
- BibTeX warnings in `sn-article.blg`: 0.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error sn-article.tex` completed successfully.

Note:
- The Springer Nature `sn-nature.bst` style does not print DOI fields for most article entries in the generated `.bbl`, but the DOI metadata is present in `sn-bibliography.bib` for submission/source-data integrity.
