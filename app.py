import streamlit as st
import pandas as pd

def calculate_fuel(flight_time):
    taxi_fuel = 1.5  # USG
    trip_fuel = (flight_time / 60) * 6  # USG
    contingency_fuel = trip_fuel * 0.05  # USG
    reserve_fuel = 3  # USG (30 min at 6 USG/h)
    alternate_fuel = 3  # USG (30 min at 6 USG/h)
    total_fuel = taxi_fuel + trip_fuel + contingency_fuel + reserve_fuel + alternate_fuel
    total_fuel_kg = total_fuel * 2.84  # Conversione in kg
    
    fuel_df = pd.DataFrame({
        "Category": ["Taxi", "Trip", "Contingency", "Reserve", "Alternate", "Total"],
        "Fuel (USG)": [
            round(taxi_fuel, 1),
            round(trip_fuel, 1),
            round(contingency_fuel, 1),
            round(reserve_fuel, 1),
            round(alternate_fuel, 1),
            round(total_fuel, 1)
        ],
        "Fuel (kg)": ["-", "-", "-", "-", "-", round(total_fuel_kg, 2)]
    })
    return fuel_df, total_fuel_kg

def calculate_mass_balance(total_fuel_kg):
    bew = 540  # kg
    arm_bew = 0.78  # m
    pilot = 70  # kg
    pax = 70  # kg
    arm_pilot_pax = 0.99  # m
    arm_fuel = 1.067  # m
    taxi_fuel_kg = 1.5 * 2.84  # kg
    trip_fuel_kg = total_fuel_kg - (taxi_fuel_kg + 3 * 2.84 + 3 * 2.84 + (flight_time / 60) * 6 * 2.84)
    
    ramp_weight = bew + pilot + pax + total_fuel_kg
    moment_ramp = (bew * arm_bew) + (pilot * arm_pilot_pax) + (pax * arm_pilot_pax) + (total_fuel_kg * arm_fuel)
    arm_ramp = moment_ramp / ramp_weight
    
    takeoff_weight = ramp_weight - taxi_fuel_kg
    moment_takeoff = moment_ramp - (taxi_fuel_kg * arm_fuel)
    arm_takeoff = moment_takeoff / takeoff_weight
    
    landing_weight = takeoff_weight - trip_fuel_kg
    moment_landing = moment_takeoff - (trip_fuel_kg * arm_fuel)
    arm_landing = moment_landing / landing_weight
    
    mass_df = pd.DataFrame({
        "Phase": ["Ramp", "Takeoff", "Landing"],
        "Weight (kg)": [round(ramp_weight, 2), round(takeoff_weight, 2), round(landing_weight, 2)],
        "Arm (m)": [round(arm_ramp, 3), round(arm_takeoff, 3), round(arm_landing, 3)],
        "Moment": [round(moment_ramp, 2), round(moment_takeoff, 2), round(moment_landing, 2)]
    })
    return mass_df

def main():
    st.title("Cessna 152 Mass & Balance and Performance Calculator")
    
    qnh = st.number_input("QNH", value=1013, step=1, format="%d")
    oat = st.number_input("OAT (°C)", value=15, step=1, format="%d")
    flight_time = st.number_input("Flight Time (min)", min_value=1, value=60, step=1)
    
    st.header("Fuel Calculation")
    fuel_df, total_fuel_kg = calculate_fuel(flight_time)
    st.table(fuel_df)
    
    st.header("Mass & Balance")
    mass_df = calculate_mass_balance(total_fuel_kg)
    st.table(mass_df)
    
    st.header("Performance & Distance Calculation")
    isa_dev = oat - 15
    st.write(f"ISA Deviation: {isa_dev}")
    
    st.write("Distance Calculation - LIPU")
    st.write("To be implemented")
    
    st.write("Distance Calculation - LIPH")
    st.write("To be implemented")

if __name__ == "__main__":
    main()
