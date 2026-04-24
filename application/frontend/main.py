import requests
import textwrap
import streamlit as st
import streamlit.components.v1 as components

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TPLANT — Plant Tree, Create a Green Future",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── NUKE ALL STREAMLIT CHROME ────────────────────────────────────────────────
st.markdown("""
<style>
/* Remove ALL Streamlit chrome */
#MainMenu { visibility: hidden !important; display: none !important; }
header[data-testid="stHeader"] { visibility: hidden !important; display: none !important; height: 0 !important; }
footer { visibility: hidden !important; display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.viewerBadge_container__r5tak { display: none !important; }
.viewerBadge_link__qRIco { display: none !important; }

.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}
[data-testid="stAppViewContainer"] {
    background: #1A0F07 !important;
    padding: 0 !important;
    margin: 0 !important;
}
[data-testid="stVerticalBlock"] {
    gap: 0 !important;
    padding: 0 !important;
}
[data-testid="stMain"] {
    padding: 0 !important;
}
.main .block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}
[data-testid="stVerticalBlock"] > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
iframe {
    display: block !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

# ── CONSTANTS ────────────────────────────────────────────────────────────────
API_URL        = "http://127.0.0.1:8000/predict/"
API_SAMPLE_URL = "http://127.0.0.1:8000/sample-condition/"

SOIL_TYPES        = ["Alluvial","Chalky","Clayey","Laterite","Loamy","Peaty","Saline","Sandy","Silty"]
PLANT_CATEGORIES  = ["cereal","legume","vegetable"]
THERMAL_REGIMES   = ["cold","optimal","heat_stress"]
MOISTURE_REGIMES  = ["dry","optimal","waterlogged"]
NUTRIENT_BALANCES = ["optimal","deficient","excessive"]
MODEL_FEATURES    = 21

# ── HELPERS ──────────────────────────────────────────────────────────────────
def get_sample_data():
    try:
        r = requests.get(API_SAMPLE_URL, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return {"soil_moisture":25,"nitrogen":100,"soil_ph":6.5,"risk_level":12.4,"soil_type":"Alluvial"}

def go_to_form():
    st.session_state.page = "form"
    st.rerun()

def go_to_landing():
    st.session_state.page = "landing"
    st.rerun()

def inject_css(css: str):
    components.html(f"<style>{css}</style>", height=0)

GLOBAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap');

:root {
  --soil:#1A0F07; --copper:#B5622A; --amber:#D4894A;
  --wheat:#E8C98A; --cream:#F5EDD8; --sage:#607A5E;
  --stone:#8A8070;
}

#MainMenu,header,footer { visibility:hidden !important; display:none !important; }
[data-testid="stToolbar"] { display:none !important; }
[data-testid="stDecoration"] { display:none !important; }
.block-container { padding:0 !important; max-width:100% !important; }
[data-testid="stAppViewContainer"] { background:#1A0F07 !important; }
[data-testid="stVerticalBlock"] { gap:0 !important; }
section[data-testid="stSidebar"] { display:none !important; }
* { font-family:'Outfit',sans-serif; box-sizing:border-box; }

.stButton>button {
  width:100% !important;
  background:linear-gradient(145deg,#D4894A,#B5622A) !important;
  color:#1A0F07 !important; border:1px solid rgba(223,161,96,.35) !important;
  border-radius:6px !important; padding:14px !important;
  font-family:'DM Mono',monospace !important; font-size:.68rem !important;
  font-weight:700 !important; letter-spacing:.2em !important; text-transform:uppercase !important;
}
.stButton>button:hover { background:linear-gradient(145deg,#e8a060,#c47030) !important; }

.panel { background:rgba(255,255,255,.02); border:1px solid rgba(196,116,57,.17); border-radius:14px; overflow:hidden; padding:20px; margin-top:14px; }
.section-block { padding:22px 0; border-bottom:1px solid rgba(196,116,57,.12); }
.section-title { font-family:'Cormorant Garamond',serif; font-size:1.08rem; font-weight:600; color:#E8C98A; }
.section-num { background:rgba(255,255,255,.04); color:#D4894A; padding:2px 7px; border-radius:3px; margin-right:8px; font-family:'DM Mono',monospace; font-size:.62rem; }
.metric-card { background:rgba(255,255,255,.03); border:1px solid rgba(196,116,57,.18); border-radius:12px; padding:16px 12px; text-align:center; position:relative; }
.metric-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; background:#B5622A; opacity:.5; }
.metric-value { font-family:'Cormorant Garamond',serif; font-size:2rem; font-weight:600; color:#E8C98A; line-height:1; margin-bottom:4px; }
.metric-label { font-family:'DM Mono',monospace; font-size:.58rem; letter-spacing:.16em; text-transform:uppercase; color:#8A8070; }
.summary-card { background:rgba(255,255,255,.02); border:1px solid rgba(196,116,57,.17); border-radius:14px; overflow:hidden; }
.summary-header { background:rgba(0,0,0,.2); padding:16px 18px; }
.summary-header-title { font-family:'DM Mono',monospace; font-size:.62rem; letter-spacing:.2em; text-transform:uppercase; color:#E8C98A; }
.summary-body { padding:14px 18px; }
.summary-row { display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px dashed rgba(168,154,133,.18); }
.summary-row:last-child { border-bottom:none; }
.summary-key { font-family:'DM Mono',monospace; font-size:.58rem; letter-spacing:.12em; text-transform:uppercase; color:#8A8070; }
.summary-val { font-size:.82rem; font-weight:600; color:#F5EDD8; }
.result-card { background:rgba(255,255,255,.02); border:1px solid rgba(196,116,57,.17); border-radius:14px; overflow:hidden; margin-top:14px; }
.result-head { padding:14px 18px; border-bottom:1px solid rgba(196,116,57,.16); font-family:'Cormorant Garamond',serif; font-size:1rem; font-weight:600; color:#E8C98A; }
.result-body { padding:14px 18px 18px; }
.risk-label { font-family:'DM Mono',monospace; font-size:.58rem; letter-spacing:.15em; text-transform:uppercase; color:#8A8070; margin-bottom:8px; }
.risk-bar-bg { background:rgba(255,255,255,.1); border-radius:4px; height:8px; overflow:hidden; }
.risk-bar-fill { height:100%; border-radius:4px; background:linear-gradient(90deg,#607A5E,#B5622A); }
.risk-value { margin-top:8px; font-family:'Cormorant Garamond',serif; font-size:1.9rem; font-weight:600; color:#E8C98A; text-align:center; }
.risk-desc { margin-top:3px; font-size:.8rem; color:#8A8070; text-align:center; font-style:italic; }

label, .stNumberInput label, .stSelectbox label {
  font-family:'DM Mono',monospace !important; font-size:.6rem !important;
  letter-spacing:.12em !important; text-transform:uppercase !important;
  color:#8A8070 !important; font-weight:500 !important;
}
.stSelectbox>div>div, .stNumberInput>div>div>input, input[readonly] {
  background:rgba(255,255,255,.06) !important;
  border:1px solid rgba(196,116,57,.2) !important;
  border-radius:8px !important; color:#F5EDD8 !important;
}
"""


# ════════════════════════════════════════════════════════════════════════════
# LANDING PAGE — full viewport, no Streamlit chrome, no scroll
# ════════════════════════════════════════════════════════════════════════════
def render_landing():
    sd           = get_sample_data()
    moisture_val = sd.get("soil_moisture", 25)
    nitrogen_val = sd.get("nitrogen", 100)
    ph_val       = sd.get("soil_ph", 6.5)
    risk_val     = sd.get("risk_level", 12.4)
    soil_name    = sd.get("soil_type", "Alluvial")
    mw = min(100, (moisture_val / 40)  * 100)
    nw = min(100, (nitrogen_val / 150) * 100)
    pw = min(100, (ph_val / 8)         * 100)
    rw = min(100, risk_val)

    landing_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{
  width:100%; height:100%;
  overflow:hidden;
  background:#1A0F07;
  font-family:'Outfit',sans-serif;
}}

