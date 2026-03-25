import streamlit as st
import random
import time
import pandas as pd
import joblib
import pydeck as pdk

# ------------------ SESSION ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------ LOGIN PAGE ------------------
def login():
    st.title("🔐 Login / Signup")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.logged_in = True
            st.success("Login Successful!")
        else:
            st.error("Enter credentials")

# ------------------ MAIN APP ------------------
def app():

    model = joblib.load("model.pkl")

    st.title("🚦 Smart Traffic AI Dashboard")

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Map", "Analytics"])

    history = []

    # ------------------ DASHBOARD ------------------
    if page == "Dashboard":

        st.subheader("📊 Live Simulation")

        col1, col2, col3 = st.columns(3)

        data_placeholder = st.empty()
        chart_placeholder = st.empty()

        for i in range(20):
            vehicle_count = random.randint(10, 120)
            avg_speed = random.randint(20, 100)

            prediction = model.predict([[vehicle_count, avg_speed]])[0]

            history.append({
                "Vehicle Count": vehicle_count,
                "Speed": avg_speed,
                "Incident": prediction
            })

            df = pd.DataFrame(history)

            col1.metric("Vehicles", vehicle_count)
            col2.metric("Speed", avg_speed)
            col3.metric("Status", "High Risk" if prediction else "Normal")

            if prediction:
                st.error("🚨 Incident Risk!")
            else:
                st.success("Normal Traffic")

            data_placeholder.dataframe(df.tail(5))
            chart_placeholder.line_chart(df[["Vehicle Count", "Speed"]])

            time.sleep(1)

    # ------------------ MAP ------------------
    elif page == "Map":

        st.subheader("🗺️ Traffic Map")

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
                    get_color='[200, 30, 0, 160]',
                    get_radius=100,
                ),
            ],
        ))

    # ------------------ ANALYTICS ------------------
    elif page == "Analytics":

        st.subheader("📈 Advanced Analytics")

        df = pd.DataFrame({
            "Vehicles": [random.randint(20, 100) for _ in range(50)],
            "Speed": [random.randint(30, 100) for _ in range(50)]
        })

        st.line_chart(df)
        st.bar_chart(df)

        st.write("📊 Statistical Summary")
        st.write(df.describe())

# ------------------ ROUTER ------------------
if not st.session_state.logged_in:
    login()
else:
    app()
