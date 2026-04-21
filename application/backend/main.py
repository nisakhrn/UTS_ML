# backend/backend_main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import logging
import time
from pathlib import Path
import random

# ==============================
# KONFIGURASI
# ==============================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="🌱 Agro Failure Prediction API",
    description="API untuk memprediksi kegagalan tumbuh tanaman berdasarkan kondisi tanah. V3 - Elegant Edition.",
    version="3.0"
)

# Izinkan request dari frontend Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# PEMUATAN MODEL (DENGAN FALLBACK)
# ==============================
MODEL_PIPELINE = None
try:
    # Path ini mengasumsikan model berada di folder UTS_ML/model/model.pkl
    # Dari application/backend/main.py, naik dua level ke UTS_ML
    MODEL_PATH = Path(__file__).resolve().parents[2] / "model" / "model.pkl"
    if MODEL_PATH.exists():
        MODEL_PIPELINE = joblib.load(MODEL_PATH)
        logger.info(f"✅ Model pipeline berhasil dimuat dari {MODEL_PATH}")
    else:
        logger.warning(f"⚠️ Model tidak ditemukan di {MODEL_PATH}. API akan berjalan dalam mode DEMO.")
except Exception as e:
    logger.error(f"❌ Gagal memuat model: {e}. API akan berjalan dalam mode DEMO.")

# ==============================
# SKEMA INPUT (Pydantic Model)
# ==============================
class AgroInput(BaseModel):
    soil_type: str = Field(..., example="Loamy")
    bulk_density: float = Field(..., ge=0, example=1.3)
    # ... (Semua field input lainnya sama seperti sebelumnya) ...
    organic_matter_pct: float = Field(..., ge=0, example=3.0)
    cation_exchange_capacity: float = Field(..., ge=0, example=15.0)
    salinity_ec: float = Field(..., ge=0, example=0.4)
    buffering_capacity: float = Field(..., ge=0, example=0.7)
    soil_moisture_pct: float = Field(..., ge=0, example=25.0)
    moisture_limit_dry: float = Field(..., ge=0, example=15.0)
    moisture_limit_wet: float = Field(..., ge=0, example=40.0)
    moisture_regime: str = Field(..., example="optimal")
    soil_temp_c: float = Field(..., example=21.0)
    air_temp_c: float = Field(..., example=25.0)
    thermal_regime: str = Field(..., example="optimal")
    light_intensity_par: float = Field(..., ge=0, example=1000.0)
    soil_ph: float = Field(..., example=6.5)
    ph_stress_flag: int = Field(..., ge=0, le=1, example=0)
    nitrogen_ppm: float = Field(..., ge=0, example=100.0)
    phosphorus_ppm: float = Field(..., ge=0, example=50.0)
    potassium_ppm: float = Field(..., ge=0, example=100.0)
    nutrient_balance: str = Field(..., example="optimal")
    plant_category: str = Field(..., example="vegetable")

# ==============================
# ENDPOINTS API
# ==============================
@app.get("/", tags=["General"])
def read_root():
    return {"message": "🌱 Agro Failure Prediction API aktif", "status": "ok", "mode": "DEMO" if MODEL_PIPELINE is None else "PRODUCTION"}

@app.post("/predict/", summary="Prediksi kegagalan tanaman", tags=["Prediction"])
def predict(user_input: AgroInput) -> dict:
    start_time = time.time()
    input_df = pd.DataFrame([user_input.dict()])
    logger.info(f"📥 Input diterima: {user_input.dict()}")

    def demo_prediction() -> tuple[int, float]:
        is_fail = (
            user_input.soil_ph < 5.5
            or user_input.soil_ph > 8
            or user_input.salinity_ec > 3
            or user_input.thermal_regime == 'heat_stress'
        )
        prediction_value = 1 if is_fail else 0
        probability_value = (0.6 + random.random() * 0.3) if is_fail else (0.05 + random.random() * 0.25)
        return prediction_value, probability_value

    if MODEL_PIPELINE is None:
        # --- Mode Demo Jika Model Tidak Ada ---
        logger.info("🤖 Menjalankan prediksi dalam mode DEMO.")
        prediction, probability = demo_prediction()
    else:
        # --- Mode Produksi dengan fallback aman ---
        try:
            logger.info("🤖 Menjalankan prediksi dengan model pipeline.")
            prediction = MODEL_PIPELINE.predict(input_df)[0]
            probability = MODEL_PIPELINE.predict_proba(input_df)[0][1]
        except Exception:
            logger.exception("❌ Model pipeline gagal dipakai, fallback ke mode DEMO.")
            prediction, probability = demo_prediction()

    probability = float(probability)
    prediction = int(prediction)

    processing_time = round(time.time() - start_time, 4)
    result = {
        "prediction": int(prediction),
        "label": "Berisiko Gagal" if prediction == 1 else "Aman untuk Tumbuh",
        "probability_failure": float(probability),
        "processing_time_seconds": processing_time
    }
    logger.info(f"✅ Hasil prediksi: {result}")
    return result


# ==============================
# JALANKAN SERVER
# ==============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
