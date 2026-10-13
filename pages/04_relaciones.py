import streamlit as st
from utils.styles import md
from utils.data_loader import load_data
from utils.stats import compute_kpis, compute_correlations, spearman, pval_label
from utils.charts import chart_cl, chart_corr

df   = load_data()
kpi  = compute_kpis(df)
corrs = compute_correlations(df)

_CFG = dict(use_container_width=True, config={"displayModeBar": False})

rho_cl_bu,  pval_cl_bu  = spearman(df, "CL_prom", "BU_prom")
rho_cl_sat, pval_cl_sat = spearman(df, "CL_prom", "SAT_prom")
rho_pt_bu,  pval_pt_bu  = spearman(df, "PT_prom",  "BU_prom")
rho_bp_bu,  pval_bp_bu  = spearman(df, "BP_prom",  "BU_prom")
rho_bu_dl,  pval_bu_dl  = spearman(df, "BU_prom",  "DL_prom")

diff     = kpi["cl_diff_pct"]
cl_h_bu  = kpi["cl_high_bu"]
cl_l_bu  = kpi["cl_low_bu"]
n_cl_h   = kpi["n_cl_high"]
n_cl_l   = kpi["n_cl_low"]

# ── HERO ────────────────────────────────────────────────────────────────────
md(f"""
<div class="hero-d">
  <div class="hero-d-bgn">04</div>
  <div class="hero-eyebrow-d">Capítulo 04 · El factor protector</div>
  <div class="hero-num-d" style="color:#5E8B7E">{diff:.0f}%</div>
  <div class="hero-lead-d">
    menos burnout en equipos con liderazgo comprometido (n={n_cl_h} vs n={n_cl_l}).
    No es un factor blando — es el mecanismo de protección más potente del sistema.
    ρ = {rho_cl_bu:+.3f} ({pval_label(pval_cl_bu)}).
  </div>
</div>
""")

# ── CL STATS STRIP ───────────────────────────────────────────────────────────
md(f"""
<div class="stat-strip-d">
  <div class="stat-cell-d">
    <div class="stat-n" style="color:#5E8B7E">{cl_h_bu:.2f}</div>
    <div class="stat-lbl" style="color:rgba(255,255,255,0.4);">BU medio · CL &gt; 3.5 (n={n_cl_h})</div>
  </div>
  <div class="stat-cell-d">
    <div class="stat-n" style="color:#C75B3C">{cl_l_bu:.2f}</div>
    <div class="stat-lbl" style="color:rgba(255,255,255,0.4);">BU medio · CL ≤ 3.5 (n={n_cl_l})</div>
  </div>
  <div class="stat-cell-d">
    <div class="stat-n" style="color:rgba(255,255,255,0.9)">{rho_cl_bu:+.3f}</div>
    <div class="stat-lbl" style="color:rgba(255,255,255,0.4);">ρ Spearman CL ↔ BU ({pval_label(pval_cl_bu)})</div>
  </div>
  <div class="stat-cell-d">
    <div class="stat-n" style="color:#5E8B7E">{rho_cl_sat:+.3f}</div>
    <div class="stat-lbl" style="color:rgba(255,255,255,0.4);">ρ CL ↔ SAT ({pval_label(pval_cl_sat)})</div>
  </div>
</div>
""")

# ── CL CHART ─────────────────────────────────────────────────────────────────
md(f"""
<div class="pad-l" style="padding-bottom:8px;">
  <span class="stag stag-r">Comparativa liderazgo comprometido vs. débil</span>
  <div class="ch-hd">Una sola variable lo cambia todo</div>
  <div class="ch-cap">Media de BU_prom según CL_prom &gt; 3.5 (comprometido) vs ≤ 3.5 (débil).</div>
  <div class="sp16"></div>
</div>
""")

col1, col2 = st.columns([2, 3])
with col1:
    st.plotly_chart(chart_cl(df), **_CFG)
