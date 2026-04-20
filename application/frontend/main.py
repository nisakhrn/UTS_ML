import requests
import streamlit as st


st.set_page_config(page_title="Agro Failure Predictor", page_icon="🌱", layout="wide")

st.title("Agro Failure Predictor")
st.write("Masukkan kondisi tanah dan lingkungan untuk memprediksi apakah tanaman berpotensi gagal tumbuh.")

API_URL = "http://localhost:8000/predict/"


with st.form(key="agro_input_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        soil_type = st.selectbox("Soil type", ["Alluvial", "Chalky", "Clayey", "Laterite", "Loamy", "Peaty", "Saline", "Sandy", "Silty"])
        bulk_density = st.number_input("Bulk density", min_value=0.0, value=1.3, step=0.1)
        organic_matter_pct = st.number_input("Organic matter (%)", min_value=0.0, value=3.0, step=0.1)
        cation_exchange_capacity = st.number_input("Cation exchange capacity", min_value=0.0, value=15.0, step=1.0)
        salinity_ec = st.number_input("Salinity EC", min_value=0.0, value=0.4, step=0.1)
        buffering_capacity = st.number_input("Buffering capacity", min_value=0.0, value=0.7, step=0.1)

    with col2:
        soil_moisture_pct = st.number_input("Soil moisture (%)", min_value=0.0, value=25.0, step=0.1)
        moisture_limit_dry = st.number_input("Moisture limit dry", min_value=0.0, value=15.0, step=1.0)
        moisture_limit_wet = st.number_input("Moisture limit wet", min_value=0.0, value=40.0, step=1.0)
        moisture_regime = st.selectbox("Moisture regime", ["dry", "optimal", "waterlogged"])
        soil_temp_c = st.number_input("Soil temperature (C)", value=21.0, step=0.1)
        air_temp_c = st.number_input("Air temperature (C)", value=25.0, step=0.1)

    with col3:
        thermal_regime = st.selectbox("Thermal regime", ["cold", "heat_stress", "optimal"])
        light_intensity_par = st.number_input("Light intensity PAR", min_value=0.0, value=1000.0, step=10.0)
        soil_ph = st.number_input("Soil pH", value=6.5, step=0.01)
        ph_stress_flag = st.selectbox("pH stress flag", [0, 1])
        nitrogen_ppm = st.number_input("Nitrogen ppm", min_value=0.0, value=100.0, step=0.1)
        phosphorus_ppm = st.number_input("Phosphorus ppm", min_value=0.0, value=50.0, step=0.1)
        potassium_ppm = st.number_input("Potassium ppm", min_value=0.0, value=100.0, step=0.1)
        nutrient_balance = st.selectbox("Nutrient balance", ["optimal", "deficient", "excessive"])
        plant_category = st.selectbox("Plant category", ["cereal", "legume", "vegetable"])

    submit_button = st.form_submit_button(label="Predict")


if submit_button:
    user_input = {
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

    response = requests.post(API_URL, json=user_input, timeout=30)

    if response.status_code == 200:
        result = response.json()
        st.subheader("Hasil Prediksi")
        st.write(f"Prediksi: **{result['label']}**")

        probability = result.get("probability_failure")
        if probability is not None:
            st.write(f"Probabilitas failure: **{probability:.4f}**")

        if result["prediction"] == 1:
            st.error("Kondisi berpotensi gagal tumbuh.")
        else:
            st.success("Kondisi berpotensi aman untuk tumbuh.")
    else:
        st.error(f"Terjadi kesalahan dari backend: {response.text}")