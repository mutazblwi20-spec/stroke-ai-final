import streamlit as st
import matplotlib.pyplot as plt
from predictor import predict_stroke

# =====================
# Page Config
# =====================
st.set_page_config(
    page_title="Medical Stroke AI",
    page_icon="🧠",
    layout="centered"
)

# =====================
# Load CSS
# =====================
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# =====================
# Header
# =====================
st.title("🧠 Medical Stroke Prediction AI")
st.caption("AI Clinical Decision Support System")

st.divider()

# =====================
# Inputs
# =====================
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

# =====================
# Prediction
# =====================
if st.button("🔬 Analyze Patient Risk"):

    diagnosis, prob, advice = predict_stroke(patient)

    risk_percent = round(prob * 100, 2)

    st.markdown('<div class="result-box">', unsafe_allow_html=True)

    # Diagnosis color
    if diagnosis == "مصاب":
        st.error(f"🚨 Diagnosis: {diagnosis}")
    else:
        st.success(f"✅ Diagnosis: {diagnosis}")

    st.subheader(f"Risk Score: {risk_percent}%")

    # ===== Gauge Chart =====
    fig, ax = plt.subplots()

    ax.pie(
        [risk_percent, 100-risk_percent],
        startangle=90,
        wedgeprops=dict(width=0.35)
    )

    ax.text(0, 0, f"{risk_percent}%", ha='center', va='center', fontsize=22)
    st.pyplot(fig)

    # ===== Smart Advice =====
    if risk_percent < 30:
        st.success("✅ Low Risk — Maintain exercise and healthy diet.")
    elif risk_percent < 70:
        st.warning("⚠️ Moderate Risk — Monitor blood pressure and glucose regularly.")
    else:
        st.error("🚨 High Risk — Medical consultation recommended immediately.")

    st.info("💡 AI recommendation generated using clinical risk factors.")

    st.markdown('</div>', unsafe_allow_html=True)
