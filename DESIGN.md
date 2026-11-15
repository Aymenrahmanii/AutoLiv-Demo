---
name: Coding Buddy
description: LLM review of R crash-analysis scripts, with and without a codebook, shown as road signs on the code.
colors:
  ink: "#111518"
  ink-2: "#3c474f"
  muted: "#55616a"
  gutter-ink: "#5f6b74"
  ground: "#e9edf0"
  surface: "#ffffff"
  surface-2: "#f5f7f8"
  line: "#d2d9de"
  line-strong: "#9aa6ae"
  steel: "#1c2328"
  steel-2: "#2a333a"
  on-steel: "#f2f5f7"
  on-steel-muted: "#b9c4cb"
  sign-blue: "#0a5aa8"
  sign-blue-deep: "#084c8f"
  sign-green: "#00704a"
  sign-yellow: "#ffd100"
  sign-yellow-soft: "#fff6c7"
  sign-red: "#d2141e"
  sign-red-soft: "#fdecec"
  truth-row: "#fff9da"
  select-row: "#e3eefa"
typography:
  display:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(3.2rem, 6vw, 5.4rem)"
    fontWeight: 800
    lineHeight: 0.9
    letterSpacing: "0"
  headline:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(1.5rem, 2.4vw, 2.05rem)"
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "-0.02em"
  sign-name:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(1.25rem, 2vw, 1.7rem)"
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "1.05rem"
    fontWeight: 800
    lineHeight: 1.15
  body:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "tnum"
  label:
    fontFamily: "Overpass, Segoe UI, system-ui, sans-serif"
    fontSize: "0.8rem"
    fontWeight: 700
    lineHeight: 1
  code:
    fontFamily: "Overpass Mono, ui-monospace, Cascadia Mono, Consolas, monospace"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.75
    fontFeature: "liga 0, calt 0"
  mono-label:
    fontFamily: "Overpass Mono, ui-monospace, Cascadia Mono, Consolas, monospace"
    fontSize: "0.8rem"
    fontWeight: 600
    lineHeight: 1
    fontFeature: "liga 0, calt 0"
rounded:
  lane: "2px"
  plate: "3px"
  control: "4px"
  sign: "6px"
spacing:
  s-1: "4px"
  s-2: "8px"
  s-3: "12px"
  s-4: "16px"
  s-5: "24px"
  s-6: "32px"
  s-7: "48px"
components:
  button-primary:
    backgroundColor: "{colors.sign-blue}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "3px 18px 0"
    height: "44px"
  button-primary-hover:
    backgroundColor: "{colors.sign-blue-deep}"
  direction-sign-code-only:
    backgroundColor: "{colors.sign-blue}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sign}"
    padding: "24px 32px"
  direction-sign-codebook:
    backgroundColor: "{colors.sign-green}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sign}"
    padding: "24px 32px"
  plate-warning:
    backgroundColor: "{colors.sign-yellow}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.plate}"
    padding: "2px 9px 0"
    height: "26px"
  plate-hit:
    backgroundColor: "{colors.sign-green}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.plate}"
    padding: "2px 9px 0"
    height: "26px"
  plate-truth:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.plate}"
    padding: "2px 9px 0"
    height: "26px"
  plate-miss:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.sign-red}"
    typography: "{typography.label}"
    rounded: "{rounded.plate}"
    padding: "2px 9px 0"
    height: "26px"
  plate-quiet:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink-2}"
    typography: "{typography.label}"
    rounded: "{rounded.plate}"
    padding: "2px 9px 0"
    height: "26px"
  plate-mono:
    backgroundColor: "{colors.steel-2}"
    textColor: "{colors.on-steel}"
    typography: "{typography.mono-label}"
    rounded: "{rounded.plate}"
    padding: "2px 9px 0"
    height: "26px"
  tally-full:
    backgroundColor: "{colors.sign-green}"
    textColor: "{colors.surface}"
    rounded: "{rounded.plate}"
    width: "50px"
    height: "44px"
  tally-part:
    backgroundColor: "{colors.sign-yellow}"
    textColor: "{colors.ink}"
    rounded: "{rounded.plate}"
    width: "50px"
    height: "44px"
  segmented-selected:
    backgroundColor: "{colors.steel}"
    textColor: "{colors.on-steel}"
    rounded: "{rounded.plate}"
    padding: "3px 12px 0"
    height: "34px"
  select:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "3px 34px 0 12px"
    height: "40px"
  finding-note:
    backgroundColor: "{colors.sign-yellow-soft}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "10px 12px"
  pane:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sign}"
  rail:
    backgroundColor: "{colors.steel}"
    textColor: "{colors.on-steel}"
    height: "60px"
    padding: "0 24px"
