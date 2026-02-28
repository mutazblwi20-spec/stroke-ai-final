import streamlit as st
import matplotlib.pyplot as plt
from predictor import predict_stroke
from datetime import datetime

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="AI Doctor Pro",
    page_icon="🧠",
    layout="wide"
)

# =========================
# CSS
# =========================
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# =========================
# Session History
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# HEADER
# =========================
st.title("🧠 AI Doctor Pro")
st.caption("Clinical Stroke Risk Decision System")

st.divider()

# =========================
# Layout
# =========================
left, right = st.columns([1,1])

# =========================
# INPUT PANEL
# =========================
with left:

    st.subheader("👨‍⚕️ Patient Information")

    age = st.slider("Age",1,100,30)
    hypertension = st.selectbox("Hypertension",[0,1])
    heart = st.selectbox("Heart Disease",[0,1])
    glucose = st.number_input("Glucose Level",50.0,300.0,100.0)
    bmi = st.number_input("BMI",10.0,60.0,25.0)

    patient = [age, hypertension, heart, glucose, bmi]

    analyze = st.button("🔬 Run AI Diagnosis")

# =========================
# RESULT PANEL
# =========================
with right:

    st.subheader("📊 AI Analysis")

    if analyze:

        diagnosis, prob, advice = predict_stroke(patient)

        risk = round(prob*100,2)

        # Save history
        st.session_state.history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "risk": risk,
            "diagnosis": diagnosis
        })

        # Diagnosis Box
        if diagnosis == "مصاب":
            st.error(f"🚨 Diagnosis: {diagnosis}")
        else:
            st.success(f"✅ Diagnosis: {diagnosis}")

        st.metric("Risk Score", f"{risk}%")

        # Gauge
        fig, ax = plt.subplots()

        ax.pie(
            [risk,100-risk],
            startangle=90,
            wedgeprops=dict(width=0.35)
        )

        ax.text(0,0,f"{risk}%",
                ha='center',
                va='center',
                fontsize=24,
                fontweight='bold')

        st.pyplot(fig)

        # Advice
        if advice["color"]=="green":
            st.success(advice["advice"])
        elif advice["color"]=="orange":
            st.warning(advice["advice"])
        else:
            st.error(advice["advice"])

# =========================
# HISTORY PANEL
# =========================
st.divider()
st.subheader("🗂 Patient Analysis History")

if st.session_state.history:
    st.table(st.session_state.history)
else:
    st.info("No analysis yet.")

# =========================
# REPORT
# =========================
st.divider()

if st.button("📄 Generate Medical Report"):

    if st.session_state.history:

        last = st.session_state.history[-1]

        report = f"""
        AI DOCTOR REPORT
        -------------------------
        Time: {last['time']}
        Diagnosis: {last['diagnosis']}
        Risk Score: {last['risk']}%

        Recommendation:
        Follow clinical monitoring and lifestyle optimization.
        """

        st.download_button(
            "⬇ Download Report",
            report,
            file_name="medical_report.txt"
        )
    else:
        st.warning("Run diagnosis first.")
