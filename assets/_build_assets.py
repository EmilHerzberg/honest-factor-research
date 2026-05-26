"""Build all PNG assets for the README + GitHub social preview.

Run from repo root:
    python assets/_build_assets.py

Produces:
    assets/banner.png               — 1280x640 hero (GitHub social preview)
    assets/trust_decomposition.png  — comparison chart
    assets/architecture.png         — pipeline flow diagram

All assets are deterministic — re-running produces byte-identical output
(matplotlib default behavior). Idempotent.

Style guide:
    - Dark navy background (deep slate, almost black)
    - High-contrast white text
    - Three-color tier palette (green=DIRECT, blue=STATISTICAL, orange=DERIVED)
    - Grey for unexplained / idiosyncratic
    - Clean sans-serif (DejaVu Sans — portable everywhere)
    - No clichés (no rockets, money bags, charts-going-up-and-right)
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

ASSETS_DIR = Path(__file__).parent

# Color palette — finance/AI research aesthetic
BG = "#0B1426"               # deep navy, almost black
PANEL_BG = "#14213D"          # slightly lighter for panels
GRID = "#1A2741"              # subtle grid lines
TEXT = "#F7FAFC"              # near-white text
TEXT_MUTED = "#A0AEC0"        # secondary text
ACCENT = "#4FB7E0"            # cool blue accent

DIRECT_COLOR = "#22C55E"      # green — trustworthy
STAT_COLOR = "#3B82F6"        # blue — statistical
DERIVED_COLOR = "#F59E0B"     # warning amber — mirror-suspect
UNEXPLAINED = "#475569"       # slate grey


# ─── Banner ────────────────────────────────────────────────────────


def build_banner() -> None:
    """Hero banner — 1280x640 for README top + GitHub social preview.

    Layout (vertical zones, percent of height):
      90-72: hairline + title block (full width)
      72-56: subtitle (full width)
      56-32: tagline + decomposition motif on right
      32-10: legend + url
      10- 0: bottom hairline
    """
    fig, ax = plt.subplots(figsize=(12.8, 6.4), dpi=100)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Top + bottom hairlines for "publication-grade" framing
    ax.add_patch(Rectangle((0, 91), 100, 0.3, color=ACCENT, zorder=2))
    ax.add_patch(Rectangle((0, 4), 100, 0.2, color=GRID, zorder=2))

    # Subtle accent stripe top-left
    ax.add_patch(Rectangle((0, 91 - 8), 0.6, 8, color=ACCENT, zorder=2))

    # ─── Title block (top half, full width) ───
    ax.text(
        4, 76, "Honest Factor Research",
        color=TEXT, fontsize=38, fontweight="bold",
        fontfamily="DejaVu Sans", zorder=2,
    )
    # Subtitle
    ax.text(
        4, 64, "A reproducible model-audit framework for stock factor models.",
        color=ACCENT, fontsize=17,
        fontfamily="DejaVu Sans", zorder=2,
    )

    # ─── Tagline (left) + Decomposition motif (right) ───
    # Tagline — left column
    ax.text(
        4, 46, "Separating real explanation from",
        color=TEXT_MUTED, fontsize=14,
        fontfamily="DejaVu Sans", zorder=2,
    )
    ax.text(
        4, 40, "sector mirrors, regime shifts,",
        color=TEXT_MUTED, fontsize=14,
        fontfamily="DejaVu Sans", zorder=2,
    )
    ax.text(
        4, 34, "and overconfident R².",
        color=TEXT_MUTED, fontsize=14,
        fontfamily="DejaVu Sans", zorder=2,
    )

    # Decomposition motif — right column (compact)
    bar_x = 58
    bar_width = 38

    # Caption above motif
    ax.text(bar_x, 51, "What an R² of 0.66 actually contains",
            color=TEXT, fontsize=10, fontweight="bold",
            fontfamily="DejaVu Sans", zorder=2)

    # "Traditional" bar (top — single block)
    ax.text(bar_x, 45, "standard view",
            color=TEXT_MUTED, fontsize=9,
            fontfamily="DejaVu Sans", zorder=2)
    ax.add_patch(Rectangle((bar_x, 39), bar_width * 0.66, 3.5,
                           color=ACCENT, zorder=2))
    ax.add_patch(Rectangle((bar_x + bar_width * 0.66, 39),
                           bar_width * 0.34, 3.5,
                           color=UNEXPLAINED, zorder=2))

    # "Honest" bar (bottom — decomposed)
    ax.text(bar_x, 32, "honest decomposition",
            color=TEXT, fontsize=9, fontweight="bold",
            fontfamily="DejaVu Sans", zorder=2)
    parts = [
        (0.17, DIRECT_COLOR),
        (0.16, STAT_COLOR),
        (0.33, DERIVED_COLOR),
        (0.34, UNEXPLAINED),
    ]
    cumulative = 0.0
    for share, color in parts:
        ax.add_patch(Rectangle(
            (bar_x + bar_width * cumulative, 26),
            bar_width * share, 3.5, color=color, zorder=2,
        ))
        cumulative += share

    # ─── Legend + URL row ───
    legend_y = 16
    legend_items = [
        ("DIRECT", DIRECT_COLOR),
        ("STAT", STAT_COLOR),
        ("DERIVED", DERIVED_COLOR),
        ("noise", UNEXPLAINED),
    ]
    legend_x = bar_x
    for label, color in legend_items:
        ax.add_patch(Rectangle((legend_x, legend_y), 1.4, 1.4,
                               color=color, zorder=2))
        ax.text(legend_x + 1.8, legend_y + 0.1, label,
                color=TEXT_MUTED, fontsize=9,
                fontfamily="DejaVu Sans", zorder=2)
        legend_x += 9

    # Bottom-left URL
    ax.text(4, 10, "github.com/EmilHerzberg/honest-factor-research",
            color=TEXT_MUTED, fontsize=10,
            fontstyle="italic", fontfamily="DejaVu Sans", zorder=2)

    out = ASSETS_DIR / "banner.png"
    fig.savefig(out, dpi=100, facecolor=BG, edgecolor="none",
                bbox_inches=None, pad_inches=0)
    plt.close(fig)
    print(f"  -> {out} (1280x640)")


# ─── Trust Decomposition explainer ────────────────────────────────


def build_trust_decomposition() -> None:
    """Side-by-side: traditional R² vs honest decomposition (DUK example).

    Uses real numbers from examples/03_explain_single_stock.py --ticker DUK
    --window-end 2024-06-28.
    """
    fig, axes = plt.subplots(
        1, 2, figsize=(12.0, 6.0), dpi=100,
        gridspec_kw={"width_ratios": [1, 1], "wspace": 0.25},
    )
    fig.patch.set_facecolor(BG)

    # Title for whole figure (lowered slightly to give the top breathing room)
    fig.text(0.5, 0.90, "When R² hides where the explanation comes from",
             ha="center", color=TEXT, fontsize=20, fontweight="bold",
             fontfamily="DejaVu Sans")
    fig.text(0.5, 0.84,
             "DUK (Duke Energy) — window ending 2024-06-28",
             ha="center", color=TEXT_MUTED, fontsize=11, fontstyle="italic",
             fontfamily="DejaVu Sans")

    # Left panel: Traditional R²
    ax_l = axes[0]
    ax_l.set_facecolor(PANEL_BG)
    ax_l.set_xlim(0, 1)
    ax_l.set_ylim(0, 4)
    ax_l.axis("off")

    ax_l.text(0.5, 3.5, "Traditional R²", ha="center", color=TEXT,
              fontsize=14, fontweight="bold", fontfamily="DejaVu Sans")
    ax_l.text(0.5, 3.1, "What you usually see",
              ha="center", color=TEXT_MUTED, fontsize=10, fontstyle="italic",
              fontfamily="DejaVu Sans")

    # Single bar: 0.658 explained / 0.342 unexplained
    ax_l.add_patch(Rectangle((0.05, 1.5), 0.90 * 0.658, 0.8,
                             color=ACCENT))
    ax_l.add_patch(Rectangle((0.05 + 0.90 * 0.658, 1.5),
                             0.90 * 0.342, 0.8, color=UNEXPLAINED))

    ax_l.text(0.05 + (0.90 * 0.658) / 2, 1.9, "R² = 0.658",
              ha="center", va="center", color=BG, fontsize=14,
              fontweight="bold", fontfamily="DejaVu Sans")
    ax_l.text(0.05 + 0.90 * 0.658 + (0.90 * 0.342) / 2, 1.9, "0.342",
              ha="center", va="center", color=TEXT, fontsize=11,
              fontfamily="DejaVu Sans")

    ax_l.text(0.5, 0.7, '"DUK looks 66% explained.\nProbably a high-quality fit."',
              ha="center", va="center", color=TEXT_MUTED, fontsize=10,
              fontstyle="italic", fontfamily="DejaVu Sans")

    # Right panel: Honest decomposition
    ax_r = axes[1]
    ax_r.set_facecolor(PANEL_BG)
    ax_r.set_xlim(0, 1)
    ax_r.set_ylim(0, 4)
    ax_r.axis("off")

    ax_r.text(0.5, 3.5, "Honest decomposition", ha="center", color=TEXT,
              fontsize=14, fontweight="bold", fontfamily="DejaVu Sans")
    ax_r.text(0.5, 3.1, "How much can we honestly defend?",
              ha="center", color=TEXT_MUTED, fontsize=10, fontstyle="italic",
              fontfamily="DejaVu Sans")

    # Stacked bar: DIRECT 0.169 / +STAT 0.160 / +DERIVED 0.330 / UNEXPL 0.341
    parts = [
        (0.173, DIRECT_COLOR, "DIRECT\n0.173"),
        (0.160, STAT_COLOR, "+ STAT\n+0.160"),
        (0.325, DERIVED_COLOR, "+ DERIVED\n+0.325"),
        (0.342, UNEXPLAINED, "noise\n0.342"),
    ]
    cum = 0.05
    for share, color, label in parts:
        width = 0.90 * share
        ax_r.add_patch(Rectangle((cum, 1.5), width, 0.8, color=color))
        if width > 0.06:
            ax_r.text(cum + width / 2, 1.9, label,
                      ha="center", va="center", color=BG, fontsize=9,
                      fontweight="bold", fontfamily="DejaVu Sans")
        cum += width

    # Annotation arrow + warning
    ax_r.annotate(
        "≈49% of explained R²\nfrom sector-baskets\n(DUK is in XLU)",
        xy=(0.05 + 0.90 * (0.173 + 0.160 + 0.325 / 2), 1.45),
        xytext=(0.05 + 0.90 * 0.5, 0.35),
        ha="center", color=DERIVED_COLOR, fontsize=10,
        fontweight="bold", fontfamily="DejaVu Sans",
        arrowprops=dict(arrowstyle="->", color=DERIVED_COLOR, lw=1.5),
    )

    out = ASSETS_DIR / "trust_decomposition.png"
    fig.savefig(out, dpi=100, facecolor=BG, edgecolor="none",
                bbox_inches=None, pad_inches=0)
    plt.close(fig)
    print(f"  -> {out} (1200x600)")


# ─── Architecture diagram ─────────────────────────────────────────


def build_architecture() -> None:
    """Pipeline flow diagram: data -> returns -> Ridge -> three outputs."""
    fig, ax = plt.subplots(figsize=(14.0, 5.0), dpi=100)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.axis("off")

    fig.text(0.5, 0.92, "Pipeline architecture",
             ha="center", color=TEXT, fontsize=18, fontweight="bold",
             fontfamily="DejaVu Sans")

    # Boxes — (x, y, w, h, label_lines, color)
    boxes_input = [
        (0.3, 2.0, 1.8, 0.9, ["Market Data", "yfinance +", "NASDAQ-screener"], PANEL_BG),
        (2.5, 2.0, 1.4, 0.9, ["Log", "Returns"], PANEL_BG),
        (4.3, 2.0, 1.8, 0.9, ["Factor Catalog", "(28 factors", "YAML)"], PANEL_BG),
        (6.5, 2.0, 1.9, 0.9, ["Rolling RidgeCV", "(252-day", "windows)"], ACCENT),
    ]
    boxes_output = [
        (9.0, 3.3, 2.4, 0.9, ["Trust-Stratified R²", "DIRECT/STAT/DERIVED"], DIRECT_COLOR),
        (9.0, 2.0, 2.4, 0.9, ["Block-Bootstrap CI", "(Politis-Romano)"], STAT_COLOR),
        (9.0, 0.7, 2.4, 0.9, ["Regime Betas", "(VIX-stratified)"], DERIVED_COLOR),
    ]
    final = (11.8, 2.0, 1.8, 0.9, ["Reports", "& CSVs"], PANEL_BG)

    def draw_box(x, y, w, h, lines, fill):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.05",
            facecolor=fill, edgecolor=TEXT_MUTED, linewidth=1.0,
        ))
        for i, line in enumerate(lines):
            font_color = BG if fill in (ACCENT, DIRECT_COLOR, STAT_COLOR, DERIVED_COLOR) else TEXT
            ax.text(x + w / 2, y + h - 0.25 - i * 0.22, line,
                    ha="center", va="center", color=font_color,
                    fontsize=9, fontweight="bold" if i == 0 else "normal",
                    fontfamily="DejaVu Sans")

    for box in boxes_input + boxes_output + [final]:
        draw_box(*box)

    # Horizontal arrows between input boxes
    arrows_h = [
        (2.1, 2.45, 2.5, 2.45),    # Market Data -> Log Returns
        (3.9, 2.45, 4.3, 2.45),    # Log Returns -> Factor Catalog
        (6.1, 2.45, 6.5, 2.45),    # Factor Catalog -> Rolling RidgeCV
    ]
    for x1, y1, x2, y2 in arrows_h:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=TEXT_MUTED, lw=1.5))

    # Rolling Ridge -> 3 outputs (branch)
    for y_out in (3.75, 2.45, 1.15):
        ax.annotate("", xy=(9.0, y_out), xytext=(8.4, 2.45),
                    arrowprops=dict(arrowstyle="->", color=TEXT_MUTED, lw=1.5))

    # 3 outputs -> Reports (merge)
    for y_out in (3.75, 2.45, 1.15):
        ax.annotate("", xy=(11.8, 2.45), xytext=(11.4, y_out),
                    arrowprops=dict(arrowstyle="->", color=TEXT_MUTED, lw=1.5))

    # Bottom caption
    fig.text(0.5, 0.04,
             "Single residualized factor matrix feeds three parallel diagnostics.",
             ha="center", color=TEXT_MUTED, fontsize=10, fontstyle="italic",
             fontfamily="DejaVu Sans")

    out = ASSETS_DIR / "architecture.png"
    fig.savefig(out, dpi=100, facecolor=BG, edgecolor="none",
                bbox_inches=None, pad_inches=0)
    plt.close(fig)
    print(f"  -> {out} (1400x500)")


# ─── Main ──────────────────────────────────────────────────────────


def main() -> int:
    print("Building visual assets...")
    build_banner()
    build_trust_decomposition()
    build_architecture()
    print("\nAll assets built. They are deterministic — re-running produces "
          "byte-identical output.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