.hero {{
  width:100vw; height:100vh;
  position:relative; overflow:hidden;
  background:
    radial-gradient(ellipse 65% 70% at 80% 50%, rgba(61,92,59,.22) 0%, transparent 65%),
    radial-gradient(ellipse 55% 80% at 15% 65%, rgba(181,98,42,.13) 0%, transparent 60%),
    linear-gradient(155deg, #0E0805 0%, #1A0D06 35%, #2A1A0C 65%, #1A0F07 100%);
  display:flex; flex-direction:column;
}}
.hero::before {{
  content:''; position:absolute; inset:0; pointer-events:none;
  background-image:
    linear-gradient(rgba(181,98,42,.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(181,98,42,.035) 1px, transparent 1px);
  background-size:72px 72px;
  mask-image:radial-gradient(ellipse 75% 75% at 50% 50%, black, transparent);
  -webkit-mask-image:radial-gradient(ellipse 75% 75% at 50% 50%, black, transparent);
}}

.orb {{ position:absolute; border-radius:50%; filter:blur(90px); pointer-events:none; animation:orbFloat 9s ease-in-out infinite alternate; }}
.orb1 {{ width:550px; height:550px; right:-100px; top:-120px; background:rgba(50,80,48,.2); }}
.orb2 {{ width:320px; height:320px; left:5%; bottom:5%; background:rgba(181,98,42,.11); animation-delay:4s; }}
@keyframes orbFloat {{ 0%{{transform:translate(0,0)}} 100%{{transform:translate(20px,-20px)}} }}

/* NAVBAR */
.navbar {{
  position:relative; z-index:10;
  padding:20px 56px;
  display:flex; align-items:center; justify-content:space-between;
  flex-shrink:0;
}}
.nav-logo {{ font-family:'Cormorant Garamond',serif; font-size:1.5rem; font-weight:600; letter-spacing:.08em; color:#F5EDD8; }}
.nav-logo span {{ color:#B5622A; }}
.nav-cta {{
  font-family:'DM Mono',monospace; font-size:.62rem; letter-spacing:.2em; text-transform:uppercase;
  background:rgba(96,122,94,.2); color:#A8C4A6;
  border:1px solid rgba(96,122,94,.4); border-radius:6px; padding:10px 22px;
  cursor:pointer; transition:background .2s;
}}
.nav-cta:hover {{ background:rgba(96,122,94,.35); }}

/* HERO BODY */
.hero-content {{
  flex:1; display:flex; flex-direction:column; justify-content:flex-start;
  position:relative; z-index:2;
  padding:20px 56px 30px;
  height:100%;
  overflow:hidden;
}}
.hero-body {{
  display:grid; grid-template-columns:1fr 380px;
  gap:30px; align-items:center;
  height:100%;
}}

.badge {{
  display:inline-flex; align-items:center; gap:12px;
  font-family:'DM Mono',monospace; font-size:.62rem; letter-spacing:.28em; text-transform:uppercase;
  color:#B5622A; margin-bottom:20px; width:fit-content;
}}
.badge::before {{ content:''; width:38px; height:1px; background:#B5622A; }}

.hero-h1 {{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(2.2rem, 3.5vw, 4.2rem);
  font-weight:700; line-height:0.95; letter-spacing:-.02em;
  margin-bottom:12px; color:#F5EDD8;
}}
.hero-h1 em {{ font-style:italic; font-weight:300; color:#B5622A; display:block; }}
.hero-h1 .out {{ display:block; -webkit-text-stroke:1px rgba(232,201,138,.28); color:transparent; }}

.hero-sub {{
  font-size:.78rem; font-weight:300; color:#8A8070; line-height:1.6;
  max-width:450px; margin-bottom:20px;
}}
.hero-sub strong {{ color:#E8C98A; font-weight:600; }}

.cta-row {{ display:flex; gap:14px; align-items:center; }}
.btn-primary {{
  font-family:'DM Mono',monospace; font-size:.62rem; font-weight:700;
  letter-spacing:.2em; text-transform:uppercase;
  background:#D4894A; color:#1A0F07;
  border:none; border-radius:6px; padding:10px 20px;
  cursor:pointer; transition:background .2s; white-space:nowrap;
}}
.btn-primary:hover {{ background:#e8a060; }}

/* DATA CARD */
.data-card {{
  background:rgba(255,255,255,.035);
  border:1px solid rgba(181,98,42,.25);
  border-radius:16px; padding:16px 14px;
  backdrop-filter:blur(14px);
  height:fit-content;
}}
.ctitle {{
  font-family:'DM Mono',monospace; font-size:.58rem; letter-spacing:.22em; text-transform:uppercase;
  color:#8A8070; margin-bottom:18px; text-align:center;
}}
.meter {{ margin-bottom:13px; }}
.mt {{ display:flex; justify-content:space-between; margin-bottom:6px; }}
.mn {{ font-size:.8rem; color:#E8C98A; }}
.mv {{ font-family:'DM Mono',monospace; font-size:.72rem; color:#B5622A; }}
.mv.green {{ color:#5DBB63; }}
.bb {{ background:rgba(255,255,255,.07); border-radius:3px; height:5px; overflow:hidden; }}
.bf {{ height:100%; border-radius:3px; }}
.bdg-row {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:18px; justify-content:center; }}
.bdg {{ font-family:'DM Mono',monospace; font-size:.56rem; letter-spacing:.12em; text-transform:uppercase; padding:5px 12px; border-radius:4px; border:1px solid; }}
.bg2 {{ color:#607A5E; border-color:rgba(96,122,94,.4); background:rgba(96,122,94,.1); }}
.ba  {{ color:#D4894A; border-color:rgba(212,137,74,.4); background:rgba(212,137,74,.1); }}
.bs  {{ color:#8A8070; border-color:rgba(138,128,112,.3); background:rgba(138,128,112,.07); }}
</style>
</head>
<body>
<div class="hero">
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>

  <!-- NAVBAR -->
  <nav class="navbar">
    <div class="nav-logo">T<span>PLANT</span></div>
    <button class="nav-cta" onclick="navigateTo()">Mulai Sekarang</button>
  </nav>

  <!-- MAIN CONTENT -->
  <div class="hero-content">
    <div class="hero-body">
      <!-- LEFT: Headline -->
      <div>
        <div class="badge">Aurora Edition &nbsp;·&nbsp; V4.0 &nbsp;·&nbsp; RF Algorithm</div>
        <div class="hero-h1">
          Plant Tree,
          <em>Create a Green</em>
          <span class="out">Future</span>
        </div>
        <p class="hero-sub">
          Sistem prediksi kegagalan pertanian berbasis <strong>Random Forest</strong>
          dengan 21 parameter tanah, iklim, dan nutrisi —
          membantu petani membuat keputusan lebih cerdas.
        </p>
        <div class="cta-row">
          <button class="btn-primary" onclick="navigateTo()">&#9654;&nbsp; Coba Sekarang</button>
        </div>
      </div>

      <!-- RIGHT: Data Card -->
      <div class="data-card">
        <div class="ctitle">Analisis Real-Time</div>
        <div class="meter">
          <div class="mt"><span class="mn">Kelembaban Tanah</span><span class="mv">{moisture_val:.0f}%</span></div>
          <div class="bb"><div class="bf" style="width:{mw:.1f}%;background:#607A5E;"></div></div>
        </div>
        <div class="meter">
          <div class="mt"><span class="mn">Nitrogen (N)</span><span class="mv">{nitrogen_val:.0f} ppm</span></div>
          <div class="bb"><div class="bf" style="width:{nw:.1f}%;background:#D4894A;"></div></div>
        </div>
        <div class="meter">
          <div class="mt"><span class="mn">pH Tanah</span><span class="mv">{ph_val:.1f}</span></div>
          <div class="bb"><div class="bf" style="width:{pw:.1f}%;background:#B5622A;"></div></div>
        </div>
        <div class="meter">
          <div class="mt"><span class="mn">Risiko Gagal</span><span class="mv green">{risk_val:.1f}%</span></div>
          <div class="bb"><div class="bf" style="width:{rw:.1f}%;background:#5DBB63;"></div></div>
        </div>
        <div class="bdg-row">
          <span class="bdg bg2">&#10003; Optimal</span>
          <span class="bdg ba">{soil_name}</span>
          <span class="bdg bs">Cereal</span>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
function navigateTo() {{
  const link = document.createElement('a');
  link.href = '?page=form';
  link.click();
}}
</script>
</body>
</html>"""

    components.html(landing_html, height=720, scrolling=False)
    
    # Check query params untuk navigation
    if st.query_params.get('page') == 'form':
        st.query_params.clear()
        go_to_form()


# ════════════════════════════════════════════════════════════════════════════
# FORM PAGE
# ════════════════════════════════════════════════════════════════════════════
def render_form():
    inject_css(GLOBAL_CSS)

    col_back, _ = st.columns([0.12, 0.88])
    with col_back:
        if st.button("← Kembali", use_container_width=True, key="btn_back"):
            go_to_landing()

    st.markdown(textwrap.dedent(f"""
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:18px;">
          <div class="metric-card"><div class="metric-value">{MODEL_FEATURES}</div><div class="metric-label">Features</div></div>
          <div class="metric-card"><div class="metric-value">{len(SOIL_TYPES)}</div><div class="metric-label">Soil Types</div></div>
          <div class="metric-card"><div class="metric-value">{len(PLANT_CATEGORIES)}</div><div class="metric-label">Plants</div></div>
          <div class="metric-card"><div class="metric-value">RF</div><div class="metric-label">Algorithm</div></div>
          <div class="metric-card"><div class="metric-value">v4.0</div><div class="metric-label">API Version</div></div>
        </div>
    """).strip(), unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown('<div class="section-block"><div class="section-title"><span class="section-num">01</span>Fisika Tanah</div></div>', unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    with a1:
        soil_type          = st.selectbox("Tipe Tanah", SOIL_TYPES, key="soil_type")
        organic_matter_pct = st.number_input("Bahan Organik (%)", min_value=0.0, value=3.0, step=0.1, format="%.2f")
        salinity_ec        = st.number_input("Salinitas (EC)", min_value=0.0, value=0.4, step=0.1, format="%.2f")
    with a2:
        bulk_density             = st.number_input("Bulk Density (g/cm3)", min_value=0.0, value=1.3, step=0.05, format="%.2f")
        cation_exchange_capacity = st.number_input("CEC (meq/100g)", min_value=0.0, value=15.0, step=0.5, format="%.2f")
        buffering_capacity       = st.number_input("Kapasitas Penyangga", min_value=0.0, value=0.7, step=0.05, format="%.2f")

    st.markdown('<div class="section-block"><div class="section-title"><span class="section-num">02</span>Iklim dan Kelembaban</div></div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        soil_moisture_pct = st.number_input("Kelembaban Tanah (%)", min_value=0.0, value=25.0, step=1.0, format="%.2f")
        soil_temp_c       = st.number_input("Suhu Tanah (C)", value=21.0, step=0.5, format="%.2f")
        air_temp_c        = st.number_input("Suhu Udara (C)", value=25.0, step=0.5, format="%.2f")
        thermal_regime    = st.selectbox("Rejim Termal", THERMAL_REGIMES, key="thermal_regime")
    with b2:
        moisture_limit_dry  = st.number_input("Batas Kering (%)", min_value=0.0, value=15.0, step=1.0, format="%.2f")
        moisture_limit_wet  = st.number_input("Batas Basah (%)", min_value=0.0, value=40.0, step=1.0, format="%.2f")
        light_intensity_par = st.number_input("Intensitas Cahaya (PAR)", min_value=0.0, value=1000.0, step=50.0, format="%.2f")
        moisture_regime     = st.selectbox("Rejim Kelembaban", MOISTURE_REGIMES, key="moisture_regime")

    st.markdown('<div class="section-block"><div class="section-title"><span class="section-num">03</span>pH dan Nutrisi</div></div>', unsafe_allow_html=True)
    d1, d2 = st.columns(2)
    with d1:
        soil_ph        = st.number_input("pH Tanah", value=6.5, step=0.1, format="%.1f")
        nitrogen_ppm   = st.number_input("Nitrogen (ppm)", min_value=0.0, value=100.0, step=5.0, format="%.2f")
        phosphorus_ppm = st.number_input("Fosfor (ppm)", min_value=0.0, value=50.0, step=5.0, format="%.2f")
    with d2:
        potassium_ppm    = st.number_input("Kalium (ppm)", min_value=0.0, value=100.0, step=5.0, format="%.2f")
        ph_stress_flag   = st.selectbox("Stres pH", [0,1], format_func=lambda x:"Normal" if x==0 else "Stres", key="ph_stress_flag")
        nutrient_balance = st.selectbox("Keseimbangan Nutrisi", NUTRIENT_BALANCES, key="nutrient_balance")

    st.markdown('<div class="section-block"><div class="section-title"><span class="section-num">04</span>Tanaman</div></div>', unsafe_allow_html=True)
    plant_category = st.selectbox("Kategori Tanaman", PLANT_CATEGORIES, key="plant_category")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(textwrap.dedent(f"""
        <div class="summary-card" style="margin-top:14px;">
          <div class="summary-header"><div class="summary-header-title">Ringkasan Input</div></div>
          <div class="summary-body">
            <div class="summary-row"><span class="summary-key">Tipe Tanah</span><span class="summary-val">{soil_type}</span></div>
            <div class="summary-row"><span class="summary-key">Kategori</span><span class="summary-val">{plant_category}</span></div>
            <div class="summary-row"><span class="summary-key">pH Tanah</span><span class="summary-val">{soil_ph:.1f}</span></div>
            <div class="summary-row"><span class="summary-key">Kelembaban</span><span class="summary-val">{soil_moisture_pct:.1f}%</span></div>
            <div class="summary-row"><span class="summary-key">Suhu Tanah</span><span class="summary-val">{soil_temp_c:.1f} C</span></div>
            <div class="summary-row"><span class="summary-key">Rejim Termal</span><span class="summary-val">{thermal_regime}</span></div>
            <div class="summary-row"><span class="summary-key">Rejim Kelembaban</span><span class="summary-val">{moisture_regime}</span></div>
            <div class="summary-row"><span class="summary-key">Nitrogen</span><span class="summary-val">{nitrogen_ppm:.1f} ppm</span></div>
            <div class="summary-row"><span class="summary-key">Fosfor</span><span class="summary-val">{phosphorus_ppm:.1f} ppm</span></div>
            <div class="summary-row"><span class="summary-key">Kalium</span><span class="summary-val">{potassium_ppm:.1f} ppm</span></div>
          </div>
        </div>
    """).strip(), unsafe_allow_html=True)

    if st.button("Jalankan Prediksi", use_container_width=True, key="btn_prediksi"):
        payload = {
            "soil_type":soil_type, "bulk_density":bulk_density,
            "organic_matter_pct":organic_matter_pct, "cation_exchange_capacity":cation_exchange_capacity,
            "salinity_ec":salinity_ec, "buffering_capacity":buffering_capacity,
            "soil_moisture_pct":soil_moisture_pct, "moisture_limit_dry":moisture_limit_dry,
            "moisture_limit_wet":moisture_limit_wet, "moisture_regime":moisture_regime,
            "soil_temp_c":soil_temp_c, "air_temp_c":air_temp_c,
            "thermal_regime":thermal_regime, "light_intensity_par":light_intensity_par,
            "soil_ph":soil_ph, "ph_stress_flag":ph_stress_flag,
            "nitrogen_ppm":nitrogen_ppm, "phosphorus_ppm":phosphorus_ppm,
            "potassium_ppm":potassium_ppm, "nutrient_balance":nutrient_balance,
            "plant_category":plant_category,
        }
        with st.spinner("Menganalisis parameter..."):
            try:
                r = requests.post(API_URL, json=payload, timeout=15)
                r.raise_for_status()
                st.session_state.prediction_result = r.json()
            except requests.exceptions.ConnectionError:
                st.error("Gagal terhubung ke API backend. Pastikan server berjalan di http://127.0.0.1:8000")
            except requests.exceptions.HTTPError as e:
                st.error(f"API Error {e.response.status_code if e.response else '?'}: {e.response.text if e.response else e}")
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.prediction_result:
        pred     = st.session_state.prediction_result
        risk_pct = max(0.0, min(100.0, float(pred.get("probability_failure", 0.0)) * 100.0))
        risk_desc= "Risiko rendah" if risk_pct < 35 else "Risiko sedang" if risk_pct < 65 else "Risiko tinggi"
        st.markdown(textwrap.dedent(f"""
            <div class="result-card">
              <div class="result-head">Hasil Analisis</div>
              <div class="result-body">
                <div class="risk-label">Tingkat Risiko Kegagalan</div>
                <div class="risk-bar-bg"><div class="risk-bar-fill" style="width:{risk_pct:.1f}%"></div></div>
                <div class="risk-value">{risk_pct:.1f}%</div>
                <div class="risk-desc">{risk_desc}</div>
              </div>
            </div>
        """).strip(), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# ROUTER
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    render_landing()
else:
    render_form()