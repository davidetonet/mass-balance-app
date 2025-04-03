import streamlit as st
import pandas as pd

# Conversion constants
USG_TO_KG = 2.84
CONSUMPTION_USG_PER_HOUR = 6
TAXI_FUEL_USG = 1.5

# Function to calculate fuel requirements
def calculate_fuel(flight_time):
    trip_time = flight_time - 15  # Removing 15 min taxi time
    contingency_time = round(0.05 * trip_time)
    alternate_time = 30
    reserve_time = 30
    
    total_minutes = sum([trip_time, contingency_time, alternate_time, reserve_time])
    extra_time_2h = max(0, 120 - total_minutes)
    extra_time_3h = max(0, 180 - total_minutes)
    extra_time_4h = max(0, 240 - total_minutes)
    
    fuel_times = [15, trip_time, contingency_time, alternate_time, reserve_time, extra_time_2h, extra_time_3h, extra_time_4h]
    fuel_usg = [round((t / 60) * CONSUMPTION_USG_PER_HOUR, 1) for t in fuel_times]
    total_fuel_kg = [round(f * USG_TO_KG, 1) for f in fuel_usg[-3:]]
    
    return pd.DataFrame({
        "Fuel Type": ["Taxi", "Trip", "Contingency", "Alternate", "Reserve", "Total (2h)", "Total (3h)", "Total (4h)"],
        "Minutes": fuel_times,
        "US Gal": fuel_usg,
        "Total Fuel (kg)": total_fuel_kg + ["", "", ""]
    })

# Function to calculate mass & balance
def calculate_mass_balance(total_fuel_kg):
    fuel_weight = total_fuel_kg
    fuel_arm = 1.067
    fuel_moment = round(fuel_weight * fuel_arm, 2)
    
    taxi_weight = round(TAXI_FUEL_USG * USG_TO_KG, 1)
    taxi_moment = round(taxi_weight * fuel_arm, 2)
    
    trip_weight = round((flight_time / 60) * CONSUMPTION_USG_PER_HOUR * USG_TO_KG, 1)
    trip_moment = round(trip_weight * fuel_arm, 2)
    
    takeoff_weight = 540 + 70 + 70 + fuel_weight - taxi_weight
    landing_weight = takeoff_weight - trip_weight
    
    return pd.DataFrame({
        "Stage": ["Fuel", "Taxi Run", "Trip Fuel", "Ramp", "Takeoff", "Landing"],
        "Weight (kg)": [fuel_weight, taxi_weight, trip_weight, takeoff_weight, takeoff_weight, landing_weight],
        "Arm (m)": [fuel_arm, fuel_arm, fuel_arm, 0.78, 0.78, 0.78],
        "Moment": [fuel_moment, taxi_moment, trip_moment, round(takeoff_weight * 0.78, 2), round(takeoff_weight * 0.78, 2), round(landing_weight * 0.78, 2)]
    })

# Function to calculate performance
def calculate_performance(qnh, oat):
    elevation = 44
    pa = round((1013 - qnh) * 30 + elevation)
    isa_dev = oat - 15
    da = round(pa + (isa_dev * 120))
    
    return pd.DataFrame({
        "Parameter": ["Elevation", "QNH", "PA", "OAT", "ISA Dev", "DA"],
        "Value": [elevation, qnh, pa, oat, isa_dev, da]
    })

# Streamlit UI
st.title("Cessna 152 Flight Planner")

# FUEL SECTION
st.header("Fuel Calculation")
flight_time = st.number_input("Enter Flight Time (min):", min_value=15, value=60, step=1)
fuel_df = calculate_fuel(flight_time)
st.table(fuel_df)

total_fuel_kg = float(fuel_df.iloc[5, 3])  # Get 2h total fuel in kg

# MASS & BALANCE SECTION
st.header("Mass & Balance")
mass_balance_df = calculate_mass_balance(total_fuel_kg)
st.table(mass_balance_df)

# PERFORMANCE SECTION
st.header("Performance - LIPU")
qnh_lipu = st.number_input("Enter QNH for LIPU:", min_value=900, max_value=1100, value=1013)
oat_lipu = st.number_input("Enter OAT for LIPU:", min_value=-20, max_value=40, value=15)
performance_lipu_df = calculate_performance(qnh_lipu, oat_lipu)
st.table(performance_lipu_df)

st.header("Performance - LIPH")
qnh_liph = st.number_input("Enter QNH for LIPH:", min_value=900, max_value=1100, value=1013)
oat_liph = st.number_input("Enter OAT for LIPH:", min_value=-20, max_value=40, value=15)
performance_liph_df = calculate_performance(qnh_liph, oat_liph)
st.table(performance_liph_df)

# DISTANCE CALCULATION PLACEHOLDER
st.header("Distance Calculation - LIPU & LIPH")
st.write("[Dati Distance Calculation verranno aggiunti] 🔧")
