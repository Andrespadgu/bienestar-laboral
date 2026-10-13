"""
Chart builders — editorial Plotly style.
All statistics are computed from the real dataframe, never hardcoded.
"""
import numpy as np
import plotly.graph_objects as go
from scipy import stats as sp

from config.settings import COLORS, DIMS, CORR_PAIRS
from utils.stats import compute_ire, compute_correlations, spearman

_FONT = dict(family="Inter, -apple-system, sans-serif")
_BG   = "rgba(0,0,0,0)"


def _base(h=340, **kw):
    base = dict(
        paper_bgcolor=_BG, plot_bgcolor=_BG,
        font=_FONT, margin=dict(l=0, r=16, t=12, b=0),
        showlegend=False, height=h,
    )
    base.update(kw)
    return base


# ── IRE HORIZONTAL BARS ──────────────────────────────────────────────────────

def chart_ire(df) -> go.Figure:
    """Horizontal bar chart — IRE values computed from real data."""
    dims = compute_ire(df)               # sorted descending
    dims_asc = list(reversed(dims))      # ascending for horizontal bar (bottom = low risk)

    labels = [d["lb"]  for d in dims_asc]
    values = [d["ire"] for d in dims_asc]
    types  = [d["t"]   for d in dims_asc]

    top3_threshold = sorted(values, reverse=True)[min(2, len(values) - 1)]
    colors = []
    for v, t in zip(values, types):
        if v >= top3_threshold:
            colors.append(COLORS["coral"] if t in ("demand", "negative") else COLORS["blue"])
        else:
            colors.append(
                "rgba(199,91,60,0.13)" if t in ("demand", "negative")
                else "rgba(46,90,135,0.13)"
            )

    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=dict(color=colors, line_width=0),
        text=[f"{v:.1f}" for v in values],
        textposition="outside",
        textfont=dict(size=10, color=COLORS["text_soft"]),
        hovertemplate="%{y}: IRE %{x:.1f}<extra></extra>",
    ))
    fig.update_layout(
        **_base(h=500),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False,
                   range=[0, max(values) * 1.16]),
        yaxis=dict(showgrid=False, zeroline=False, ticklen=0,
                   tickfont=dict(size=11, color=COLORS["text_soft"])),
        bargap=0.38,
    )
    return fig


# ── JDR BALANCE ──────────────────────────────────────────────────────────────

def chart_jdr(df) -> go.Figure:
    """IRE mean by dimension type — all computed from real data."""
    dims = compute_ire(df)

    type_labels = {
        "demand":     "Demandas",
        "negative":   "Resultados negativos",
        "resource":   "Recursos",
        "protective": "Factores protectores",
    }
    type_colors = {
        "demand":     COLORS["coral"],
        "negative":   "rgba(199,91,60,0.55)",
        "resource":   COLORS["blue"],
        "protective": COLORS["green"],
    }

    avg = {}
    for t, lb in type_labels.items():
        ires = [d["ire"] for d in dims if d["t"] == t]
        if ires:
            avg[t] = np.mean(ires)

    order = sorted(avg.items(), key=lambda x: x[1])
    labels  = [type_labels[t]  for t, _ in order]
    values  = [v               for _, v  in order]
    colors  = [type_colors[t]  for t, _ in order]

    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker=dict(color=colors, line_width=0),
        text=[f"{v:.1f}" for v in values],
        textposition="outside",
        textfont=dict(size=12, color=COLORS["text_soft"]),
        hovertemplate="%{y}: IRE medio %{x:.1f}<extra></extra>",
    ))
    fig.update_layout(
        **_base(h=220),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False,
                   range=[0, max(values) * 1.18]),
        yaxis=dict(showgrid=False, zeroline=False, ticklen=0,
                   tickfont=dict(size=11, color=COLORS["text_soft"])),
        bargap=0.42,
    )
    return fig


# ── BURNOUT HISTOGRAM ─────────────────────────────────────────────────────────

