import streamlit as st
import pandas as pd
import numpy as np

def calculate_fuel(flight_time):
    taxi_time = 15  # minuti
    trip_time = flight_time - taxi_time  # Differenza tra flight time e taxi
    contingency_time = trip_time * 0.05
    alternate_time = 30
    reserve_time = 30
    
    fuel_values = {
        "Taxi": 6 * (taxi_time / 60),
        "Trip": 6 * (trip_time / 60),
        "Contingency": 6 * (contingency_time / 60),
        "Alternate": 6 * (alternate_time / 60),
        "Reserve": 6 * (reserve_time / 60)
    }
    
    total_fuel_kg = {2: 12, 3: 18, 4: 24}  # kg per autonomia di 2, 3 e 4 ore
    extra_fuel = {k: max(v - sum(fuel_values.values()), 0) for k, v in total_fuel_kg.items()}
    
    fuel_table = pd.DataFrame({
        "Time (min)": [taxi_time, trip_time, contingency_time, alternate_time, reserve_time, "-", "-"],
        "US Gal": list(fuel_values.values()) + ["-", "-"],
        "Total Fuel (kg)": ["-", "-", "-", "-", "-", total_fuel_kg[2], total_fuel_kg[3], total_fuel_kg[4]],
        "Extra Fuel (kg)": ["-", "-", "-", "-", "-", extra_fuel[2], extra_fuel[3], extra_fuel[4]]
    }, index=["Taxi", "Trip", "Contingency", "Alternate", "Reserve", "Total (2h)", "Total (3h)", "Total (4h)"])
    return fuel_table

st.title("Cessna 152 Fuel & Performance Calculator")

# Input: Flight Time
flight_time = st.number_input("Inserisci il Flight Time (minuti):", min_value=60, max_value=240, step=10)

if flight_time:
    st.subheader("Fuel Calculation")
    st.table(calculate_fuel(flight_time))
    
    # Input: QNH & OAT per LIPU e LIPH
    st.subheader("Performance Input")
    qnh_lipu = st.number_input("QNH LIPU:")
    oat_lipu = st.number_input("OAT LIPU:")
    qnh_liph = st.number_input("QNH LIPH:")
    oat_liph = st.number_input("OAT LIPH:")
    
    # Calcolo PA, ISA Dev, DA
    def calculate_atmospheric_data(elevation, qnh, oat):
        pa = elevation + (1013 - qnh) * 30  # Corretto moltiplicatore
        isa_dev = oat - (15 - (2 * (pa / 1000)))
        da = pa + (120 * isa_dev)
        return pa, isa_dev, da
    
    pa_lipu, isa_dev_lipu, da_lipu = calculate_atmospheric_data(44, qnh_lipu, oat_lipu)
    pa_liph, isa_dev_liph, da_liph = calculate_atmospheric_data(59, qnh_liph, oat_liph)
    
    performance_table = pd.DataFrame({
        "Elevation": [44, 59],
        "QNH": [qnh_lipu, qnh_liph],
        "PA": [pa_lipu, pa_liph],
        "OAT": [oat_lipu, oat_liph],
        "ISA Dev": [isa_dev_lipu, isa_dev_liph],
        "DA": [da_lipu, da_liph]
    }, index=["LIPU", "LIPH"])
    
    st.subheader("Performance Data")
    st.table(performance_table)
    
    # Condizione pista
    st.subheader("Distance Calculation")
    runway_condition = st.radio("Condizione Pista", ["Dry", "Wet"])
    
    # Tabella distance calculation (valori esempio, da implementare interpolazione su tabelle vere)
    takeoff_gnd_roll = 457.5 if runway_condition == "Dry" else 457.5 * 1.15
    takeoff_distance = takeoff_gnd_roll * 1.25 * 0.3048
    landing_gnd_roll = 500 if runway_condition == "Dry" else 500 * 1.15
    landing_distance = landing_gnd_roll * 1.25 * 0.3048
    asdr = (takeoff_gnd_roll + landing_gnd_roll) * 1.25 * 0.3048
    
    distance_table = pd.DataFrame({
        "GND Roll (m)": [takeoff_gnd_roll * 0.3048, landing_gnd_roll * 0.3048],
        "Distance (m)": [takeoff_distance, landing_distance],
        "ASDR (m)": [asdr, asdr]
    }, index=["Take Off", "Landing"])
    
    st.table(distance_table)
