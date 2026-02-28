import pickle
import numpy as np
import random

# Load model
model = pickle.load(open("FINAL_stroke_model.pkl", "rb"))

def predict_stroke(data):

    data = np.array(data).reshape(1, -1)

    probability = model.predict_proba(data)[0][1]

    diagnosis = "مصاب" if probability > 0.5 else "غير مصاب"

    # Different advice every time
    low = [
        "Excellent health indicators. Keep active.",
        "Maintain balanced nutrition.",
        "Continue healthy lifestyle habits."
    ]

    medium = [
        "Monitor blood pressure regularly.",
        "Reduce sugar intake.",
        "Increase physical activity weekly."
    ]

    high = [
        "Consult a physician immediately.",
        "Medical evaluation recommended.",
        "High stroke risk detected — seek care."
    ]

    if probability < 0.3:
        advice = {"color":"green","advice":random.choice(low)}
    elif probability < 0.7:
        advice = {"color":"orange","advice":random.choice(medium)}
    else:
        advice = {"color":"red","advice":random.choice(high)}

    return diagnosis, probability, advice
