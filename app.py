import streamlit as st
import pandas as pd

# Costanti
USG_TO_KG = 2.84  # Conversione carburante
FUEL_BURN_RATE = 6  # USG/h
FUEL_ARM = 1.067  # Braccio del carburante

# Funzione per calcolare il carburante
def calculate_fuel(flight_time):
    taxi_time = 15
    trip_time = flight_time - taxi_time
    contingency_time = round(trip_time * 0.05)
    alternate_time = 30
    reserve_time = 30
    extra_time = max(0, (120 - (trip_time + taxi_time + contingency_time + alternate_time + reserve_time)))
    total_time = taxi_time + trip_time + contingency_time + alternate_time + reserve_time + extra_time
    
    # Conversione in USG
    taxi_usg = round(taxi_time / 60 * FUEL_BURN_RATE, 1)
    trip_usg = round(trip_time / 60 * FUEL_BURN_RATE, 1)
    contingency_usg = round(contingency_time / 60 * FUEL_BURN_RATE, 1)
    alternate_usg = round(alternate_time / 60 * FUEL_BURN_RATE, 1)
    reserve_usg = round(reserve_time / 60 * FUEL_BURN_RATE, 1)
    extra_usg = round(extra_time / 60 * FUEL_BURN_RATE, 1)
    total_usg = taxi_usg + trip_usg + contingency_usg + alternate_usg + reserve_usg + extra_usg
    total_kg = round(total_usg * USG_TO_KG)
    
    return pd.DataFrame({
        "Time (min)": [taxi_time, trip_time, contingency_time, alternate_time, reserve_time, extra_time, total_time],
        "USG": [taxi_usg, trip_usg, contingency_usg, alternate_usg, reserve_usg, extra_usg, total_usg],
        "Kg": ["-", "-", "-", "-", "-", "-", total_kg]
    }, index=["Taxi", "Trip", "Contingency", "Alternate", "Reserve", "Extra", "Total"])

# Funzione per Mass & Balance
def calculate_mass_balance(total_fuel_kg):
    basic_empty_weight = 540
    basic_moment = 540 * 0.78
    fuel_moment = total_fuel_kg * FUEL_ARM
    taxi_fuel_kg = round(1.5 * USG_TO_KG, 2)
    taxi_moment = taxi_fuel_kg * FUEL_ARM
    trip_fuel_kg = round((total_fuel_kg - taxi_fuel_kg) * 0.85, 2)
    trip_moment = trip_fuel_kg * FUEL_ARM
    
    ramp_weight = basic_empty_weight + total_fuel_kg
    ramp_moment = basic_moment + fuel_moment
    
    takeoff_weight = ramp_weight - taxi_fuel_kg
    takeoff_moment = ramp_moment - taxi_moment
    
    landing_weight = takeoff_weight - trip_fuel_kg
    landing_moment = takeoff_moment - trip_moment
    
    return pd.DataFrame({
        "Weight (kg)": [total_fuel_kg, ramp_weight, takeoff_weight, landing_weight],
        "Arm (m)": [FUEL_ARM, "-", "-", "-"],
        "Moment": [fuel_moment, ramp_moment, takeoff_moment, landing_moment]
    }, index=["Fuel", "Ramp", "Takeoff", "Landing"])

# Funzione per Performance
def calculate_performance(qnh, oat, elevation):
    PA = (1013 - qnh) * 27 + elevation
    ISA_Dev = oat - 15
    DA = PA + (ISA_Dev * 120)
    return pd.DataFrame({
        "Elevation": [elevation],
        "QNH": [qnh],
        "PA": [PA],
        "OAT": [oat],
        "ISA Dev": [ISA_Dev],
        "DA": [DA]
    })

# UI
st.title("Cessna 152 - Mass & Balance & Performance")

# Input
flight_time = st.number_input("Flight Time (min)", min_value=30, max_value=240, step=5)
qnh_lipu = st.number_input("QNH LIPU")
oat_lipu = st.number_input("OAT LIPU")
qnh_liph = st.number_input("QNH LIPH")
oat_liph = st.number_input("OAT LIPH")

# Calcoli
fuel_df = calculate_fuel(flight_time)
total_fuel_kg = int(fuel_df.loc["Total", "Kg"])
mass_balance_df = calculate_mass_balance(total_fuel_kg)
performance_lipu_df = calculate_performance(qnh_lipu, oat_lipu, 44)
performance_liph_df = calculate_performance(qnh_liph, oat_liph, 59)

# Output
st.subheader("Fuel Calculation")
st.table(fuel_df)

st.subheader("Mass & Balance")
st.table(mass_balance_df)

st.subheader("Performance - LIPU")
st.table(performance_lipu_df)

st.subheader("Performance - LIPH")
st.table(performance_liph_df)
