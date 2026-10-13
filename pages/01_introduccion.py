import streamlit as st
from utils.styles import md
from utils.data_loader import load_data
from utils.stats import compute_kpis
from utils.charts import chart_ire, chart_jdr

df  = load_data()
kpi = compute_kpis(df)

_CFG = dict(use_container_width=True, config={"displayModeBar": False})

top1   = kpi["top1_dim"]
bot1   = kpi["bottom1_dim"]
top3   = kpi["top3_dims"]
dims   = kpi["dims_sorted"]

# rank of burnout (1 = highest risk)
bu_rank = next((i + 1 for i, d in enumerate(dims) if d["k"] == "BU_prom"), "—")

# ── HERO ────────────────────────────────────────────────────────────────────
md(f"""
<div class="hero-l">
  <div class="hero-l-bgn">01</div>
  <div class="hero-eyebrow-l">Capítulo 01 · El mapa del riesgo</div>
  <div class="hero-num-l">El burnout<br>no es el peor problema</div>
  <div class="hero-lead-l">
    {top1.get('lb','—')} lidera el riesgo con IRE {top1.get('ire', 0):.1f}.
    El burnout aparece en el puesto {bu_rank}. El sistema falla donde menos se ve.
  </div>
</div>
""")

# ── CONTEXT STRIP ───────────────────────────────────────────────────────────
n_women   = (df["Sexo"] == "Mujer").sum()
pct_women = n_women / len(df) * 100
pct_pub   = (df["Sector"] == "Público").sum() / len(df) * 100
mean_hrs  = df["Horas_Semana"].mean()
pct_48    = (df["Horas_Semana"] > 48).mean() * 100
pct_smlv  = (df["Ingreso"] == "Entre 1 y 3 SMLV").mean() * 100 if "Ingreso" in df.columns else 81.5

md(f"""
<div class="stat-strip">
  <div class="stat-cell">
    <div class="stat-n" style="color:#0D1E2E">{len(df)}</div>
    <div class="stat-lbl">Trabajadores · sector público y mixto</div>
  </div>
  <div class="stat-cell">
    <div class="stat-n" style="color:#2E5A87">{pct_women:.1f}%</div>
    <div class="stat-lbl">Mujeres en la muestra</div>
  </div>
  <div class="stat-cell">
    <div class="stat-n" style="color:#2E5A87">{pct_pub:.1f}%</div>
    <div class="stat-lbl">Sector público</div>
  </div>
  <div class="stat-cell">
    <div class="stat-n" style="color:#2E5A87">{mean_hrs:.1f}h</div>
    <div class="stat-lbl">Promedio semanal · {pct_48:.0f}% supera 48h</div>
  </div>
  <div class="stat-cell">
    <div class="stat-n" style="color:#2E5A87">{pct_smlv:.1f}%</div>
    <div class="stat-lbl">Gana entre 1 y 3 SMLV</div>
  </div>
</div>
""")

# ── IRE CHART ───────────────────────────────────────────────────────────────
md(f"""
<div class="pad-l" style="padding-bottom:8px;">
  <span class="sec-lbl">Índice de Riesgo Estandarizado · 0–100 · {len(dims)} dimensiones</span>
  <div class="ch-hd">Las dimensiones más deterioradas no son las más visibles</div>
  <div class="ch-cap">Azul = recursos deteriorados &nbsp;·&nbsp; Coral = demandas / resultados negativos &nbsp;·&nbsp; Top 3 a color completo</div>
  <div class="sp16"></div>
</div>
""")

col_chart, col_aside = st.columns([3, 1])
with col_chart:
    st.plotly_chart(chart_ire(df), **_CFG)
with col_aside:
    second = dims[1] if len(dims) > 1 else {}
    md(f"""
    <div style="padding: 32px 16px 0 8px;">
      <div style="margin-bottom:32px;">
        <div class="sec-lbl">Mayor riesgo</div>
        <div style="font-size:2.6rem;font-weight:900;color:#0D1E2E;letter-spacing:-0.05em;line-height:1">{top1.get('ire', 0):.1f}</div>
        <div style="font-size:0.78rem;color:#5C6E80;margin-top:4px;">{top1.get('lb','—')}</div>
      </div>
      <div style="margin-bottom:32px;">
        <div class="sec-lbl">2.° mayor riesgo</div>
        <div style="font-size:2.6rem;font-weight:900;color:#0D1E2E;letter-spacing:-0.05em;line-height:1">{second.get('ire', 0):.1f}</div>
        <div style="font-size:0.78rem;color:#5C6E80;margin-top:4px;">{second.get('lb','—')}</div>
      </div>
      <div style="border-top:1px solid rgba(0,0,0,0.07);padding-top:20px;">
        <div class="sec-lbl">Menor riesgo</div>
        <div style="font-size:2.6rem;font-weight:900;color:#0D1E2E;letter-spacing:-0.05em;line-height:1">{bot1.get('ire', 0):.1f}</div>
        <div style="font-size:0.78rem;color:#5C6E80;margin-top:4px;">{bot1.get('lb','—')}</div>
      </div>
      <div style="border-top:1px solid rgba(0,0,0,0.07);padding-top:18px;margin-top:24px;">
        <div class="sec-lbl">Nota metodológica</div>
        <div style="font-size:0.72rem;color:#5C6E80;line-height:1.6;">
          IRE escala 0–100.<br>
          Recursos: IRE alto = deterioro.<br>
          Demandas: IRE alto = sobrecarga.
        </div>
      </div>
    </div>
    """)

# ── INSIGHT ─────────────────────────────────────────────────────────────────
top3_txt = " · ".join(f"{d['lb']} ({d['ire']:.1f})" for d in top3)
md(f"""
<div class="pad-l" style="padding-top:0;padding-bottom:40px;">
  <div class="insight">
    <p>Top 3 en riesgo: <strong>{top3_txt}</strong>.
    El sistema no falla donde se ve. {top1.get('lb','—')} (IRE {top1.get('ire',0):.1f}) encabeza el riesgo
    porque toca lo más básico: si la organización cuida a las personas.
    El burnout —puesto {bu_rank}— es consecuencia, no causa.</p>
  </div>
</div>
""")

# ── JDR BALANCE ─────────────────────────────────────────────────────────────
md("""
<div class="pad-alt" style="padding-bottom:8px;">
  <span class="stag stag-r">Modelo Demandas–Recursos</span>
  <div class="ch-hd">Los recursos fallan más que las demandas</div>
  <div class="ch-cap">IRE promedio por tipo de dimensión. El sistema exige más de lo que provee.</div>
  <div class="sp16"></div>
</div>
""")
st.plotly_chart(chart_jdr(df), **_CFG)

from utils.stats import compute_ire
dims_data = compute_ire(df)
avg_res = sum(d["ire"] for d in dims_data if d["t"] in ("resource","protective")) / max(1, sum(1 for d in dims_data if d["t"] in ("resource","protective")))
avg_dem = sum(d["ire"] for d in dims_data if d["t"] in ("demand","negative")) / max(1, sum(1 for d in dims_data if d["t"] in ("demand","negative")))

md(f"""
<div class="pad-alt" style="padding-top:0;padding-bottom:48px;">
  <div class="insight">
    <p>IRE medio de recursos/protectores: <strong>{avg_res:.1f}</strong> ·
    IRE medio de demandas/negativos: <strong>{avg_dem:.1f}</strong>.
    {"El sistema exige más de lo que provee." if avg_res > avg_dem else "Demandas y recursos están en desequilibrio."}
    Cuando los recursos fallan, ningún nivel de resiliencia individual alcanza a compensar.</p>
  </div>
</div>
""")
