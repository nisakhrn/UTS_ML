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

# ── SESSION STATE ────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

# ── CONSTANTS ────────────────────────────────────────────────────────────────
API_URL = "http://127.0.0.1:8000/predict/"
API_SAMPLE_URL = "http://127.0.0.1:8000/sample-condition/"

SOIL_TYPES = ["Alluvial", "Chalky", "Clayey", "Laterite", "Loamy", "Peaty", "Saline", "Sandy", "Silty"]
PLANT_CATEGORIES = ["cereal", "legume", "vegetable"]
THERMAL_REGIMES = ["cold", "optimal", "heat_stress"]
MOISTURE_REGIMES = ["dry", "optimal", "waterlogged"]
NUTRIENT_BALANCES = ["optimal", "deficient", "excessive"]
MODEL_FEATURES = 21

# ── HELPERS ──────────────────────────────────────────────────────────────────
def get_sample_data():
    """Ambil sample data dari API backend"""
    try:
        response = requests.get(API_SAMPLE_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    return {
        "soil_moisture": 25,
        "nitrogen": 100,
        "phosphorus": 50,
        "potassium": 100,
        "soil_ph": 6.5,
        "soil_temp": 21,
        "air_temp": 25,
        "risk_level": 12.4,
        "soil_type": "Alluvial"
    }

def go_to_form():
    st.session_state.page = "form"
    st.rerun()

def go_to_landing():
    st.session_state.page = "landing"
    st.rerun()

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
:root {
  --soil:   #1A0F07;
  --bark:   #3A2010;
  --copper: #B5622A;
  --amber:  #D4894A;
  --wheat:  #E8C98A;
  --cream:  #F5EDD8;
  --sage:   #607A5E;
  --moss:   #3D5C3B;
  --deep:   #243823;
  --stone:  #8A8070;
}

/* Hide Streamlit chrome */
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { background: var(--soil); }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
section[data-testid="stSidebar"] { display: none; }

/* Base typography */
* { font-family: 'Outfit', sans-serif; box-sizing: border-box; }

/* Form styles */
.panel {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(196,116,57,0.17);
  border-radius: 14px;
  overflow: hidden;
  padding: 20px;
  margin-top: 14px;
}

.section-block {
  padding: 22px 0;
  border-bottom: 1px solid rgba(196,116,57,0.12);
}

.section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.08rem;
  font-weight: 600;
  color: var(--wheat);
}

.section-num {
  background: rgba(255,255,255,0.04);
  color: var(--amber);
  padding: 2px 7px;
  border-radius: 3px;
  margin-right: 8px;
  font-family: 'DM Mono', monospace;
  font-size: 0.62rem;
}

.metric-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(196,116,57,0.18);
  border-radius: 12px;
  padding: 16px 12px;
  text-align: center;
  position: relative;
}

.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--copper);
  opacity: 0.5;
}

.metric-value {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  font-weight: 600;
  color: var(--wheat);
  line-height: 1;
  margin-bottom: 4px;
}

.metric-label {
  font-family: 'DM Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--stone);
}

.summary-card {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(196,116,57,0.17);
  border-radius: 14px;
  overflow: hidden;
}

.summary-header {
  background: rgba(0,0,0,0.2);
  padding: 16px 18px;
}

.summary-header-title {
  font-family: 'DM Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--wheat);
}

.summary-body {
  padding: 14px 18px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px dashed rgba(168,154,133,0.18);
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-key {
  font-family: 'DM Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--stone);
}

.summary-val {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--cream);
}

.result-card {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(196,116,57,0.17);
  border-radius: 14px;
  overflow: hidden;
  margin-top: 14px;
}

.result-head {
  padding: 14px 18px;
  border-bottom: 1px solid rgba(196,116,57,0.16);
  font-family: 'Cormorant Garamond', serif;
  font-size: 1rem;
  font-weight: 600;
  color: var(--wheat);
}

.result-body {
  padding: 14px 18px 18px;
}

.risk-label {
  font-family: 'DM Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--stone);
  margin-bottom: 8px;
}

.risk-bar-bg {
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
  height: 8px;
  overflow: hidden;
}

.risk-bar-fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--sage), var(--copper));
}

.risk-value {
  margin-top: 8px;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.9rem;
  font-weight: 600;
  color: var(--wheat);
  text-align: center;
}

.risk-desc {
  margin-top: 3px;
  font-size: 0.8rem;
  color: var(--stone);
  text-align: center;
  font-style: italic;
}

