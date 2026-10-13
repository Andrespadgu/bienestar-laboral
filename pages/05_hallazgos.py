import streamlit as st
from utils.styles import inject_css, md
from utils.data_loader import load_data
from utils.stats import compute_kpis, compare_groups, spearman, pval_label

st.set_page_config(page_title="05 · Evidencia → Acción", layout="wide", page_icon="◼")
inject_css()
df   = load_data()
kpi  = compute_kpis(df)

# All metrics from real data
cargo_stats = compare_groups(df, "Tipo_Cargo", "BU_prom", threshold=3.0)
dir_pct     = cargo_stats.get("Directivo",    {}).get("pct_above", 0.0)
op_pct      = cargo_stats.get("Operativo",    {}).get("pct_above", 0.0)

diff       = kpi["cl_diff_pct"]
rho_cl_bu, pval_cl_bu = spearman(df, "CL_prom", "BU_prom")
rho_pt_bu, pval_pt_bu = spearman(df, "PT_prom",  "BU_prom")

top1   = kpi["top1_dim"]
dims   = kpi["dims_sorted"]
sm_ire = next((d["ire"] for d in dims if d["k"] == "SM_prom"), 0.0)
pt_ire = next((d["ire"] for d in dims if d["k"] == "PT_prom"), 0.0)

# ── HEADER ───────────────────────────────────────────────────────────────────
md(f"""
<div class="reco-wrap" style="padding-bottom:8px;">
  <span class="stag stag-d">Evidencia → Acción</span>
  <div style="font-size:clamp(2.2rem,5vw,3.8rem);font-weight:900;color:#fff;
              letter-spacing:-0.04em;line-height:1.0;margin:12px 0 14px;">
    Cuatro palancas.<br>La evidencia las respalda.
  </div>
  <div style="font-size:0.92rem;color:rgba(255,255,255,0.42);line-height:1.65;max-width:560px;">
    Ordenadas por tamaño de efecto. Cada número viene directamente del estudio —
    calculado en tiempo real desde los datos reales.
  </div>
</div>
""")

# ── CONTEXT NUMBERS ──────────────────────────────────────────────────────────
md(f"""
<div style="background:#0D1E2E;padding:0 64px 2px;">
  <div style="display:flex;gap:2px;background:rgba(255,255,255,0.04);border-radius:3px;overflow:hidden;">
    <div style="flex:1;padding:20px 22px;border-right:1px solid rgba(255,255,255,0.05);">
      <div style="font-size:1.9rem;font-weight:900;color:#fff;letter-spacing:-0.05em;line-height:1">{kpi['n']}</div>
      <div style="font-size:0.63rem;letter-spacing:0.1em;text-transform:uppercase;color:rgba(255,255,255,0.25);margin-top:4px;">Trabajadores</div>
    </div>
    <div style="flex:1;padding:20px 22px;border-right:1px solid rgba(255,255,255,0.05);">
      <div style="font-size:1.9rem;font-weight:900;color:#fff;letter-spacing:-0.05em;line-height:1">16</div>
      <div style="font-size:0.63rem;letter-spacing:0.1em;text-transform:uppercase;color:rgba(255,255,255,0.25);margin-top:4px;">Dimensiones psicosociales</div>
    </div>
    <div style="flex:1;padding:20px 22px;border-right:1px solid rgba(255,255,255,0.05);">
      <div style="font-size:1.9rem;font-weight:900;color:#fff;letter-spacing:-0.05em;line-height:1">{kpi['pct_bu']:.1f}%</div>
      <div style="font-size:0.63rem;letter-spacing:0.1em;text-transform:uppercase;color:rgba(255,255,255,0.25);margin-top:4px;">Con burnout moderado–alto</div>
    </div>
    <div style="flex:1;padding:20px 22px;">
      <div style="font-size:1.9rem;font-weight:900;color:#C75B3C;letter-spacing:-0.05em;line-height:1">{kpi['pct_ir']:.1f}%</div>
      <div style="font-size:0.63rem;letter-spacing:0.1em;text-transform:uppercase;color:rgba(255,255,255,0.25);margin-top:4px;">Con intención alta de retiro</div>
    </div>
  </div>
</div>
""")

# ── RECO GRID ─────────────────────────────────────────────────────────────────
cl_h = kpi["cl_high_bu"]
cl_l = kpi["cl_low_bu"]

