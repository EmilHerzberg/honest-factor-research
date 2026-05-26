# Marketing Graphics Specifications

> Three production-ready specs in the **marketing-content-generation V2
> "Warm Technical Editorial"** prompt format. Each spec is meant to be
> handed directly to that project's AI for code-generation (Remotion /
> React / Tailwind via `src/posts/<id>/`).
>
> Specs follow the structure required by `prompts/infographic.md`:
> Block A (content+format) · Block B (layout safety map) · Block C
> (creator signature) · Block D (color role plan) · then exact text +
> visual instructions.
>
> Color tokens, font sizes, and floors come from
> `marketing-content-generation/memory/visual_identity_v2.md` and
> `mobile_first_readability.md`. Schema enums match
> `marketing-content-generation/schemas/infographic.schema.json`.

---

## Shared context (all 3 graphics)

- **Project:** honest-factor-research (https://github.com/EmilHerzberg/honest-factor-research)
- **Positioning:** "A reproducible model-audit framework for stock factor models."
- **Three-line core message** (use verbatim somewhere on at least the hero):
  - This project audits stock factor models.
  - It does not try to predict the market.
  - It asks whether a model's explanation can actually be trusted.
- **Tone:** restrained, technical, intelligent, slightly editorial. No hype.
  No emoji. No rockets. No "I just discovered…" energy.
- **Target audience:** AI/ML hiring managers, data scientists, FinTech
  founders, investor-curious technical readers. **Not** retail-trading
  influencer audience.

---

# Spec 1 — Hero Banner

**ID:** `honest_factor_hero_v1`
**Purpose:** repo README top + GitHub social preview + LinkedIn post hero
**Two variants required:**
- `1a` portrait 1080×1350 (LinkedIn feed)
- `1b` landscape 1280×640 (GitHub social preview)

## Block A — Content + format

```
Content type:           conceptual_metaphor
Primary visual format:  Title card with embedded "before/after R²" decomposition motif (compact stacked-bar metaphor)
Secondary supporting:   Eyebrow tag + 3-line headline + bottom legend strip
Reason format fits:     The project's elevator pitch IS a visual metaphor —
                        "what looks like one bar of R² is actually three
                        components stacked together". Showing that comparison
                        in the hero is the elevator pitch.
Anti-repetition note:   Not a line chart. Not a pipeline diagram (that's
                        Spec 3's job). Not a 2×2 matrix. The decomp-bar
                        metaphor only appears on the hero.
Chart used?:            no — illustrative stacked-bar metaphor, not data
Story / motion pattern: Before → System → Result (compressed to one frame)
Mobile readability:     Headline 80px source = ~29px phone. All other text
                        kept above the floors in §10b. Decomp bars 28px
                        tall = ~10px phone (legible block, but legend below
                        carries semantics).
```

## Block B-portrait — Layout safety map (1080×1350)

```
Canvas:           1080 × 1350 · portrait
Safe margins:     top 96 · right 80 · bottom 96 · left 80 · bottomReserve 96

Zones:
  - hero_top    {x:80, y:96,  w:920, h:340, purpose:"eyebrow + 3-line headline"}
  - hero_middle {x:80, y:480, w:920, h:540, purpose:"decomposition metaphor (centered)"}
  - hero_bottom {x:80, y:1060,w:920, h:194, purpose:"3-line core message + signature"}

Bounding boxes:
  - bb_eyebrow      · eyebrow      · x:80,  y:128, w:920, h:36  · P2 · textSize 26 · maxLines 1 · collisionRisk none
  - bb_headline     · headline     · x:80,  y:184, w:920, h:240 · P1 · textSize 78 · maxLines 3 · collisionRisk none
  - bb_decomp_label · annotation   · x:80,  y:500, w:920, h:36  · P2 · textSize 24 · maxLines 1 · collisionRisk none
  - bb_decomp_bar_1 · visualization· x:120, y:580, w:840, h:64  · P1 · textSize n/a · collisionRisk none
  - bb_decomp_cap_1 · annotation   · x:80,  y:660, w:920, h:32  · P3 · textSize 22 · maxLines 1 · collisionRisk none
  - bb_decomp_bar_2 · visualization· x:120, y:760, w:840, h:64  · P1 · textSize n/a · collisionRisk none
  - bb_decomp_cap_2 · annotation   · x:80,  y:840, w:920, h:32  · P3 · textSize 22 · maxLines 1 · collisionRisk none
  - bb_decomp_legnd · annotation   · x:80,  y:920, w:920, h:36  · P3 · textSize 22 · maxLines 1 · collisionRisk none
  - bb_three_line   · takeaway     · x:80,  y:1060,w:760, h:120 · P1 · textSize 28 · maxLines 3 · collisionRisk none
  - bb_signature    · signature    · x:840, y:1180,w:160, h:80  · P3 · textSize 18 · maxLines 2 · collisionRisk none

Collision risks:
  - staticOverlapRisk:        none
  - finalFrameOverlapRisk:    none
  - mobileReadabilityRisk:    low (headline must wrap to 3 lines for "stock factor models" to fit)

Mitigation plan:           If the 3-line headline wraps differently at
                           render time, drop fontSize to 72 and re-flow.
                           Never shrink below 68. If still too tight,
                           break headline into 4 lines and reduce eyebrow
                           top-margin by 16px.
Auto-simplification applied: none needed
Safe to render?:           yes
```

## Block B-landscape — Layout safety map (1280×640, GitHub variant)

```
Canvas:           1280 × 640 · landscape
Safe margins:     top 64 · right 80 · bottom 64 · left 80 · bottomReserve 0
                  (GitHub social preview has no chrome reserve)

Zones:
  - left_col   {x:80,  y:64,  w:660, h:512, purpose:"eyebrow + headline + 3-line message + signature"}
  - right_col  {x:780, y:64,  w:420, h:512, purpose:"compact decomposition metaphor"}

Bounding boxes:
  - bb_eyebrow      · eyebrow      · x:80,  y:96,  w:660, h:36  · P2 · textSize 24 · maxLines 1 · collisionRisk none
  - bb_headline     · headline     · x:80,  y:152, w:660, h:200 · P1 · textSize 68 · maxLines 3 · collisionRisk none
  - bb_three_line   · takeaway     · x:80,  y:404, w:660, h:120 · P1 · textSize 22 · maxLines 3 · collisionRisk none
  - bb_url          · annotation   · x:80,  y:548, w:480, h:28  · P3 · textSize 16 · maxLines 1 · collisionRisk none
  - bb_decomp_lbl   · annotation   · x:780, y:120, w:420, h:32  · P2 · textSize 20 · maxLines 1 · collisionRisk none
  - bb_decomp_bar_1 · visualization· x:780, y:180, w:420, h:48  · P1 · collisionRisk none
  - bb_decomp_cap_1 · annotation   · x:780, y:240, w:420, h:28  · P3 · textSize 18 · maxLines 1 · collisionRisk none
  - bb_decomp_bar_2 · visualization· x:780, y:300, w:420, h:48  · P1 · collisionRisk none
  - bb_decomp_cap_2 · annotation   · x:780, y:360, w:420, h:28  · P3 · textSize 18 · maxLines 1 · collisionRisk none
  - bb_legend       · annotation   · x:780, y:440, w:420, h:32  · P3 · textSize 18 · maxLines 1 · collisionRisk none
  - bb_signature    · signature    · x:1100,y:548, w:160, h:48  · P3 · textSize 16 · maxLines 2 · collisionRisk none

Collision risks:           none
Safe to render?:           yes
```

## Block C — Creator signature

```
Variant:                compact
Placement:              bottomRight
Bounding box:            (portrait) x:840 y:1180 w:160 h:80
                         (landscape) x:1100 y:548 w:160 h:48
Show email:              no
Entrance timing:         0.6s–1.2s (only relevant if animated; still: render visible)
Idle motion:             slow-pulse (only if motion variant rendered)
Final-frame emphasis:    yes
Collision check:         overlapsContent: no · insideSafeMargins: yes ·
                         mobileReadable: yes · finalFrameVisible: yes ·
                         safeToRender: yes
```

## Block D — Color Role Plan

```
Primary system accent:    systemCyan #59D8E6
  · means:                "DIRECT explanation — the part of R² we can
                          honestly defend"
  · appears at:           green block of the decomp bar (left-most segment),
                          eyebrow tag accent underline
Warm contrast accent:     insightAmber #E7A95A
  · means:                "DERIVED / sector-mirror — the part of R² that
                          might be artifact"
  · appears at:           orange-amber middle-right block of the decomp bar,
                          the word 'audited' in the headline (if optical-
                          weighted highlight desired)
Differentiator accent:    strategicViolet #8E7CC3
  · means:                "STATISTICAL component — academic style factors,
                          medium-trust middle layer"
  · appears at:           violet block of the decomp bar (second segment from left)
Distribution:             ~72% neutral · 10% primary · 7% warm · 4% differentiator
                          (decomp bars are bounded so accent coverage stays low)
Mobile contrast check:    primary ✓ · warm ✓ · differentiator ✓ (all visible
                          against bgWarmGraphite at phone scale)
Anti-monochrome check:    ✓ (three accents semantically distinct)
```

> **Note on signalMint:** for the hero we intentionally use `successMint
> #6ED3A3` as the green for DIRECT instead of `systemCyan`, because the
> "trust tier" mental model reads more naturally as green=safe. If your
> design system requires cyan as the primary, swap: cyan → DIRECT, mint
> dropped, and place amber/violet as before. Either palette is acceptable
> as long as the four-segment decomp uses **distinct hues**.

## Text content (verbatim)

```
Eyebrow:    HONEST FACTOR RESEARCH · MODEL-AUDIT FRAMEWORK
Headline:   Most stock factor
            models look smarter
            than they really are.
Three-line: This project audits stock factor models.
            It does not try to predict the market.
            It asks whether a model's explanation can actually be trusted.
URL:        github.com/EmilHerzberg/honest-factor-research
Decomp lbl: What "R² = 0.66" actually contains
Cap 1:      standard view  →  looks like 66 % explained
Cap 2:      honest decomposition  →  only ~17 % really direct, ~33 % may be sector-mirror
Legend:     ■ DIRECT     ■ STATISTICAL     ■ DERIVED     ■ unexplained
```

## Visual instructions

- **Background:** `bgWarmGraphite #151A22` with subtle 1.5px grid overlay
  at 4% opacity. Optional warm corner-glow `glowCopper` top-right
  (radius 320px, opacity 0.16, very subtle).
- **Decomp bar metaphor:** two horizontal stacked bars, vertically stacked.
  Bar height ≥48px (landscape) / 64px (portrait). Subtle 1px rounded
  rectangle stroke at `rgba(244,241,234,0.08)`.
  - Bar 1 ("standard"): single block, `systemCyan` for 66% width + `textTaupe @ 22% opacity` for the remaining 34%.
  - Bar 2 ("honest"): four segments in order — green 17% · violet 16% · amber 33% · grey 34%.
- **Number positions:** decomp percentages (17% / 16% / 33% / 34%) match
  the empirical DUK 2024-06-28 result. **Round, not invented.**
- **Headline word-break (portrait):** break after "factor" and "models" —
  3 lines balanced. If the rendering engine auto-breaks differently,
  manual `<br>` is acceptable.
- **No icons in hero.** Symbolic load is in the decomp metaphor itself.
- **Signature variant compact:** "EH" monogram in a 36×36 rounded-square
  panel + "AI Systems · Automation · Design" 2-line at 14px.

## Motion brief (if a video variant is needed)

- **Beat 1 (0.0–1.2s, Hook):** eyebrow + headline fade in line-by-line
  with 200ms stagger. Decomp metaphor stays hidden.
- **Beat 2 (1.2–2.5s, Orientation):** "standard" bar (Bar 1) draws left-
  to-right with `easeOutCubic`, 700ms. Caption fades in at 2.2s.
- **Beat 3 (2.5–4.5s, Mechanism — the main motion event):** "honest"
  bar (Bar 2) is built segment-by-segment, 350ms each, `easeOutQuart`.
  After all four segments are placed, a focus lock holds for 1500ms with
  Bar 1 dimmed to 35% opacity to draw the eye to Bar 2.
- **Beat 4 (4.5–6.5s, Insight):** three-line message types/fades in
  line-by-line. Word "audit" gets a subtle amber underline 200ms after
  line-1 settles.
- **Beat 5 (6.5–8.0s, Memory Anchor):** final frame holds. Signature
  pulses once at 0.4 opacity.
- **Total duration:** 8s. Final frame must be thumbnail-suitable
  (everything in place, no mid-transitions).
- **Camera:** static.

---

# Spec 2 — Trust Decomposition (Myth vs Reality)

**ID:** `honest_factor_trust_decomp_v1`
**Purpose:** README "Visual example" section + LinkedIn carousel slide
**Format:** portrait 1080×1350 (LinkedIn primary; same image is reused as
the 1200×600 README embed)

## Block A — Content + format

```
Content type:           myth_vs_reality
Primary visual format:  Side-by-side comparison (two stacked panels in portrait
                        layout) — "Traditional R²" vs "Honest Decomposition"
Secondary supporting:   Annotation callout with arrow pointing to the mirror-
                        suspect segment + asset/date stamp
Reason format fits:     The whole methodology IS a before/after — "what the
                        standard view shows" vs "what an honest decomposition
                        shows for the same asset". Side-by-side is the
                        cleanest format for that comparison.
Anti-repetition note:   Not a line chart (no time series). Not a pipeline
                        (Spec 3). Not a 2×2 matrix.
Chart used?:            no — bar comparison is illustrative of methodology,
                        not a data trend
Story / motion pattern: Before → Bottleneck → After  (where "bottleneck" is
                        the unseen sector-mirror artifact)
Mobile readability:     Headline 64px = ~23px phone. R² values displayed at
                        56px = ~20px phone (well above floor). Bar segment
                        captions at 22px = ~8px floor.
```

## Block B — Layout safety map (1080×1350)

```
Canvas:           1080 × 1350 · portrait
Safe margins:     top 88 · right 80 · bottom 96 · left 80 · bottomReserve 88

Zones:
  - title_zone    {x:80, y:88,  w:920, h:160, purpose:"headline + asset stamp"}
  - panel_top     {x:80, y:280, w:920, h:380, purpose:"Traditional R² panel"}
  - panel_bottom  {x:80, y:700, w:920, h:380, purpose:"Honest decomposition panel"}
  - takeaway_zone {x:80, y:1120,w:920, h:142, purpose:"final takeaway + signature"}

Bounding boxes:
  - bb_headline     · headline     · x:80,  y:96,  w:920, h:104 · P1 · textSize 60 · maxLines 2 · collisionRisk none
  - bb_asset_stamp  · subtitle     · x:80,  y:212, w:920, h:36  · P3 · textSize 22 · maxLines 1 · collisionRisk none

  - bb_panel_top_bg · decoration   · x:80,  y:280, w:920, h:380 · P3 · collisionRisk none
  - bb_panel_top_h  · annotation   · x:120, y:316, w:840, h:36  · P2 · textSize 26 · maxLines 1 · collisionRisk none
  - bb_panel_top_sub· annotation   · x:120, y:360, w:840, h:28  · P3 · textSize 20 · maxLines 1 · collisionRisk none
  - bb_trad_bar     · visualization· x:160, y:436, w:760, h:88  · P1 · collisionRisk none
  - bb_trad_label   · annotation   · x:160, y:548, w:760, h:36  · P2 · textSize 30 · maxLines 1 · collisionRisk none
  - bb_trad_quote   · annotation   · x:120, y:600, w:840, h:48  · P3 · textSize 22 · maxLines 2 · collisionRisk none

  - bb_panel_bot_bg · decoration   · x:80,  y:700, w:920, h:380 · P3 · collisionRisk none
  - bb_panel_bot_h  · annotation   · x:120, y:736, w:840, h:36  · P2 · textSize 26 · maxLines 1 · collisionRisk none
  - bb_panel_bot_sub· annotation   · x:120, y:780, w:840, h:28  · P3 · textSize 20 · maxLines 1 · collisionRisk none
  - bb_honest_bar   · visualization· x:160, y:856, w:760, h:88  · P1 · collisionRisk none
  - bb_segment_labs · annotation   · x:120, y:960, w:840, h:40  · P2 · textSize 22 · maxLines 1 · collisionRisk none
  - bb_arrow_warn   · callout      · x:540, y:1004,w:420, h:72  · P2 · textSize 20 · maxLines 3 · collisionRisk medium

  - bb_takeaway     · takeaway     · x:80,  y:1136,w:760, h:120 · P1 · textSize 28 · maxLines 3 · collisionRisk none
  - bb_signature    · signature    · x:840, y:1180,w:160, h:80  · P3 · textSize 18 · maxLines 2 · collisionRisk none

Collision risks:
  - staticOverlapRisk:        none
  - finalFrameOverlapRisk:    low (callout arrow vector must terminate above the takeaway zone — see mitigation)
  - mobileReadabilityRisk:    none

Mitigation plan:           Callout arrow originates at (740,1040) and points
                           UP to the amber segment of bb_honest_bar at
                           (740,944). It must NOT cross into bb_takeaway.
                           If layout drift makes the arrow cross the takeaway
                           zone, shorten callout text to one line and move
                           the callout up by 16px.
Auto-simplification applied: none needed
Safe to render?:           yes
```

## Block C — Creator signature

```
Variant:                compact
Placement:              bottomRight
Bounding box:           x:840 y:1180 w:160 h:80
Show email:             no
Entrance timing:        n/a (still)
Idle motion:            none
Final-frame emphasis:   n/a (still)
Collision check:         overlapsContent: no · insideSafeMargins: yes ·
                         mobileReadable: yes · finalFrameVisible: yes ·
                         safeToRender: yes
```

## Block D — Color Role Plan

```
Primary system accent:    systemCyan #59D8E6
  · means:                "the standard view's R² — looks comprehensive
                          but is undecomposed"
  · appears at:           bb_trad_bar (single cyan block representing 0.658)
Warm contrast accent:     frictionOrange #D9864D  (NOT insightAmber — this
                          IS a friction/risk story, not a positive insight)
  · means:                "DERIVED / sector-mirror — the part of R² that
                          could be artifact"
  · appears at:           the third segment of bb_honest_bar (0.325 portion),
                          bb_arrow_warn text + arrow stroke
Differentiator accent:    strategicViolet #8E7CC3
  · means:                "STATISTICAL — academic style factors, the medium-
                          trust contribution"
  · appears at:           second segment of bb_honest_bar (0.160 portion)
Distribution:             ~73% neutral · 9% primary · 6% warm · 4% differentiator
Mobile contrast check:    primary ✓ · warm ✓ · differentiator ✓
Anti-monochrome check:    ✓ (cyan + orange + violet on the same frame)
```

> **Use `successMint #6ED3A3`** for the FIRST segment of bb_honest_bar
> (the 0.173 DIRECT portion). This is the fourth visible color but it's
> a state color not an "accent" — it signals "this is the trustworthy
> part". `textTaupe @ 22% opacity` for the unexplained (0.342) segment.

## Data (real, verified)

All numbers from running `examples/03_explain_single_stock.py --ticker DUK
--window-end 2024-06-28` against the bundled snapshot:

```
Asset:           DUK (Duke Energy)
Window-end:      2024-06-28 (252-day rolling window)
Standard R²:     0.658
Honest decomposition:
  DIRECT          0.173  →  ~17 % of total variance, mint segment
  + STATISTICAL  +0.160  →  ~16 %, violet segment
  + DERIVED      +0.325  →  ~33 %, orange segment — MIRROR-SUSPECT
  unexplained     0.342  →  ~34 %, grey segment
Derived share:   49.4 % of explained R² comes from sector-baskets
                 (DUK is a constituent of XLU, the Utilities Sector ETF)
```

## Text content (verbatim)

```
Headline:        When R² hides where
                 the explanation comes from.
Asset stamp:     DUK (Duke Energy) · window ending 2024-06-28

Panel top header:    Traditional R²
Panel top sub:       What you usually see
Trad bar label:      R² = 0.658  (rendered inside the bar, centered)
Trad quote:          "DUK looks 66 % explained.
                     Probably a high-quality fit."

Panel bottom header: Honest decomposition
Panel bottom sub:    How much can we honestly defend?
Segment labels:      DIRECT 0.173  ·  + STAT +0.160  ·  + DERIVED +0.325  ·  noise 0.342
                     (labels sit BELOW the bar, each centered under its segment)

Callout (with arrow up to orange segment):
                     49 % of explained R²
                     comes from sector-baskets
                     (DUK is in XLU)

Takeaway:        Same asset. Same data.
                 Half the apparent R² may be the model
                 explaining DUK with a basket that contains DUK.
```

## Visual instructions

- **Panel backgrounds:** `panelSoft #202735` with 1px stroke at
  `rgba(244,241,234,0.06)`, 16px corner radius. Each panel has
  `glowCopper` very subtle at top-right corner (radius 240, opacity 0.10).
- **Bar geometry:** 88px tall, 16px corner radius. Stroke 1px at
  `rgba(244,241,234,0.08)`. Each segment in the honest-decomp bar gets
  the same corner-radius treatment only on the outermost segments
  (first segment left-rounded; last segment right-rounded).
- **R² = 0.658 label** centered in the cyan portion of bb_trad_bar.
  `textWarmWhite` semibold 40px. The "0.342" number sits centered in the
  grey portion at `textWarmWhite` 24px regular.
- **Segment labels** below the honest-decomp bar are 22px mono, color-
  matched to their segment (mint label below mint segment, etc.) — gives
  the legend without a separate legend strip.
- **Callout** is a small `panelSoft` rounded-rect (16px radius) with the
  arrow drawn as a 2.5px stroke in `frictionOrange`. Arrow terminates
  in a 12px filled triangle.
- **Background:** `bgWarmGraphite #151A22` with 1.5px grid at 4% opacity
  + warm corner-glow top-right.

## Motion brief (if video)

8-second version:
- **Beat 1 (0–1.2s):** headline + asset stamp fade in. Panels (empty)
  fade in at 30% opacity.
- **Beat 2 (1.2–2.4s):** top panel "Traditional R²" fills — trad bar
  draws left-to-right (700ms easeOutCubic); R² number counts up 0 → 0.658.
- **Beat 3 (2.4–5.4s, MAIN EVENT):** bottom panel "Honest decomposition"
  segments place in sequentially — mint (400ms), violet (350ms), orange
  (450ms with subtle highlight pulse), grey (300ms). Segment labels fade
  in 200ms after each segment lands.
- **Beat 4 (5.4–6.8s):** callout arrow draws from below up to the orange
  segment (easeOutQuart 600ms), callout text fades in. Focus lock on
  bottom panel for 1.2s (top panel dims to 50%).
- **Beat 5 (6.8–8.0s):** takeaway fades in line by line. Signature
  visible. Final frame holds — all elements clean, no mid-transitions.

---

# Spec 3 — Pipeline Architecture

**ID:** `honest_factor_pipeline_v1`
**Purpose:** README "Architecture" section + portfolio carousel slide
**Format:** portrait 1080×1350 (LinkedIn)

## Block A — Content + format

```
Content type:           architecture_system_design
Primary visual format:  Top-down pipeline with a three-way branch (single
                        input → linear chain → 1-to-3 fan-out → re-converge)
Secondary supporting:   Short caption strip + per-stage one-liner labels
Reason format fits:     The pipeline literally is a top-down dataflow:
                        market data enters at the top, residualized factor
                        matrix is built, then three parallel diagnostics
                        consume the same matrix. Top-down respects
                        gravity-of-causality and fits a portrait canvas.
Anti-repetition note:   Not a chart. Not a metaphor. Not a comparison.
                        This is the architectural diagram counterpart to
                        Spec 1 (metaphor) and Spec 2 (myth/reality).
Chart used?:            no
Story / motion pattern: Input → Agent → Decision → Action  (variant:
                        Input → Transform → Multi-Output → Reports)
Mobile readability:     All node labels 30px source (~11px phone) with
                        24px supporting line. No node has more than 2
                        labeled lines. Arrows 5px source stroke (~2px phone).
```

## Block B — Layout safety map (1080×1350)

```
Canvas:           1080 × 1350 · portrait
Safe margins:     top 88 · right 80 · bottom 96 · left 80 · bottomReserve 88

Zones:
  - title_zone   {x:80, y:88,  w:920, h:140, purpose:"eyebrow + headline"}
  - pipe_top     {x:80, y:264, w:920, h:380, purpose:"linear chain (4 nodes vertical)"}
  - pipe_branch  {x:80, y:670, w:920, h:380, purpose:"fan-out to 3 diagnostic nodes"}
  - pipe_merge   {x:80, y:1076,w:920, h:140, purpose:"reports/CSVs convergence node"}
  - footer_zone  {x:80, y:1232,w:920, h:30,  purpose:"caption strip"}

Bounding boxes:
  - bb_eyebrow      · eyebrow      · x:80,  y:96,  w:920, h:36  · P2 · textSize 26 · maxLines 1 · collisionRisk none
  - bb_headline     · headline     · x:80,  y:148, w:920, h:80  · P1 · textSize 56 · maxLines 2 · collisionRisk none

  Linear chain (4 nodes, vertical stack 80px gaps):
  - bb_node_data    · visualization· x:340, y:268, w:400, h:84  · P1 · textSize 28 · collisionRisk none
  - bb_arrow_1      · decoration   · x:530, y:360, w:20,  h:40  · P3 · collisionRisk none
  - bb_node_returns · visualization· x:340, y:408, w:400, h:84  · P1 · textSize 28 · collisionRisk none
  - bb_arrow_2      · decoration   · x:530, y:500, w:20,  h:40  · P3 · collisionRisk none
  - bb_node_catalog · visualization· x:340, y:548, w:400, h:84  · P1 · textSize 28 · collisionRisk none
  - bb_arrow_3      · decoration   · x:530, y:640, w:20,  h:40  · P3 · collisionRisk none

  HUB node (the convergence point, given accent treatment):
  - bb_node_ridge   · visualization· x:300, y:688, w:480, h:96  · P1 · textSize 30 · collisionRisk none

  Fan-out to 3 diagnostic nodes (horizontal row below hub):
  - bb_branch_arrows· decoration   · x:200, y:792, w:680, h:80  · P3 · collisionRisk none
  - bb_node_trust   · visualization· x:80,  y:880, w:280, h:140 · P1 · textSize 24 · maxLines 3 · collisionRisk none
  - bb_node_ci      · visualization· x:400, y:880, w:280, h:140 · P1 · textSize 24 · maxLines 3 · collisionRisk none
  - bb_node_regime  · visualization· x:720, y:880, w:280, h:140 · P1 · textSize 24 · maxLines 3 · collisionRisk none

  Re-merge into reports node:
  - bb_merge_arrows · decoration   · x:200, y:1024, w:680, h:60 · P3 · collisionRisk none
  - bb_node_reports · visualization· x:380, y:1088, w:320, h:84 · P1 · textSize 28 · collisionRisk none

  Footer + signature:
  - bb_caption      · annotation   · x:80, y:1196, w:760, h:36  · P3 · textSize 20 · maxLines 1 · collisionRisk none
  - bb_signature    · signature    · x:840,y:1180, w:160, h:80  · P3 · textSize 18 · maxLines 2 · collisionRisk none

Collision risks:
  - staticOverlapRisk:         none
  - finalFrameOverlapRisk:     low (branch-arrows must NOT cross into the
                               diagnostic-node text zones — they curve from
                               the hub down to each node's TOP edge only)
  - mobileReadabilityRisk:     low (3-column diagnostic row is dense; each
                               node has 280px width which gives ~95px after
                               2.77x downscale — fine for 3-line labels)

Mitigation plan:           Branch arrows use a smooth S-curve (not straight
                           diagonals) so they enter each diagnostic node
                           from the top-center. No labels on the arrows
                           themselves — keeps text density inside the nodes.
Auto-simplification applied: none needed
Safe to render?:           yes
```

## Block C — Creator signature

```
Variant:                compact
Placement:              bottomRight
Bounding box:           x:840 y:1180 w:160 h:80
Show email:             no
Entrance timing:        n/a (still)
Idle motion:            none
Final-frame emphasis:   n/a (still)
Collision check:         all yes · safeToRender: yes
```

## Block D — Color Role Plan

```
Primary system accent:    systemCyan #59D8E6
  · means:                "active data flow — the residualized factor
                          matrix is the central artifact that all three
                          diagnostics consume"
  · appears at:           bb_node_ridge (filled cyan background, the hub),
                          all arrows between linear-chain nodes (stroke)
Warm contrast accent:     insightAmber #E7A95A
  · means:                "the diagnostic outputs — what makes this
                          pipeline distinctive (trust-stratification,
                          uncertainty, regime-awareness)"
  · appears at:           bb_node_trust accent border (1px amber top-stroke
                          + amber icon dot), bb_node_ci accent border,
                          bb_node_regime accent border
Differentiator accent:    strategicViolet #8E7CC3
  · means:                "the convergence — reports as the strategic
                          deliverable that ties all three outputs together"
  · appears at:           bb_node_reports filled background (panelSoft +
                          violet accent stroke at top, violet icon)
Distribution:             ~78% neutral · 9% primary · 7% warm · 4% differentiator
Mobile contrast check:    primary ✓ · warm ✓ · differentiator ✓
Anti-monochrome check:    ✓
```

## Pipeline content (verbatim node text)

```
Eyebrow:       PIPELINE ARCHITECTURE · END-TO-END
Headline:      One residualized factor matrix
               feeds three parallel diagnostics.

Linear chain (top-down, all P1):
  Node 1:  MARKET DATA
           yfinance + NASDAQ screener
  Node 2:  LOG RETURNS
           wide DataFrame
  Node 3:  FACTOR CATALOG
           28 factors · YAML

Hub (accent-treated):
  Node 4:  ROLLING RidgeCV
           252-day windows

Fan-out (3 diagnostic outputs):
  Node 5:  TRUST-STRATIFIED R²
           DIRECT / STAT / DERIVED
           decomposition
  Node 6:  BLOCK-BOOTSTRAP CI
           Politis-Romano stationary
           non-parametric uncertainty
  Node 7:  REGIME BETAS
           VIX-stratified beta refit
           low-VIX / high-VIX

Re-merge:
  Node 8:  REPORTS + CSVs
           reproducible outputs

Caption:    Same residualized factor matrix · three parallel diagnostics ·
            one reproducible report set.
```

## Visual instructions

- **Node style:** all nodes are 16px-rounded panels in `panelSoft #202735`
  with a 1px stroke at `rgba(244,241,234,0.10)`. Node header in
  `textWarmWhite` semibold; supporting line in `textMutedStone` regular.
- **Accent treatment per node type:**
  - Linear-chain nodes (1, 2, 3): neutral panel, no accent. Just structure.
  - Hub node (4 "Rolling RidgeCV"): **cyan-filled panel**
    (`rgba(89,216,230,0.18)` background + 1.5px cyan stroke) — this is the
    visual center of gravity. Header text in `textWarmWhite` semibold 30px.
  - Diagnostic nodes (5, 6, 7): neutral `panelSoft` background but with a
    **3px amber top-border** (acts as a tab-style accent strip). Each gets
    a small lucide icon in the top-left of the panel: `Layers` for
    trust-stratified, `Activity` for bootstrap CI, `Gauge` for regime
    betas. Icon stroke 1.75px, color `insightAmber`.
  - Re-merge node (8 "Reports + CSVs"): **3px violet top-border** with a
    `FileText` lucide icon. Different from the diagnostic nodes (different
    accent) so it reads as a different stage type.
- **Arrows in the linear chain:** straight vertical lines (2.5px stroke,
  `accentCyan @ 60% opacity`) ending in 10px filled triangles.
- **Branch arrows (hub → 3 diagnostics):** smooth S-curve paths (Bezier),
  2.5px stroke, `textMutedStone @ 50% opacity`. They originate from the
  bottom-center of the hub and terminate at the top-center of each
  diagnostic. **No labels.**
- **Merge arrows (3 diagnostics → reports):** same style as branch but in
  reverse, terminating at the top-center of the reports node.
- **Background:** `bgWarmGraphite #151A22` with 1.5px grid overlay at 4%
  opacity. Optional cyan corner-glow at the position of the hub node
  (radius 280, opacity 0.10) for a subtle "system online" feel.
- **No icons in linear-chain nodes.** Icons only at the diagnostic + reports
  layer (where they help readers parse 3 similar-looking nodes faster).
- **Caption strip** in `textTaupe` regular 20px, full-width centered. Use
  middle-dot separators (`·`).

## Motion brief (if video)

10-second version (5-beat attention choreography):

- **Beat 1 (0–1.5s, Hook):** eyebrow + headline fade in. Background grid
  drifts 2px slowly (`easeInOutSine`). Camera 1.00 → 1.02 subtle zoom.
- **Beat 2 (1.5–4.0s, Orientation):** linear-chain nodes appear top-down
  with 350ms stagger (`easeOutQuart`). Each arrow draws after its source
  node settles. After node 3 lands, hub node appears with a 700ms scale
  pop-in from 0.85 to 1.00 (`easeOutQuart`) — this is the visual anchor.
- **Beat 3 (4.0–6.5s, MAIN EVENT — Mechanism):** **focus lock on hub**
  (700ms hold at 100%, everything else dims to 50%). Then the three
  branch arrows draw simultaneously (easeOutCubic 600ms), and the three
  diagnostic nodes appear together — each with a 200ms stagger so they
  don't feel mechanical (trust first, then CI, then regime).
- **Beat 4 (6.5–8.5s, Insight):** merge arrows draw, reports node appears
  with a violet pulse to signal "the output". Caption strip fades in.
- **Beat 5 (8.5–10.0s, Memory Anchor):** all nodes at full opacity. Hub
  has a single slow cyan pulse (0.8 → 1.0 → 0.8 over 1.2s, easeInOutSine).
  Signature visible. Final frame clean.

- **Camera:** static after the initial 1.00 → 1.02 settle. No further moves.
- **Total duration:** 10s. Final frame thumbnail-suitable.

---

# Optional Spec 4 — LinkedIn carousel hook

If the user runs a 5-slide carousel, slides 1-3 should be:

1. **Spec 1 (hero)** — what is honest factor research
2. **Spec 2 (myth-vs-reality)** — the DUK example
3. **Spec 3 (pipeline)** — how it works

Slides 4-5 would be auxiliary single-finding slides — leave for separate
specs once the first three exist.

---

# Schema-conformant JSON skeletons

Each spec above can be serialized into the `infographic.schema.json` format
the marketing-content-generation system requires. Below are minimal stubs
with the schema-required fields populated; the implementing AI should fill
the `visualization.data` blocks and any remaining required nested fields
from the specs above.

```json
{
  "id": "honest_factor_hero_v1_portrait",
  "designSystemVersion": "v2-warm-technical-editorial",
  "visualArsenalVersion": "v1-content-type-based-visual-formats",
  "layoutCollisionProtectionVersion": "v1-no-overlap-system",
  "creatorIdentityMarkVersion": "v1-animated-signature-system",
  "colorStrategyVersion": "v1-multi-accent-semantic-color-system",
  "format": "portrait",
  "canvas": { "width": 1080, "height": 1350, "format": "portrait" },
  "contentType": "conceptual_metaphor",
  "primaryVisualFormat": "Title card with embedded R² decomposition metaphor",
  "formatSelectionReason": "The project's elevator pitch IS a visual metaphor — what looks like one bar of R² is actually three components stacked together. Showing that comparison in the hero IS the pitch.",
  "visualDiversityTags": ["conceptual", "comparison", "non_chart"],
  "headline": "Most stock factor models look smarter than they really are.",
  "eyebrow": "HONEST FACTOR RESEARCH · MODEL-AUDIT FRAMEWORK",
  "takeaway": "This project audits stock factor models. It does not try to predict the market. It asks whether a model's explanation can actually be trusted.",
  "visualization": { "kind": "stack" }
}

{
  "id": "honest_factor_trust_decomp_v1",
  "designSystemVersion": "v2-warm-technical-editorial",
  "visualArsenalVersion": "v1-content-type-based-visual-formats",
  "layoutCollisionProtectionVersion": "v1-no-overlap-system",
  "creatorIdentityMarkVersion": "v1-animated-signature-system",
  "colorStrategyVersion": "v1-multi-accent-semantic-color-system",
  "format": "portrait",
  "canvas": { "width": 1080, "height": 1350, "format": "portrait" },
  "contentType": "myth_vs_reality",
  "primaryVisualFormat": "Side-by-side stacked-bar comparison (Traditional R² vs Honest decomposition)",
  "formatSelectionReason": "The methodology IS a before/after — what the standard view shows vs what an honest decomposition shows for the same asset. Side-by-side is the cleanest format for that.",
  "visualDiversityTags": ["comparison", "conceptual", "non_chart"],
  "headline": "When R² hides where the explanation comes from.",
  "takeaway": "Same asset. Same data. Half the apparent R² may be the model explaining DUK with a basket that contains DUK.",
  "visualization": { "kind": "comparison" }
}

{
  "id": "honest_factor_pipeline_v1",
  "designSystemVersion": "v2-warm-technical-editorial",
  "visualArsenalVersion": "v1-content-type-based-visual-formats",
  "layoutCollisionProtectionVersion": "v1-no-overlap-system",
  "creatorIdentityMarkVersion": "v1-animated-signature-system",
  "colorStrategyVersion": "v1-multi-accent-semantic-color-system",
  "format": "portrait",
  "canvas": { "width": 1080, "height": 1350, "format": "portrait" },
  "contentType": "architecture_system_design",
  "primaryVisualFormat": "Top-down pipeline with 1→3 fan-out and re-converge",
  "formatSelectionReason": "Top-down dataflow respects gravity-of-causality and fits portrait. The single-matrix-to-three-diagnostics structure is the system's distinctive architectural choice.",
  "visualDiversityTags": ["architecture", "data_flow", "non_chart"],
  "headline": "One residualized factor matrix feeds three parallel diagnostics.",
  "takeaway": "Same residualized factor matrix · three parallel diagnostics · one reproducible report set.",
  "visualization": { "kind": "pipeline" }
}
```

The implementing AI fills in `boundingBoxes`, `safeMargins`, `layoutZones`,
`collisionCheck`, `finalFrameCheck`, `creatorSignature`, `colorRolePlan`,
and `qualityChecklist` from the corresponding Block B / C / D sections
above.

---

# How to use these specs

1. Copy this whole document to the marketing-content-generation project.
2. For each spec, hand its Block A / B / C / D / Text / Visual section to
   the prompt at `prompts/infographic.md` (or `prompts/motion_graphic.md`
   for the video variant).
3. The implementing AI generates a `src/posts/<spec-id>/` folder with
   the Remotion composition + still export.
4. Run `npm run remotion:render <id> out/<id>.mp4` (motion) or render the
   still to `out/<id>.png` for the static variant.
5. Output ends up under `out/<id>.{png,mp4}` and is ready for LinkedIn /
   the honest-factor-research repo `assets/` folder.

All numerical claims in these specs (DUK 0.658 / 0.173 / 0.160 / 0.325 /
0.342 / 49 %) are verifiable by running the source repo's
`examples/03_explain_single_stock.py --ticker DUK --window-end 2024-06-28`.
None of the numbers are invented.

---

*Spec written: 2026-05-25. Compatible with marketing-content-generation
Design System V2: Warm Technical Editorial + Visual Content Arsenal V1 +
Layout Collision Protection V1 + Creator Identity Mark V1 + Multi-Accent
Color Strategy V1.*
