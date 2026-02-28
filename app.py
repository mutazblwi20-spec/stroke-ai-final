import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import joblib

# ===============================
# إعداد الصفحة
# ===============================
st.set_page_config(
    page_title="Medical Stroke AI",
    page_icon="🧠",
    layout="centered"
)

# ===============================
# تحميل CSS
# ===============================
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ===============================
# تحميل نموذج الذكاء الاصطناعي
# ===============================
model = joblib.load("FINAL_stroke_model.pkl")

# ===============================
# النصائح الطبية الذكية
# ===============================
def medical_advice(prob):

    if prob < 0.30:
        return {
            "advice": "✅ Excellent condition. Maintain exercise and healthy diet.",
            "color": "green"
        }

    elif prob < 0.60:
        return {
            "advice": "⚠️ Moderate risk. Monitor blood pressure and glucose regularly.",
            "color": "orange"
        }

    else:
        return {
            "advice": "🚨 High stroke risk detected. Consult a doctor immediately.",
            "color": "red"
        }

# ===============================
# دالة التنبؤ النهائية
# ===============================
def predict_stroke(patient_data):

    columns = model.feature_names_in_

    data = pd.DataFrame(
        np.zeros((1, len(columns))),
        columns=columns
    )

    data["age"] = patient_data[0]
    data["hypertension"] = patient_data[1]
    data["heart_disease"] = patient_data[2]
    data["avg_glucose_level"] = patient_data[3]
    data["bmi"] = patient_data[4]

    probability = model.predict_proba(data)[0][1]

    diagnosis = "مصاب" if probability >= 0.5 else "غير مصاب"

    return diagnosis, probability, medical_advice(probability)

# ===============================
# واجهة التطبيق
# ===============================
st.title("🧠 Medical Stroke Prediction AI")
st.caption("AI Clinical Decision Support System")

st.divider()

# ===============================
# إدخال البيانات
# ===============================
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 1, 100, 30)
    hypertension = st.selectbox("Hypertension", [0,1])
    heart = st.selectbox("Heart Disease", [0,1])

with col2:
    glucose = st.number_input("Glucose Level", 50.0, 300.0, 100.0)
    bmi = st.number_input("BMI", 10.0, 60.0, 25.0)

patient = [age, hypertension, heart, glucose, bmi]

st.divider()

# ===============================
# زر التحليل
# ===============================
if st.button("🔬 Analyze Patient Risk"):

    diagnosis, prob, advice = predict_stroke(patient)

    st.markdown('<div class="result-box">', unsafe_allow_html=True)

    # النتيجة
    if diagnosis == "مصاب":
        st.error(f"🚨 Diagnosis: {diagnosis}")
    else:
        st.success(f"✅ Diagnosis: {diagnosis}")

    # نسبة الخطر
    risk_percent = round(prob * 100, 2)
    st.subheader(f"Risk Score: {risk_percent}%")

    # ===============================
    # الرسم البياني
    # ===============================
    fig, ax = plt.subplots()

    ax.pie(
        [risk_percent, 100-risk_percent],
        startangle=90,
        wedgeprops=dict(width=0.4)
    )

    ax.text(0, 0, f"{risk_percent}%", ha='center', va='center', fontsize=20)

    st.pyplot(fig)

    # ===============================
    # النصيحة
    # ===============================
    if advice["color"] == "green":
        st.success(advice["advice"])
    elif advice["color"] == "orange":
        st.warning(advice["advice"])
    else:
        st.error(advice["advice"])

    st.markdown('</div>', unsafe_allow_html=True)