---

# Design System: Coding Buddy

## Overview

**Creative North Star: "Road Signs on the Code"**

The system is the Swedish road-sign world applied to code review. A finding is not a card or a chat bubble; it is a yellow warning triangle with a red border, planted in the gutter at the line it is about, meant to be read at speed. The two experimental conditions are direction signs on a gantry: blue for code only, green for code plus codebook, each carrying one monumental figure. Ground truth is a white plate with a black border, the way a road sign states a fixed fact. Everything else (rail, panes, controls) is quiet steel and pale ground so the signs carry the meaning.

Density is that of a working tool viewed through a compressed screen share: a sticky 60px gantry-steel rail, a two-pane work area, tabular figures everywhere, and text that stays legible at reduced size. Colour is semantic, not decorative. Every saturated hue on screen means something specific (condition, hit, warning, miss), which is why the rail is steel rather than blue: a blue rail would blur the meaning of the blue code-only sign.

Motion is a sign panel swinging down on its hinge: warning triangles flip into place (rotateX from -80deg, 520ms, expo-out) and finding notes unroll top to bottom (clip-path, 420ms), staggered per line. All motion collapses under reduced-motion preferences.

**Key Characteristics:**
- Semantic sign palette (blue, green, yellow, red) on steel and pale grey-blue ground.
- Overpass (highway-gothic lineage) for UI and sign figures; Overpass Mono for code, model names and tallies.
- Findings live on the code line as warning triangles, never in a separate feed.
- Plates (small rounded labels, inset borders) carry every status: hit, warning, miss, truth, quiet.
- Flat bordered panes; shadow reserved for the signs, the rail and the primary button.

## Colors

A road-sign palette: four saturated sign colours with fixed meanings, set on cool steel and grey-blue neutrals.

### Primary
- **Direction Sign Blue** (sign-blue): the code-only condition. Fills the code-only direction sign and its condition plates; also the primary action button, links, focus rings, the editor caret and checkbox accent. Hover deepens to **Deep Sign Blue** (sign-blue-deep).

### Secondary
- **Motorway Green** (sign-green): the code-plus-codebook condition and every confirmed hit. Fills the codebook direction sign, "right line, right cause" plates, full-level tallies and codebook condition plates.

### Tertiary
- **Warning Yellow** (sign-yellow): the warning-triangle fill, partial results ("right line, wrong cause"), the "Synthetic data" plate, the active-tab bar, text selection and the skip link. **Warning Wash** (sign-yellow-soft) backs finding notes; **Truth Row** (truth-row) highlights the injected line.
- **Warning Border Red** (sign-red): the triangle border, misses and false alarms (white plate, red inset border), the sign count and error states. **Alarm Wash** (sign-red-soft) backs false-alarm tallies.

### Neutral
- **Gantry Steel** (steel) and **Steel Edge** (steel-2): the top rail, the selected segment of a segmented control, and the mono model plate on the rail. Text on steel is **Rail White** (on-steel), secondary text **Rail Grey** (on-steel-muted).
- **Road Ink** (ink): primary text, plate borders for ground truth, codebook table header rule.
- **Slate Ink** (ink-2) for secondary text; **Muted Slate** (muted) for meta lines and hints; **Gutter Slate** (gutter-ink) for line numbers.
- **Overcast Ground** (ground): the page background behind panes.
- **Surface White** (surface) and **Mist** (surface-2): pane fills, hover rows, quiet plates, editor gutter.
- **Hairline** (line) for pane borders and dividers; **Strong Hairline** (line-strong) for select borders, dashed empty notes and scrollbars.
- **Selected Row Blue** (select-row): the selected script in the list, paired with a 1.5px sign-blue inset.

### Named Rules
**The Sign Meaning Rule.** Blue means code only, green means codebook or a confirmed hit, yellow means warning or partial, red means miss or error. No saturated sign colour is ever used as decoration or as shell chrome.

