import pickle
import os
import numpy as np

# ======================
# Load Model (Cloud Safe)
# ======================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "FINAL_stroke_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


# ======================
# Prediction Function
# ======================

def predict_stroke(patient):

    # model expects 10 features
    EXPECTED_FEATURES = 10

    # convert to numpy
    data = list(patient)

    # auto complete missing features
    if len(data) < EXPECTED_FEATURES:
        data += [0] * (EXPECTED_FEATURES - len(data))

    data = np.array(data).reshape(1, -1)

    # prediction
    prob = float(model.predict_proba(data)[0][1])

    diagnosis = "مصاب" if prob >= 0.5 else "غير مصاب"

    # Smart AI Advice
    if prob < 0.30:
        advice = {
            "color": "green",
            "advice": "Low risk. Maintain exercise, hydration, and balanced diet."
        }

    elif prob < 0.70:
        advice = {
            "color": "orange",
            "advice": "Moderate risk. Monitor blood pressure, glucose, and sleep quality."
        }

    else:
        advice = {
            "color": "red",
            "advice": "High stroke risk detected. Consult a neurologist immediately."
        }

    return diagnosis, prob, advice
