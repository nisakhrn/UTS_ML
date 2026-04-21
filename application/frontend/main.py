# main.py

import streamlit as st
import requests

# ==============================
# KONFIGURASI HALAMAN
# ==============================
st.set_page_config(
    page_title="TPLANT | Agro Failure Predictor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# GAYA CSS (PUTIH BERSIH + LABEL JELAS)
# ==============================
CLEAN_WHITE_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&family=Manrope:wght@400;500;600;700;800&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* BACKGROUND PUTIH TOTAL */
html, body, .stApp, .main, .main .block-container {
    background-color: #ffffff !important;
    background: #ffffff !important;
}

body {
    background-color: #ffffff !important;
    font-family: 'Inter', sans-serif;
    color: #1a1a2e;
}

/* Hide Streamlit default elements */
#MainMenu, footer, header {
    visibility: hidden;
    display: none;
}

.main .block-container {
    padding: 2rem 2rem;
    max-width: 1300px;
    margin: 0 auto;
    background: #ffffff;
}

/* ========== HEADER ========== */
.main-header {
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #e8ecef;
}

.logo-row {
    display: flex;
    justify-content: center;
    align-items: baseline;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.logo-row h1 {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #1a1a2e;
    margin: 0;
    font-family: 'Manrope', sans-serif;
}

.logo-highlight {
    color: #2e7d64;
}

.tagline {
    text-align: center;
    color: #2e7d64;
    font-size: 0.85rem;
    letter-spacing: 3px;
    margin-top: 0.5rem;
    font-weight: 600;
}

/* ========== URL BAR ========== */
.url-bar {
    background: #f8f9fa;
    border-radius: 2rem;
    padding: 0.5rem 1rem;
    margin-bottom: 2rem;
    text-align: center;
    font-size: 0.8rem;
    color: #6c757d;
    font-family: monospace;
    border: 1px solid #e9ecef;
}

/* ========== METRICS ROW ========== */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}

.metric-card {
    background: #f8f9fa;
    border-radius: 1rem;
    padding: 1rem;
    text-align: center;
    border: 1px solid #e9ecef;
    transition: all 0.2s;
}

.metric-card:hover {
    border-color: #2e7d64;
    background: #ffffff;
    transform: translateY(-2px);
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #2e7d64;
}

.metric-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #6c757d;
    font-weight: 500;
}

/* ========== CARD STYLE ========== */
.card {
    background: #ffffff;
    border-radius: 1rem;
    padding: 1.2rem;
    border: 1px solid #e9ecef;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid #e9ecef;
}

.card-header h3 {
    font-size: 0.9rem;
    font-weight: 700;
    margin: 0;
    color: #1a1a2e;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ========== TAB STYLING ========== */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.25rem;
    background: #f8f9fa;
    border-radius: 0.75rem;
    padding: 0.25rem;
    margin-bottom: 1.2rem;
    border: 1px solid #e9ecef;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 0.6rem;
    padding: 0.5rem 1rem;
    font-weight: 600;
    font-size: 0.75rem;
    color: #6c757d;
}

.stTabs [aria-selected="true"] {
    background: #2e7d64 !important;
    color: white !important;
}

/* ========== LABEL STYLE - YANG INI PENTING! ========== */
/* Label harus terlihat jelas, warna gelap */
label, .stSelectbox label, .stNumberInput label {
    font-weight: 700 !important;
    font-size: 0.75rem !important;
    color: #1e293b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 0.5rem !important;
    display: block !important;
}

/* Label saat hover atau focus tetap gelap */
label:hover, .stSelectbox label:hover, .stNumberInput label:hover {
    color: #2e7d64 !important;
}

/* ========== FORM INPUTS ========== */
.stSelectbox > div {
    margin-bottom: 0.75rem;
}

.stSelectbox > div > div {
    border-radius: 0.5rem;
    border: 1px solid #dee2e6;
    background: #ffffff !important;
    min-height: 42px;
}

.stSelectbox > div > div > div {
    background: #ffffff !important;
    color: #1a1a2e !important;
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
}