def chart_bu_hist(df) -> go.Figure:
    """Burnout distribution — threshold % computed from real data."""
    bu   = df["BU_prom"].dropna().values
    bins = np.arange(1.0, 5.26, 0.25)
    counts, edges = np.histogram(bu, bins=bins)
    bar_colors = [
        "rgba(199,91,60,0.82)" if e >= 3.0 else "rgba(122,155,184,0.3)"
        for e in edges[:-1]
    ]
    pct = (bu > 3).mean() * 100

    fig = go.Figure(go.Bar(
        x=edges[:-1] + 0.125, y=counts,
        width=0.22,
        marker=dict(color=bar_colors, line_width=0),
        hovertemplate="BU ≈ %{x:.2f}: %{y} personas<extra></extra>",
    ))
    fig.add_vline(
        x=3.0, line_width=1.5, line_color="rgba(199,91,60,0.55)",
        annotation_text="umbral crítico",
        annotation_font=dict(size=9, color=COLORS["coral"]),
        annotation_position="top right",
    )
    fig.add_annotation(
        x=4.3, y=counts.max() * 0.78,
        text=f"<b>{pct:.1f}%</b><br>sobre umbral",
        font=dict(size=11, color=COLORS["coral"]),
        showarrow=False, align="center",
    )
    fig.update_layout(
        **_base(h=300),
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(size=10, color=COLORS["text_soft"])),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.04)",
                   zeroline=False, tickfont=dict(size=9, color=COLORS["text_soft"])),
        bargap=0.05,
    )
    return fig


# ── SCATTER SAT vs IR ─────────────────────────────────────────────────────────

def chart_scatter(df) -> go.Figure:
    """
    Scatter SAT vs IR with Spearman ρ and OLS trend computed from real data.
    The annotation shows the actual correlation — never a hardcoded string.
    """
    merged = df[["SAT_prom", "IR_prom"]].dropna()
    sat = merged["SAT_prom"].values
    ir  = merged["IR_prom"].values

    rho, pval = sp.spearmanr(sat, ir)

    # OLS trend line (visual aid — not Spearman, but visually cleaner than ranked)
    slope, intercept, *_ = sp.linregress(sat, ir)
    xl = np.linspace(sat.min(), sat.max(), 80)
    yl = slope * xl + intercept

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sat, y=ir, mode="markers",
        marker=dict(color="rgba(92,110,128,0.14)", size=5, line_width=0),
        hovertemplate="SAT: %{x:.2f} · IR: %{y:.2f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=xl, y=yl, mode="lines",
        line=dict(color=COLORS["coral"], width=1.8),
        hoverinfo="skip",
    ))
    # Dynamic annotation — no hardcoded rho
    sign  = "−" if rho < 0 else "+"
    p_lbl = "p < 0.001" if pval < 0.001 else f"p = {pval:.3f}"
    fig.add_annotation(
        x=sat.min() + 0.4, y=yl[0] + 0.45,
        text=f"ρ = {sign}{abs(rho):.3f}  ·  {p_lbl}",
        font=dict(size=12, color=COLORS["coral"], family="Inter"),
        showarrow=False,
    )
    fig.update_layout(
        **_base(h=300),
        xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.04)", zeroline=False,
                   tickfont=dict(size=9, color=COLORS["text_soft"]),
                   title_text="Satisfacción laboral",
                   title_font=dict(size=9, color=COLORS["text_soft"])),
        yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.04)", zeroline=False,
                   tickfont=dict(size=9, color=COLORS["text_soft"]),
                   title_text="Intención de retiro",
                   title_font=dict(size=9, color=COLORS["text_soft"])),
    )
    return fig, round(float(rho), 4), float(pval)


# ── BURNOUT BY CARGO ──────────────────────────────────────────────────────────

def chart_cargo(df) -> go.Figure:
    """Burnout % by Tipo_Cargo — all computed from real data."""
    groups = [g for g in ["Operativo", "Administrativo", "Directivo"]
              if g in df["Tipo_Cargo"].values]
    pcts = [(df[df["Tipo_Cargo"] == g]["BU_prom"] > 3).mean() * 100 for g in groups]

    max_pct = max(pcts) if pcts else 1
    max_group = groups[pcts.index(max_pct)]
    colors = [
        COLORS["coral"] if g == max_group else "rgba(46,90,135,0.2)"
        for g in groups
    ]
    txt_colors = [
        COLORS["coral"] if g == max_group else COLORS["text_soft"]
        for g in groups
    ]

    fig = go.Figure(go.Bar(
        x=groups, y=pcts,
        marker=dict(color=colors, line_width=0),
        text=[f"{p:.1f}%" for p in pcts],
        textposition="outside",
        textfont=dict(size=14, color=txt_colors),
        width=0.42,
        hovertemplate="%{x}: %{y:.1f}% con BU > 3<extra></extra>",
    ))
    fig.update_layout(
        **_base(h=300),
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(size=12, color=COLORS["text_soft"])),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False,
                   range=[0, max_pct * 1.28]),
        bargap=0.38,
    )
    return fig


