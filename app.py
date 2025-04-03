import streamlit as st
import pandas as pd

def calculate_fuel(flight_time):
    taxi_fuel = 0.25  # 15 min
    trip_fuel = flight_time * 6 / 60
    contingency_fuel = trip_fuel * 0.05
    alternate_fuel = 0.5  # 30 min
    reserve_fuel = 0.5  # 30 min
    total_required_fuel = taxi_fuel + trip_fuel + contingency_fuel + alternate_fuel + reserve_fuel
    
    total_fuel_2h = max(total_required_fuel, 2 * 6)
    total_fuel_3h = max(total_required_fuel, 3 * 6)
    total_fuel_4h = max(total_required_fuel, 4 * 6)
    
    extra_fuel_2h = max(0, total_fuel_2h - total_required_fuel)
    extra_fuel_3h = max(0, total_fuel_3h - total_required_fuel)
    extra_fuel_4h = max(0, total_fuel_4h - total_required_fuel)
    
    return pd.DataFrame({
        "Flight Time": [f"{flight_time} min"],
        "Taxi": [taxi_fuel],
        "Trip": [trip_fuel],
        "Contingency": [contingency_fuel],
        "Alternate": [alternate_fuel],
        "Reserve": [reserve_fuel],
        "Extra": [extra_fuel_2h, extra_fuel_3h, extra_fuel_4h],
        "Total (USG)": [total_fuel_2h, total_fuel_3h, total_fuel_4h],
        "Total (kg)": [total_fuel_2h * 2.84, total_fuel_3h * 2.84, total_fuel_4h * 2.84]
    })

def calculate_mass_balance(total_fuel_kg):
    fuel_arm = 1.067
    ramp_weight = 540 + 70 + 70 + total_fuel_kg
    taxi_weight = ramp_weight - (1.5 * 2.84)
    takeoff_weight = taxi_weight
    landing_weight = takeoff_weight - ((trip_fuel := total_fuel_kg - 2.84 * 1.5))
    
    return pd.DataFrame({
        "Item": ["Fuel", "Ramp", "Taxi/Run", "Takeoff", "Trip Fuel", "Landing"],
        "Weight (kg)": [total_fuel_kg, ramp_weight, taxi_weight, takeoff_weight, trip_fuel, landing_weight],
        "Arm (m)": [fuel_arm, 0.78, 0.78, 0.78, fuel_arm, 0.78]
    })

def calculate_performance(elevation, qnh, oat):
    pa = elevation + (1013 - qnh) * 30
    isa_dev = oat - (15 - (elevation / 1000 * 2))
    da = pa + isa_dev * 120
    
    return pd.DataFrame({
        "Parameter": ["Elevation", "QNH", "PA", "OAT", "ISA Dev", "DA"],
        "Value": [elevation, qnh, pa, oat, isa_dev, da]
    })

def calculate_distance(pa, oat, condition):
    gnd_roll = (450 + 465) / 2 if pa == 0 and oat == 5 else 500  # Placeholder
    total_distance = gnd_roll * 2
    factor = 1.15 if condition == "Wet" else 1.0
    final_gnd_roll = gnd_roll * factor * 1.25 * 0.3048
    final_distance = total_distance * factor * 1.25 * 0.3048
    asdr = (gnd_roll + gnd_roll) * 1.25 * 0.3048
    
    return pd.DataFrame({
        "Parameter": ["Ground Roll", "Total Distance", "ASDR"],
        "Value (m)": [final_gnd_roll, final_distance, asdr]
    })

st.title("Cessna 152 Flight Performance Calculator")

flight_time = st.number_input("Enter Flight Time (minutes)", min_value=30, max_value=240, step=10)
fuel_table = calculate_fuel(flight_time)
st.subheader("Fuel Calculation")
st.dataframe(fuel_table)

mass_balance_table = calculate_mass_balance(fuel_table["Total (kg)"].iloc[0])
st.subheader("Mass & Balance")
st.dataframe(mass_balance_table)

dep_qnh = st.number_input("QNH at LIPU", min_value=950, max_value=1050)
dep_oat = st.number_input("OAT at LIPU", min_value=-20, max_value=40)
alt_qnh = st.number_input("QNH at LIPH", min_value=950, max_value=1050)
alt_oat = st.number_input("OAT at LIPH", min_value=-20, max_value=40)

dep_performance = calculate_performance(44, dep_qnh, dep_oat)
st.subheader("Departure Performance (LIPU)")
st.dataframe(dep_performance)

alt_performance = calculate_performance(59, alt_qnh, alt_oat)
st.subheader("Alternate Performance (LIPH)")
st.dataframe(alt_performance)

condition = st.radio("Select Runway Condition", ["Dry", "Wet"])
distance_table_lipu = calculate_distance(dep_performance["Value"].iloc[2], dep_performance["Value"].iloc[3], condition)
st.subheader("Distance Calculation (LIPU)")
st.dataframe(distance_table_lipu)

distance_table_liph = calculate_distance(alt_performance["Value"].iloc[2], alt_performance["Value"].iloc[3], condition)
st.subheader("Distance Calculation (LIPH)")
st.dataframe(distance_table_liph)