/* Dropdown list container */
div[data-baseweb="popover"] {
    background: #ffffff !important;
    border: 1px solid #dee2e6 !important;
    border-radius: 0.5rem !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

div[data-baseweb="popover"] > div {
    background: #ffffff !important;
}

div[role="listbox"] {
    background: #ffffff !important;
    border: none !important;
}

div[role="option"] {
    background: #ffffff !important;
    color: #1a1a2e !important;
    padding: 0.5rem 0.75rem !important;
    font-size: 0.85rem !important;
    cursor: pointer !important;
}

div[role="option"]:hover {
    background: #f0fdf4 !important;
    color: #2e7d64 !important;
}

div[role="option"][aria-selected="true"] {
    background: #e8f5e9 !important;
    color: #2e7d64 !important;
    font-weight: 600 !important;
}

/* Number inputs */
.stNumberInput > div > div > input {
    border-radius: 0.5rem;
    border: 1px solid #dee2e6;
    padding: 0.6rem 0.75rem;
    font-size: 0.85rem;
    background: #ffffff;
    color: #1a1a2e;
    min-height: 42px;
}

.stNumberInput > div > div > input:focus,
.stSelectbox > div > div:focus-within {
    border-color: #2e7d64;
    box-shadow: 0 0 0 2px rgba(46,125,100,0.1);
    outline: none;
}

/* ========== SUMMARY LIST - 2 COLUMNS ========== */
.summary-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem 1rem;
}

.summary-list li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid #f0f2f4;
    font-size: 0.85rem;
}

.summary-label {
    font-weight: 700;
    color: #475569;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.summary-value {
    font-weight: 700;
    color: #1a1a2e;
    font-size: 0.85rem;
}

/* ========== PREDICT BUTTON ========== */
.stButton > button {
    background: #2e7d64;
    color: white;
    border: none;
    padding: 0.8rem;
    font-size: 0.9rem;
    font-weight: 700;
    border-radius: 0.75rem;
    width: 100%;
    transition: all 0.2s;
    cursor: pointer;
    margin-top: 0.5rem;
}

.stButton > button:hover {
    background: #1a5d4a;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(46,125,100,0.2);
}

/* ========== RESULT CARD ========== */
.result-card {
    background: #f8f9fa;
    border-radius: 0.75rem;
    padding: 1rem;
    margin-top: 1rem;
    border: 1px solid #e9ecef;
}

.result-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.8rem;
}

.result-icon {
    font-size: 2rem;
}

.result-title {
    font-size: 1rem;
    font-weight: 700;
    margin: 0;
    color: #1a1a2e;
}

.result-subtitle {
    font-size: 0.7rem;
    color: #6c757d;
}

.prob-section {
    margin-top: 0.8rem;
}

.prob-label {
    font-size: 0.7rem;
    font-weight: 600;
    margin-bottom: 0.3rem;
    color: #475569;
}

.progress-bar {
    background: #e9ecef;
    border-radius: 1rem;
    height: 8px;
    overflow: hidden;
}

.progress-fill {
    background: #2e7d64;
    height: 100%;
    border-radius: 1rem;
    transition: width 0.3s ease;
}

.progress-fill.danger {
    background: #dc3545;
}

.prob-percent {
    text-align: right;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.25rem;
    color: #1a1a2e;
}

/* Info Message */
.info-message {
    background: #f8f9fa;
    border-radius: 0.75rem;
    padding: 1rem;
    text-align: center;
    font-size: 0.8rem;
    color: #6c757d;
    margin-top: 1rem;
    border: 1px solid #e9ecef;
}

/* Divider */
.custom-divider {
    height: 1px;
    background: #e9ecef;
    margin: 1.5rem 0;
}

/* ========== PRODUCT SECTIONS ========== */
.section-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin: 1.5rem 0 1rem 0;
}

.section-header h3 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a1a2e;
}

.section-link {
    color: #2e7d64;
    font-size: 0.7rem;
    font-weight: 500;
    cursor: pointer;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
}

.product-card {
    background: #f8f9fa;
    border-radius: 0.75rem;
    padding: 1rem;
    text-align: center;
    border: 1px solid #e9ecef;
    transition: all 0.2s;
}

.product-card:hover {
    border-color: #2e7d64;
    transform: translateY(-3px);
    background: #ffffff;
}

.product-icon {
    font-size: 1.8rem;
}

.product-name {
    font-weight: 700;
    font-size: 0.85rem;
    margin: 0.5rem 0 0.25rem;
    color: #1a1a2e;
}

.product-price {
    font-size: 0.8rem;
    color: #2e7d64;
    font-weight: 600;
}

.old-price {
    text-decoration: line-through;
    color: #adb5bd;
    font-size: 0.7rem;
    margin-left: 0.3rem;
    font-weight: normal;
}

.product-sub {
    font-size: 0.7rem;
    color: #6c757d;
}