.stButton > button {
  width: 100%;
  background: linear-gradient(145deg, var(--amber), var(--copper));
  color: var(--soil);
  border: 1px solid rgba(223,161,96,0.35);
  border-radius: 10px;
  padding: 14px;
  font-family: 'DM Mono', monospace;
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.stButton > button:hover {
  color: var(--soil);
  border: 1px solid rgba(223,161,96,0.5);
}

label, .stNumberInput label, .stSelectbox label {
  font-family: 'DM Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--stone);
  font-weight: 500;
}

.stSelectbox > div > div,
.stNumberInput > div > div > input,
input[readonly] {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(196,116,57,0.2) !important;
  border-radius: 8px !important;
  color: var(--cream) !important;
}

input[readonly] {
  font-family: 'DM Mono', monospace;
  color: var(--wheat) !important;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ════════════════════════════════════════════════════════════════════════════
def render_landing():
    # Load sample data
    sample_data = get_sample_data()
    moisture_width = min(100, (sample_data.get('soil_moisture', 25) / 40) * 100)
    nitrogen_width = min(100, (sample_data.get('nitrogen', 100) / 150) * 100)
    ph_width = min(100, (sample_data.get('soil_ph', 6.5) / 8) * 100)
    risk_width = min(100, sample_data.get('risk_level', 12.4))
    
    components.html(f"""
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ background:#1A0F07; color:#F5EDD8; font-family:'Outfit',sans-serif; overflow-x:hidden; }}

    /* NAV */
    nav {{
      position:relative; top:0; left:0; right:0; z-index:100;
      padding:22px 60px;
      display:flex; align-items:center; justify-content:space-between;
      background:rgba(26,15,7,0.9);
      backdrop-filter:blur(16px);
      border-bottom:1px solid rgba(181,98,42,0.15);
    }}
    .nav-logo {{ font-family:'Cormorant Garamond',serif; font-size:1.5rem; font-weight:600; letter-spacing:0.1em; color:#F5EDD8; text-decoration:none; }}
    .nav-logo span {{ color:#B5622A; }}
    .nav-links {{ display:flex; gap:36px; list-style:none; }}
    .nav-links a {{ font-family:'DM Mono',monospace; font-size:0.65rem; letter-spacing:0.2em; text-transform:uppercase; color:#8A8070; text-decoration:none; transition:color 0.2s; }}
    .nav-links a:hover {{ color:#E8C98A; }}

    /* HERO */
    .hero {{
      min-height:92vh; display:flex; flex-direction:column; justify-content:center;
      position:relative; overflow:hidden; padding:0 60px;
    }}
    .hero-bg {{
      position:absolute; inset:0;
      background:
        radial-gradient(ellipse 70% 60% at 75% 50%, rgba(61,92,59,0.25) 0%, transparent 70%),
        radial-gradient(ellipse 50% 80% at 20% 60%, rgba(181,98,42,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 100% 50% at 50% 100%, rgba(26,15,7,1) 0%, transparent 50%),
        linear-gradient(160deg, #0E0805 0%, #1F1208 40%, #2C1A0E 70%, #1A0F07 100%);
      animation:bgShift 12s ease-in-out infinite alternate;
    }}
    @keyframes bgShift {{
      0%   {{ filter:hue-rotate(0deg) brightness(1); }}
      100% {{ filter:hue-rotate(8deg) brightness(1.05); }}
    }}
    .orb {{ position:absolute; border-radius:50%; filter:blur(80px); pointer-events:none; animation:orbFloat 8s ease-in-out infinite alternate; }}
    .orb1 {{ width:500px; height:500px; right:-100px; top:-100px; background:rgba(61,92,59,0.2); }}
    .orb2 {{ width:350px; height:350px; left:10%; bottom:5%; background:rgba(181,98,42,0.15); animation-delay:3s; }}
    .orb3 {{ width:250px; height:250px; right:30%; top:20%; background:rgba(212,137,74,0.1); animation-delay:1.5s; }}
    @keyframes orbFloat {{
      0%   {{ transform:translate(0,0) scale(1); }}
      100% {{ transform:translate(30px,-30px) scale(1.1); }}
    }}
    .hero-grid {{
      position:absolute; inset:0;
      background-image:linear-gradient(rgba(181,98,42,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(181,98,42,0.04) 1px,transparent 1px);
      background-size:80px 80px;
      mask-image:radial-gradient(ellipse 80% 80% at 50% 50%,black 0%,transparent 100%);
    }}
    .hero-inner {{ position:relative; z-index:2; max-width:1200px; margin:0 auto; width:100%; display:grid; grid-template-columns:1fr 340px; gap:60px; align-items:center; }}
    .hero-eyebrow {{
      font-family:'DM Mono',monospace; font-size:0.65rem; letter-spacing:0.3em; text-transform:uppercase;
      color:#B5622A; margin-bottom:28px; display:flex; align-items:center; gap:14px;
      opacity:0; animation:slideUp 0.8s 0.2s ease forwards;
    }}
    .hero-eyebrow::before {{ content:''; width:40px; height:1px; background:#B5622A; }}
    .hero-title {{
      font-family:'Cormorant Garamond',serif; font-size:clamp(3rem,6vw,6.5rem);
      font-weight:600; line-height:0.95; letter-spacing:-0.01em; margin-bottom:10px;
      opacity:0; animation:slideUp 0.9s 0.35s ease forwards;
    }}
    .hero-title em {{ font-style:italic; font-weight:300; color:#B5622A; }}
    .hero-title .outline {{ -webkit-text-stroke:1px rgba(232,201,138,0.4); color:transparent; }}
    .hero-subtitle {{
      font-size:0.95rem; font-weight:300; color:#8A8070; line-height:1.7; max-width:460px; margin-top:28px;
      opacity:0; animation:slideUp 0.9s 0.5s ease forwards;
    }}
    .hero-subtitle strong {{ color:#E8C98A; font-weight:500; }}
    .hero-cta-row {{ display:flex; align-items:center; gap:16px; margin-top:36px; opacity:0; animation:slideUp 0.9s 0.65s ease forwards; }}
    .btn-primary {{ background:#B5622A; color:#1A0F07; border:none; padding:14px 32px; font-family:'DM Mono',monospace; font-size:0.7rem; letter-spacing:0.2em; text-transform:uppercase; font-weight:500; cursor:pointer; border-radius:4px; text-decoration:none; display:inline-flex; align-items:center; gap:8px; transition:background 0.2s; }}
    .btn-primary:hover {{ background:#D4894A; }}
    .btn-secondary {{ color:#8A8070; border:1px solid rgba(138,128,112,0.3); padding:14px 32px; font-family:'DM Mono',monospace; font-size:0.7rem; letter-spacing:0.2em; text-transform:uppercase; cursor:pointer; border-radius:4px; text-decoration:none; display:inline-flex; align-items:center; gap:8px; transition:color 0.2s,border-color 0.2s; background:transparent; }}
    .btn-secondary:hover {{ color:#E8C98A; border-color:rgba(232,201,138,0.4); }}

    /* HERO CARD */
    .hero-card {{ background:rgba(255,255,255,0.03); border:1px solid rgba(181,98,42,0.2); border-radius:16px; padding:28px; backdrop-filter:blur(10px); opacity:0; animation:fadeIn 1.2s 0.8s forwards; }}
    .hero-card-title {{ font-family:'DM Mono',monospace; font-size:0.58rem; letter-spacing:0.2em; text-transform:uppercase; color:#8A8070; margin-bottom:16px; }}
    .mini-meter {{ margin-bottom:12px; }}
    .mini-meter-top {{ display:flex; justify-content:space-between; font-size:0.78rem; color:#E8C98A; margin-bottom:5px; }}
    .mini-meter-top span:last-child {{ font-family:'DM Mono',monospace; font-size:0.7rem; color:#B5622A; }}
    .mini-bar-bg {{ background:rgba(255,255,255,0.06); border-radius:2px; height:4px; }}
    .mini-bar-fill {{ height:100%; border-radius:2px; }}
    .badge-row {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:16px; }}
    .badge {{ font-family:'DM Mono',monospace; font-size:0.58rem; letter-spacing:0.12em; text-transform:uppercase; padding:5px 10px; border-radius:3px; border:1px solid; }}
    .badge-green {{ color:#607A5E; border-color:rgba(96,122,94,0.4); background:rgba(96,122,94,0.1); }}
    .badge-amber {{ color:#D4894A; border-color:rgba(212,137,74,0.4); background:rgba(212,137,74,0.1); }}
    .badge-stone {{ color:#8A8070; border-color:rgba(138,128,112,0.3); background:rgba(138,128,112,0.07); }}

    /* STATS ROW */
    .hero-stats-row {{ display:flex; gap:36px; margin-top:40px; opacity:0; animation:slideUp 0.9s 0.75s ease forwards; }}
    .hero-stat {{ text-align:center; }}
    .hero-stat-num {{ font-family:'Cormorant Garamond',serif; font-size:2.4rem; font-weight:600; color:#E8C98A; line-height:1; }}
    .hero-stat-label {{ font-family:'DM Mono',monospace; font-size:0.55rem; letter-spacing:0.18em; text-transform:uppercase; color:#8A8070; margin-top:4px; }}

    @keyframes slideUp {{ from {{ opacity:0; transform:translateY(30px); }} to {{ opacity:1; transform:none; }} }}
    @keyframes fadeIn  {{ from {{ opacity:0; }} to {{ opacity:1; }} }}
    </style>

    <nav>
      <a href="#" class="nav-logo">T<span>PLANT</span></a>
      <ul class="nav-links">
        <li><a href="#">Cara Kerja</a></li>
        <li><a href="#">Fitur</a></li>
        <li><a href="#">Statistik</a></li>
        <li><a href="#">Kontak</a></li>
      </ul>
    </nav>

    <div class="hero">
      <div class="hero-bg"></div>
      <div class="orb orb1"></div>
      <div class="orb orb2"></div>
      <div class="orb orb3"></div>
      <div class="hero-grid"></div>
      <div class="hero-inner">
        <div class="hero-left">
          <div class="hero-eyebrow">Aurora Edition &nbsp;·&nbsp; v4.0 &nbsp;·&nbsp; RF Algorithm</div>
          <h1 class="hero-title">Plant Tree,<br><em>Create a</em><br><span class="outline">Green Future</span></h1>
          <p class="hero-subtitle">Sistem prediksi kegagalan pertanian berbasis <strong>Random Forest</strong> dengan 21 parameter tanah, iklim, dan nutrisi — membantu petani membuat keputusan lebih cerdas.</p>
          <div class="hero-stats-row">
            <div class="hero-stat"><div class="hero-stat-num">21</div><div class="hero-stat-label">Parameters</div></div>
            <div class="hero-stat"><div class="hero-stat-num">9</div><div class="hero-stat-label">Soil Types</div></div>
            <div class="hero-stat"><div class="hero-stat-num">94%</div><div class="hero-stat-label">Accuracy</div></div>
          </div>
          <div class="hero-cta-row">
            <a href="javascript:void(0);" class="btn-primary" onclick="parent.postMessage({{type:'streamlit:setComponentValue', value:'goto_form'}}, '*');">▶ Coba Sekarang</a>
            <a href="#" class="btn-secondary">Cara Kerja ↓</a>
          </div>
        </div>
        <div class="hero-card">
          <div class="hero-card-title">Analisis Real-Time</div>
          <div class="mini-meter">
            <div class="mini-meter-top"><span>Kelembaban Tanah</span><span>{sample_data.get('soil_moisture', 25):.1f}%</span></div>
            <div class="mini-bar-bg"><div class="mini-bar-fill" style="width:{moisture_width}%;background:#607A5E;"></div></div>
          </div>
          <div class="mini-meter">
            <div class="mini-meter-top"><span>Nitrogen (N)</span><span>{sample_data.get('nitrogen', 100):.1f} ppm</span></div>
            <div class="mini-bar-bg"><div class="mini-bar-fill" style="width:{nitrogen_width}%;background:#D4894A;"></div></div>
          </div>
          <div class="mini-meter">
            <div class="mini-meter-top"><span>pH Tanah</span><span>{sample_data.get('soil_ph', 6.5):.1f}</span></div>
            <div class="mini-bar-bg"><div class="mini-bar-fill" style="width:{ph_width}%;background:#B5622A;"></div></div>
          </div>
          <div class="mini-meter">
            <div class="mini-meter-top"><span>Risiko Gagal</span><span style="color:#5DBB63;">{sample_data.get('risk_level', 12.4):.1f}%</span></div>
            <div class="mini-bar-bg"><div class="mini-bar-fill" style="width:{risk_width}%;background:#5DBB63;"></div></div>
          </div>
          <div class="badge-row">
            <span class="badge badge-green">✓ Optimal</span>
            <span class="badge badge-amber">{sample_data.get('soil_type', 'Alluvial')}</span>
            <span class="badge badge-stone">Cereal</span>
          </div>
        </div>
      </div>
    </div>
    """, height=780)

    # Tombol untuk navigate ke form (Streamlit)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Mulai Sekarang →", use_container_width=True, key="landing_start_btn"):
            go_to_form()

    # MARQUEE
    components.html("""
    <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background:#1A0F07; }
    .marquee-wrap { background:#B5622A; padding:14px 0; overflow:hidden; }
    .marquee-track { display:flex; animation:marqueeScroll 25s linear infinite; white-space:nowrap; }
    .marquee-item { font-family:'DM Mono',monospace; font-size:0.65rem; letter-spacing:0.2em; text-transform:uppercase; color:#1A0F07; font-weight:500; padding:0 40px; display:flex; align-items:center; gap:20px; }
    .marquee-dot { width:4px; height:4px; background:#1A0F07; border-radius:50%; opacity:0.5; }
    @keyframes marqueeScroll { from { transform:translateX(0); } to { transform:translateX(-50%); } }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400&display=swap" rel="stylesheet">
    <div class="marquee-wrap">
      <div class="marquee-track">
        <span class="marquee-item">Agro Failure Predictor <span class="marquee-dot"></span></span>
        <span class="marquee-item">Random Forest Algorithm <span class="marquee-dot"></span></span>
        <span class="marquee-item">21 Input Features <span class="marquee-dot"></span></span>
        <span class="marquee-item">9 Jenis Tanah <span class="marquee-dot"></span></span>
        <span class="marquee-item">Aurora Edition v4.0 <span class="marquee-dot"></span></span>
        <span class="marquee-item">Precision Agriculture <span class="marquee-dot"></span></span>
        <span class="marquee-item">Smart Farming <span class="marquee-dot"></span></span>
        <span class="marquee-item">Agro Failure Predictor <span class="marquee-dot"></span></span>
        <span class="marquee-item">Random Forest Algorithm <span class="marquee-dot"></span></span>
        <span class="marquee-item">21 Input Features <span class="marquee-dot"></span></span>
        <span class="marquee-item">9 Jenis Tanah <span class="marquee-dot"></span></span>
        <span class="marquee-item">Aurora Edition v4.0 <span class="marquee-dot"></span></span>
        <span class="marquee-item">Precision Agriculture <span class="marquee-dot"></span></span>
        <span class="marquee-item">Smart Farming <span class="marquee-dot"></span></span>
      </div>
    </div>
    """, height=50)

    # HOW IT WORKS
    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,300&family=DM+Mono:wght@300;400&family=Outfit:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background:#1A0F07; color:#F5EDD8; font-family:'Outfit',sans-serif; }
    .section { padding:90px 60px; border-top:1px solid rgba(181,98,42,0.12); max-width:1300px; margin:0 auto; }
    .section-label { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.3em; text-transform:uppercase; color:#B5622A; margin-bottom:18px; display:flex; align-items:center; gap:12px; }
    .section-label::before { content:''; width:30px; height:1px; background:#B5622A; }
    .section-title { font-family:'Cormorant Garamond',serif; font-size:clamp(2rem,3.5vw,3rem); font-weight:600; line-height:1.1; margin-bottom:16px; }
    .section-title em { font-style:italic; font-weight:300; color:#B5622A; }
    .how-grid { display:grid; grid-template-columns:1fr 1fr; gap:70px; align-items:center; margin-top:50px; }
    .step-item { display:flex; gap:22px; padding:26px 0; border-bottom:1px solid rgba(181,98,42,0.1); transition:padding-left 0.3s; }
    .step-item:last-child { border-bottom:none; }
    .step-item:hover { padding-left:8px; }
    .step-num { font-family:'Cormorant Garamond',serif; font-size:2.8rem; font-weight:300; color:rgba(181,98,42,0.2); line-height:1; flex-shrink:0; width:52px; transition:color 0.3s; }
    .step-item:hover .step-num { color:rgba(181,98,42,0.6); }
    .step-title { font-family:'Cormorant Garamond',serif; font-size:1.2rem; font-weight:600; color:#E8C98A; margin-bottom:7px; }
    .step-desc { font-size:0.85rem; color:#8A8070; line-height:1.7; font-weight:300; }
    .terminal { background:rgba(255,255,255,0.02); border:1px solid rgba(181,98,42,0.15); border-radius:12px; overflow:hidden; }
    .terminal-bar { background:rgba(255,255,255,0.04); padding:12px 16px; display:flex; align-items:center; gap:8px; border-bottom:1px solid rgba(181,98,42,0.1); }
    .td { width:10px; height:10px; border-radius:50%; }
    .td1 { background:#FF5F56; } .td2 { background:#FFBD2E; } .td3 { background:#27C93F; }
    .terminal-title { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.15em; color:#8A8070; margin:0 auto; }
    .terminal-body { padding:22px; font-family:'DM Mono',monospace; font-size:0.78rem; line-height:2; }
    .t-prompt { color:#3D5C3B; } .t-cmd { color:#E8C98A; } .t-out { color:#8A8070; }
    .t-val { color:#D4894A; } .t-good { color:#5DBB63; } .t-warn { color:#B5622A; }
    .t-cursor { display:inline-block; width:8px; height:14px; background:#B5622A; animation:blink 1s infinite; vertical-align:middle; }
    @keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0; } }
    </style>
    <div style="background:#1A0F07; padding-bottom:20px;">
    <div class="section">
      <div class="section-label">Cara Kerja</div>
      <h2 class="section-title">Dari Data Lapangan<br>Menjadi <em>Keputusan Cerdas</em></h2>
      <div class="how-grid">
        <div>
          <div class="step-item">
            <div class="step-num">01</div>
            <div><div class="step-title">Input Parameter</div><div class="step-desc">Masukkan 21 parameter meliputi fisika tanah, kondisi iklim, kandungan nutrisi, dan jenis tanaman yang ditanam.</div></div>
          </div>
          <div class="step-item">
            <div class="step-num">02</div>
            <div><div class="step-title">Kalkulasi Otomatis</div><div class="step-desc">Sistem secara otomatis menghitung rejim termal, rejim kelembaban, stres pH, dan keseimbangan nutrisi dari input Anda.</div></div>
          </div>
          <div class="step-item">
            <div class="step-num">03</div>
            <div><div class="step-title">Analisis Random Forest</div><div class="step-desc">Algoritma RF memproses seluruh parameter melalui 100+ decision tree untuk menghasilkan prediksi yang akurat.</div></div>
          </div>
          <div class="step-item">
            <div class="step-num">04</div>
            <div><div class="step-title">Hasil &amp; Rekomendasi</div><div class="step-desc">Dapatkan persentase risiko, level kegagalan, faktor utama penyebab, dan rekomendasi tindakan yang harus diambil.</div></div>
          </div>
        </div>
        <div class="terminal">
          <div class="terminal-bar">
            <div class="td td1"></div><div class="td td2"></div><div class="td td3"></div>
            <div class="terminal-title">tplant — predict.sh</div>
          </div>
          <div class="terminal-body">
            <div><span class="t-prompt">$ </span><span class="t-cmd">tplant analyze</span></div>
            <div><span class="t-out">→ Loading RF model </span><span class="t-val">v4.0</span><span class="t-out">...</span></div>
            <div><span class="t-out">→ Features: </span><span class="t-good">21 / 21 ✓</span></div>
            <div><span class="t-out">→ Soil type: </span><span class="t-val">Alluvial</span></div>
            <div><span class="t-out">→ pH stress: </span><span class="t-good">Normal</span></div>
            <div><span class="t-out">→ Moisture: </span><span class="t-warn">dry</span></div>
            <div><span class="t-out">→ Nutrient: </span><span class="t-good">optimal</span></div>
            <div>&nbsp;</div>
            <div><span class="t-out">Running trees...</span></div>
            <div><span class="t-out">████████████ </span><span class="t-good">100%</span></div>
            <div>&nbsp;</div>
            <div><span class="t-out">FAILURE RISK: </span><span class="t-good">12.4%</span></div>
            <div><span class="t-out">LEVEL: </span><span class="t-good">RENDAH</span></div>
            <div><span class="t-prompt">$ </span><span class="t-cursor"></span></div>
          </div>
        </div>
      </div>
    </div>
    </div>
    """, height=620)

    # FEATURES
    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,300&family=DM+Mono:wght@400&family=Outfit:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background:#1A0F07; color:#F5EDD8; font-family:'Outfit',sans-serif; }
    .section { padding:90px 60px; border-top:1px solid rgba(181,98,42,0.12); max-width:1300px; margin:0 auto; }
    .section-label { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.3em; text-transform:uppercase; color:#B5622A; margin-bottom:18px; display:flex; align-items:center; gap:12px; }
    .section-label::before { content:''; width:30px; height:1px; background:#B5622A; }
    .section-title { font-family:'Cormorant Garamond',serif; font-size:clamp(2rem,3.5vw,3rem); font-weight:600; line-height:1.1; }
    .section-title em { font-style:italic; font-weight:300; color:#B5622A; }
    .feat-header { display:grid; grid-template-columns:1fr 1fr; gap:50px; align-items:end; margin-bottom:50px; }
    .feat-desc { font-size:0.9rem; color:#8A8070; line-height:1.75; font-weight:300; align-self:end; }
    .features-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:2px; background:rgba(181,98,42,0.08); border-radius:14px; overflow:hidden; }
    .feat-card { background:#1A0F07; padding:34px 28px; transition:background 0.3s; position:relative; overflow:hidden; }
    .feat-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:#B5622A; transform:scaleX(0); transition:transform 0.4s; transform-origin:left; }
    .feat-card:hover { background:rgba(181,98,42,0.07); }
    .feat-card:hover::before { transform:scaleX(1); }
    .feat-icon { font-size:1.4rem; margin-bottom:18px; }
    .feat-title { font-family:'Cormorant Garamond',serif; font-size:1.15rem; font-weight:600; color:#E8C98A; margin-bottom:9px; }
    .feat-desc-text { font-size:0.82rem; color:#8A8070; line-height:1.7; font-weight:300; }
    .feat-tag { display:inline-block; margin-top:13px; font-family:'DM Mono',monospace; font-size:0.58rem; letter-spacing:0.14em; text-transform:uppercase; color:#B5622A; background:rgba(181,98,42,0.1); padding:4px 9px; border-radius:2px; }
    </style>
    <div style="background:#1A0F07; padding-bottom:20px;">
    <div class="section">
      <div class="feat-header">
        <div>
          <div class="section-label">Fitur Unggulan</div>
          <h2 class="section-title">Teknologi yang Dirancang<br>untuk <em>Pertanian Modern</em></h2>
        </div>
        <p class="feat-desc">TPLANT menggabungkan kecerdasan machine learning dengan pengetahuan agronomis mendalam untuk memberikan prediksi yang dapat diandalkan di lapangan.</p>
      </div>
      <div class="features-grid">
        <div class="feat-card"><div class="feat-icon">🌱</div><div class="feat-title">Multi-Parameter Analysis</div><div class="feat-desc-text">Analisis 21 variabel secara simultan mencakup fisika tanah, iklim mikro, dan nutrisi untuk prediksi komprehensif.</div><span class="feat-tag">21 Features</span></div>
        <div class="feat-card"><div class="feat-icon">🌲</div><div class="feat-title">Random Forest Algorithm</div><div class="feat-desc-text">Ensemble learning dengan ratusan decision tree memberikan akurasi tinggi dan tahan terhadap noise data lapangan.</div><span class="feat-tag">RF Model</span></div>
        <div class="feat-card"><div class="feat-icon">🌾</div><div class="feat-title">9 Tipe Tanah</div><div class="feat-desc-text">Mendukung Alluvial, Andosol, Latosol, Podsolik, Grumusol, Regosol, Litosol, Organosol, dan Gleisol.</div><span class="feat-tag">Soil Types</span></div>
        <div class="feat-card"><div class="feat-icon">⚗️</div><div class="feat-title">Auto Kalkulasi</div><div class="feat-desc-text">Rejim termal, rejim kelembaban, stres pH, dan keseimbangan nutrisi dihitung otomatis dari input dasar Anda.</div><span class="feat-tag">Smart Calc</span></div>
        <div class="feat-card"><div class="feat-icon">📊</div><div class="feat-title">Risk Scoring</div><div class="feat-desc-text">Output berupa persentase risiko 0–100% dengan empat level: Rendah, Sedang, Tinggi, dan Kritis.</div><span class="feat-tag">4 Risk Levels</span></div>
        <div class="feat-card"><div class="feat-icon">💡</div><div class="feat-title">AI Recommendation</div><div class="feat-desc-text">Rekomendasi tindakan berbasis AI yang kontekstual sesuai kondisi spesifik lahan dan tanaman Anda.</div><span class="feat-tag">Claude API</span></div>
      </div>
    </div>
    </div>
    """, height=600)

    # STATS
    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,300&family=DM+Mono:wght@400&family=Outfit:wght@300;400&display=swap" rel="stylesheet">
    <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background:#3A2010; color:#F5EDD8; font-family:'Outfit',sans-serif; }
    .section { padding:90px 60px; max-width:1300px; margin:0 auto; }
    .section-label { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.3em; text-transform:uppercase; color:#D4894A; margin-bottom:18px; display:flex; align-items:center; gap:12px; }
    .section-label::before { content:''; width:30px; height:1px; background:#D4894A; }
    .section-title { font-family:'Cormorant Garamond',serif; font-size:clamp(2rem,3.5vw,3rem); font-weight:600; line-height:1.1; margin-bottom:50px; }
    .section-title em { font-style:italic; font-weight:300; color:#B5622A; }
    .stats-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:rgba(181,98,42,0.15); border-radius:12px; overflow:hidden; }
    .stat-card { background:#3A2010; padding:48px 32px; text-align:center; transition:background 0.3s; }
    .stat-card:hover { background:rgba(181,98,42,0.08); }
    .stat-num { font-family:'Cormorant Garamond',serif; font-size:4rem; font-weight:600; color:#B5622A; line-height:1; margin-bottom:8px; }
    .stat-label { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.2em; text-transform:uppercase; color:#8A8070; }
    .stat-desc { font-size:0.8rem; color:rgba(138,128,112,0.6); margin-top:8px; line-height:1.5; }
    </style>
    <div style="background:#3A2010; border-top:1px solid rgba(181,98,42,0.15); border-bottom:1px solid rgba(181,98,42,0.15);">
    <div class="section">
      <div class="section-label">Statistik Platform</div>
      <h2 class="section-title">Dipercaya oleh<br><em>Komunitas Pertanian</em></h2>
      <div class="stats-grid">
        <div class="stat-card"><div class="stat-num">94%</div><div class="stat-label">Akurasi Model</div><div class="stat-desc">Validasi pada dataset uji independen</div></div>
        <div class="stat-card"><div class="stat-num">21</div><div class="stat-label">Input Parameter</div><div class="stat-desc">Cakupan analisis terlengkap</div></div>
        <div class="stat-card"><div class="stat-num">9</div><div class="stat-label">Tipe Tanah</div><div class="stat-desc">Mencakup mayoritas tanah Indonesia</div></div>
        <div class="stat-card"><div class="stat-num">&lt;2s</div><div class="stat-label">Waktu Prediksi</div><div class="stat-desc">Hasil analisis hampir instan</div></div>
      </div>
    </div>
    </div>
    """, height=420)

    # QUOTE + CTA + FOOTER
    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,300;1,400&family=DM+Mono:wght@400&family=Outfit:wght@300;400&display=swap" rel="stylesheet">
    <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background:#1A0F07; color:#F5EDD8; font-family:'Outfit',sans-serif; }
    .quote-section { padding:100px 60px; max-width:900px; margin:0 auto; text-align:center; border-top:1px solid rgba(181,98,42,0.12); }
    .quote-mark { font-family:'Cormorant Garamond',serif; font-size:7rem; color:#B5622A; opacity:0.15; line-height:0; display:block; margin-bottom:28px; }
    .quote-text { font-family:'Cormorant Garamond',serif; font-size:clamp(1.4rem,2.5vw,2.2rem); font-weight:300; font-style:italic; color:#E8C98A; line-height:1.5; margin-bottom:28px; }
    .quote-author { font-family:'DM Mono',monospace; font-size:0.65rem; letter-spacing:0.2em; text-transform:uppercase; color:#8A8070; }
    .cta-section { background:#243823; padding:100px 60px; text-align:center; position:relative; overflow:hidden; }
    .cta-section::before { content:''; position:absolute; inset:0; background:radial-gradient(ellipse 60% 70% at 50% 50%,rgba(181,98,42,0.15) 0%,transparent 70%); pointer-events:none; }
    .cta-inner { position:relative; z-index:2; max-width:700px; margin:0 auto; }
    .cta-title { font-family:'Cormorant Garamond',serif; font-size:clamp(2.2rem,4vw,4rem); font-weight:600; line-height:1.05; margin-bottom:18px; }
    .cta-title em { font-style:italic; font-weight:300; color:#B5622A; }
    .cta-desc { font-size:0.92rem; color:#8A8070; line-height:1.75; font-weight:300; margin-bottom:36px; }
    .cta-btns { display:flex; gap:14px; justify-content:center; flex-wrap:wrap; }
    .btn-p { background:#B5622A; color:#1A0F07; border:none; padding:15px 34px; font-family:'DM Mono',monospace; font-size:0.7rem; letter-spacing:0.2em; text-transform:uppercase; font-weight:500; cursor:pointer; border-radius:4px; text-decoration:none; transition:background 0.2s; display:inline-block; }
    .btn-p:hover { background:#D4894A; }
    .btn-s { color:#8A8070; border:1px solid rgba(138,128,112,0.3); padding:15px 34px; font-family:'DM Mono',monospace; font-size:0.7rem; letter-spacing:0.2em; text-transform:uppercase; cursor:pointer; border-radius:4px; text-decoration:none; background:transparent; display:inline-block; transition:color 0.2s,border-color 0.2s; }
    .btn-s:hover { color:#E8C98A; border-color:rgba(232,201,138,0.4); }
    footer { background:#1A0F07; padding:56px 60px 36px; border-top:1px solid rgba(181,98,42,0.12); }
    .footer-top { display:flex; justify-content:space-between; align-items:flex-start; padding-bottom:36px; border-bottom:1px solid rgba(181,98,42,0.1); margin-bottom:28px; }
    .footer-logo { font-family:'Cormorant Garamond',serif; font-size:1.5rem; font-weight:600; letter-spacing:0.08em; color:#F5EDD8; margin-bottom:8px; }
    .footer-logo span { color:#B5622A; }
    .footer-tagline { font-size:0.82rem; color:#8A8070; font-weight:300; font-style:italic; font-family:'Cormorant Garamond',serif; }
    .footer-cols { display:flex; gap:56px; }
    .footer-col-title { font-family:'DM Mono',monospace; font-size:0.58rem; letter-spacing:0.22em; text-transform:uppercase; color:#B5622A; margin-bottom:14px; }
    .footer-col ul { list-style:none; display:flex; flex-direction:column; gap:9px; }
    .footer-col ul a { font-size:0.83rem; color:#8A8070; text-decoration:none; transition:color 0.2s; }
    .footer-col ul a:hover { color:#E8C98A; }
    .footer-bottom { display:flex; justify-content:space-between; align-items:center; }
    .footer-copy { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.14em; color:rgba(138,128,112,0.45); }
    .footer-ver { font-family:'DM Mono',monospace; font-size:0.6rem; letter-spacing:0.14em; color:rgba(181,98,42,0.45); }
    </style>
    <div style="background:#1A0F07;">

    <div class="quote-section">
      <span class="quote-mark">"</span>
      <p class="quote-text">Teknologi bukan pengganti petani — ia adalah kompas yang memberi arah lebih jelas di tengah ketidakpastian alam.</p>
      <div class="quote-author">Tim TPLANT &nbsp;·&nbsp; Aurora Edition</div>
    </div>

    <div class="cta-section">
      <div class="cta-inner">
        <h2 class="cta-title">Siap Prediksi<br><em>Masa Depan Lahan</em> Anda?</h2>
        <p class="cta-desc">Mulai analisis pertama Anda sekarang — gratis, tanpa perlu mendaftar. Masukkan parameter lahan dan dapatkan hasil prediksi dalam hitungan detik.</p>
        <div class="cta-btns">
          <a href="javascript:void(0);" class="btn-p" onclick="parent.postMessage({type:'streamlit:setComponentValue', value:'goto_form'}, '*');">▶ &nbsp;Jalankan Prediksi</a>
          <a href="#" class="btn-s">Dokumentasi API →</a>
        </div>
      </div>
    </div>

    <footer>
      <div class="footer-top">
        <div>
          <div class="footer-logo">T<span>PLANT</span></div>
          <div class="footer-tagline">Plant Tree, Create a Green Future</div>
        </div>
        <div class="footer-cols">
          <div class="footer-col">
            <div class="footer-col-title">Produk</div>
            <ul><li><a href="#">Predictor</a></li><li><a href="#">API Docs</a></li><li><a href="#">Aurora Edition</a></li></ul>
          </div>
          <div class="footer-col">
            <div class="footer-col-title">Info</div>
            <ul><li><a href="#">Tentang Kami</a></li><li><a href="#">Algoritma RF</a></li><li><a href="#">Kontak</a></li></ul>
          </div>
          <div class="footer-col">
            <div class="footer-col-title">Dukungan</div>
            <ul><li><a href="#">Panduan</a></li><li><a href="#">FAQ</a></li><li><a href="#">Laporan Bug</a></li></ul>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <div class="footer-copy">© 2025 TPLANT. All rights reserved.</div>
        <div class="footer-ver">API v4.0 &nbsp;·&nbsp; Aurora Edition</div>
      </div>
    </footer>
    </div>
    """, height=900)


# ════════════════════════════════════════════════════════════════════════════
# FORM PAGE
# ════════════════════════════════════════════════════════════════════════════
def render_form():
    st.markdown(
        textwrap.dedent(f"""
        <div style="display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-bottom:18px;">
          <div class="metric-card"><div class="metric-value">{MODEL_FEATURES}</div><div class="metric-label">Features</div></div>
          <div class="metric-card"><div class="metric-value">{len(SOIL_TYPES)}</div><div class="metric-label">Soil Types</div></div>
          <div class="metric-card"><div class="metric-value">{len(PLANT_CATEGORIES)}</div><div class="metric-label">Plants</div></div>
          <div class="metric-card"><div class="metric-value">RF</div><div class="metric-label">Algorithm</div></div>
          <div class="metric-card"><div class="metric-value">v4.0</div><div class="metric-label">API Version</div></div>
        </div>
        """).strip(),
        unsafe_allow_html=True,
    )

    col_back, col_spacer = st.columns([0.15, 0.85])
    with col_back:
        if st.button("← Kembali", use_container_width=True, key="btn_back"):
            go_to_landing()

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown('<div class="section-block"><div class="section-title"><span class="section-num">01</span>Fisika Tanah</div></div>', unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    with a1:
        soil_type = st.selectbox("Tipe Tanah", SOIL_TYPES, key="soil_type")
        organic_matter_pct = st.number_input("Bahan Organik (%)", min_value=0.0, value=3.0, step=0.1, format="%.2f")
        salinity_ec = st.number_input("Salinitas (EC)", min_value=0.0, value=0.4, step=0.1, format="%.2f")
    with a2:
        bulk_density = st.number_input("Bulk Density (g/cm3)", min_value=0.0, value=1.3, step=0.05, format="%.2f")
        cation_exchange_capacity = st.number_input("CEC (meq/100g)", min_value=0.0, value=15.0, step=0.5, format="%.2f")
        buffering_capacity = st.number_input("Kapasitas Penyangga", min_value=0.0, value=0.7, step=0.05, format="%.2f")

    st.markdown('<div class="section-block"><div class="section-title"><span class="section-num">02</span>Iklim dan Kelembaban</div></div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        soil_moisture_pct = st.number_input("Kelembaban Tanah (%)", min_value=0.0, value=25.0, step=1.0, format="%.2f")
        soil_temp_c = st.number_input("Suhu Tanah (C)", value=21.0, step=0.5, format="%.2f")
        air_temp_c = st.number_input("Suhu Udara (C)", value=25.0, step=0.5, format="%.2f")
        thermal_regime = st.selectbox("Rejim Termal", THERMAL_REGIMES, key="thermal_regime")
    with b2:
        moisture_limit_dry = st.number_input("Batas Kering (%)", min_value=0.0, value=15.0, step=1.0, format="%.2f")
        moisture_limit_wet = st.number_input("Batas Basah (%)", min_value=0.0, value=40.0, step=1.0, format="%.2f")
        light_intensity_par = st.number_input("Intensitas Cahaya (PAR)", min_value=0.0, value=1000.0, step=50.0, format="%.2f")
        moisture_regime = st.selectbox("Rejim Kelembaban", MOISTURE_REGIMES, key="moisture_regime")

    st.markdown('<div class="section-block"><div class="section-title"><span class="section-num">03</span>pH dan Nutrisi</div></div>', unsafe_allow_html=True)
    d1, d2 = st.columns(2)
    with d1:
        soil_ph = st.number_input("pH Tanah", value=6.5, step=0.1, format="%.1f")
        nitrogen_ppm = st.number_input("Nitrogen (ppm)", min_value=0.0, value=100.0, step=5.0, format="%.2f")
        phosphorus_ppm = st.number_input("Fosfor (ppm)", min_value=0.0, value=50.0, step=5.0, format="%.2f")
    with d2:
        potassium_ppm = st.number_input("Kalium (ppm)", min_value=0.0, value=100.0, step=5.0, format="%.2f")
        ph_stress_flag = st.selectbox("Stres pH", [0, 1], format_func=lambda x: "Normal" if x == 0 else "Stres", key="ph_stress_flag")
        nutrient_balance = st.selectbox("Keseimbangan Nutrisi", NUTRIENT_BALANCES, key="nutrient_balance")

    st.markdown('<div class="section-block"><div class="section-title"><span class="section-num">04</span>Tanaman</div></div>', unsafe_allow_html=True)
    plant_category = st.selectbox("Kategori Tanaman", PLANT_CATEGORIES, key="plant_category")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        textwrap.dedent(f"""
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
        """).strip(),
        unsafe_allow_html=True,
    )

    if st.button("Jalankan Prediksi", use_container_width=True, key="btn_prediksi"):
        payload = {
            "soil_type": soil_type,
            "bulk_density": bulk_density,
            "organic_matter_pct": organic_matter_pct,
            "cation_exchange_capacity": cation_exchange_capacity,
            "salinity_ec": salinity_ec,
            "buffering_capacity": buffering_capacity,
            "soil_moisture_pct": soil_moisture_pct,
            "moisture_limit_dry": moisture_limit_dry,
            "moisture_limit_wet": moisture_limit_wet,
            "moisture_regime": moisture_regime,
            "soil_temp_c": soil_temp_c,
            "air_temp_c": air_temp_c,
            "thermal_regime": thermal_regime,
            "light_intensity_par": light_intensity_par,
            "soil_ph": soil_ph,
            "ph_stress_flag": ph_stress_flag,
            "nitrogen_ppm": nitrogen_ppm,
            "phosphorus_ppm": phosphorus_ppm,
            "potassium_ppm": potassium_ppm,
            "nutrient_balance": nutrient_balance,
            "plant_category": plant_category,
        }

        with st.spinner("Menganalisis parameter..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=15)
                response.raise_for_status()
                result = response.json()
                st.session_state.prediction_result = result
            except requests.exceptions.ConnectionError:
                st.error("Gagal terhubung ke API backend. Pastikan server berjalan di http://127.0.0.1:8000")
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code if e.response is not None else "unknown"
                detail = e.response.text if e.response is not None else str(e)
                st.error(f"API Error {status}: {detail}")
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.prediction_result:
        pred = st.session_state.prediction_result
        risk_pct = max(0.0, min(100.0, float(pred.get("probability_failure", 0.0)) * 100.0))
        risk_desc = "Risiko rendah" if risk_pct < 35 else "Risiko sedang" if risk_pct < 65 else "Risiko tinggi"

        st.markdown(
            textwrap.dedent(f"""
            <div class="result-card">
              <div class="result-head">Hasil Analisis</div>
              <div class="result-body">
              <div class="risk-label">Tingkat Risiko Kegagalan</div>
              <div class="risk-bar-bg"><div class="risk-bar-fill" style="width:{risk_pct:.1f}%"></div></div>
              <div class="risk-value">{risk_pct:.1f}%</div>
              <div class="risk-desc">{risk_desc}</div>
              </div>
            </div>
            """).strip(),
            unsafe_allow_html=True,
        )


# ════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    render_landing()
else:
    render_form()