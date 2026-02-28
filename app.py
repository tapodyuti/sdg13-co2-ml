import streamlit as st
import pandas as pd
import joblib

# caching the loaded model so it is not reloaded on every rerun
@st.cache_resource
def load_model():
    return joblib.load("sdg13_rf_pipeline.pkl")

model = load_model()

st.title("SDG-13: Household CO₂ Emission Estimator")

st.write("Enter your household/building details to estimate monthly CO₂ emissions (kg).")

floor_area = st.number_input("Floor area (m²)", min_value=20.0, max_value=400.0, value=80.0, step=5.0)
num_rooms = st.number_input("Number of rooms", min_value=1, max_value=10, value=3, step=1)
building_type = st.selectbox("Building type", ["apartment", "independent"])
climate_zone = st.selectbox("Climate zone", ["hot", "moderate", "cool"])
elec_kwh = st.number_input("Monthly electricity use (kWh)", min_value=0.0, max_value=2000.0, value=300.0, step=10.0)
lpg_kg = st.number_input("Monthly LPG/other fuel (kg)", min_value=0.0, max_value=100.0, value=10.0, step=1.0)
ac_hours = st.number_input("Average AC hours per day", min_value=0.0, max_value=24.0, value=4.0, step=0.5)
occupants = st.number_input("Number of occupants", min_value=1, max_value=15, value=4, step=1)

if st.button("Predict CO₂ emissions"):
    input_df = pd.DataFrame([{
        "floor_area": floor_area,
        "num_rooms": num_rooms,
        "building_type": building_type,
        "climate_zone": climate_zone,
        "elec_kwh": elec_kwh,
        "lpg_kg": lpg_kg,
        "ac_hours": ac_hours,
        "occupants": occupants,
    }])

    co2_pred = model.predict(input_df)[0]
    st.subheader(f"Estimated monthly CO₂ emissions: {co2_pred:.1f} kg")

    