/* Responsive */
@media (max-width: 900px) {
    .product-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .metrics-row {
        grid-template-columns: repeat(3, 1fr);
    }
    .summary-list {
        grid-template-columns: 1fr;
    }
}
</style>
"""

st.markdown(CLEAN_WHITE_STYLE, unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000/predict/"

# ==============================
# HEADER
# ==============================
st.markdown("""
<div class="main-header">
    <div class="logo-row">
        <h1>TPLANT</h1>
        <h1><span class="logo-highlight">TPLANT</span></h1>
    </div>
    <div class="logo-row">
        <h1>PLANT<span class="logo-highlight">TREE</span>CREATE</h1>
        <h1>A<span class="logo-highlight">GREEN</span>FUTURE</h1>
    </div>
    <div class="tagline">🌿 AGRO FAILURE PREDICTOR | AURORA EDITION</div>
</div>
""", unsafe_allow_html=True)

# ==============================
# METRICS
# ==============================
st.markdown("""
<div class="metrics-row">
    <div class="metric-card"><div class="metric-value">21</div><div class="metric-label">FEATURES</div></div>
    <div class="metric-card"><div class="metric-value">9</div><div class="metric-label">SOIL TYPES</div></div>
    <div class="metric-card"><div class="metric-value">3</div><div class="metric-label">PLANTS</div></div>
    <div class="metric-card"><div class="metric-value">RF</div><div class="metric-label">ALGORITHM</div></div>
    <div class="metric-card"><div class="metric-value">v4.0</div><div class="metric-label">API</div></div>
