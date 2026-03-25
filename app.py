import streamlit as st
import random
import pandas as pd
import joblib
import sqlite3
import pydeck as pdk

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="TrafficAI", layout="wide")

# ------------------ DATABASE ------------------
conn = sqlite3.connect("traffic.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS traffic (
    vehicle_count INT,
    speed INT,
    prediction INT
)
""")

# ------------------ SESSION ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------ LOGIN PAGE ------------------
def login():
    st.markdown("<h1 style='text-align:center;'>🔐 TrafficAI Login</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password:
                st.session_state.logged_in = True
                st.success("Login Successful ✅")
            else:
                st.error("Enter valid credentials")

# ------------------ MAIN APP ------------------
def app():

    model = joblib.load("model.pkl")

    st.sidebar.title("🚦 TrafficAI")
    page = st.sidebar.radio("Navigation", ["🏠 Home", "📊 Dashboard", "🗺️ Map", "📈 Analytics"])

    # ------------------ HOME ------------------
    if page == "🏠 Home":
        st.markdown("""
        <div style='text-align:center; padding:50px;'>
            <h1>🚦 Smart Traffic Analytics System</h1>
            <p>AI-powered traffic incident prediction</p>
        </div>
        """, unsafe_allow_html=True)

    # ------------------ DASHBOARD ------------------
    elif page == "📊 Dashboard":

        st.subheader("📊 Live Traffic Dashboard")

        if st.button("▶ Generate Traffic Data"):

            vehicle_count = random.randint(10, 120)
            speed = random.randint(20, 100)

            prediction = model.predict([[vehicle_count, speed]])[0]

            # Save to DB
            cursor.execute("INSERT INTO traffic VALUES (?, ?, ?)",
                           (vehicle_count, speed, prediction))
            conn.commit()

            col1, col2, col3 = st.columns(3)
            col1.metric("🚗 Vehicles", vehicle_count)
            col2.metric("⚡ Speed", speed)
            col3.metric("⚠ Status", "HIGH RISK" if prediction else "NORMAL")

            if prediction:
                st.error("🚨 Accident Risk Detected!")
            else:
                st.success("✅ Traffic Normal")

        # Show DB data
        df_db = pd.read_sql("SELECT * FROM traffic", conn)

        st.subheader("📂 Stored Data")
        st.dataframe(df_db.tail(10))

        if not df_db.empty:
            st.subheader("📈 Trends")
            st.line_chart(df_db[["vehicle_count", "speed"]])

    # ------------------ MAP ------------------
    elif page == "🗺️ Map":

        st.subheader("🌍 Traffic Map")

        map_html = """
        <iframe width="100%" height="400"
        src="https://www.google.com/maps?q=Hyderabad&output=embed"></iframe>
        """
        st.markdown(map_html, unsafe_allow_html=True)

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

        st.subheader("📈 Traffic Analytics")

        df_db = pd.read_sql("SELECT * FROM traffic", conn)

        if not df_db.empty:
            st.line_chart(df_db[["vehicle_count", "speed"]])
            st.bar_chart(df_db[["vehicle_count", "speed"]])
            st.write("📊 Statistical Summary")
            st.write(df_db.describe())
        else:
            st.warning("No data available yet")

# ------------------ ROUTER ------------------
if not st.session_state.logged_in:
    login()
else:
    app()
