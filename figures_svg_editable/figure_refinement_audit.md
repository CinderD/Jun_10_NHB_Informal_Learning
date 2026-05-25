# Figure refinement audit

This note records the final figure-generation pass used for the camera-ready manuscript figures. The final PDFs in `figures/` and the editable SVG counterparts in `figures_svg_editable/final_figures/` are generated from `scripts/make_camera_ready_figures.py`.

## Figure 1 focused review

1. Title hierarchy: reduced the oversized title and subtitle to avoid dominating the conceptual diagram.
2. Three-card geometry: kept the interaction ecology, turn-level labels and inference-scales cards aligned on a common baseline.
3. Card headers: separated panel letters, titles and subtitles after the first render showed header overlap.
4. Left-card exchange schematic: retained the user-to-LLM arrow but shifted the bubbles so they do not collide with the context chips.
5. Left-card context chips: grouped corpus, task setting and user framing into evenly spaced chips with consistent edges.
6. Middle-card timeline: shortened the centre node to "Assistant t / support" after the earlier "response support" label collided internally.
7. Middle-card code columns: shortened user-code descriptions to active, constructive and passive so they no longer run into the assistant-code chips.
8. Middle-card support forms: compacted the S1/S2 and M1-M6 chips into a two-column grid with stable spacing.
9. Right-card evidence modules: shortened module headings and descriptions to avoid text collisions while preserving the three evidence scales.
10. Manuscript-scale check: rendered page 3 of `sn-article.pdf` after rebuild and verified that Fig. 1 remains readable, uncropped and non-overlapping in context.

## Other figure checks

- Fig. 2: moved the passive labels in panel a outside the stacked bars in black text; shortened the panel-a title to avoid collision with panel b.
- Fig. 3: checked the support-association panels after rebuild; legend and panel labels do not obscure data.
- Fig. 4: increased bottom margin so the heatmap x labels and footnote do not overlap.
- Fig. 5: removed the vertical colorbar that crowded panel d; the heatmap values and title now carry the probability scale without label overlap.

## Verification commands

- `python scripts/make_camera_ready_figures.py`
- `latexmk -pdf -interaction=nonstopmode -halt-on-error sn-article.tex`
- `pdffonts sn-article.pdf`
