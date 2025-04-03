import streamlit as st
import pandas as pd

# Funzione per il calcolo del carburante
def calculate_fuel(flight_time):
    taxi_fuel = 1.5 * 2.84  # Taxi fuel in kg
    alternate_fuel = 30 * 6 / 60  # Alternate fuel in USG
    reserve_fuel = 30 * 6 / 60  # Reserve fuel in USG
    contingency_fuel = (flight_time * 6 / 60) * 0.05  # 5% del trip fuel
    trip_fuel = (flight_time * 6 / 60)  # Trip fuel in USG
    total_fuel_usg = trip_fuel + contingency_fuel + reserve_fuel + alternate_fuel
    total_fuel_kg = total_fuel_usg * 2.84

    return pd.DataFrame({
        "Fuel Type": ["Taxi Fuel", "Trip Fuel", "Contingency Fuel", "Reserve Fuel", "Alternate Fuel", "Total Fuel"],
        "USG": [round(x, 1) for x in [taxi_fuel / 2.84, trip_fuel, contingency_fuel, reserve_fuel, alternate_fuel, total_fuel_usg]],
        "Kg": ["-", round(trip_fuel * 2.84, 2), round(contingency_fuel * 2.84, 2), round(reserve_fuel * 2.84, 2), round(alternate_fuel * 2.84, 2), round(total_fuel_kg, 2)]
    })

# Funzione per il calcolo del Mass & Balance
def calculate_mass_balance(total_fuel_kg, trip_fuel_kg):
    bew = 540  # Basic Empty Weight
    bew_arm = 0.78
    pilot = 70
    passenger = 70
    arm_occupants = 0.99
    arm_fuel = 1.067
    taxi_fuel_kg = 1.5 * 2.84

    ramp_weight = bew + pilot + passenger + total_fuel_kg
    ramp_moment = ramp_weight * arm_fuel
    takeoff_weight = ramp_weight - taxi_fuel_kg
    takeoff_moment = ramp_moment - (taxi_fuel_kg * arm_fuel)
    takeoff_arm = round(takeoff_moment / takeoff_weight, 3)
    landing_weight = takeoff_weight - trip_fuel_kg
    landing_moment = takeoff_moment - (trip_fuel_kg * arm_fuel)
    landing_arm = round(landing_moment / landing_weight, 3)

    return pd.DataFrame({
        "Phase": ["Ramp", "Takeoff", "Landing"],
        "Weight (kg)": [round(x, 2) for x in [ramp_weight, takeoff_weight, landing_weight]],
        "Arm (m)": [takeoff_arm, takeoff_arm, landing_arm],
        "Moment": [round(x, 2) for x in [ramp_moment, takeoff_moment, landing_moment]]
    })

# Funzione per il calcolo della distanza di decollo e atterraggio
def calculate_distance(temp, qnh):
    takeoff_distance = 400  # Valore fittizio in metri
    landing_distance = 500  # Valore fittizio in metri
    return pd.DataFrame({
        "Type": ["Takeoff Distance", "Landing Distance"],
        "Distance (m)": [takeoff_distance, landing_distance]
    })

# Streamlit UI
st.title("Cessna 152 - Mass & Balance and Performance")

# Input
qnh = st.number_input("QNH (hPa)", min_value=900, max_value=1100, value=1013, step=1, format="%d")
oat = st.number_input("OAT (°C)", min_value=-50, max_value=50, value=15, step=1, format="%d")
flight_time = st.number_input("Flight Time (min)", min_value=10, max_value=300, value=60, step=1)

total_fuel_df = calculate_fuel(flight_time)
total_fuel_kg = float(total_fuel_df.iloc[-1]['Kg'])
trip_fuel_kg = float(total_fuel_df.iloc[1]['Kg'])

# Sezioni
st.header("Fuel Calculation")
st.table(total_fuel_df)

st.header("Mass & Balance")
st.table(calculate_mass_balance(total_fuel_kg, trip_fuel_kg))

st.header("Performance & Distance Calculation")
st.table(calculate_distance(oat, qnh))
