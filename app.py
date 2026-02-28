import streamlit as st
import matplotlib.pyplot as plt
from predictor import predict_stroke
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Doctor Pro",
    page_icon="🧠",
    layout="wide"
)

# =========================
# LOAD CSS
# =========================
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# =========================
# SESSION MEMORY
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

# =========================
# HEADER
# =========================
st.markdown("<h1 class='title'>🧠 AI Doctor Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Clinical Stroke Risk Decision System</p>", unsafe_allow_html=True)

st.divider()

# =========================
# LAYOUT
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

        # Risk Level
        if risk < 30:
            level = "Low Risk"
            color = "green"
        elif risk < 70:
            level = "Moderate Risk"
            color = "orange"
        else:
            level = "High Risk"
            color = "red"

        # Save history
        st.session_state.history.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Risk %": risk,
            "Diagnosis": diagnosis,
            "Level": level
        })

        # Diagnosis
        if diagnosis == "مصاب":
            st.error(f"🚨 Diagnosis: {diagnosis}")
        else:
            st.success(f"✅ Diagnosis: {diagnosis}")

        st.metric("Risk Score", f"{risk}%")
        st.info(f"Risk Level: {level}")

        # Gauge Chart
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
# HISTORY
# =========================
st.divider()
st.subheader("🗂 Patient Analysis History")

if st.session_state.history:
    st.dataframe(st.session_state.history, use_container_width=True)
else:
    st.info("No analysis yet.")

# =========================
# REPORT GENERATOR
# =========================
st.divider()

if st.button("📄 Generate Medical Report"):

    if st.session_state.history:

        last = st.session_state.history[-1]

        report = f"""
AI DOCTOR PRO REPORT
----------------------------
Time: {last['Time']}
Diagnosis: {last['Diagnosis']}
Risk Score: {last['Risk %']}%
Risk Level: {last['Level']}

Recommendation:
Maintain medical follow-up and healthy lifestyle.
"""

        st.download_button(
            "⬇ Download Report",
            report,
            file_name="AI_Doctor_Report.txt"
        )
    else:
        st.warning("Run diagnosis first.")