with col2:
    md(f"""
    <div style="padding:32px 24px 0 40px;">
      <div style="margin-bottom:32px;">
        <div class="sec-lbl">La diferencia</div>
        <div style="font-size:5rem;font-weight:900;color:#C75B3C;letter-spacing:-0.05em;line-height:0.9">+{diff:.0f}%</div>
        <div style="font-size:0.9rem;color:#5C6E80;margin-top:10px;line-height:1.6;">
          más burnout cuando el liderazgo<br>no está comprometido
        </div>
      </div>
      <div style="border-top:1px solid rgba(0,0,0,0.07);padding-top:24px;">
        <div class="sec-lbl">Correlaciones de soporte</div>
        <div style="font-size:0.82rem;color:#5C6E80;line-height:1.85;">
          CL ↔ BU: ρ = {rho_cl_bu:+.3f} ({pval_label(pval_cl_bu)})<br>
          CL ↔ SAT: ρ = {rho_cl_sat:+.3f} ({pval_label(pval_cl_sat)})<br>
          PT ↔ BU: ρ = {rho_pt_bu:+.3f} ({pval_label(pval_pt_bu)})<br>
          BP ↔ BU: ρ = {rho_bp_bu:+.3f} ({pval_label(pval_bp_bu)})
        </div>
      </div>
    </div>
    """)

md(f"""
<div class="pad-l" style="padding-top:8px;padding-bottom:48px;">
  <div class="insight">
    <p>CL ↔ BU: ρ = {rho_cl_bu:+.3f} ({pval_label(pval_cl_bu)}). El liderazgo actúa como buffer:
    absorbe presión, genera señales de seguridad y provee recursos donde la organización
    no llega. Cuando falta, cada demanda se amplifica sin amortiguador.</p>
  </div>
</div>
""")

# ── CORRELATIONS ─────────────────────────────────────────────────────────────
md("""
<div class="pad-alt" style="padding-bottom:8px;">
  <span class="stag stag-r">Top correlaciones Spearman · calculadas desde los datos reales</span>
  <div class="ch-hd">El diagrama de fuerzas</div>
  <div class="ch-cap">Verde = factor protector · Coral = factor dañino · Todos los ρ calculados en tiempo real.</div>
  <div class="sp16"></div>
</div>
""")

col3, col4 = st.columns([3, 2])
with col3:
    st.plotly_chart(chart_corr(df), **_CFG)
with col4:
    top_corr = corrs[0] if corrs else {}
    prot = [(c["a"], c["rho"], c["pval"]) for c in corrs if c["dir"] == "protective"]
    harm = [(c["a"], c["rho"], c["pval"]) for c in corrs if c["dir"] == "harmful"]

    prot_lines = "".join(
        f'{a}: ρ = {r:+.3f} ({pval_label(p)})<br>'
        for a, r, p in prot
    )
    harm_lines = "".join(
        f'{a}: ρ = {r:+.3f} ({pval_label(p)})<br>'
        for a, r, p in harm
    )

    md(f"""
    <div style="padding:16px 16px 0 32px;">
      <div style="margin-bottom:20px;padding-bottom:20px;border-bottom:1px solid rgba(0,0,0,0.07);">
        <div class="sec-lbl">Correlación dominante</div>
        <div style="font-size:2.2rem;font-weight:900;color:#C75B3C;letter-spacing:-0.04em;line-height:1">{top_corr.get('rho', 0):+.3f}</div>
        <div style="font-size:0.75rem;color:#5C6E80;margin-top:4px;">{top_corr.get('a','—')} · {pval_label(top_corr.get('pval', 1))}</div>
      </div>
      <div style="font-size:0.78rem;color:#5C6E80;line-height:1.85;">
        <div style="margin-bottom:10px;"><strong style="color:#5E8B7E">Protectores:</strong><br>
          {prot_lines or "—"}
        </div>
        <div><strong style="color:#C75B3C">Dañinos:</strong><br>
          {harm_lines or "—"}
        </div>
      </div>
    </div>
    """)

md(f"""
<div class="pad-alt" style="padding-top:4px;padding-bottom:48px;">
  <div class="insight">
    <p>PT ↔ BU: ρ = {rho_pt_bu:+.3f} ({pval_label(pval_pt_bu)}) — la presión del tiempo
    es el predictor de burnout más accionable entre las demandas.
    BP ↔ BU: ρ = {rho_bp_bu:+.3f} ({pval_label(pval_bp_bu)}) — el bienestar percibido
    es el mayor escudo entre los recursos. El sistema tiene dos palancas claras:
    reducir PT y fortalecer BP.</p>
  </div>
</div>
""")