**The Steel Shell Rule.** The application shell (rail, selected controls) is gantry steel, never a sign colour, so the signs are the only coloured objects that speak.

## Typography

**Display Font:** Overpass (with Segoe UI, system-ui, sans-serif)
**Body Font:** Overpass (with Segoe UI, system-ui, sans-serif)
**Label/Mono Font:** Overpass Mono (with ui-monospace, Cascadia Mono, Consolas, monospace)

**Character:** Overpass descends from the US highway-gothic sign face, so headings and sign figures read like signage: heavy (800), slightly tightened, numerals tabular. Overpass Mono carries everything that is typed or counted: code, script filenames, model names, tallies, categories.

### Hierarchy
- **Display** (800, clamp(3.2rem, 6vw, 5.4rem), 0.9): the monumental figure on each direction sign only, followed by a smaller "/ N" at clamp(1.4rem, 2.4vw, 2rem).
- **Headline** (800, clamp(1.5rem, 2.4vw, 2.05rem), 1.15, -0.02em): the view title (one per view); codebook page title at 1.9rem.
- **Sign name** (800, clamp(1.25rem, 2vw, 1.7rem), -0.01em): the destination line of a direction sign.
- **Title** (800, 1.05rem): pane headings; the viewer's script title drops to 600 in mono.
- **Body** (400, 16px, 1.5, tabular numerals): prose and meta; bench heads cap at 70ch, codebook prose at 72ch, notes at 78ch.
- **Label** (700, 0.8rem, line-height 1): plates and condition chips; sentence case.
- **Code** (Overpass Mono 400, 0.875rem, 1.75): code view, editor and gutter.

### Named Rules
**The Sign Numeral Rule.** Monumental sign figures stay in Overpass sans, never mono: sign numerals are not monospace.

**The Typed-As-Typed Rule.** Ligatures and contextual alternates are off for all code, mono labels and tallies, so R's `<-` reads as typed, never as an arrow.

## Layout

A sticky top rail (60px, three-column grid: brand, centred tabs, plates) over a centred main column (max 1440px, padding 32px 24px 48px). Views stack vertically with 24px gaps: a heading block, then the gantry (two equal direction signs, 16px gap), then the work area: a sticky script list (minmax(300px, 380px)) beside a fluid code viewer. The live view splits editor and findings into two equal columns. Spacing follows a 4px-based scale (4, 8, 12, 16, 24, 32, 48).

Responsive: under 1100px the brand subtitle drops, live review stacks and two-column notes stack; under 860px the tabs wrap to a second rail row, the gantry and work area go single-column and the script list stops being sticky; under 520px the model plate hides and the primary button goes full width.

## Elevation & Depth

Mostly flat. Panes are white fills with a 1px hairline border and no shadow; depth between page and pane comes from the grey-blue ground. Shadow is reserved for objects that stand up off the road: the direction signs, the rail and the primary button. Plates use inset strokes (box-shadow inset) for their borders, which is a border technique, not elevation.

### Shadow Vocabulary
- **Sign lift** (`box-shadow: 0 1px 2px rgb(17 21 24 / 0.2), 0 6px 18px -8px rgb(17 21 24 / 0.35)`): direction signs only.
- **Rail shade** (`box-shadow: 0 2px 10px rgb(17 21 24 / 0.18)`): the sticky rail over scrolling content.
- **Button press** (`box-shadow: 0 1px 2px rgb(17 21 24 / 0.25)`): primary button; it nudges down 1px on press.

### Named Rules
**The Signs Stand Up Rule.** Only signs, the rail and the primary action carry shadow. Panes, plates, notes and tallies stay flat.

## Shapes

Gently rounded rectangles, sized by role: 6px for signs and panes, 4px for controls, script rows and notes, 3px for plates and tallies, 2px for lane bars and the active-tab bar. Direction signs carry an inner white border (2px, inset 6px, 3px radius), the defining silhouette of a road sign. Status plates use inset strokes: 2px ink for ground truth and distance, 2px red for misses, 1px hairline for quiet. The warning triangle (yellow fill, red 2.4px stroke, round joins, ink exclamation) is the one icon shape, drawn as inline SVG; the favicon is the same triangle on a bordered blue sign.

## Components

