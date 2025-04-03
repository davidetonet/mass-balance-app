import streamlit as st
import pandas as pd
import numpy as np

def calculate_fuel(flight_time):
    taxi_time = 15
    trip_time = flight_time - taxi_time
    contingency_time = 0.05 * trip_time
    alternate_time = 30
    reserve_time = 30
    
    extra_fuel_time_2h = max(0, 120 - (taxi_time + trip_time + contingency_time + alternate_time + reserve_time))
    extra_fuel_time_3h = max(0, 180 - (taxi_time + trip_time + contingency_time + alternate_time + reserve_time))
    extra_fuel_time_4h = max(0, 240 - (taxi_time + trip_time + contingency_time + alternate_time + reserve_time))
    
    total_fuel_2h = taxi_time + trip_time + contingency_time + alternate_time + reserve_time + extra_fuel_time_2h
    total_fuel_3h = taxi_time + trip_time + contingency_time + alternate_time + reserve_time + extra_fuel_time_3h
    total_fuel_4h = taxi_time + trip_time + contingency_time + alternate_time + reserve_time + extra_fuel_time_4h
    
    fuel_table = pd.DataFrame({
        "Category": ["Taxi", "Trip", "Contingency", "Alternate", "Reserve", "Extra", "Total"],
        "2h (min)": [taxi_time, trip_time, contingency_time, alternate_time, reserve_time, extra_fuel_time_2h, total_fuel_2h],
        "3h (min)": [taxi_time, trip_time, contingency_time, alternate_time, reserve_time, extra_fuel_time_3h, total_fuel_3h],
        "4h (min)": [taxi_time, trip_time, contingency_time, alternate_time, reserve_time, extra_fuel_time_4h, total_fuel_4h]
    })
    return fuel_table

def calculate_mass_balance(total_fuel_kg):
    ramp_weight = 540 + 140 + total_fuel_kg
    takeoff_weight = ramp_weight - 4.26  # Taxi fuel in kg
    landing_weight = takeoff_weight - (6 * (120/60))  # Trip fuel in kg
    
    mass_balance_table = pd.DataFrame({
        "Category": ["Ramp Weight", "Takeoff Weight", "Landing Weight"],
        "Weight (kg)": [ramp_weight, takeoff_weight, landing_weight]
    })
    return mass_balance_table

def calculate_performance(qnh, oat, elevation):
    pressure_altitude = ((1013 - qnh) * 30) + elevation
    isa_dev = oat - (15 - (pressure_altitude / 1000) * 2)
    density_altitude = pressure_altitude + (120 * isa_dev)
    
    performance_table = pd.DataFrame({
        "Metric": ["Elevation", "QNH", "Pressure Altitude", "OAT", "ISA Dev", "Density Altitude"],
        "Value": [elevation, qnh, pressure_altitude, oat, isa_dev, density_altitude]
    })
    return performance_table

# Streamlit UI
st.title("Mass & Balance e Performance Cessna 152")

# Fuel Calculation
flight_time = st.number_input("Flight Time (min)", min_value=30, max_value=240, step=1)
st.table(calculate_fuel(flight_time))

total_fuel_kg = st.number_input("Total Fuel in kg", value=0.0)
st.table(calculate_mass_balance(total_fuel_kg))

# Performance Input
st.subheader("Performance LIPU")
qnh_lipu = st.number_input("QNH LIPU", min_value=950, max_value=1050)
oat_lipu = st.number_input("OAT LIPU (°C)", min_value=-20, max_value=40)
st.table(calculate_performance(qnh_lipu, oat_lipu, 44))

st.subheader("Performance LIPH")
qnh_liph = st.number_input("QNH LIPH", min_value=950, max_value=1050)
oat_liph = st.number_input("OAT LIPH (°C)", min_value=-20, max_value=40)
st.table(calculate_performance(qnh_liph, oat_liph, 59))
