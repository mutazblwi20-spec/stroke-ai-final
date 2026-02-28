import pickle
import numpy as np
import os

# =========================
# SAFE MODEL LOADING
# =========================

MODEL_PATH = "FINAL_stroke_model.pkl"

model = None

def load_model():
    global model

    if model is None:
        try:
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            print("✅ Model loaded successfully")

        except Exception as e:
            print("❌ Model loading error:", e)
            model = None

load_model()

# =========================
# Prediction Function
# =========================

def predict_stroke(patient):

    if model is None:
        return "خطأ", 0.0, {
            "color": "red",
            "advice": "Model failed to load"
        }

    data = np.array([patient])

    prob = model.predict_proba(data)[0][1]

    if prob > 0.5:
        diagnosis = "مصاب"
        advice = {
            "color": "red",
            "advice": "High stroke risk. Immediate clinical evaluation recommended."
        }

    elif prob > 0.25:
        diagnosis = "خطر متوسط"
        advice = {
            "color": "orange",
            "advice": "Moderate risk. Improve lifestyle and monitor health."
        }

    else:
        diagnosis = "سليم"
        advice = {
            "color": "green",
            "advice": "Low risk. Maintain healthy habits."
        }

    return diagnosis, prob, advice
