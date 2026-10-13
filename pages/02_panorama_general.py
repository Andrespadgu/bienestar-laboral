import streamlit as st
from utils.styles import md
from utils.data_loader import load_data
from utils.stats import compute_kpis, spearman
from utils.charts import chart_bu_hist, chart_scatter

df  = load_data()
kpi = compute_kpis(df)

_CFG = dict(use_container_width=True, config={"displayModeBar": False})

rho_bu_som, pval_bu_som = spearman(df, "BU_prom", "SOM_prom")
rho_sat_ir = kpi["rho_sat_ir"]

# ── HERO ────────────────────────────────────────────────────────────────────
n_bu_above = int(kpi["pct_bu"] / 100 * kpi["n"])
md(f"""
<div class="hero-d">
  <div class="hero-d-bgn">02</div>
  <div class="hero-eyebrow-d">Capítulo 02 · Señales físicas</div>
  <div class="hero-num-d" style="color:#C75B3C">1 de cada {round(100/kpi['pct_bu'])}</div>
  <div class="hero-lead-d">
    ya cruzó el límite del agotamiento (n={n_bu_above}).
    Y {kpi['pct_som']:.1f}% siente ese agotamiento en el cuerpo.
    Burnout y somatización correlacionan ρ = {rho_bu_som:+.3f} —
    el desgaste no se queda en la cabeza.
  </div>
</div>
""")

# ── KEY STATS STRIP ─────────────────────────────────────────────────────────
md(f"""
<div class="stat-strip-d">
  <div class="stat-cell-d">
    <div class="stat-n" style="color:#C75B3C">{kpi['pct_bu']:.1f}%</div>
    <div class="stat-lbl">Burnout moderado–alto (BU &gt; 3)</div>
  </div>
  <div class="stat-cell-d">
    <div class="stat-n" style="color:#C75B3C">{kpi['pct_som']:.1f}%</div>
    <div class="stat-lbl">Somatización alta (SOM &gt; 4)</div>
  </div>
  <div class="stat-cell-d">
    <div class="stat-n">{kpi['mean_bu']:.2f}</div>
    <div class="stat-lbl">Media burnout (escala 1–5)</div>
  </div>
  <div class="stat-cell-d">
    <div class="stat-n" style="color:#5E8B7E">{kpi['mean_sat']:.2f}</div>
    <div class="stat-lbl">Media satisfacción (escala 1–7)</div>
  </div>
</div>
""")

# ── BURNOUT HISTOGRAM ────────────────────────────────────────────────────────
md("""
<div class="pad-l" style="padding-bottom:8px;">
  <span class="stag stag-n">Distribución de burnout</span>
  <div class="ch-hd">La cola derecha es el problema</div>
  <div class="ch-cap">Distribución de BU_prom. Barras en coral = sobre el umbral crítico (BU &gt; 3).</div>
  <div class="sp16"></div>
</div>
""")

col1, col2 = st.columns([3, 2])
with col1:
    st.plotly_chart(chart_bu_hist(df), **_CFG)
with col2:
    n_bu_mod  = int(kpi["pct_bu"]      / 100 * kpi["n"])
    n_bu_high = int(kpi["pct_bu_high"] / 100 * kpi["n"])
    n_som     = int(kpi["pct_som"]     / 100 * kpi["n"])
    md(f"""
    <div style="padding:24px 16px 0 24px;">
      <div style="margin-bottom:28px;padding-bottom:28px;border-bottom:1px solid rgba(0,0,0,0.07);">
        <div class="sec-lbl">Burnout moderado–alto</div>
        <div style="font-size:3.2rem;font-weight:900;color:#C75B3C;letter-spacing:-0.05em;line-height:1">{kpi['pct_bu']:.1f}%</div>
        <div style="font-size:0.78rem;color:#5C6E80;margin-top:5px;">BU_prom &gt; 3 · n = {n_bu_mod}</div>
      </div>
      <div style="margin-bottom:28px;padding-bottom:28px;border-bottom:1px solid rgba(0,0,0,0.07);">
        <div class="sec-lbl">Burnout alto</div>
        <div style="font-size:3.2rem;font-weight:900;color:#C75B3C;letter-spacing:-0.05em;line-height:1">{kpi['pct_bu_high']:.1f}%</div>
        <div style="font-size:0.78rem;color:#5C6E80;margin-top:5px;">BU_prom &gt; 3.5 · n = {n_bu_high}</div>
      </div>
      <div>
        <div class="sec-lbl">Somatización alta</div>
        <div style="font-size:3.2rem;font-weight:900;color:#C4820A;letter-spacing:-0.05em;line-height:1">{kpi['pct_som']:.1f}%</div>
        <div style="font-size:0.78rem;color:#5C6E80;margin-top:5px;">SOM_prom &gt; 4 · n = {n_som}</div>
      </div>
    </div>
    """)