# ── DESGASTE BY MODALIDAD ─────────────────────────────────────────────────────

def chart_modal(df) -> go.Figure:
    """DL mean by Modalidad — computed from real data."""
    groups = [g for g in ["Presencial", "Híbrido"]
              if g in df["Modalidad"].values]
    means = [df[df["Modalidad"] == g]["DL_prom"].mean() for g in groups]

    max_mean  = max(means) if means else 1
    max_group = groups[means.index(max_mean)]
    colors    = [COLORS["amber"] if g == max_group else "rgba(122,155,184,0.3)" for g in groups]
    txt_c     = [COLORS["amber"] if g == max_group else COLORS["text_soft"] for g in groups]

    fig = go.Figure(go.Bar(
        x=groups, y=means,
        marker=dict(color=colors, line_width=0),
        text=[f"{m:.2f}" for m in means],
        textposition="outside",
        textfont=dict(size=14, color=txt_c),
        width=0.32,
        hovertemplate="%{x}: DL medio %{y:.2f}<extra></extra>",
    ))
    fig.update_layout(
        **_base(h=280),
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(size=12, color=COLORS["text_soft"])),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False,
                   range=[0, max_mean * 1.28]),
        bargap=0.52,
    )
    return fig


# ── LIDERAZGO vs BURNOUT ──────────────────────────────────────────────────────

def chart_cl(df) -> go.Figure:
    """BU mean by CL group — split and % difference all computed from real data."""
    high = df[df["CL_prom"] >  3.5]["BU_prom"].mean()
    low  = df[df["CL_prom"] <= 3.5]["BU_prom"].mean()
    diff = (low - high) / high * 100 if high > 0 else 0

    groups = ["Liderazgo\ncomprometido", "Liderazgo\ndébil"]
    means  = [high, low]
    colors = ["rgba(94,139,126,0.55)", "rgba(199,91,60,0.82)"]
    txt_c  = [COLORS["green"], COLORS["coral"]]

    fig = go.Figure(go.Bar(
        x=groups, y=means,
        marker=dict(color=colors, line_width=0),
        text=[f"{m:.2f}" for m in means],
        textposition="outside",
        textfont=dict(size=14, color=txt_c),
        width=0.36,
        hovertemplate="%{x}: BU medio %{y:.2f}<extra></extra>",
    ))
    fig.add_annotation(
        x=0.5, y=(high + low) / 2,
        text=f"+{diff:.0f}%",
        font=dict(size=22, color=COLORS["coral"], family="Inter"),
        showarrow=False, xref="paper",
    )
    fig.update_layout(
        **_base(h=310),
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(size=11, color=COLORS["text_soft"])),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False,
                   range=[0, max(means) * 1.32]),
        bargap=0.52,
    )
    return fig


# ── TOP CORRELATIONS ──────────────────────────────────────────────────────────

