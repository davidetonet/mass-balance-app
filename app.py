import streamlit as st
import numpy as np

def calculate_pressure_altitude(qnh, elevation):
    return (1013 - qnh) * 30 + elevation

def calculate_isa_dev(oat):
    return oat - 15

def interpolate(value, lower_bound, upper_bound, lower_result, upper_result):
    return lower_result + (value - lower_bound) * (upper_result - lower_result) / (upper_bound - lower_bound)

def calculate_takeoff_landing(oat, pa, table):
    temp_keys = sorted(table.keys())
    pa_keys = sorted(table[temp_keys[0]].keys())
    
    lower_temp = max(t for t in temp_keys if t <= oat)
    upper_temp = min(t for t in temp_keys if t >= oat)
    
    lower_pa = max(p for p in pa_keys if p <= pa)
    upper_pa = min(p for p in pa_keys if p >= pa)
    
    lower_temp_lower_pa = table[lower_temp][lower_pa]
    lower_temp_upper_pa = table[lower_temp][upper_pa]
    upper_temp_lower_pa = table[upper_temp][lower_pa]
    upper_temp_upper_pa = table[upper_temp][upper_pa]
    
    interp_pa_low = interpolate(pa, lower_pa, upper_pa, lower_temp_lower_pa, lower_temp_upper_pa)
    interp_pa_high = interpolate(pa, lower_pa, upper_pa, upper_temp_lower_pa, upper_temp_upper_pa)
    
    return interpolate(oat, lower_temp, upper_temp, interp_pa_low, interp_pa_high)

st.title("Cessna 152 Flight Performance Calculator")

flight_time = st.number_input("Flight Time (minutes)", min_value=60, max_value=240, step=10)

qnh_departure = st.number_input("QNH at Departure (hPa)", value=1013)
oat_departure = st.number_input("OAT at Departure (°C)", value=15)
elevation_departure = 44
pa_departure = calculate_pressure_altitude(qnh_departure, elevation_departure)
isa_dev_departure = calculate_isa_dev(oat_departure)

takeoff_distance = calculate_takeoff_landing(oat_departure, pa_departure, takeoff_table) * 1.25
landing_distance = calculate_takeoff_landing(oat_departure, pa_departure, landing_table) * 1.25
asdr = takeoff_distance + landing_distance

st.write(f"**Pressure Altitude:** {pa_departure} ft")
st.write(f"**ISA Deviation:** {isa_dev_departure:.2f}°C")
st.write(f"**Takeoff Distance (meters):** {takeoff_distance:.2f}")
st.write(f"**Landing Distance (meters):** {landing_distance:.2f}")
st.write(f"**ASDR (meters):** {asdr:.2f}")
