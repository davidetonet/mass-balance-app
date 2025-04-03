import streamlit as st
import pandas as pd
import numpy as np

def calculate_fuel(flight_time):
    taxi_fuel = 1.5  # USG
    trip_fuel = round((flight_time / 60) * 6, 1)
    contingency_fuel = round(trip_fuel * 0.05, 1)
    reserve_fuel = 3.0  # 30 min = 3 USG
    alternate_fuel = 3.0  # 30 min = 3 USG
    total_fuel_usg = round(taxi_fuel + trip_fuel + contingency_fuel + reserve_fuel + alternate_fuel, 1)
    total_fuel_kg = round(total_fuel_usg * 2.84, 2)
    
    fuel_df = pd.DataFrame({
        "Type": ["Taxi", "Trip", "Contingency", "Reserve", "Alternate", "Total"],
        "Time (min)": [15, flight_time, round(flight_time * 0.05), 30, 30, sum([15, flight_time, round(flight_time * 0.05), 30, 30])],
        "Fuel (USG)": [taxi_fuel, trip_fuel, contingency_fuel, reserve_fuel, alternate_fuel, total_fuel_usg],
        "Fuel (kg)": [round(x * 2.84, 2) for x in [taxi_fuel, trip_fuel, contingency_fuel, reserve_fuel, alternate_fuel, total_fuel_usg]]
    })
    return fuel_df

def calculate_mass_balance(total_fuel_kg, flight_time):
    bew = 540
    bew_arm = 0.78
    pilot_weight = 70
    pax_weight = 70
    fuel_weight = total_fuel_kg
    fuel_arm = 1.067
    taxi_fuel_kg = round(1.5 * 2.84, 2)
    trip_fuel_kg = round((flight_time / 60) * 6 * 2.84, 2)
    
    ramp_weight = round(bew + pilot_weight + pax_weight + fuel_weight, 2)
    ramp_moment = round(ramp_weight * fuel_arm, 2)
    
    takeoff_weight = round(ramp_weight - taxi_fuel_kg, 2)
    takeoff_moment = round(ramp_moment - (taxi_fuel_kg * fuel_arm), 2)
    takeoff_arm = round(takeoff_moment / takeoff_weight, 3)
    
    landing_weight = round(takeoff_weight - trip_fuel_kg, 2)
    landing_moment = round(takeoff_moment - (trip_fuel_kg * fuel_arm), 2)
    landing_arm = round(landing_moment / landing_weight, 3)
    
    mass_balance_df = pd.DataFrame({
        "Phase": ["Ramp", "Takeoff", "Landing"],
        "Weight (kg)": [ramp_weight, takeoff_weight, landing_weight],
        "Arm (m)": [fuel_arm, takeoff_arm, landing_arm],
        "Moment": [ramp_moment, takeoff_moment, landing_moment]
    })
    return mass_balance_df

def calculate_distance():
    lipu_toda = 1172
    lipu_lda = 898
    lipu_asda = 1122
    liph_toda = 2480
    liph_lda = 2342
    liph_asda = 2420
    
    distance_df = pd.DataFrame({
        "Airport": ["LIPU (Padova)", "LIPH (Treviso)"],
        "TODA (m)": [lipu_toda, liph_toda],
        "LDA (m)": [lipu_lda, liph_lda],
        "ASDA (m)": [lipu_asda, liph_asda]
    })
    return distance_df

st.title("Cessna 152 - Mass & Balance & Performance")

qnh = st.number_input("QNH (hPa)", min_value=900, max_value=1100, value=1013, step=1)
oat = st.number_input("Outside Air Temperature (°C)", min_value=-50, max_value=50, value=15, step=1)
flight_time = st.number_input("Flight Time (min)", min_value=30, max_value=240, value=60, step=1)

st.subheader("Fuel Calculation")
st.table(calculate_fuel(flight_time))

total_fuel_kg = calculate_fuel(flight_time)["Fuel (kg)"].iloc[-1]

st.subheader("Mass & Balance")
st.table(calculate_mass_balance(total_fuel_kg, flight_time))

st.subheader("Distance Calculation")
st.table(calculate_distance())
