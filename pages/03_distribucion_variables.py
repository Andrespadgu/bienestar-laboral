import streamlit as st
from utils.styles import inject_css, md
from utils.data_loader import load_data
from utils.stats import compute_kpis, compare_groups
from utils.charts import chart_cargo, chart_modal, chart_sex, chart_horas

st.set_page_config(page_title="03 · La Paradoja del Cargo", layout="wide", page_icon="◼")
inject_css()
df  = load_data()
kpi = compute_kpis(df)

_CFG = dict(use_container_width=True, config={"displayModeBar": False})

cargo_stats = compare_groups(df, "Tipo_Cargo", "BU_prom", threshold=3.0)
modal_stats = compare_groups(df, "Modalidad",  "DL_prom")

dir_pct = cargo_stats.get("Directivo",    {}).get("pct_above", 0.0)
op_pct  = cargo_stats.get("Operativo",    {}).get("pct_above", 0.0)
adm_pct = cargo_stats.get("Administrativo", {}).get("pct_above", 0.0)

pres_mean = modal_stats.get("Presencial", {}).get("mean", 0.0)
hyb_mean  = modal_stats.get("Híbrido",    {}).get("mean", pres_mean)
modal_diff = (hyb_mean - pres_mean) / pres_mean * 100 if pres_mean > 0 else 0

hyb_n  = int(modal_stats.get("Híbrido",    {}).get("n", 0))
pres_n = int(modal_stats.get("Presencial", {}).get("n", 0))

# ── HERO ────────────────────────────────────────────────────────────────────
md(f"""
<div class="hero-l">
  <div class="hero-l-bgn">03</div>
  <div class="hero-eyebrow-l">Capítulo 03 · La paradoja del cargo</div>
  <div class="hero-num-l" style="color:#C75B3C">{dir_pct:.1f}%</div>
  <div class="hero-lead-l">
    de los directivos (n={cargo_stats.get('Directivo',{}).get('n',0)}) supera el umbral de burnout
    — la tasa más alta por cargo. En operativos es {op_pct:.1f}%.
    El cargo no protege: expone.
  </div>
</div>
""")

# ── BURNOUT BY CARGO + MODAL ─────────────────────────────────────────────────
md("""
<div class="pad-l" style="padding-bottom:8px;">
  <span class="stag stag-n">La persona que menos esperabas encontrar aquí</span>
  <div class="ch-hd">El cargo no protege del agotamiento. Lo amplifica.</div>
  <div class="ch-cap">% que supera BU_prom &gt; 3 por tipo de cargo.</div>
  <div class="sp16"></div>
</div>
""")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(chart_cargo(df), **_CFG)
    md(f"""
    <div style="padding:0 0 8px 0;">
      <div class="insight">
        <p>Los directivos tienen la tasa de burnout más alta del estudio por cargo:
        <strong>{dir_pct:.1f}%</strong> vs {op_pct:.1f}% en operativos
        y {adm_pct:.1f}% en administrativos.
        El agotamiento del liderazgo se transmite hacia abajo.</p>
      </div>
    </div>
    """)

with col2:
    caveat = f"⚠ n={hyb_n} — muestra pequeña, interpretar con cautela." if hyb_n < 50 else ""
    sign_txt = f"+{modal_diff:.0f}% más" if modal_diff > 0 else f"{modal_diff:.0f}%"
    md(f"""
    <div class="pad-l" style="padding:0 0 8px 0;">
      <span class="stag stag-r">Paradoja del híbrido</span>
      <div class="ch-hd">La promesa de flexibilidad</div>
      <div class="ch-cap">Desgaste laboral (DL_prom) por modalidad. {caveat}</div>
      <div class="sp16"></div>
    </div>
    """)
    st.plotly_chart(chart_modal(df), **_CFG)
    md(f"""
    <div style="padding:0 0 8px 0;">
      <div class="insight">
        <p>Híbrido (n={hyb_n}): DL medio = {hyb_mean:.2f} ·
        Presencial (n={pres_n}): DL medio = {pres_mean:.2f}.
        Diferencia: <strong>{sign_txt} desgaste</strong> en modalidad híbrida.
        {"La flexibilidad puede esconder mayor disponibilidad exigida." if modal_diff > 0 else ""}
        {caveat}</p>
      </div>
    </div>
    """)

# ── DEMOGRAPHICS ─────────────────────────────────────────────────────────────
md("""
<div class="pad-alt" style="padding-bottom:8px;margin-top:8px;">
  <span class="stag stag-n">Demografía del riesgo</span>
  <div class="ch-hd">La carga no se reparte igual</div>
  <div class="ch-cap">Burnout, somatización e intención de retiro por sexo.</div>
  <div class="sp16"></div>
</div>
""")

col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(chart_sex(df), **_CFG)
with col4:
    md("""
    <div class="pad-alt" style="padding:0 0 8px 0;">
      <div class="ch-hd">Burnout por carga horaria</div>
      <div class="ch-cap">Media BU_prom por tramo de horas semanales.</div>
      <div class="sp16"></div>
    </div>
    """)
    st.plotly_chart(chart_horas(df), **_CFG)

n_over48 = int(kpi["pct_over48"] / 100 * kpi["n"])
md(f"""
<div class="pad-alt" style="padding-top:4px;padding-bottom:48px;">
  <div class="insight">
    <p>El {kpi['pct_over48']:.1f}% trabaja más de 48h semanales (n≈{n_over48}).
    Ese grupo concentra la mayor media de burnout por carga horaria.
    <strong>Más horas no es más productividad — es más riesgo.</strong>
    Media general de horas: {kpi['mean_hours']:.1f}h/semana.</p>
  </div>
</div>
""")