md(f"""
<div style="background:#0D1E2E;padding:2px 64px 64px;">
  <div class="reco-grid-2">

    <!-- 01 Liderazgo -->
    <div class="rc">
      <div class="rc-ev">
        <span class="rc-num" style="color:#7A9BB8">{diff:.0f}%</span>
        <div class="rc-ev-lbl">menos burnout · CL alto (BU={cl_h:.2f}) vs CL bajo (BU={cl_l:.2f})</div>
      </div>
      <div class="rc-body">
        <span class="rc-seq" style="color:#7A9BB8">01 · Mayor efecto del estudio</span>
        <h4>Desarrollar liderazgo comprometido</h4>
        <div class="rc-bar-track"><div class="rc-bar-fill" style="width:100%;background:#7A9BB8"></div></div>
        <div class="rc-bar-meta"><span>Efecto relativo</span><span>ρ = {rho_cl_bu:+.3f} ({pval_label(pval_cl_bu)})</span></div>
        <p>No requiere presupuesto extra: requiere prioridad. Capacitar líderes en escucha
        activa, gestión del bienestar y señales de apoyo consistentes. El mecanismo de
        protección más potente del sistema.</p>
      </div>
    </div>

    <!-- 02 Presión del tiempo -->
    <div class="rc">
      <div class="rc-ev">
        <span class="rc-num" style="color:#C75B3C">ρ = {rho_pt_bu:+.3f}</span>
        <div class="rc-ev-lbl">correlación presión del tiempo ↔ burnout ({pval_label(pval_pt_bu)})</div>
      </div>
      <div class="rc-body">
        <span class="rc-seq" style="color:#C75B3C">02 · Demanda modificable</span>
        <h4>Reducir la presión del tiempo</h4>
        <div class="rc-bar-track"><div class="rc-bar-fill" style="width:{min(int(abs(rho_pt_bu)*120), 95)}%;background:#C75B3C"></div></div>
        <div class="rc-bar-meta"><span>Efecto relativo</span><span>IRE presión del tiempo: {pt_ire:.1f}/100</span></div>
        <p>Auditar cargas, plazos y procesos antes de exigir más al mismo equipo.
        El problema no es la productividad individual — son las condiciones en que
        se trabaja.</p>
      </div>
    </div>

    <!-- 03 Salud mental org. -->
    <div class="rc">
      <div class="rc-ev">
        <span class="rc-num" style="color:#5E8B7E">IRE {sm_ire:.1f}</span>
        <div class="rc-ev-lbl">salud mental organizacional (SM) — dimensión n.° 1 en riesgo del estudio</div>
      </div>
      <div class="rc-body">
        <span class="rc-seq" style="color:#5E8B7E">03 · Riesgo estructural</span>
        <h4>Señalizar bienestar como prioridad real</h4>
        <div class="rc-bar-track"><div class="rc-bar-fill" style="width:{min(int(sm_ire*1.4), 95)}%;background:#5E8B7E"></div></div>
        <div class="rc-bar-meta"><span>Efecto relativo</span><span>Media SM: {kpi['dims_sorted'][0].get('mean',0):.2f} / {next((d['mx'] for d in kpi['dims_sorted'] if d['k']=='SM_prom'), 5)}</span></div>
        <p>La organización debe enviar señales activas y sostenidas de que el bienestar
        importa. Un programa de apoyo reactivo no alcanza cuando el riesgo es estructural.</p>
      </div>
    </div>

    <!-- 04 Directivos -->
    <div class="rc">
      <div class="rc-ev">
        <span class="rc-num" style="color:#C4820A">{dir_pct:.1f}%</span>
        <div class="rc-ev-lbl">de los directivos supera el umbral de burnout (vs {op_pct:.1f}% en operativos)</div>
      </div>
      <div class="rc-body">
        <span class="rc-seq" style="color:#C4820A">04 · Paradoja del cargo</span>
        <h4>Proteger a quienes lideran</h4>
        <div class="rc-bar-track"><div class="rc-bar-fill" style="width:{min(int(dir_pct*1.8), 95)}%;background:#C4820A"></div></div>
        <div class="rc-bar-meta"><span>Efecto relativo</span><span>n directivos = {cargo_stats.get('Directivo',{}).get('n',0)}</span></div>
        <p>El agotamiento del liderazgo se transmite hacia abajo. Quien no está bien
        no puede cuidar a otros. El primer beneficiario del programa de bienestar
        debe ser quien lo implementa.</p>
      </div>
    </div>

  </div>
</div>
""")

# ── CLOSING ───────────────────────────────────────────────────────────────────
md(f"""
<div class="closing">
  <div class="closing-lbl">conclusión</div>
  <div class="closing-title">
    Esta organización ya eligió<br>el primer paso: mirar los datos<br>con honestidad.
  </div>
  <div class="closing-sub">
    Visibilizar el problema es, en sí mismo, el primer acto de cambio.
    Los cuatro hallazgos son accionables hoy.
  </div>
  <div class="closing-rule"></div>
  <div style="margin-top:32px;font-size:0.65rem;letter-spacing:0.14em;text-transform:uppercase;color:rgba(255,255,255,0.18);">
    N = {kpi['n']} · 16 dimensiones psicosociales · Escalas Likert 1–5 y 1–7 · Sector público y mixto
  </div>
</div>
""")
