import pickle
import os
import numpy as np

# ===============================
# تحميل الموديل بطريقة آمنة
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "FINAL_stroke_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


# ===============================
# Prediction Function
# ===============================

def predict_stroke(patient):

    # تحويل البيانات لشكل numpy
    data = np.array(patient).reshape(1, -1)

    # توقع الاحتمال
    prob = model.predict_proba(data)[0][1]

    # التشخيص
    diagnosis = "مصاب" if prob >= 0.5 else "غير مصاب"

    # نصيحة ذكية
    if prob < 0.3:
        advice = {
            "color": "green",
            "advice": "Excellent condition. Maintain healthy lifestyle and regular exercise."
        }

    elif prob < 0.7:
        advice = {
            "color": "orange",
            "advice": "Moderate risk. Monitor blood pressure and glucose regularly."
        }

    else:
        advice = {
            "color": "red",
            "advice": "High stroke risk. Immediate medical consultation recommended."
        }

    return diagnosis, prob, adviceimport pickle
import os
import numpy as np

# ===============================
# تحميل الموديل بطريقة آمنة
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "FINAL_stroke_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


# ===============================
# Prediction Function
# ===============================

def predict_stroke(patient):

    # تحويل البيانات لشكل numpy
    data = np.array(patient).reshape(1, -1)

    # توقع الاحتمال
    prob = model.predict_proba(data)[0][1]

    # التشخيص
    diagnosis = "مصاب" if prob >= 0.5 else "غير مصاب"

    # نصيحة ذكية
    if prob < 0.3:
        advice = {
            "color": "green",
            "advice": "Excellent condition. Maintain healthy lifestyle and regular exercise."
        }

    elif prob < 0.7:
        advice = {
            "color": "orange",
            "advice": "Moderate risk. Monitor blood pressure and glucose regularly."
        }

    else:
        advice = {
            "color": "red",
            "advice": "High stroke risk. Immediate medical consultation recommended."
        }

    return diagnosis, prob, advice
