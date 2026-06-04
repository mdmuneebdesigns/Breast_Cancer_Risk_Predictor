from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and scaler
model = joblib.load("final_model.pkl")
scaler = joblib.load("scaler.pkl")

# Input data model (30 features)
class InputFeatures(BaseModel):
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float
    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    compactness_se: float
    concavity_se: float
    concave_points_se: float
    symmetry_se: float
    fractal_dimension_se: float
    radius_worst: float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float

@app.post("/predict")
async def predict(data: InputFeatures):
    try:
        # Convert input to numpy array
        features = np.array([[
            data.radius_mean, data.texture_mean, data.perimeter_mean, data.area_mean,
            data.smoothness_mean, data.compactness_mean, data.concavity_mean,
            data.concave_points_mean, data.symmetry_mean, data.fractal_dimension_mean,
            data.radius_se, data.texture_se, data.perimeter_se, data.area_se,
            data.smoothness_se, data.compactness_se, data.concavity_se,
            data.concave_points_se, data.symmetry_se, data.fractal_dimension_se,
            data.radius_worst, data.texture_worst, data.perimeter_worst, data.area_worst,
            data.smoothness_worst, data.compactness_worst, data.concavity_worst,
            data.concave_points_worst, data.symmetry_worst, data.fractal_dimension_worst
        ]])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]  # 0 or 1
        confidence = model.predict_proba(features_scaled)[0][prediction] * 100
        return {"prediction": int(prediction), "confidence": confidence}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def root():
    return {"message": "Breast Cancer Prediction API"}