p_lbl_bu_som = "p < 0.001" if pval_bu_som < 0.001 else f"p = {pval_bu_som:.3f}"
md(f"""
<div class="pad-l" style="padding-top:4px;padding-bottom:48px;">
  <div class="insight">
    <p>La correlación burnout–somatización (ρ = {rho_bu_som:+.3f}, {p_lbl_bu_som}) muestra que el
    desgaste no es abstracto. Cefaleas, tensión muscular, insomnio — señales de un sistema
    que ya llegó a su límite. <strong>{kpi['pct_som']:.1f}% tiene somatización alta.</strong></p>
  </div>
</div>
""")

# ── SCATTER SAT vs IR ────────────────────────────────────────────────────────
md("""
<div class="pad-alt" style="padding-bottom:8px;">
  <span class="stag stag-n">La correlación más fuerte del estudio</span>
  <div class="ch-hd">Menos satisfacción. Más deseos de irse.</div>
  <div class="ch-cap">SAT_prom vs IR_prom · correlación Spearman calculada en tiempo real</div>
  <div class="sp16"></div>
</div>
""")

col_s1, col_s2 = st.columns([3, 2])
with col_s1:
    fig_scatter, rho_computed, pval_computed = chart_scatter(df)
    st.plotly_chart(fig_scatter, **_CFG)
with col_s2:
    n_ir      = int(kpi["pct_ir"]      / 100 * kpi["n"])
    n_sat_low = int(kpi["pct_sat_low"] / 100 * kpi["n"])
    sign_lbl  = "−" if rho_computed < 0 else "+"
    p_lbl     = "p < 0.001" if pval_computed < 0.001 else f"p = {pval_computed:.3f}"
    md(f"""
    <div style="padding:24px 16px 0 24px;">
      <div style="margin-bottom:28px;padding-bottom:28px;border-bottom:1px solid rgba(0,0,0,0.07);">
        <div class="sec-lbl">Correlación Spearman</div>
        <div style="font-size:3rem;font-weight:900;color:#C75B3C;letter-spacing:-0.04em;line-height:1">{sign_lbl}{abs(rho_computed):.3f}</div>
        <div style="font-size:0.78rem;color:#5C6E80;margin-top:5px;">SAT ↔ IR · {p_lbl}</div>
      </div>
      <div style="margin-bottom:28px;padding-bottom:28px;border-bottom:1px solid rgba(0,0,0,0.07);">
        <div class="sec-lbl">Intención de retiro alta</div>
        <div style="font-size:3rem;font-weight:900;color:#C75B3C;letter-spacing:-0.04em;line-height:1">{kpi['pct_ir']:.1f}%</div>
        <div style="font-size:0.78rem;color:#5C6E80;margin-top:5px;">IR_prom &gt; 4.5 · n = {n_ir}</div>
      </div>
      <div>
        <div class="sec-lbl">Satisfacción baja</div>
        <div style="font-size:3rem;font-weight:900;color:#C4820A;letter-spacing:-0.04em;line-height:1">{kpi['pct_sat_low']:.1f}%</div>
        <div style="font-size:0.78rem;color:#5C6E80;margin-top:5px;">SAT_prom &lt; 3.5 · n = {n_sat_low}</div>
      </div>
    </div>
    """)

md(f"""
<div class="pad-alt" style="padding-top:4px;padding-bottom:48px;">
  <div class="insight">
    <p>ρ = {sign_lbl}{abs(rho_computed):.3f} ({p_lbl}) es la correlación más fuerte del estudio.
    A menor satisfacción, mayor intención de retiro — sin ambigüedad.
    <strong>{kpi['pct_ir']:.1f}% ya tiene intención alta de retiro.</strong>
    Actuar sobre la satisfacción laboral es la palanca más barata de retención.</p>
  </div>
</div>
""")
