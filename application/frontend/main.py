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

# ── NUKE ALL STREAMLIT CHROME & FIX DOUBLE SCROLL ───────────────────────────
st.markdown("""
<style>
/* Hilangkan semua chrome Streamlit */
#MainMenu { visibility: hidden !important; display: none !important; }
header[data-testid="stHeader"] { visibility: hidden !important; display: none !important; height: 0 !important; }
footer { visibility: hidden !important; display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.viewerBadge_container__r5tak { display: none !important; }

/* SOLUSI DOUBLE SCROLL - HILANGKAN SEMUA SCROLLBAR */
html, body {
  overflow-x: hidden !important;
  overflow-y: auto !important;
    height: 100% !important;
}

[data-testid="stAppViewContainer"] {
    background: #1A0F07 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    height: 100vh !important;
    position: relative !important;
}

[data-testid="stMain"] {
    overflow: visible !important;
    height: auto !important;
    padding: 40px 50px !important;
}

[data-testid="stMainBlockContainer"] {
  overflow: visible !important;
    height: auto !important;
    max-height: none !important;
}

.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
  overflow: visible !important;
    height: auto !important;
}

[data-testid="stVerticalBlock"] {
    gap: 0 !important;
    padding: 0 !important;
  overflow: visible !important;
}

div[data-testid="stVerticalBlock"] > div {
  overflow: visible !important;
}

iframe {
    display: block !important;
}

/* HIDE ALL SCROLLBARS COMPLETELY */
::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}

::-webkit-scrollbar-track {
    display: none !important;
}

::-webkit-scrollbar-thumb {
    display: none !important;
}

/* Firefox scrollbar hide */
* {
    scrollbar-width: none !important;
    scrollbar-color: transparent transparent !important;
}

html {
    scrollbar-width: none !important;
}

body {
    scrollbar-width: none !important;
}

[data-testid="stAppViewContainer"] {
    scrollbar-width: none !important;
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

SOIL_TYPES        = ["Alluvial","Andosol","Latosol","Podsolik","Grumusol","Regosol","Litosol","Organosol","Gleisol"]
PLANT_CATEGORIES  = ["cereal","legume","vegetable"]
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
  st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def derive_moisture_regime(soil_moisture_pct: float, moisture_limit_dry: float, moisture_limit_wet: float) -> str:
    if soil_moisture_pct < moisture_limit_dry:
        return "dry_stress"
    if soil_moisture_pct > moisture_limit_wet:
        return "wet_stress"
    return "optimal"

def derive_thermal_regime(air_temp_c: float) -> str:
    if air_temp_c > 32:
        return "heat_stress"
    if air_temp_c < 15:
        return "cold_stress"
    return "optimal"

FORM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&family=DM+Mono:wght@300;400;500&family=Instrument+Sans:wght@400;500;600&display=swap');

:root {
  --soil: #2C1A0E;
  --bark: #4A2E1A;
  --copper: #B5622A;
  --amber: #D4894A;
  --wheat: #E8C98A;
  --cream: #F5EDD8;
  --fog: #EDE5D0;
  --sage: #5C7A5A;
  --moss: #3D5C3B;
  --stone: #8A8070;
  --light: #FAF6EE;
  --dark-bg: #1A0F07;
}

* { font-family: 'Instrument Sans', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }
h1, h2, h3 { font-family: 'Cormorant Garamond', serif; }

/* MAIN CONTAINER — samakan dengan landing: 20px 70px */
[data-testid="stMain"] {
    padding: 20px 70px !important;
    background: var(--dark-bg) !important;
}

/* SELECT DROPDOWN */
.stSelectbox > div > div {
  background: rgba(212, 149, 93, 0.2) !important;
  border: 1.2px solid rgba(205, 145, 92, 0.7) !important;
  border-radius: 7px !important;
  color: #F3D9AE !important;
  padding: 7px 10px !important;
  font-size: 0.76rem !important;
}

.stSelectbox > div > div:focus-within {
  border-color: var(--copper) !important;
  box-shadow: none !important;
  outline: none !important;
}

.stSelectbox svg { color: var(--stone) !important; }

/* BaseWeb select internals (fix selected text invisibility) */
.stSelectbox [data-baseweb="select"] > div {
  min-height: 44px !important;
  height: 44px !important;
  background: rgba(212, 149, 93, 0.2) !important;
  border: 1.2px solid rgba(205, 145, 92, 0.7) !important;
  border-radius: 7px !important;
  box-shadow: none !important;
  outline: none !important;
  overflow: visible !important;
}

.stSelectbox [data-baseweb="select"] > div > div {
  display: flex !important;
  align-items: center !important;
  height: 100% !important;
  min-height: 100% !important;
}

.stSelectbox [data-baseweb="select"] [class*="valueContainer"] {
  display: flex !important;
  align-items: center !important;
  height: 100% !important;
  min-height: 44px !important;
  padding-left: 12px !important;
  padding-right: 8px !important;
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

.stSelectbox [data-baseweb="select"] span,
.stSelectbox [data-baseweb="select"] input,
.stSelectbox [data-baseweb="select"] div {
  color: #FFE8C4 !important;
  -webkit-text-fill-color: #FFE8C4 !important;
  opacity: 1 !important;
}

.stSelectbox [data-baseweb="select"] [class*="singleValue"],
.stSelectbox [data-baseweb="select"] [class*="placeholder"] {
  color: #FFE8C4 !important;
  -webkit-text-fill-color: #FFE8C4 !important;
  opacity: 1 !important;
  font-size: 0.76rem !important;
  line-height: 44px !important;
  position: static !important;
  display: block !important;
  height: 44px !important;
  margin: 0 !important;
  padding: 0 !important;
  transform: none !important;
  top: unset !important;
  bottom: unset !important;
  left: unset !important;
  right: unset !important;
  white-space: nowrap !important;
  overflow: visible !important;
}

.stSelectbox [data-baseweb="select"] input {
  color: #FFE8C4 !important;
  -webkit-text-fill-color: #FFE8C4 !important;
  line-height: 1.2 !important;
  padding: 0 !important;
  margin: 0 !important;
}

/* Dropdown menu list/options for all selects */
div[role="listbox"] {
  background: rgba(58, 34, 19, 0.98) !important;
  border: 1px solid rgba(205, 145, 92, 0.55) !important;
  border-radius: 8px !important;
}

div[role="option"] {
  color: #F3D9AE !important;
  background: transparent !important;
}

div[role="option"][aria-selected="true"],
div[role="option"]:hover {
  background: rgba(212, 149, 93, 0.2) !important;
  color: #FFE4BD !important;
}

/* NUMBER INPUT */
.stNumberInput > div {
  position: relative !important;
}

.stNumberInput > div > div {
  display: flex !important;
  align-items: center !important;
  background: rgba(212,149,93,0.22) !important;
  border: 1.2px solid rgba(205,145,92,0.7) !important;
  border-radius: 7px !important;
  height: 40px !important;
  overflow: hidden !important;
  padding: 0 !important;
  gap: 0 !important;
  box-shadow: none !important;
  outline: none !important;
}

.stNumberInput input {
  flex: 1 1 auto !important;
  min-width: 0 !important;
  background: transparent !important;
  border: none !important;
  outline: none !important;
  color: #FFE8C4 !important;
  -webkit-text-fill-color: #FFE8C4 !important;
  font-family: 'DM Mono', monospace !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.04em !important;
  text-align: center !important;
  height: 100% !important;
  padding: 0 8px !important;
  margin: 0 !important;
  box-shadow: none !important;
}

.stNumberInput > div > div > div:last-child {
  position: static !important;
  display: flex !important;
  flex-direction: row !important;
  align-items: stretch !important;
  width: auto !important;
  min-width: auto !important;
  height: 100% !important;
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  padding: 0 !important;
  margin: 0 !important;
  gap: 0 !important;
  box-shadow: none !important;
  pointer-events: auto !important;
  inset: auto !important;
}

.stNumberInput > div > div > div:last-child > div {
  background: transparent !important;
  border: none !important;
  height: 100% !important;
  display: flex !important;
  padding: 0 !important;
}

.stNumberInput button {
  position: static !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 24px !important;
  min-width: 24px !important;
  max-width: 24px !important;
  height: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  background: transparent !important;
  border: none !important;
  border-left: 1px solid rgba(205,145,92,0.4) !important;
  border-radius: 0 !important;
  color: #FFE8C4 !important;
  cursor: pointer !important;
  transition: background 0.15s !important;
  line-height: 1 !important;
  box-shadow: none !important;
}

.stNumberInput button:first-of-type {
  border-left: none !important;
  border-right: 1px solid rgba(205,145,92,0.3) !important;
  order: -1 !important;
}

.stNumberInput button:hover {
  background: rgba(181,98,42,0.25) !important;
}

.stNumberInput button svg {
  width: 8px !important;
  height: 8px !important;
  display: block !important;
}

.stNumberInput button > * {
  width: 8px !important;
  height: 8px !important;
  line-height: 1 !important;
}

/* LABELS */
label, .stNumberInput label, .stSelectbox label {
  font-family: 'DM Mono', monospace !important;
  font-size: 0.5rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: var(--wheat) !important;
  font-weight: 600 !important;
  margin-bottom: 8px !important;
  display: block !important;
}

.stSelectbox,
.stNumberInput {
  margin-bottom: 10px !important;
}

/* BUTTONS */
.stButton > button {
  background: linear-gradient(135deg, #D4894A 0%, #B5622A 100%) !important;
  color: var(--cream) !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 7px 10px !important;
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 0.76rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.07em !important;
  text-transform: uppercase !important;
  width: 100% !important;
  cursor: pointer !important;
  transition: background 0.2s ease, box-shadow 0.2s ease !important;
  box-shadow: 0 4px 12px rgba(212, 137, 74, 0.2) !important;
}

.stButton > button:hover {
  background: linear-gradient(135deg, #c27a3f 0%, #a5521f 100%) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 16px rgba(212, 137, 74, 0.35) !important;
}

.stButton > button:active {
  transform: translateY(0) !important;
}

/* COLUMN SPACING */
[data-testid="stHorizontalBlock"] { gap: 12px !important; }

/* SPINNER */
.stSpinner > div { border-top-color: var(--copper) !important; }

/* TEXT */
body { color: var(--cream) !important; }
p { color: var(--cream) !important; }

/* CUSTOM CLASSES */
.metric-card {
  background: rgba(26, 15, 7, 0.45) !important;
  border: 1px solid rgba(181, 98, 42, 0.5) !important;
  border-radius: 4px !important;
  min-height: 64px !important;
  padding: 12px 16px !important;
  text-align: center !important;
  position: relative !important;
  overflow: visible !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  gap: 4px !important;
  transition: transform 0.2s, box-shadow 0.2s !important;
}

.metric-card:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(181, 98, 42, 0.15) !important;
}

.metric-card::before {
  content: none;
}

.section-chip {
  display: inline-flex !important;
  align-items: center !important;
  gap: 10px !important;
  border: 1px solid rgba(181, 98, 42, 0.45) !important;
  border-radius: 4px !important;
  background: rgba(26, 15, 7, 0.4) !important;
  padding: 5px 10px !important;
  margin-top: 16px !important;
  margin-bottom: 24px !important;
}

.section-chip .section-num {
  margin: 0 !important;
}

.section-chip .section-title {
  margin: 0 !important;
  font-size: 0.9rem !important;
  letter-spacing: 0.05em !important;
}

.section-title {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  color: var(--wheat) !important;
  letter-spacing: 0.04em !important;
  margin-bottom: 0 !important;
  display: inline-block !important;
}

.metric-value {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 1.1rem !important;
  font-weight: 600 !important;
  color: var(--copper) !important;
  line-height: 1 !important;
  margin-bottom: 0 !important;
}

.metric-label {
  font-family: 'DM Mono', monospace !important;
  font-size: 0.52rem !important;
  line-height: 1.4 !important;
  letter-spacing: 0.11em !important;
  text-transform: uppercase !important;
  color: var(--wheat) !important;
}

@media (max-width: 1200px) {
  [data-testid="stMain"] {
    padding: 20px 40px !important;
  }

  .metric-card {
    min-height: 56px !important;
  }

  .metric-value {
    font-size: 1rem !important;
  }

  .metric-label {
    font-size: 0.5rem !important;
    letter-spacing: 0.1em !important;
  }
}

@media (max-width: 768px) {
  [data-testid="stMain"] {
    padding: 14px 16px !important;
  }

  .form-panel {
    padding: 14px 12px !important;
  }

  .summary-row {
    padding: 8px 10px !important;
  }
}

.form-panel {
  background: rgba(255, 255, 255, 0.02) !important;
  border: 1px solid rgba(181, 98, 42, 0.15) !important;
  border-radius: 14px !important;
  overflow: hidden !important;
  padding: 28px 32px !important;
}

.section-title {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  color: var(--wheat) !important;
  letter-spacing: 0.04em !important;
  margin-bottom: 22px !important;
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
}

.section-num {
  font-family: 'DM Mono', monospace !important;
  font-size: 0.65rem !important;
  background: rgba(212, 137, 74, 0.15) !important;
  color: var(--copper) !important;
  padding: 2px 7px !important;
  border-radius: 3px !important;
  letter-spacing: 0.1em !important;
}

.summary-panel {
  background: transparent !important;
  border-radius: 0px !important;
  overflow: visible !important;
  border: none !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  height: auto !important;
  width: 100% !important;
  margin-top: 20px !important;
}

.summary-title {
  font-family: 'DM Mono', monospace !important;
  font-size: 0.58rem !important;
  letter-spacing: 0.2em !important;
  text-transform: uppercase !important;
  color: var(--wheat) !important;
  padding: 0 0 12px 0 !important;
  margin: 0 0 12px 0 !important;
  border-bottom: 1px solid rgba(181, 98, 42, 0.3) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
}

.summary-dot {
  width: 8px !important;
  height: 8px !important;
  background: var(--amber) !important;
  border-radius: 50% !important;
  animation: pulse 2s infinite !important;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.summary-content {
  padding: 0 !important;
  border: 1px solid rgba(181, 98, 42, 0.3) !important;
  border-radius: 8px !important;
  overflow: hidden !important;
}

.summary-row {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding: 12px 16px !important;
  border-bottom: 1px solid rgba(181, 98, 42, 0.2) !important;
  background: transparent !important;
}

.summary-row:last-child {
  border-bottom: none !important;
}

.summary-key {
  font-family: 'DM Mono', monospace !important;
  font-size: 0.54rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: var(--stone) !important;
}

.summary-val {
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  color: var(--cream) !important;
  text-align: right !important;
}

.result-card {
  background: rgba(255, 255, 255, 0.02) !important;
  border: 1px solid rgba(181, 98, 42, 0.15) !important;
  border-radius: 14px !important;
  overflow: hidden !important;
  margin-top: 24px !important;
}

.result-header {
  padding: 20px 24px !important;
  border-bottom: 1px solid rgba(181, 98, 42, 0.15) !important;
  background: rgba(44, 26, 14, 0.3) !important;
}

.result-title {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 0.92rem !important;
  font-weight: 600 !important;
  color: var(--wheat) !important;
  letter-spacing: 0.04em !important;
  margin: 0 !important;
}

.risk-label {
  font-family: 'DM Mono', monospace !important;
  font-size: 0.56rem !important;
  letter-spacing: 0.16em !important;
  text-transform: uppercase !important;
  color: var(--wheat) !important;
  margin-bottom: 10px !important;
}

.risk-bar-bg {
  background: rgba(255, 255, 255, 0.1) !important;
  border-radius: 4px !important;
  height: 8px !important;
  overflow: hidden !important;
  margin-bottom: 8px !important;
}

.risk-bar-fill {
  height: 100% !important;
  border-radius: 4px !important;
  background: linear-gradient(90deg, var(--sage), var(--copper)) !important;
}

.risk-value {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 1.55rem !important;
  font-weight: 600 !important;
  color: var(--copper) !important;
  text-align: center !important;
  margin-top: 6px !important;
}

.risk-desc {
  font-size: 0.72rem !important;
  color: var(--wheat) !important;
  text-align: center !important;
  margin-top: 4px !important;
  font-style: italic !important;
}

hr {
  border: none !important;
  border-top: 1px solid rgba(181, 98, 42, 0.15) !important;
  margin: 14px 0 !important;
}
"""


# ═════════════════󠀀══════════════════════════════════════════════════════════
# LANDING PAGE
# ════════════════════════════════════════════════════════════════════════════
def render_landing():
    st.markdown(
        """
        <style>
        /* Landing-only viewport fit */
        [data-testid="stMain"] {
          padding: 0 !important;
          margin: 0 !important;
          overflow: hidden !important;
        }

        .block-container {
          padding: 0 !important;
          margin: 0 !important;
          max-width: 100% !important;
        }

        [data-testid="stAppViewContainer"] {
          overflow: hidden !important;
          height: 100vh !important;
        }

        div[data-testid="stElementContainer"] iframe {
          width: 100vw !important;
          height: 100vh !important;
          border: none !important;
          margin: 0 !important;
          display: block !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

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

.navbar {{
  position:relative; z-index:10;
  padding:20px 70px;
  display:flex; align-items:center; justify-content:space-between;
  flex-shrink:0;
}}
.nav-logo {{ font-family:'Cormorant Garamond',serif; font-size:2rem; font-weight:600; letter-spacing:.08em; color:#F5EDD8; }}
.nav-logo span {{ color:#B5622A; }}
.nav-cta {{
  font-family:'DM Mono',monospace; font-size:.75rem; letter-spacing:.2em; text-transform:uppercase;
  background:rgba(96,122,94,.2); color:#A8C4A6;
  border:1px solid rgba(96,122,94,.4); border-radius:6px; padding:12px 28px;
  cursor:pointer; transition:background .2s;
}}
.nav-cta:hover {{ background:rgba(96,122,94,.35); }}

.hero-content {{
  flex:1; display:flex; flex-direction:column; justify-content:flex-start;
  position:relative; z-index:2;
  padding:20px 70px 30px;
  height:100%;
  overflow:hidden;
}}
.hero-body {{
  display:grid; grid-template-columns:1.2fr 420px;
  gap:40px; align-items:flex-start;
  height:100%;
}}

.badge {{
  display:inline-flex; align-items:center; gap:14px;
  font-family:'DM Mono',monospace; font-size:.7rem; letter-spacing:.28em; text-transform:uppercase;
  color:#B5622A; margin-bottom:16px; width:fit-content;
}}
.badge::before {{ content:''; width:35px; height:1px; background:#B5622A; }}

.hero-h1 {{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(2.4rem, 5vw, 4.8rem);
  font-weight:700; line-height:0.9; letter-spacing:-.02em;
  margin-bottom:12px; color:#F5EDD8;
}}
.hero-h1 em {{ font-style:italic; font-weight:300; color:#B5622A; display:block; }}
.hero-h1 .out {{ display:block; -webkit-text-stroke:1px rgba(232,201,138,.28); color:transparent; }}

.hero-sub {{
  font-size:.9rem; font-weight:300; color:#8A8070; line-height:1.7;
  max-width:480px; margin-bottom:20px;
}}
.hero-sub strong {{ color:#E8C98A; font-weight:600; }}

.cta-row {{ display:flex; gap:18px; align-items:center; }}
.btn-primary {{
  font-family:'DM Mono',monospace; font-size:.7rem; font-weight:700;
  letter-spacing:.2em; text-transform:uppercase;
  background:#D4894A; color:#1A0F07;
  border:none; border-radius:6px; padding:12px 24px;
  cursor:pointer; transition:background .2s; white-space:nowrap;
}}
.btn-primary:hover {{ background:#e8a060; }}

.data-card {{
  background:rgba(255,255,255,.035);
  border:1px solid rgba(181,98,42,.25);
  border-radius:14px; padding:16px 16px;
  backdrop-filter:blur(14px);
  height:fit-content;
}}
.ctitle {{
  font-family:'DM Mono',monospace; font-size:.75rem; letter-spacing:.22em; text-transform:uppercase;
  color:#8A8070; margin-bottom:16px; text-align:center;
}}
.meter {{ margin-bottom:14px; }}
.mt {{ display:flex; justify-content:space-between; margin-bottom:6px; }}
.mn {{ font-size:.85rem; color:#E8C98A; }}
.mv {{ font-family:'DM Mono',monospace; font-size:.8rem; color:#B5622A; }}
.mv.green {{ color:#5DBB63; }}
.bb {{ background:rgba(255,255,255,.07); border-radius:3px; height:6px; overflow:hidden; }}
.bf {{ height:100%; border-radius:3px; }}
.bdg-row {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:16px; justify-content:center; }}
.bdg {{ font-family:'DM Mono',monospace; font-size:.65rem; letter-spacing:.12em; text-transform:uppercase; padding:6px 12px; border-radius:3px; border:1px solid; }}
.bg2 {{ color:#607A5E; border-color:rgba(96,122,94,.4); background:rgba(96,122,94,.1); }}
.ba  {{ color:#D4894A; border-color:rgba(212,137,74,.4); background:rgba(212,137,74,.1); }}
.bs  {{ color:#8A8070; border-color:rgba(138,128,112,.3); background:rgba(138,128,112,.07); }}
</style>
</head>
<body>
<div class="hero">
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>

  <nav class="navbar">
    <div class="nav-logo">T<span>PLANT</span></div>
    <button class="nav-cta" onclick="navigateTo()">Mulai Sekarang</button>
  </nav>

  <div class="hero-content">
    <div class="hero-body">
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
    
    if st.query_params.get('page') == 'form':
        st.query_params.clear()
        go_to_form()


# ════════════════════════════════════════════════════════════════════════════
# FORM PAGE
# ════════════════════════════════════════════════════════════════════════════
def render_form():
    inject_css(FORM_CSS)

    # ── HEADER ──
    st.markdown("""
      <div style="text-align: center; margin-bottom: 28px; padding-bottom: 16px; border-bottom: 1px solid rgba(181, 98, 42, 0.15);">
        <div style="font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 600; letter-spacing: 0.08em; color: #E8C98A;">T<span style="color: #B5622A;">PLANT</span></div>
      </div>
    """, unsafe_allow_html=True)

    # ── METRICS ──
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{MODEL_FEATURES}</div><div class="metric-label">Features</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(SOIL_TYPES)}</div><div class="metric-label">Soil Types</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(PLANT_CATEGORIES)}</div><div class="metric-label">Plants</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">RF</div><div class="metric-label">Algorithm</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="metric-card"><div class="metric-value">v4.0</div><div class="metric-label">API Version</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height: 32px;"></div>', unsafe_allow_html=True)

    # ── MAIN GRID ──
    left_col, right_col = st.columns([1, 0.35], gap="medium")

    with left_col:
        # Section 01
        st.markdown('<div class="section-chip"><span class="section-num">01</span><span class="section-title">Fisika Tanah</span></div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            soil_type = st.selectbox("Tipe Tanah", SOIL_TYPES, key="soil_type")
            organic_matter_pct = st.number_input("Bahan Organik (%)", min_value=0.0, value=3.0, step=0.1, format="%.2f")
            salinity_ec = st.number_input("Salinitas (EC)", min_value=0.0, value=0.4, step=0.1, format="%.2f")
        with col_b:
            bulk_density = st.number_input("Bulk Density (g/cm³)", min_value=0.0, value=1.3, step=0.05, format="%.2f")
            cation_exchange_capacity = st.number_input("CEC (meq/100g)", min_value=0.0, value=15.0, step=0.5, format="%.2f")
            buffering_capacity = st.number_input("Kapasitas Penyangga", min_value=0.0, value=0.7, step=0.05, format="%.2f")

        st.markdown('<hr>', unsafe_allow_html=True)

        # Section 02
        st.markdown('<div class="section-chip"><span class="section-num">02</span><span class="section-title">Iklim &amp; Kelembaban</span></div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            soil_moisture_pct = st.number_input("Kelembaban Tanah (%)", min_value=0.0, value=25.0, step=1.0, format="%.2f")
            soil_temp_c = st.number_input("Suhu Tanah (°C)", value=21.0, step=0.5, format="%.2f")
            air_temp_c = st.number_input("Suhu Udara (°C)", value=25.0, step=0.5, format="%.2f")
            light_intensity_par = st.number_input("Intensitas Cahaya (PAR)", min_value=0.0, value=1000.0, step=50.0, format="%.2f")
        with col_b:
            moisture_limit_dry = st.number_input("Batas Kering (%)", min_value=0.0, value=15.0, step=1.0, format="%.2f")
            moisture_limit_wet = st.number_input("Batas Basah (%)", min_value=0.0, value=40.0, step=1.0, format="%.2f")

        st.markdown('<hr>', unsafe_allow_html=True)

        # Section 03
        st.markdown('<div class="section-chip"><span class="section-num">03</span><span class="section-title">pH &amp; Nutrisi</span></div>', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            soil_ph = st.number_input("pH Tanah", value=6.5, step=0.1, format="%.1f")
            nitrogen_ppm = st.number_input("Nitrogen (ppm)", min_value=0.0, value=100.0, step=5.0, format="%.2f")
            phosphorus_ppm = st.number_input("Fosfor (ppm)", min_value=0.0, value=50.0, step=5.0, format="%.2f")
        with col_b:
            potassium_ppm = st.number_input("Kalium (ppm)", min_value=0.0, value=100.0, step=5.0, format="%.2f")
            ph_stress_flag = st.selectbox("Stres pH", [0,1], format_func=lambda x:"Normal" if x==0 else "Stres", key="ph_stress_flag")
            nutrient_balance = st.selectbox("Keseimbangan Nutrisi", ["optimal","defisiensi","berlebih"], key="nutrient_balance")

        st.markdown('<hr>', unsafe_allow_html=True)

        # Section 04
        st.markdown('<div class="section-chip"><span class="section-num">04</span><span class="section-title">Tanaman</span></div>', unsafe_allow_html=True)
        plant_category = st.selectbox("Kategori Tanaman", PLANT_CATEGORIES, key="plant_category")

    with right_col:
        # Spacer untuk push ke bawah
        st.markdown('<div style="height: 100%;"></div>', unsafe_allow_html=True)

    # ── SUMMARY PANEL DI BAWAH ──
    st.markdown(f"""
        <div class="summary-panel">
            <div class="summary-title">
                ◆ Ringkasan Input
                <div class="summary-dot"></div>
            </div>
            <div class="summary-content">
                <div class="summary-row"><span class="summary-key">Tipe Tanah</span><span class="summary-val">{soil_type}</span></div>
                <div class="summary-row"><span class="summary-key">Kategori</span><span class="summary-val">{plant_category.capitalize()}</span></div>
                <div class="summary-row"><span class="summary-key">pH Tanah</span><span class="summary-val">{soil_ph:.1f}</span></div>
                <div class="summary-row"><span class="summary-key">Kelembaban</span><span class="summary-val">{soil_moisture_pct:.1f}%</span></div>
                <div class="summary-row"><span class="summary-key">Suhu Tanah</span><span class="summary-val">{soil_temp_c:.1f}°C</span></div>
                <div class="summary-row"><span class="summary-key">Suhu Udara</span><span class="summary-val">{air_temp_c:.1f}°C</span></div>
                <div class="summary-row"><span class="summary-key">Nitrogen</span><span class="summary-val">{nitrogen_ppm:.1f} ppm</span></div>
                <div class="summary-row"><span class="summary-key">Fosfor</span><span class="summary-val">{phosphorus_ppm:.1f} ppm</span></div>
                <div class="summary-row"><span class="summary-key">Kalium</span><span class="summary-val">{potassium_ppm:.1f} ppm</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)

    # ── BUTTONS DI BAWAH ──
    spacer_left, col_btn1, col_btn2, spacer_right = st.columns([1.35, 1, 1, 1.35])
    with col_btn1:
      if st.button("⟳  Jalankan Prediksi", use_container_width=True, key="btn_prediksi"):
        moisture_regime = derive_moisture_regime(
          soil_moisture_pct,
          moisture_limit_dry,
          moisture_limit_wet,
        )
        thermal_regime = derive_thermal_regime(air_temp_c)

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

        with st.spinner("🔄 Menganalisis parameter... Mohon tunggu sebentar"):
          try:
            r = requests.post(API_URL, json=payload, timeout=15)
            r.raise_for_status()
            st.session_state.prediction_result = r.json()
            st.rerun()
          except Exception as e:
            if isinstance(e, requests.HTTPError) and e.response is not None:
              detail_msg = None
              try:
                error_body = e.response.json()
                detail_msg = error_body.get("detail")
              except Exception:
                detail_msg = None

              if detail_msg:
                st.error(f"❌ Error API ({e.response.status_code}): {detail_msg}")
              else:
                st.error(f"❌ Error API ({e.response.status_code}): {e.response.text}")
            else:
              st.error(f"❌ Error: {str(e)}")

    with col_btn2:
        if st.button("← Kembali ke Landing", use_container_width=True, key="btn_back"):
            go_to_landing()

    if st.session_state.prediction_result:
        st.markdown('<br>', unsafe_allow_html=True)
        pred     = st.session_state.prediction_result
        risk_pct = max(0.0, min(100.0, float(pred.get("probability_failure", 0.0)) * 100.0))
        risk_level = "Rendah" if risk_pct < 35 else "Sedang" if risk_pct < 65 else "Tinggi"
        
        st.markdown(f"""
            <div class="result-card">
              <div class="result-header">
                <div class="result-title">✓ Hasil Analisis</div>
              </div>
              <div style="padding: 20px 24px;">
                <div class="risk-label">Tingkat Risiko Gagal Panen</div>
                <div class="risk-bar-bg"><div class="risk-bar-fill" style="width:{risk_pct:.1f}%;"></div></div>
                <div class="risk-value">{risk_pct:.1f}%</div>
                <div class="risk-desc">Risiko: {risk_level}</div>
              </div>
            </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# ROUTER
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    render_landing()
else:
    render_form()