def chart_corr(df) -> go.Figure:
    """
    Top-8 Spearman correlations — all rho values computed from real data.
    No hardcoded correlation values.
    """
    corrs = compute_correlations(df)

    pairs  = [c["a"]   for c in corrs]
    rhos   = [c["rho"] for c in corrs]
    dirs   = [c["dir"] for c in corrs]

    color_map = {
        "harmful":    COLORS["coral"],
        "protective": COLORS["green"],
        "negative":   COLORS["blue_light"],
    }
    max_abs = max(abs(r) for r in rhos) if rhos else 1

    # sort ascending by |rho| for horizontal bar (strongest at top)
    order    = sorted(range(len(rhos)), key=lambda i: abs(rhos[i]))
    s_pairs  = [pairs[i] for i in order]
    s_rhos   = [rhos[i]  for i in order]
    s_dirs   = [dirs[i]  for i in order]
    s_abs    = [abs(rhos[i]) for i in order]

    final_colors = [
        color_map.get(d, COLORS["blue_light"]) if a == max(s_abs)
        else "rgba(92,110,128,0.25)"
        for a, d in zip(s_abs, s_dirs)
    ]

    fig = go.Figure(go.Bar(
        x=s_rhos, y=s_pairs, orientation="h",
        marker=dict(color=final_colors, line_width=0),
        text=[f"ρ={r:+.3f}" for r in s_rhos],
        textposition="outside",
        textfont=dict(size=10, color=COLORS["text_soft"]),
        hovertemplate="%{y}: ρ=%{x:.4f}<extra></extra>",
    ))
    fig.add_vline(x=0, line_width=1, line_color="rgba(0,0,0,0.1)")
    rng = max(abs(r) for r in s_rhos) * 1.32 if s_rhos else 1
    fig.update_layout(
        **_base(h=360),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False,
                   range=[-rng, rng]),
        yaxis=dict(showgrid=False, zeroline=False, ticklen=0,
                   tickfont=dict(size=10, color=COLORS["text_soft"])),
        bargap=0.3,
    )
    return fig


# ── BURNOUT BY SEX ────────────────────────────────────────────────────────────

def chart_sex(df) -> go.Figure:
    """BU / SOM / IR by Sexo — all means computed from real data."""
    groups  = [g for g in ["Mujer", "Hombre"] if g in df["Sexo"].values]
    metrics = [
        ("BU_prom",  "Burnout",          COLORS["coral"]),
        ("SOM_prom", "Somatización",      COLORS["amber"]),
        ("IR_prom",  "Intención retiro",  COLORS["blue"]),
    ]
    fig = go.Figure()
    for col, name, color in metrics:
        means = [df[df["Sexo"] == g][col].mean() for g in groups]
        fig.add_trace(go.Bar(
            name=name, x=groups, y=means,
            marker=dict(color=color, line_width=0),
            text=[f"{m:.2f}" for m in means],
            textposition="outside",
            textfont=dict(size=10),
            width=0.2,
            hovertemplate=f"{name} · %{{x}}: %{{y:.2f}}<extra></extra>",
        ))
    fig.update_layout(
        **_base(h=300, showlegend=True),
        legend=dict(orientation="h", x=0, y=1.1,
                    font=dict(size=9, color=COLORS["text_soft"]),
                    bgcolor=_BG, borderwidth=0),
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(size=12, color=COLORS["text_soft"])),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        barmode="group", bargap=0.3, bargroupgap=0.06,
    )
    return fig


# ── BURNOUT BY HORAS ──────────────────────────────────────────────────────────

def chart_horas(df) -> go.Figure:
    """Burnout by Horas_Semana groups — all computed from real data."""
    def grp(h):
        return "≤ 40h" if h <= 40 else ("41–48h" if h <= 48 else "> 48h")

    df2 = df.copy()
    df2["hg"] = df2["Horas_Semana"].apply(grp)
    order  = ["≤ 40h", "41–48h", "> 48h"]
    means  = [df2[df2["hg"] == g]["BU_prom"].mean() for g in order]
    max_m  = max(means)
    colors = [COLORS["coral"] if m == max_m else "rgba(46,90,135,0.22)"
              if m == min(means) else "rgba(196,130,10,0.5)" for m in means]
    txt_c  = [COLORS["coral"] if m == max_m else COLORS["text_soft"]
              if m == min(means) else COLORS["amber"] for m in means]

    fig = go.Figure(go.Bar(
        x=order, y=means,
        marker=dict(color=colors, line_width=0),
        text=[f"{m:.2f}" for m in means],
        textposition="outside",
        textfont=dict(size=13, color=txt_c),
        width=0.38,
        hovertemplate="%{x}: BU medio %{y:.2f}<extra></extra>",
    ))
    fig.update_layout(
        **_base(h=280),
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(size=12, color=COLORS["text_soft"])),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False,
                   range=[0, max_m * 1.28]),
        bargap=0.42,
    )
    return fig
