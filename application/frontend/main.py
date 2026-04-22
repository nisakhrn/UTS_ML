import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/predict/"


st.set_page_config(
    page_title="TPLANT | Agro Failure Predictor",
    page_icon="T",
    layout="wide",
    initial_sidebar_state="collapsed",
)


STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:wght@300;400;500&family=Instrument+Sans:wght@400;500;600&display=swap');

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
}

html, body, .stApp {
  background: var(--light);
  color: var(--soil);
  font-family: 'Instrument Sans', sans-serif;
}

#MainMenu, footer, header {
  visibility: hidden;
  display: none;
}

.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    radial-gradient(ellipse 80% 60% at 10% 20%, rgba(181,98,42,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 60% 80% at 90% 80%, rgba(92,122,90,0.08) 0%, transparent 60%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
}

.main .block-container {
  max-width: 1480px;
  padding: 28px 24px 40px;
  position: relative;
  z-index: 1;
}

.hero {
  padding: 24px 0 26px;
  text-align: center;
  border-bottom: 1px solid rgba(44,26,14,0.1);
  margin-bottom: 30px;
}

.logo-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: var(--moss);
  border-radius: 9px;
  color: var(--wheat);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'DM Mono', monospace;
  font-size: 0.88rem;
}

.logo-text {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2.35rem;
  font-weight: 600;
  letter-spacing: 0.08em;
}

.logo-text span {
  color: var(--copper);
}

.tagline {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.6rem;
  font-weight: 300;
  font-style: italic;
  color: var(--bark);
}

.tagline strong {
  font-style: normal;
  font-weight: 600;
  color: var(--copper);
}

.edition-badge {
  margin-top: 8px;
  display: inline-block;
  font-family: 'DM Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--stone);
  border: 1px solid rgba(138,128,112,0.35);
  padding: 5px 14px;
  border-radius: 2px;
}

.metrics-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.metric-card {
  background: #ffffff;
  border: 1px solid rgba(44,26,14,0.08);
  border-radius: 10px;
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
  color: var(--copper);
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

.panel {
  background: #ffffff;
  border: 1px solid rgba(44,26,14,0.08);
  border-radius: 14px;
  overflow: hidden;
}

.section-block {
  padding: 22px 24px;
  border-bottom: 1px solid rgba(44,26,14,0.07);
}

.section-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.08rem;
  font-weight: 600;
  color: var(--bark);
  letter-spacing: 0.04em;
  margin-bottom: 14px;
}

.section-num {
  font-family: 'DM Mono', monospace;
  font-size: 0.62rem;
  background: var(--fog);
  color: var(--stone);
  padding: 2px 7px;
  border-radius: 3px;
  letter-spacing: 0.1em;
  margin-right: 8px;
}

.summary-card {
  background: #ffffff;
  border: 1px solid rgba(44,26,14,0.08);
  border-radius: 14px;
  overflow: hidden;
}

.summary-header {
  background: var(--soil);
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
  border-bottom: 1px dashed rgba(44,26,14,0.08);
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
  color: var(--bark);
}

.landing-card {
  background: #ffffff;
  border: 1px solid rgba(44,26,14,0.08);
  border-radius: 14px;
  padding: 24px;
  margin: 0 auto 18px;
}

.landing-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 2rem;
  color: var(--bark);
  margin-bottom: 10px;
}

.landing-desc {
  font-size: 0.95rem;
  color: var(--stone);
  line-height: 1.7;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 16px;
}

.feature-item {
  background: var(--fog);
  border: 1px solid rgba(44,26,14,0.08);
  border-radius: 10px;
  padding: 12px;
}

.feature-item h4 {
  font-family: 'DM Mono', monospace;
  font-size: 0.62rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--bark);
  margin-bottom: 6px;
}

.feature-item p {
  font-size: 0.82rem;
  color: var(--stone);
  line-height: 1.5;
}

