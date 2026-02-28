import joblib
import pandas as pd
import numpy as np

model = joblib.load("FINAL_stroke_model.pkl")

def predict_stroke(patient):

    columns = model.feature_names_in_

    data = pd.DataFrame(
        np.zeros((1, len(columns))),
        columns=columns
    )

    data["age"] = patient[0]
    data["hypertension"] = patient[1]
    data["heart_disease"] = patient[2]
    data["avg_glucose_level"] = patient[3]
    data["bmi"] = patient[4]

    prob = model.predict_proba(data)[0][1]

    diagnosis = "مصاب" if prob >= 0.5 else "غير مصاب"

    return diagnosis, prob
