import streamlit as st
import random
import time
import pandas as pd
import joblib
import pydeck as pdk

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="TrafficAI", layout="wide")

# ------------------ SESSION ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------ LOGIN PAGE ------------------
def login():
    st.markdown("<h1 style='text-align:center;'>🚦 TrafficAI Login</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password:
                st.session_state.logged_in = True
                st.success("Login Successful ✅")
            else:
                st.error("Enter valid details")

# ------------------ MAIN APP ------------------
def app():

    model = joblib.load("model.pkl")

    # Sidebar Navigation
    st.sidebar.title("🚦 TrafficAI")
    page = st.sidebar.radio("Navigation", ["🏠 Home", "📊 Dashboard", "🗺️ Map", "📈 Analytics"])

    # ------------------ HOME ------------------
    if page == "🏠 Home":
        st.markdown("""
        <div style='text-align:center; padding:50px;'>
            <h1>🚦 Smart Traffic Analytics System</h1>
            <p>AI-powered system to predict traffic incidents in real-time</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("### 🚀 Features")
        col1, col2, col3 = st.columns(3)
        col1.info("🚗 Real-time Simulation")
        col2.info("🤖 AI Prediction")
        col3.info("📊 Live Dashboard")

    # ------------------ DASHBOARD ------------------
    elif page == "📊 Dashboard":

        st.subheader("📊 Live Traffic Dashboard")

        col1, col2, col3 = st.columns(3)
        data_placeholder = st.empty()
        chart_placeholder = st.empty()

        history = []

        for i in range(30):
            vehicle_count = random.randint(10, 120)
            speed = random.randint(20, 100)

            prediction = model.predict([[vehicle_count, speed]])[0]

            history.append({
                "Vehicle Count": vehicle_count,
                "Speed": speed,
                "Incident": prediction
            })

            df = pd.DataFrame(history)

            col1.metric("🚗 Vehicles", vehicle_count)
            col2.metric("⚡ Speed", speed)
            col3.metric("⚠ Status", "HIGH RISK" if prediction else "NORMAL")

            if prediction:
                st.error("🚨 Accident Risk Detected!")
            else:
                st.success("✅ Traffic Normal")

            data_placeholder.dataframe(df.tail(5))
            chart_placeholder.line_chart(df[["Vehicle Count", "Speed"]])

            time.sleep(1)

    # ------------------ MAP ------------------
    elif page == "🗺️ Map":

        st.subheader("🌍 Live Traffic Map")

        # Google Map Embed
        map_html = """
        <iframe
        width="100%"
        height="400"
        src="https://www.google.com/maps?q=Hyderabad&output=embed">
        </iframe>
        """
        st.markdown(map_html, unsafe_allow_html=True)

        # Pydeck Markers
        st.subheader("📍 Traffic Points")

        map_data = pd.DataFrame({
            "lat": [17.3850 + random.random()/100 for _ in range(50)],
            "lon": [78.4867 + random.random()/100 for _ in range(50)]
        })

        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=17.3850,
                longitude=78.4867,
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=map_data,
                    get_position='[lon, lat]',
                    get_color='[255, 0, 0, 160]',
                    get_radius=100,
                ),
            ],
        ))

    # ------------------ ANALYTICS ------------------
    elif page == "📈 Analytics":

        st.subheader("📈 Advanced Analytics")

        df = pd.DataFrame({
            "Vehicles": [random.randint(20, 100) for _ in range(50)],
            "Speed": [random.randint(30, 100) for _ in range(50)]
        })

        st.line_chart(df)
        st.bar_chart(df)

        st.write("### 📊 Statistical Summary")
        st.write(df.describe())

        st.success("📱 Mobile Friendly Dashboard Enabled")

# ------------------ ROUTER ------------------
if not st.session_state.logged_in:
    login()
else:
    app()
