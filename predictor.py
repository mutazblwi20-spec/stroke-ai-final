import pickle
import os
import numpy as np

# ======================
# Safe Model Loader
# ======================

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "FINAL_stroke_model.pkl")

def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

model = load_model()

# ======================
# Prediction
# ======================

def predict_stroke(patient):

    EXPECTED_FEATURES = 10

    data = list(patient)

    if len(data) < EXPECTED_FEATURES:
        data += [0]*(EXPECTED_FEATURES-len(data))

    data = np.array(data).reshape(1,-1)

    prob = float(model.predict_proba(data)[0][1])

    diagnosis = "مصاب" if prob >= 0.5 else "غير مصاب"

    if prob < 0.3:
        advice = {
            "color":"green",
            "advice":"Low risk. Maintain healthy lifestyle."
        }
    elif prob < 0.7:
        advice = {
            "color":"orange",
            "advice":"Moderate risk. Monitor glucose and blood pressure."
        }
    else:
        advice = {
            "color":"red",
            "advice":"High risk. Consult a neurologist immediately."
        }

    return diagnosis, prob, advice
