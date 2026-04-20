from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Agro Environment Classifier", version="1.0.0")


class AgroInput(BaseModel):
    soil_type: str = Field(..., description="Jenis tanah")
    bulk_density: float = Field(..., ge=0)
    organic_matter_pct: float = Field(..., ge=0)
    cation_exchange_capacity: float = Field(..., ge=0)
    salinity_ec: float = Field(..., ge=0)
    buffering_capacity: float = Field(..., ge=0)
    soil_moisture_pct: float = Field(..., ge=0)
    moisture_limit_dry: float = Field(..., ge=0)
    moisture_limit_wet: float = Field(..., ge=0)
    moisture_regime: str = Field(..., description="Regim kelembapan")
    soil_temp_c: float
    air_temp_c: float
    thermal_regime: str = Field(..., description="Regim suhu")
    light_intensity_par: float = Field(..., ge=0)
    soil_ph: float
    ph_stress_flag: int = Field(..., ge=0, le=1)
    nitrogen_ppm: float = Field(..., ge=0)
    phosphorus_ppm: float = Field(..., ge=0)
    potassium_ppm: float = Field(..., ge=0)
    nutrient_balance: str = Field(..., description="Keseimbangan nutrisi")
    plant_category: str = Field(..., description="Kategori tanaman")


MODEL_PATH = Path(__file__).resolve().parents[2] / "model" / "model.pkl"
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health_check():
    return {"status": "ok", "model_path": str(MODEL_PATH)}


@app.post("/predict/", summary="Prediksi apakah kondisi tanah menyebabkan failure")
def predict(user_input: AgroInput):
    try:
        data = pd.DataFrame([user_input.model_dump()])
        prediction = model.predict(data)[0]
        probability = None

        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(data)[0][1])

        return {
            "prediction": int(prediction),
            "label": "Failure" if int(prediction) == 1 else "No Failure",
            "probability_failure": probability,
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {error}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


