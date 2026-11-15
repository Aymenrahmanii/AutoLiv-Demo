---
version: 1
slug: "src-coding-buddy-web-index-html"
primary_target: "src/coding_buddy/web/index.html"
related_targets: []
---

# Surface: Coding Buddy demo UI (src/coding_buddy/web/index.html)

Mode: Operate. Screen-shared on Teams to the thesis supervisor; the candidate narrates.
Job: show the benchmark result (code only vs code + codebook) and run a live review of a pasted R script.
Constraints: synthetic data labelled as such; key stays server-side; legible through compressed video.
Choice: user delegated ("use whatever is recommended"); assigned direction taken, no decision round.

## Direction contract

THESIS: Review findings are road signs on the code. The screen refuses the generic dashboard of KPI cards and chat bubbles; a finding is a sign planted at the line it is about, read at speed.

OWN-WORLD: Swedish road-sign system. Gantry-steel shell rail (amended at finish review: a blue rail would blur the meaning of the blue Code-only sign), yellow-with-red-border warning triangles for findings, motorway green plates for confirmed hits, white plates with black border for ground truth. Overpass (highway-gothic lineage) for UI, Overpass Mono for code, model names and tallies; the monumental sign figures stay in Overpass sans because sign numerals are not monospace (amended at finish review).

STORY: The supervisor sees one comparison (errors found without vs with codebook), picks a script, sees the injected error and the model's signs on the same lines, then watches a live review land.

FIRST VIEWPORT: Gantry-steel top rail: product name, model, "synthetic data" plate, tabs Benchmark / Live review. Below: a direction-sign band with two monumental figures (code only X/6, + codebook Y/6) and false alarms. Then a two-pane work area: script list (left, 300px) with per-condition status plates; code viewer (right) with gutter signs, toggle between conditions or side-by-side.

FORM: Swedish road signage, candidate 4 of 7 (crash-test targets, NCAP body ratings, proof marks, road signage, collision diagram, AIS dictionary, journal figures). Seed key 3592056f. Signature move: a sign that misses the exact line carries a distance plate ("2 lines ↑") like a distance-ahead sign. Raises: Metro tiles (monumental figure scale), botanical folio (both conditions registered line for line at one scale), airport wayfinding (one message per sign line), Ikeda (tabular mono density for figures).

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
