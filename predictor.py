import streamlit as st
import numpy as np
import joblib

# =====================
# Load model once
# =====================
@st.cache_resource
def load_model():
    return joblib.load("FINAL_stroke_model.pkl")

model = load_model()

# =====================
# Prediction Function
# =====================
def predict_stroke(patient):

    data = np.array(patient).reshape(1, -1)

    prob = model.predict_proba(data)[0][1]

    if prob > 0.5:
        diagnosis = "مصاب"
        advice = {
            "color": "red",
            "advice": "🚨 High stroke risk. Visit a doctor immediately."
        }

    elif prob > 0.3:
        diagnosis = "غير مصاب"
        advice = {
            "color": "orange",
            "advice": "⚠️ Moderate risk. Monitor glucose and blood pressure."
        }

    else:
        diagnosis = "غير مصاب"
        advice = {
            "color": "green",
            "advice": "✅ Low risk. Maintain healthy lifestyle."
        }

    return diagnosis, prob, advice
