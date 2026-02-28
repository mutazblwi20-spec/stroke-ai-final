import pickle
import numpy as np

with open("FINAL_stroke_model.pkl","rb") as f:
    model = pickle.load(f)

def predict_stroke(patient):

    data = np.array(patient).reshape(1,-1)

    prob = model.predict_proba(data)[0][1]
    diagnosis = "مصاب" if prob > 0.5 else "غير مصاب"

    if prob < 0.3:
        advice = {"color":"green",
                  "advice":"Low risk. Maintain healthy lifestyle."}
    elif prob < 0.7:
        advice = {"color":"orange",
                  "advice":"Moderate risk. Monitor blood pressure and glucose."}
    else:
        advice = {"color":"red",
                  "advice":"High risk. Consult a physician immediately."}

    return diagnosis, prob, advice