</div>
""", unsafe_allow_html=True)

# ==============================
# DUA KOLOM UTAMA
# ==============================
col_left, col_right = st.columns([1.2, 0.8], gap="medium")

with col_left:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <h3>🌱 PARAMETER TANAH & IKLIM</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🪨 Fisika Tanah", "🌡️ Iklim & Kelembaban", "🧪 Kimia & Nutrisi", "🌱 Tanaman"])
    
    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            soil_type = st.selectbox("TIPE TANAH", ["Alluvial", "Chalky", "Clayey", "Laterite", "Loamy", "Peaty", "Saline", "Sandy", "Silty"], key="soil")
            organic_matter_pct = st.number_input("BAHAN ORGANIK (%)", min_value=0.0, value=3.0, step=0.1, format="%.2f")
            salinity_ec = st.number_input("SALINITAS (EC)", min_value=0.0, value=0.4, step=0.1, format="%.2f")
        with col_b:
            bulk_density = st.number_input("BULK DENSITY (g/cm³)", min_value=0.0, value=1.3, step=0.1, format="%.2f")
            cation_exchange_capacity = st.number_input("CEC (meq/100g)", min_value=0.0, value=15.0, step=0.1, format="%.2f")
            buffering_capacity = st.number_input("KAPASITAS PENYANGGA", min_value=0.0, value=0.7, step=0.1, format="%.2f")
    
    with tab2:
        col_a, col_b = st.columns(2)
        with col_a:
            soil_moisture_pct = st.number_input("KELEMBABAN TANAH (%)", min_value=0.0, value=25.0, step=0.1)
            soil_temp_c = st.number_input("SUHU TANAH (°C)", value=21.0, step=0.1)
            thermal_regime = st.selectbox("REJIM TERMAL", ["cold", "optimal", "heat_stress"])
        with col_b:
            moisture_limit_dry = st.number_input("BATAS KERING (%)", min_value=0.0, value=15.0, step=0.1)
            moisture_limit_wet = st.number_input("BATAS BASAH (%)", min_value=0.0, value=40.0, step=0.1)
            moisture_regime = st.selectbox("REJIM KELEMBABAN", ["dry", "optimal", "waterlogged"])
            air_temp_c = st.number_input("SUHU UDARA (°C)", value=25.0, step=0.1)
        light_intensity_par = st.number_input("INTENSITAS CAHAYA (PAR)", min_value=0.0, value=1000.0, step=10.0)
    
    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            soil_ph = st.number_input("pH TANAH", value=6.5, step=0.1, format="%.1f")
            nitrogen_ppm = st.number_input("NITROGEN (ppm)", min_value=0.0, value=100.0, step=1.0)
            phosphorus_ppm = st.number_input("FOSFOR (ppm)", min_value=0.0, value=50.0, step=1.0)
        with col_b:
            ph_stress_flag = st.selectbox("STRES pH", [0, 1], format_func=lambda x: "Normal" if x == 0 else "Stres")
            potassium_ppm = st.number_input("KALIUM (ppm)", min_value=0.0, value=100.0, step=1.0)
            nutrient_balance = st.selectbox("KESEIMBANGAN NUTRISI", ["optimal", "deficient", "excessive"])
    
    with tab4:
        plant_category = st.selectbox("KATEGORI TANAMAN", ["cereal", "legume", "vegetable"], label_visibility="visible")
    
    if st.button("🚀 JALANKAN PREDIKSI AI", use_container_width=True):
        payload = {
            "soil_type": soil_type, "bulk_density": bulk_density, "organic_matter_pct": organic_matter_pct,
            "cation_exchange_capacity": cation_exchange_capacity, "salinity_ec": salinity_ec,
            "buffering_capacity": buffering_capacity, "soil_moisture_pct": soil_moisture_pct,
            "moisture_limit_dry": moisture_limit_dry, "moisture_limit_wet": moisture_limit_wet,
            "moisture_regime": moisture_regime, "soil_temp_c": soil_temp_c, "air_temp_c": air_temp_c,
            "thermal_regime": thermal_regime, "light_intensity_par": light_intensity_par, "soil_ph": soil_ph,
            "ph_stress_flag": ph_stress_flag, "nitrogen_ppm": nitrogen_ppm, "phosphorus_ppm": phosphorus_ppm,
            "potassium_ppm": potassium_ppm, "nutrient_balance": nutrient_balance, "plant_category": plant_category
        }
        
        with st.spinner("🧠 Menganalisis dengan model Random Forest..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=10)
                response.raise_for_status()
                result = response.json()
                
                is_fail = result['prediction'] == 1
                prob = round(result['probability_failure'] * 100)
                
                st.session_state['prediction_result'] = {
                    'is_fail': is_fail,
                    'prob': prob
                }
                st.rerun()
                
            except requests.exceptions.ConnectionError:
                st.error("🔌 Gagal terhubung ke server API. Pastikan backend berjalan di http://127.0.0.1:8000")
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code if e.response is not None else "unknown"
                detail = e.response.text if e.response is not None else str(e)
                st.error(f"⚠️ API Error {status}: {detail}")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

with col_right:
    st.markdown(f"""
    <div class="card">
        <div class="card-header">
            <h3>📋 RINGKASAN INPUT</h3>
        </div>
        <ul class="summary-list">
            <li><span class="summary-label">TIPE TANAH</span><span class="summary-value">{soil_type}</span></li>
            <li><span class="summary-label">KATEGORI TANAMAN</span><span class="summary-value">{plant_category.upper()}</span></li>
            <li><span class="summary-label">pH TANAH</span><span class="summary-value">{soil_ph}</span></li>
            <li><span class="summary-label">KELEMBABAN TANAH</span><span class="summary-value">{soil_moisture_pct}%</span></li>
            <li><span class="summary-label">SUHU TANAH</span><span class="summary-value">{soil_temp_c}°C</span></li>
            <li><span class="summary-label">REJIM KELEMBABAN</span><span class="summary-value">{moisture_regime}</span></li>
            <li><span class="summary-label">REJIM TERMAL</span><span class="summary-value">{thermal_regime}</span></li>
            <li><span class="summary-label">NITROGEN</span><span class="summary-value">{nitrogen_ppm} ppm</span></li>
            <li><span class="summary-label">FOSFOR</span><span class="summary-value">{phosphorus_ppm} ppm</span></li>
            <li><span class="summary-label">KALIUM</span><span class="summary-value">{potassium_ppm} ppm</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if 'prediction_result' in st.session_state:
        res = st.session_state['prediction_result']
        icon = "⚠️" if res['is_fail'] else "✅"
        title = "Potensi Gagal Tanam Tinggi" if res['is_fail'] else "Kondisi Pertumbuhan Optimal"
        subtitle = "Segera lakukan tindakan korektif" if res['is_fail'] else "Parameter tanah dan iklim dalam batas aman"
        fill_class = "danger" if res['is_fail'] else ""
        
        st.markdown(f"""
        <div class="result-card">
            <div class="result-header">
                <div class="result-icon">{icon}</div>
                <div>
                    <div class="result-title">{title}</div>
                    <div class="result-subtitle">{subtitle}</div>
                </div>
            </div>
            <div class="prob-section">
                <div class="prob-label">PROBABILITAS KEGAGALAN</div>
                <div class="progress-bar">
                    <div class="progress-fill {fill_class}" style="width: {res['prob']}%;"></div>
                </div>
                <div class="prob-percent">{res['prob']}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-message">
            📊 Klik 'Jalankan Prediksi AI' untuk melihat hasil analisis.
        </div>
        """, unsafe_allow_html=True)

# ==============================
# DIVIDER
# ==============================
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)