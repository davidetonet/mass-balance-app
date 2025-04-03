import streamlit as st
import pandas as pd

# Impostazioni predefinite
DEFAULT_QNH = 1013
DEFAULT_OAT = 15
FUEL_BURN_RATE = 6  # USG per ora
USG_TO_KG = 2.84  # Conversione da USG a kg
TAXI_FUEL_USG = 1.5  # 15 minuti di taxi
BEW = 540  # kg
BEW_ARM = 0.78  # m
PILOT_WEIGHT = 70  # kg
PASSENGER_WEIGHT = 70  # kg
SEAT_ARM = 0.99  # m
FUEL_ARM = 1.067  # m

# Funzione per calcolare il fuel
def calculate_fuel(flight_time):
    trip_time = flight_time - 15  # Trip time = Flight Time - Taxi Time
    contingency_time = trip_time * 0.05
    reserve_time = 30
    alternate_time = 30
    total_time = 15 + trip_time + contingency_time + reserve_time + alternate_time

    fuel_data = {
        "Phase": ["Taxi", "Trip", "Contingency", "Reserve", "Alternate", "Total"],
        "Time (min)": [15, round(trip_time), round(contingency_time), 30, 30, round(total_time)],
        "Fuel (USG)": [
            round(TAXI_FUEL_USG, 1),
            round(trip_time / 60 * FUEL_BURN_RATE, 1),
            round(contingency_time / 60 * FUEL_BURN_RATE, 1),
            round(reserve_time / 60 * FUEL_BURN_RATE, 1),
            round(alternate_time / 60 * FUEL_BURN_RATE, 1),
            round(total_time / 60 * FUEL_BURN_RATE, 1),
        ],
    }
    df = pd.DataFrame(fuel_data)
    return df

# Funzione per calcolare Mass & Balance
def calculate_mass_balance(total_fuel_kg, flight_time):
    ramp_weight = BEW + PILOT_WEIGHT + PASSENGER_WEIGHT + total_fuel_kg
    ramp_moment = (BEW * BEW_ARM) + (PILOT_WEIGHT * SEAT_ARM) + (PASSENGER_WEIGHT * SEAT_ARM) + (total_fuel_kg * FUEL_ARM)
    ramp_arm = ramp_moment / ramp_weight
    
    taxi_fuel_kg = TAXI_FUEL_USG * USG_TO_KG
    takeoff_weight = ramp_weight - taxi_fuel_kg
    takeoff_moment = ramp_moment - (taxi_fuel_kg * FUEL_ARM)
    takeoff_arm = takeoff_moment / takeoff_weight
    
    trip_fuel_kg = (flight_time / 60) * FUEL_BURN_RATE * USG_TO_KG
    landing_weight = takeoff_weight - trip_fuel_kg
    landing_moment = takeoff_moment - (trip_fuel_kg * FUEL_ARM)
    landing_arm = landing_moment / landing_weight
    
    mass_data = {
        "Phase": ["Ramp", "Takeoff", "Landing"],
        "Weight (kg)": [round(ramp_weight, 2), round(takeoff_weight, 2), round(landing_weight, 2)],
        "Arm (m)": [round(ramp_arm, 3), round(takeoff_arm, 3), round(landing_arm, 3)],
        "Moment": [round(ramp_moment, 2), round(takeoff_moment, 2), round(landing_moment, 2)]
    }
    df = pd.DataFrame(mass_data)
    return df

# Funzione per il calcolo della performance
def performance_calculation(oat):
    isa_dev = oat - 15
    return round(isa_dev, 0)

# Funzione per il calcolo delle distanze (da completare con interpolazione)
def distance_calculation():
    # Placeholder per i calcoli sulle distanze
    return "Distanza di decollo e atterraggio non ancora implementata."

# Streamlit UI
st.title("Mass & Balance Calculator")

# Input QNH e OAT
qnh = st.number_input("QNH", value=DEFAULT_QNH, step=1, format="%d")
oat = st.number_input("OAT (°C)", value=DEFAULT_OAT, step=1, format="%d")
flight_time = st.number_input("Flight Time (min)", min_value=1, step=1)

total_fuel_kg = round(((flight_time / 60) * FUEL_BURN_RATE) * USG_TO_KG, 2)

tab1, tab2, tab3, tab4 = st.tabs(["Fuel Calculation", "Mass & Balance", "Performance", "Distance Calculation"])

with tab1:
    st.header("Fuel Calculation")
    st.table(calculate_fuel(flight_time))

with tab2:
    st.header("Mass & Balance")
    st.table(calculate_mass_balance(total_fuel_kg, flight_time))

with tab3:
    st.header("Performance")
    st.write(f"ISA Dev: {performance_calculation(oat)}")

with tab4:
    st.header("Distance Calculation")
    st.write(distance_calculation())
