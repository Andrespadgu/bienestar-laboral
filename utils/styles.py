import textwrap
import streamlit as st

_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');

html, body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: #F7F2EA !important;
}

/* ── STREAMLIT SHELL ── */
#MainMenu, footer, [data-testid="stDecoration"], .stDeployButton { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; box-shadow: none !important; }
[data-testid="stToolbarActions"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stVerticalBlockBorderWrapper"] { border: none !important; padding: 0 !important; }

/* ── SIDEBAR EXPAND BUTTON (stExpandSidebarButton = Streamlit 1.29+) ── */
[data-testid="stExpandSidebarButton"] {
    display: flex !important;
    visibility: visible !important;
    z-index: 999999 !important;
    pointer-events: all !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0D1E2E !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.65) !important; }
[data-testid="stSidebarNav"] { padding-top: 24px !important; }
[data-testid="stSidebarNav"] a {
    padding: 9px 16px !important;
    border-radius: 3px !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.01em !important;
    color: rgba(255,255,255,0.55) !important;
    transition: background 0.15s !important;
}
[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.05) !important;
    color: rgba(255,255,255,0.85) !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(199,91,60,0.18) !important;
    color: #fff !important;
}

/* ── COVER ── */
.cover-wrap {
    background: #0D1E2E;
    padding: 72px 64px 64px;
    display: flex;
    flex-direction: column;
    gap: 56px;
    box-sizing: border-box;
}
.cover-eyebrow {
    font-size: 0.67rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.28);
    margin-bottom: 32px;
}
.cover-title {
    font-size: clamp(4rem, 9vw, 7.5rem);
    font-weight: 900;
    line-height: 0.9;
    letter-spacing: -0.04em;
    color: #ffffff;
    margin: 0 0 24px;
}
.cover-sub {
    font-size: 1rem;
    color: rgba(255,255,255,0.38);
    line-height: 1.65;
    max-width: 500px;
    margin-bottom: 72px;
}
.cover-rule { width: 40px; height: 2px; background: #C75B3C; margin-bottom: 32px; }
.cover-stats {
    display: flex;
    gap: 0;
    border-top: 1px solid rgba(255,255,255,0.07);
    padding-top: 32px;
    margin-top: auto;
}
.cover-stat {
    flex: 1;
    padding-right: 32px;
    border-right: 1px solid rgba(255,255,255,0.07);
    margin-right: 32px;
}
.cover-stat:last-child { border-right: none; margin-right: 0; }
.cover-stat-n {
    font-size: 2.6rem;
    font-weight: 900;
    letter-spacing: -0.05em;
    color: #fff;
    line-height: 1;
    margin-bottom: 5px;
}
.cover-stat-lbl {
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.28);
}

/* ── HERO DARK ── */
.hero-d {
    background: #0D1E2E;
    padding: 64px 64px 52px;
    position: relative;
    overflow: hidden;
}
.hero-d-bgn {
    position: absolute;
    right: 48px;
    top: -32px;
    font-size: 18rem;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.06em;
    color: rgba(255,255,255,0.022);
    user-select: none;
    pointer-events: none;
}
.hero-eyebrow-d {
    font-size: 0.63rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.28);
    margin-bottom: 14px;
}
.hero-num-d {
    font-size: clamp(4.5rem, 10vw, 8.5rem);
    font-weight: 900;
    letter-spacing: -0.05em;
    line-height: 0.88;
    margin-bottom: 20px;
    color: #fff;
}
.hero-lead-d {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.45);
    line-height: 1.7;
    max-width: 580px;
}

/* ── HERO LIGHT ── */
.hero-l {
    background: #F7F2EA;
    padding: 64px 64px 52px;
    position: relative;
    overflow: hidden;
    border-bottom: 1px solid rgba(0,0,0,0.05);
}
.hero-l-bgn {
    position: absolute;
    right: 48px;
    top: -32px;
    font-size: 18rem;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.06em;
    color: rgba(0,0,0,0.022);
    user-select: none;
    pointer-events: none;
}
.hero-eyebrow-l {
    font-size: 0.63rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(28,43,58,0.3);
    margin-bottom: 14px;
}
.hero-num-l {
    font-size: clamp(4.5rem, 10vw, 8.5rem);
    font-weight: 900;
    letter-spacing: -0.05em;
    line-height: 0.88;
    margin-bottom: 20px;
    color: #0D1E2E;
}
.hero-lead-l {
    font-size: 0.95rem;
    color: #5C6E80;
    line-height: 1.7;
    max-width: 580px;
}

