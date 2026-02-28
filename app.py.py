import streamlit as st
import matplotlib.pyplot as plt
from predictor import predict_stroke
import numpy as np

# ==================
# تحميل CSS
# ==================
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.set_page_config(page_title="Medical Stroke AI", page_icon="🧠")

# ==================
# Header
# ==================
st.title("🧠 Medical Stroke Prediction AI")
st.caption("AI Clinical Decision Support System")

st.divider()

# ==================
# Inputs
# ==================
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

# ==================
# Prediction Button
# ==================
if st.button("🔬 Analyze Patient Risk"):

    diagnosis, prob, advice = predict_stroke(patient)

    st.markdown('<div class="result-box">', unsafe_allow_html=True)

    # Diagnosis
    if diagnosis == "مصاب":
        st.error(f"🚨 Diagnosis: {diagnosis}")
    else:
        st.success(f"✅ Diagnosis: {diagnosis}")

    # Risk %
    risk_percent = round(prob*100,2)
    st.subheader(f"Risk Score: {risk_percent}%")

    # Gauge Chart
    fig, ax = plt.subplots()

    ax.pie(
        [risk_percent, 100-risk_percent],
        startangle=90,
        wedgeprops=dict(width=0.4)
    )

    ax.text(0,0,f"{risk_percent}%",ha='center',va='center',fontsize=20)
    st.pyplot(fig)

    # Advice
    if advice["color"] == "green":
        st.success(advice["advice"])
    elif advice["color"] == "orange":
        st.warning(advice["advice"])
    else:
        st.error(advice["advice"])

    st.markdown('</div>', unsafe_allow_html=True)