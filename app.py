import streamlit as st
import numpy as np

def interpolate(value, x_points, y_points):
    return np.interp(value, x_points, y_points)

def convert_feet_to_meters(feet):
    return feet * 0.3048

def calculate_mass_balance(total_flight_time):
    taxi_time = 15
    trip_time = total_flight_time - taxi_time
    contingency_time = round(trip_time * 0.05)
    alternate_time = 30
    reserve_time = 30
    extra_time_2h = max(0, 120 - total_flight_time)
    extra_time_3h = max(0, 180 - total_flight_time)
    extra_time_4h = max(0, 240 - total_flight_time)
    
    fuel_times = [taxi_time, trip_time, contingency_time, alternate_time, reserve_time]
    fuel_times += [extra_time_2h, extra_time_3h, extra_time_4h]
    fuel_gal = [round(t / 60 * 6, 2) for t in fuel_times]
    fuel_kg = [round(g * 2.84, 2) for g in fuel_gal]
    
    return fuel_times, fuel_gal, fuel_kg

def calculate_performance(qnh, oat, airport):
    elevation = 44 if airport == "LIPU" else 59
    pressure_altitude = elevation + (1013 - qnh) * 30
    isa_dev = oat - (15 - (elevation / 1000 * 2))
    density_altitude = pressure_altitude + (120 * isa_dev)
    
    return elevation, pressure_altitude, isa_dev, density_altitude

def main():
    st.title("Cessna 152 Performance Calculator")
    
    total_flight_time = st.number_input("Total Flight Time (min)", min_value=0, max_value=240, step=1)
    fuel_times, fuel_gal, fuel_kg = calculate_mass_balance(total_flight_time)
    
    st.header("Fuel Calculation")
    categories = ["Taxi", "Trip", "Contingency", "Alternate", "Reserve", "Extra (2h)", "Extra (3h)", "Extra (4h)"]
    for i, cat in enumerate(categories):
        st.write(f"{cat}: {fuel_times[i]} min, {fuel_gal[i]} USG, {fuel_kg[i]} kg")
    
    st.header("Mass & Balance")
    st.write("Calculations for weight, arm, and moment based on fuel weight.")
    
    st.header("Performance Calculation")
    qnh_lipu = st.number_input("QNH (LIPU)", value=1013)
    oat_lipu = st.number_input("OAT (LIPU)", value=15)
    elevation_lipu, pa_lipu, isa_dev_lipu, da_lipu = calculate_performance(qnh_lipu, oat_lipu, "LIPU")
    
    st.write(f"Elevation: {elevation_lipu} ft, PA: {pa_lipu} ft, ISA Dev: {isa_dev_lipu}, DA: {da_lipu} ft")
    
    qnh_liph = st.number_input("QNH (LIPH)", value=1013)
    oat_liph = st.number_input("OAT (LIPH)", value=15)
    elevation_liph, pa_liph, isa_dev_liph, da_liph = calculate_performance(qnh_liph, oat_liph, "LIPH")
    
    st.write(f"Elevation: {elevation_liph} ft, PA: {pa_liph} ft, ISA Dev: {isa_dev_liph}, DA: {da_liph} ft")
    
    st.header("Runway Conditions")
    condition = st.selectbox("Runway Condition", ["Dry", "Wet"])
    factor = 1.00 if condition == "Dry" else 1.15
    
    takeoff_roll = interpolate(pa_lipu, [0, 1000], [450, 480])  # Example interpolation
    landing_roll = interpolate(pa_liph, [0, 1000], [500, 530])  # Example interpolation
    
    takeoff_distance = takeoff_roll * factor * 1.25
    landing_distance = landing_roll * factor * 1.25
    asdr = takeoff_distance + landing_distance
    
    st.write(f"Takeoff Ground Roll: {convert_feet_to_meters(takeoff_distance):.2f} m")
    st.write(f"Landing Ground Roll: {convert_feet_to_meters(landing_distance):.2f} m")
    st.write(f"Accelerate-Stop Distance Required (ASDR): {convert_feet_to_meters(asdr):.2f} m")
    
if __name__ == "__main__":
    main()