/* ── SECTION TAGS ── */
.stag {
    display: inline-block;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 2px;
    margin-bottom: 10px;
}
.stag-r  { background: #E8EEF5; color: #2E5A87; }
.stag-n  { background: #FDEEE9; color: #C75B3C; }
.stag-d  { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.45); }
.stag-g  { background: rgba(94,139,126,0.15); color: #5E8B7E; }

/* ── STAT STRIP (light) ── */
.stat-strip {
    display: flex;
    gap: 0;
    border-top: 1px solid rgba(0,0,0,0.06);
    border-bottom: 1px solid rgba(0,0,0,0.06);
    margin: 0;
}
.stat-cell {
    flex: 1;
    padding: 28px 32px 36px;
    border-right: 1px solid rgba(0,0,0,0.06);
}
.stat-cell:last-child { border-right: none; }
.stat-n {
    font-size: 2.8rem;
    font-weight: 900;
    letter-spacing: -0.05em;
    line-height: 1;
    margin-bottom: 8px;
}
.stat-lbl {
    font-size: 0.7rem;
    color: #5C6E80;
    line-height: 1.4;
    letter-spacing: 0.01em;
}

/* ── STAT STRIP (dark) ── */
.stat-strip-d {
    display: flex;
    gap: 0;
    border-top: 1px solid rgba(255,255,255,0.06);
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.stat-cell-d {
    flex: 1;
    padding: 28px 32px 36px;
    border-right: 1px solid rgba(255,255,255,0.06);
}
.stat-cell-d:last-child { border-right: none; }

/* ── CONTENT PADS ── */
.pad-l  { padding: 48px 64px; background: #F7F2EA; }
.pad-d  { padding: 48px 64px; background: #0D1E2E; }
.pad-alt { padding: 48px 64px; background: #EEF2F7; }

/* ── CHART HEADERS ── */
.ch-hd   { font-size: 1.1rem; font-weight: 800; letter-spacing: -0.02em; color: #0D1E2E; margin-bottom: 3px; }
.ch-hd-d { font-size: 1.1rem; font-weight: 800; letter-spacing: -0.02em; color: #fff; margin-bottom: 3px; }
.ch-cap  { font-size: 0.7rem; color: #5C6E80; letter-spacing: 0.01em; margin-bottom: 0; }
.ch-cap-d { font-size: 0.7rem; color: rgba(255,255,255,0.32); letter-spacing: 0.01em; margin-bottom: 0; }
.sec-lbl   { font-size: 0.6rem; letter-spacing: 0.18em; text-transform: uppercase; color: rgba(28,43,58,0.3); display: block; margin-bottom: 5px; }
.sec-lbl-d { font-size: 0.6rem; letter-spacing: 0.18em; text-transform: uppercase; color: rgba(255,255,255,0.22); display: block; margin-bottom: 5px; }

/* ── INSIGHT ── */
.insight {
    border-left: 3px solid #C4820A;
    padding: 14px 18px;
    margin: 24px 0 0;
}
.insight p { font-size: 0.85rem; color: #5C6E80; line-height: 1.7; margin: 0; }
.insight-d {
    border-left: 3px solid #C4820A;
    padding: 14px 18px;
    margin: 24px 0 0;
}
.insight-d p { font-size: 0.85rem; color: rgba(255,255,255,0.45); line-height: 1.7; margin: 0; }

/* ── RECO SECTION ── */
.reco-wrap { background: #0D1E2E; padding: 56px 64px 64px; }
.reco-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2px;
    margin-top: 36px;
    background: rgba(255,255,255,0.05);
    border-radius: 3px;
    overflow: hidden;
}
.rc {
    background: #0D1E2E;
    display: flex;
    flex-direction: column;
}
.rc-ev { padding: 28px 32px 20px; border-bottom: 1px solid rgba(255,255,255,0.055); }
.rc-num {
    display: block;
    font-size: 3.4rem;
    font-weight: 900;
    letter-spacing: -0.05em;
    line-height: 1;
    margin-bottom: 7px;
}
.rc-ev-lbl { font-size: 0.73rem; color: rgba(255,255,255,0.3); font-style: italic; line-height: 1.4; }
.rc-body { padding: 18px 32px 28px; flex: 1; display: flex; flex-direction: column; }
.rc-seq {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 8px;
    display: block;
}
.rc h4 { font-size: 1rem; font-weight: 800; color: #fff; line-height: 1.25; margin: 0 0 12px; letter-spacing: -0.02em; }
.rc p  { font-size: 0.8rem; color: rgba(255,255,255,0.38); line-height: 1.65; margin: 0; flex: 1; }
.rc-bar-track { height: 3px; background: rgba(255,255,255,0.07); border-radius: 2px; overflow: hidden; margin-bottom: 5px; }
.rc-bar-fill  { height: 100%; border-radius: 2px; }
.rc-bar-meta  {
    display: flex;
    justify-content: space-between;
    font-size: 0.62rem;
    color: rgba(255,255,255,0.2);
    letter-spacing: 0.04em;
    margin-bottom: 14px;
}

/* ── CLOSING ── */
.closing {
    background: #0D1E2E;
    padding: 80px 64px;
    text-align: center;
    border-top: 1px solid rgba(255,255,255,0.06);
}
.closing-lbl {
    font-size: 0.6rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.18);
    margin-bottom: 24px;
}
.closing-title {
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 900;
    color: #fff;
    line-height: 1.08;
    letter-spacing: -0.04em;
    max-width: 660px;
    margin: 0 auto 14px;
}
.closing-sub {
    font-size: 0.88rem;
    color: rgba(255,255,255,0.32);
    max-width: 460px;
    margin: 0 auto;
    line-height: 1.65;
}
.closing-rule { width: 40px; height: 2px; background: #C75B3C; margin: 36px auto 0; }

/* ── SPACER ── */
.sp8  { height: 8px; }
.sp16 { height: 16px; }
.sp24 { height: 24px; }
.sp40 { height: 40px; }

/* ── PLOTLY OVERRIDES ── */
.stPlotlyChart { background: transparent !important; }
.js-plotly-plot .plotly { background: transparent !important; }

/* ── RESPONSIVE / MOBILE ── */
@media (max-width: 640px) {
  .cover-wrap  { padding: 40px 24px !important; gap: 32px; }
  .hero-d, .hero-l { padding: 40px 24px 32px !important; }
  .pad-l, .pad-d, .pad-alt { padding: 28px 24px !important; }
  .reco-wrap  { padding: 36px 24px 48px !important; }
  .closing    { padding: 48px 24px !important; }

  .cover-title  { font-size: clamp(2.8rem,12vw,4rem) !important; }
  .hero-num-d, .hero-num-l { font-size: clamp(3.2rem,14vw,5.5rem) !important; }
  .stat-n       { font-size: 2rem !important; }
  .cover-stat-n { font-size: 1.8rem !important; }

  /* Cover stats: 2 columns on mobile */
  .cover-stats { flex-wrap: wrap !important; padding-top: 16px; }
  .cover-stat  {
    flex: 0 0 50% !important;
    padding: 12px 0 !important;
    border-right: none !important;
    margin-right: 0 !important;
    border-bottom: 1px solid rgba(255,255,255,0.06);
  }

  /* KPI strips: wrap to 2 columns */
  .stat-strip, .stat-strip-d { flex-wrap: wrap !important; }
  .stat-cell, .stat-cell-d {
    flex: 0 0 50% !important;
    border-right: none !important;
    padding: 18px 16px 24px !important;
    border-bottom: 1px solid rgba(0,0,0,0.06);
  }
  .stat-cell-d { border-bottom-color: rgba(255,255,255,0.06) !important; }

  /* Reco grid: single column */
  .reco-grid-2 { grid-template-columns: 1fr !important; }

  /* Streamlit columns → stack vertically */
  [data-testid="stHorizontalBlock"] { flex-direction: column !important; }
  [data-testid="stColumn"] {
    width: 100% !important;
    flex: none !important;
    min-width: 100% !important;
    max-width: 100% !important;
  }
}
"""


def inject_css():
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)


def md(html: str):
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)
