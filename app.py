import streamlit as st
import random
import time
import pandas as pd
import joblib

# Load model
model = joblib.load("model.pkl")

# Page config
st.set_page_config(page_title="Traffic Incident Detection", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>🚦 Traffic Incident Detection System</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Control Panel")
run = st.sidebar.button("▶ Start Simulation")

# Metrics placeholders
col1, col2, col3 = st.columns(3)

data_placeholder = st.empty()
chart_placeholder = st.empty()

history = []

if run:
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
        col3.metric("⚠ Incident", "YES" if prediction == 1 else "NO")

        # Alerts
        if prediction == 1:
            st.error("🚨 HIGH RISK: Possible Accident Detected!")
        else:
            st.success("✅ Traffic Normal")

        # Data table
        data_placeholder.subheader("📊 Live Data")
        data_placeholder.write(df.tail(5))

        # Chart
        chart_placeholder.subheader("📈 Traffic Trends")
        chart_placeholder.line_chart(df[["Vehicle Count", "Average Speed"]])

        time.sleep(1)
