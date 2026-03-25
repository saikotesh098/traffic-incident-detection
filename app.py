import streamlit as st
import random
import time
import pandas as pd
import joblib

# Load trained model
model = joblib.load("model.pkl")

# Page config
st.set_page_config(page_title="Traffic Incident Detection", layout="wide")

# Title
st.title("🚦 Streaming Analytics for Traffic Incident Detection System")

# Sidebar
st.sidebar.header("Control Panel")
run = st.sidebar.button("Start Simulation")

# Placeholders
data_placeholder = st.empty()
chart_placeholder = st.empty()

# Store history
history = []

if run:
    for i in range(30):
        # Generate random traffic data
        vehicle_count = random.randint(10, 120)
        avg_speed = random.randint(20, 100)

        # Predict using ML model
        prediction = model.predict([[vehicle_count, avg_speed]])[0]

        # Store data
        record = {
            "Vehicle Count": vehicle_count,
            "Average Speed": avg_speed,
            "Incident": prediction
        }

        history.append(record)

        df = pd.DataFrame(history)

        # Show latest data
        data_placeholder.subheader("📊 Live Traffic Data")
        data_placeholder.write(df.tail(5))

        # Alerts
        if prediction == 1:
            st.error(f"🚨 High Risk! Vehicles: {vehicle_count}, Speed: {avg_speed}")
        else:
            st.success(f"✅ Normal Traffic Flow")

        # Chart
        chart_placeholder.subheader("📈 Traffic Trends")
        chart_placeholder.line_chart(df[["Vehicle Count", "Average Speed"]])

        time.sleep(1)
