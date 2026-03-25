import streamlit as st
import random
import time
import pandas as pd
import joblib

# Load model
model = joblib.load("model.pkl")

# Page config
st.set_page_config(page_title="Traffic Analytics System", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }
    .stButton>button {
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align:center;'>🚦 Smart Traffic Monitoring Dashboard</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Control Panel")

mode = st.sidebar.selectbox("Select Mode", ["Manual", "Auto Simulation"])
start = st.sidebar.button("▶ Start")
stop = st.sidebar.button("⏹ Stop")

vehicle_input = st.sidebar.slider("Vehicle Count", 10, 120, 50)
speed_input = st.sidebar.slider("Average Speed", 20, 100, 60)

# Layout
col1, col2, col3 = st.columns(3)

data_placeholder = st.empty()
chart_placeholder = st.empty()

history = []

running = False

if start:
    running = True

if stop:
    running = False

# MAIN LOGIC
while running:

    if mode == "Manual":
        vehicle_count = vehicle_input
        avg_speed = speed_input
    else:
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
    col3.metric("⚠ Status", "HIGH RISK" if prediction == 1 else "NORMAL")

    # Alerts
    if prediction == 1:
        st.error("🚨 Accident Risk Detected!")
    else:
        st.success("✅ Traffic is Smooth")

    # Data Table
    data_placeholder.subheader("📊 Live Traffic Data")
    data_placeholder.dataframe(df.tail(5))

    # Chart
    chart_placeholder.subheader("📈 Traffic Trends")
    chart_placeholder.line_chart(df[["Vehicle Count", "Average Speed"]])

    time.sleep(1)