.result-card {
  margin-top: 14px;
  background: #ffffff;
  border: 1px solid rgba(44,26,14,0.08);
  border-radius: 14px;
  overflow: hidden;
}

.result-head {
  padding: 14px 18px;
  border-bottom: 1px solid rgba(44,26,14,0.08);
  font-family: 'Cormorant Garamond', serif;
  font-size: 1rem;
  font-weight: 600;
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
  background: var(--fog);
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
  color: var(--copper);
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
  background: var(--moss);
  color: var(--cream);
  border: none;
  border-radius: 10px;
  padding: 14px;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.04rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.stButton > button:hover {
  background: var(--sage);
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
  background: var(--fog) !important;
  border: 1px solid rgba(44,26,14,0.12) !important;
  border-radius: 8px !important;
  color: var(--soil) !important;
}

input[readonly] {
  font-family: 'DM Mono', monospace;
  color: var(--moss) !important;
}

@media (max-width: 900px) {
  .metrics-row {
    grid-template-columns: repeat(3, 1fr);
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style>
"""

st.markdown(STYLES, unsafe_allow_html=True)

if "show_prediction_form" not in st.session_state:
  st.session_state["show_prediction_form"] = False

st.markdown(
  """
  <div class="hero">
    <div class="logo-row">
      <div class="logo-icon">TP</div>
      <div class="logo-text">T<span>PLANT</span></div>
    </div>
    <div class="tagline">Plant Tree, <strong>Create a Green Future</strong></div>
    <div class="edition-badge">Agro Failure Predictor · Aurora Edition</div>
  </div>
  """,
  unsafe_allow_html=True,
)

if not st.session_state["show_prediction_form"]:
  st.markdown(
    """
    <div class="landing-card">
      <div class="landing-title">Selamat Datang di TPLANT</div>
      <div class="landing-desc">
        Sistem ini membantu mengestimasi risiko kegagalan pertumbuhan tanaman berdasarkan parameter tanah,
        iklim, dan nutrisi. Input yang kamu isi akan diproses oleh model machine learning sehingga kamu bisa
        mendapatkan indikasi risiko secara cepat sebelum mengambil keputusan budidaya.
      </div>
      <div class="feature-grid">
        <div class="feature-item">
          <h4>Input Terstruktur</h4>
          <p>Form disusun sesuai fitur model: fisika tanah, iklim, kimia-nutrisi, dan kategori tanaman.</p>
        </div>
        <div class="feature-item">
          <h4>Prediksi Cepat</h4>
          <p>Hasil memberikan probabilitas risiko kegagalan untuk mendukung evaluasi kondisi lahan.</p>
        </div>
        <div class="feature-item">
          <h4>Selaras Dataset</h4>
          <p>Semua pilihan kategorikal di form disesuaikan dengan skema dataset dan model backend.</p>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
  )
  if st.button("Mulai Prediksi", use_container_width=True):
    st.session_state["show_prediction_form"] = True
    st.rerun()
else:
  st.markdown(
      """
      <div class="metrics-row">
        <div class="metric-card"><div class="metric-value">21</div><div class="metric-label">Features</div></div>
        <div class="metric-card"><div class="metric-value">9</div><div class="metric-label">Soil Types</div></div>
        <div class="metric-card"><div class="metric-value">3</div><div class="metric-label">Plants</div></div>
        <div class="metric-card"><div class="metric-value">RF</div><div class="metric-label">Algorithm</div></div>
        <div class="metric-card"><div class="metric-value">v4.0</div><div class="metric-label">API Version</div></div>
      </div>
      """,
      unsafe_allow_html=True,
  )

  top_left, top_right = st.columns([0.85, 0.15])
  with top_right:
    if st.button("Kembali", use_container_width=True):
      st.session_state["show_prediction_form"] = False
      st.rerun()

  st.markdown('<div class="panel">', unsafe_allow_html=True)

  st.markdown('<div class="section-block"><div class="section-title"><span class="section-num">01</span>Fisika Tanah</div></div>', unsafe_allow_html=True)
  a1, a2 = st.columns(2)
  with a1:
    soil_type = st.selectbox(
      "Tipe Tanah",
      ["Alluvial", "Chalky", "Clayey", "Laterite", "Loamy", "Peaty", "Saline", "Sandy", "Silty"],
      key="soil_type",
    )
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
    thermal_regime = st.selectbox("Rejim Termal", ["cold", "optimal", "heat_stress"], key="thermal_regime")
  with b2:
    moisture_limit_dry = st.number_input("Batas Kering (%)", min_value=0.0, value=15.0, step=1.0, format="%.2f")
    moisture_limit_wet = st.number_input("Batas Basah (%)", min_value=0.0, value=40.0, step=1.0, format="%.2f")
    light_intensity_par = st.number_input("Intensitas Cahaya (PAR)", min_value=0.0, value=1000.0, step=50.0, format="%.2f")
    moisture_regime = st.selectbox("Rejim Kelembaban", ["dry", "optimal", "waterlogged"], key="moisture_regime")

  st.markdown('<div class="section-block"><div class="section-title"><span class="section-num">03</span>pH dan Nutrisi</div></div>', unsafe_allow_html=True)
  d1, d2 = st.columns(2)
  with d1:
    soil_ph = st.number_input("pH Tanah", value=6.5, step=0.1, format="%.1f")
    nitrogen_ppm = st.number_input("Nitrogen (ppm)", min_value=0.0, value=100.0, step=5.0, format="%.2f")
    phosphorus_ppm = st.number_input("Fosfor (ppm)", min_value=0.0, value=50.0, step=5.0, format="%.2f")
  with d2:
    potassium_ppm = st.number_input("Kalium (ppm)", min_value=0.0, value=100.0, step=5.0, format="%.2f")
    ph_stress_flag = st.selectbox("Stres pH", [0, 1], format_func=lambda x: "Normal" if x == 0 else "Stres", key="ph_stress_flag")
    nutrient_balance = st.selectbox("Keseimbangan Nutrisi", ["optimal", "deficient", "excessive"], key="nutrient_balance")

  st.markdown('<div class="section-block"><div class="section-title"><span class="section-num">04</span>Tanaman</div></div>', unsafe_allow_html=True)
  plant_category = st.selectbox("Kategori Tanaman", ["cereal", "legume", "vegetable"], key="plant_category")

  st.markdown('</div>', unsafe_allow_html=True)

  st.markdown(
    f"""
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
    """,
    unsafe_allow_html=True,
  )

  if st.button("Jalankan Prediksi", use_container_width=True):
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
        st.session_state["prediction_result"] = result
      except requests.exceptions.ConnectionError:
        st.error("Gagal terhubung ke API backend. Pastikan server berjalan di http://127.0.0.1:8000")
      except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        detail = e.response.text if e.response is not None else str(e)
        st.error(f"API Error {status}: {detail}")
      except Exception as e:
        st.error(f"Error: {e}")

  if "prediction_result" in st.session_state:
    pred = st.session_state["prediction_result"]
    risk_pct = max(0.0, min(100.0, float(pred.get("probability_failure", 0.0)) * 100.0))
    risk_desc = "Risiko rendah" if risk_pct < 35 else "Risiko sedang" if risk_pct < 65 else "Risiko tinggi"

    st.markdown(
      f"""
      <div class="result-card">
        <div class="result-head">Hasil Analisis</div>
        <div class="result-body">
        <div class="risk-label">Tingkat Risiko Kegagalan</div>
        <div class="risk-bar-bg"><div class="risk-bar-fill" style="width:{risk_pct:.1f}%"></div></div>
        <div class="risk-value">{risk_pct:.1f}%</div>
        <div class="risk-desc">{risk_desc}</div>
        </div>
      </div>
      """,
      unsafe_allow_html=True,
    )
