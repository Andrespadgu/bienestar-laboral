import streamlit as st
from utils.styles import inject_css, md
from utils.data_loader import load_data
from utils.stats import compute_kpis

st.set_page_config(
    page_title="Bienestar Laboral — EDA",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

df  = load_data()
kpi = compute_kpis(df)

md(f"""
<div class="cover-wrap">
  <div>
    <div class="cover-eyebrow">Análisis Exploratorio de Datos · 2025</div>
    <div class="cover-title">BIENESTAR<br>LABORAL</div>
    <div class="cover-sub">
      Una historia sobre agotamiento, liderazgo y las señales<br>
      que una organización envía —o deja de enviar.
    </div>
    <div class="cover-rule"></div>
    <div style="font-size:0.72rem;color:rgba(255,255,255,0.28);letter-spacing:0.12em;text-transform:uppercase;">
      Navega por los capítulos en el menú lateral →
    </div>
  </div>

  <div class="cover-stats">
    <div class="cover-stat">
      <div class="cover-stat-n">{kpi['n']}</div>
      <div class="cover-stat-lbl">Trabajadores</div>
    </div>
    <div class="cover-stat">
      <div class="cover-stat-n">16</div>
      <div class="cover-stat-lbl">Dimensiones psicosociales</div>
    </div>
    <div class="cover-stat">
      <div class="cover-stat-n" style="color:#C75B3C">{kpi['pct_bu']:.1f}%</div>
      <div class="cover-stat-lbl">Con burnout moderado–alto</div>
    </div>
    <div class="cover-stat">
      <div class="cover-stat-n" style="color:#5E8B7E">{kpi['cl_diff_pct']:.0f}%</div>
      <div class="cover-stat-lbl">Menos burnout con buen liderazgo</div>
    </div>
    <div class="cover-stat">
      <div class="cover-stat-n" style="color:#C75B3C">{kpi['pct_ir']:.1f}%</div>
      <div class="cover-stat-lbl">Con intención alta de retiro</div>
    </div>
  </div>
</div>
""")
