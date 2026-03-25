import streamlit as st
import random
import time
import pandas as pd
import joblib

# Load model
model = joblib.load("model.pkl")

# Page config
st.set_page_config(layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.hero {
    background-image: url("https://images.unsplash.com/photo-1502877338535-766e1452684a");
    background-size: cover;
    padding: 120px 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
}
.big-title {
    font-size: 50px;
    font-weight: bold;
}
.sub-text {
    font-size: 20px;
    margin-bottom: 20px;
}
.stButton>button {
    height: 3em;
    width: 200px;
    border-radius: 10px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HERO SECTION ------------------
st.markdown("""
<div class="hero">
    <div class="big-title">🚦 Smart Traffic Analytics</div>
    <div class="sub-text">Predict traffic incidents in real-time using AI</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# ------------------ BUTTONS ------------------
col1, col2, col3 = st.columns(3)

start = col1.button("▶ Start Simulation")
dashboard = col2.button("📊 Open Dashboard")
about = col3.button("ℹ About Project")

# ------------------ ABOUT SECTION ------------------
if about:
    st.subheader("📘 About This Project")
    st.write("""
    This system simulates real-time traffic and predicts incidents using Machine Learning.
    
    Features:
    - Live traffic simulation
    - AI-based prediction
    - Real-time dashboard
    """)

# ------------------ DASHBOARD ------------------
history = []

if start or dashboard:

    st.subheader("📊 Live Traffic Dashboard")

    col1, col2, col3 = st.columns(3)

    data_placeholder = st.empty()
    chart_placeholder = st.empty()

    for i in range(30):

        vehicle_count = random.randint(10, 120)
        avg_speed = random.randint(20, 100)

        prediction = model.predict([[vehicle_count, avg_speed]])[0]

        history.append({
            "Vehicle Count": vehicle_count,
            "Average Speed": avg_speed,
            "Incident": prediction
        })

        df = pd.DataFrame(history)

        # Metrics
        col1.metric("🚗 Vehicles", vehicle_count)
        col2.metric("⚡ Speed", avg_speed)
        col3.metric("⚠ Status", "HIGH RISK" if prediction else "NORMAL")

        # Alerts
        if prediction:
            st.error("🚨 Accident Risk Detected!")
        else:
            st.success("✅ Traffic Normal")

        # Data
        data_placeholder.dataframe(df.tail(5))

        # Chart
        chart_placeholder.line_chart(df[["Vehicle Count", "Average Speed"]])

        time.sleep(1)
