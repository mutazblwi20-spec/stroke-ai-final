import pickle
import numpy as np
import random

# =============================
# Load Model
# =============================
model = pickle.load(open("FINAL_stroke_model.pkl", "rb"))

EXPECTED_FEATURES = 10


# =============================
# Prediction Function
# =============================
def predict_stroke(patient):

    # تحويل إلى numpy
    data = list(patient)

    # ---- FIX IMPORTANT ----
    # إذا المدخلات أقل من المطلوب نكملها بقيم افتراضية
    while len(data) < EXPECTED_FEATURES:
        data.append(0)

    data = np.array(data).reshape(1, -1)

    # Prediction
    prob = model.predict_proba(data)[0][1]

    diagnosis = "مصاب" if prob > 0.5 else "غير مصاب"

    # =============================
    # Smart Medical Advice AI
    # =============================
    if prob < 0.3:
        advice = {
            "color": "green",
            "advice": random.choice([
                "Excellent health condition. Maintain your lifestyle.",
                "Low stroke risk. Continue healthy diet and exercise.",
                "Your indicators look stable. Keep monitoring yearly."
            ])
        }

    elif prob < 0.6:
        advice = {
            "color": "orange",
            "advice": random.choice([
                "Moderate risk. Monitor blood pressure regularly.",
                "Consider improving diet and physical activity.",
                "Schedule periodic medical checkups."
            ])
        }

    else:
        advice = {
            "color": "red",
            "advice": random.choice([
                "High risk detected. Consult a doctor immediately.",
                "Medical evaluation recommended urgently.",
                "Reduce glucose and blood pressure immediately."
            ])
        }

    return diagnosis, prob, advice