### Buttons
Direct and sign-coloured.
- **Shape:** control radius (4px), min-height 44px.
- **Primary:** Direction Sign Blue fill, white 700 0.95rem text, padding 3px 18px 0, a keyboard hint (kbd on a 16% white chip) inside.
- **Hover / Focus:** hover deepens to Deep Sign Blue; press translates 1px down; focus uses the global 3px sign-blue outline with 2px offset; while running, the kbd is replaced by a spinner and the fill desaturates (#6f8eae).

### Plates
The status vocabulary. Inline-flex, 26px tall, 0.8rem 700 label, 3px radius.
- **Warning** (yellow, ink text): partial result, synthetic-data notice.
- **Hit** (green, white text): right line, right cause; "with codebook".
- **Truth** (white, 2px ink inset): the injected line and its description.
- **Miss** (white, 2px red inset, red text): false alarm.
- **Quiet** (Mist, 1px hairline inset): clean control, code only.
- **Mono** (Steel Edge, mono 600): the model name on the rail.

### Tallies
Two per script row (code only, codebook), 50 by 44px, mono figure over a small condition code. Levels: full (green), part (yellow), none (white with red inset), clean (Mist), alarm (Alarm Wash with pale red inset).

### Cards / Containers
- **Corner Style:** 6px.
- **Background:** Surface White on Overcast Ground.
- **Shadow Strategy:** none (see Elevation).
- **Border:** 1px Hairline; pane heads divided by a 1px Hairline rule.
- **Internal Padding:** 16px head (16 16 12), 8px list padding.

### Inputs / Fields
- **Select:** white fill, 1px Strong Hairline, 4px radius, 40px tall, a drawn chevron (rotated 2px border), 600 0.88rem.
- **Segmented control:** Mist track with hairline border; selected segment is Gantry Steel with Rail White text.
- **Editor:** mono textarea beside a Mist gutter; focus-within draws a 2px sign-blue inset ring; caret is sign blue.
- **Error:** hint text turns Warning Border Red at 600.

### Navigation
Tabs sit centred in the steel rail at full rail height, Rail Grey 600 text, brightening to Rail White on hover. The current tab carries a 4px Warning Yellow bar at the bottom edge (top corners 2px). Tab focus rings switch to yellow, inset 4px, to stay visible on steel.

### Direction Signs (signature)
Two equal signs on the gantry: blue for code only, green for code plus codebook. Each has the inner white border, a destination name and detail lines on the left, the monumental figure ("X / N") on the right, and a row of lane bars below: one bar per injected script, filled white to the share of runs that named the cause, with a mono two-character label.

### Warning Triangles and Finding Notes (signature)
In the code view each condition has a 30px sign column beside the line numbers (dashed divider between columns). A finding plants a warning triangle on its line, with a red count when several land there. The note below the line is a Warning Wash panel (pale yellow, 1px gold inset, 4px radius) with a condition chip, a mono category and verdict plates. The injected line itself is painted Truth Row with its number boxed in a 1.5px ink plate. Empty conditions show a dashed "no sign here" note in compare mode.

### Distance Plate (signature)
A sign that misses the exact line carries a distance plate, like a distance-ahead sign: white, 2px ink inset, mono 600, a 12px arrow SVG and "N lines". It exists in code but does not appear in the current benchmark run, because every hit lands on the exact line; treat its look as implemented but not yet seen in a rendered result.

## Do's and Don'ts

### Do:
- **Do** plant every finding on its code line as a warning triangle, with its note directly beneath.
- **Do** keep blue for code only and green for codebook or confirmed hits, everywhere (signs, plates, tallies, chips).
- **Do** state ground truth as a white plate with a 2px ink inset border.
- **Do** set code, filenames, model names and tallies in Overpass Mono with ligatures off.
- **Do** keep sign figures in Overpass sans at weight 800.
- **Do** say "synthetic data" on a yellow plate in the rail.
- **Do** respect reduced motion: animations and transitions collapse to 1ms.

### Don't:
- **Don't** colour the shell (rail, panes, controls) with a sign colour; the rail is gantry steel.
- **Don't** show findings as KPI cards, chat bubbles or a feed detached from the code.
- **Don't** put shadows on panes, plates, notes or tallies.
- **Don't** set the monumental sign figures in mono.
