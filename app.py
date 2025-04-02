import streamlit as st
import numpy as np

# Conversione da piedi a metri
FT_TO_M = 0.3048

# Dati di riferimento per il Cessna 152
takeoff_data = {
    0: {0: [940, 1640], 1000: [1040, 1775], 2000: [1150, 1935]},  # PA: Ground Roll, Total Distance in ft
    10: {0: [965, 1690], 1000: [1070, 1835], 2000: [1185, 2000]},
    20: {0: [990, 1745], 1000: [1100, 1900], 2000: [1225, 2075]},
    30: {0: [1015, 1800], 1000: [1130, 1970], 2000: [1265, 2155]},
    40: {0: [1055, 1885], 1000: [1180, 2070], 2000: [1330, 2265]}
}

landing_data = {
    0: {0: [445, 1000], 1000: [500, 1100], 2000: [555, 1215]},
    10: {0: [465, 1045], 1000: [520, 1150], 2000: [580, 1275]},
    20: {0: [485, 1090], 1000: [540, 1200], 2000: [605, 1335]},
    30: {0: [510, 1150], 1000: [570, 1270], 2000: [645, 1410]},
    40: {0: [535, 1210], 1000: [600, 1340], 2000: [685, 1495]}
}

def interpolate(value, x1, y1, x2, y2):
    """Interpolazione lineare per valori intermedi."""
    return y1 + (value - x1) * (y2 - y1) / (x2 - x1)

def get_performance(temp, pressure_alt, data_table):
    """Interpolazione doppia su temperatura e altitudine di pressione."""
    temp_keys = sorted(data_table.keys())
    pa_keys = sorted(data_table[temp_keys[0]].keys())

    # Interpolazione tra temperature
    for i in range(len(temp_keys) - 1):
        if temp_keys[i] <= temp <= temp_keys[i + 1]:
            lower_pa = []
            upper_pa = []

            # Interpolazione su pressure altitude per ogni temperatura
            for j in range(len(pa_keys) - 1):
                if pa_keys[j] <= pressure_alt <= pa_keys[j + 1]:
                    lower_pa_roll = interpolate(pressure_alt, pa_keys[j], data_table[temp_keys[i]][pa_keys[j]][0], 
                                                pa_keys[j + 1], data_table[temp_keys[i]][pa_keys[j + 1]][0])
                    lower_pa_total = interpolate(pressure_alt, pa_keys[j], data_table[temp_keys[i]][pa_keys[j]][1], 
                                                 pa_keys[j + 1], data_table[temp_keys[i]][pa_keys[j + 1]][1])
                    
                    upper_pa_roll = interpolate(pressure_alt, pa_keys[j], data_table[temp_keys[i + 1]][pa_keys[j]][0], 
                                                pa_keys[j + 1], data_table[temp_keys[i + 1]][pa_keys[j + 1]][0])
                    upper_pa_total = interpolate(pressure_alt, pa_keys[j], data_table[temp_keys[i + 1]][pa_keys[j]][1], 
                                                 pa_keys[j + 1], data_table[temp_keys[i + 1]][pa_keys[j + 1]][1])

                    lower_pa = [lower_pa_roll, lower_pa_total]
                    upper_pa = [upper_pa_roll, upper_pa_total]
                    break

            # Interpolazione tra le due temperature
            if lower_pa and upper_pa:
                ground_roll = interpolate(temp, temp_keys[i], lower_pa[0], temp_keys[i + 1], upper_pa[0])
                total_dist = interpolate(temp, temp_keys[i], lower_pa[1], temp_keys[i + 1], upper_pa[1])
                return ground_roll * FT_TO_M, total_dist * FT_TO_M

    return None, None  # Se fuori range

# --- UI Streamlit ---
st.title("Calcolo Performance Cessna 152 ✈️")

# Input utente
temperature = st.number_input("Inserisci la temperatura esterna (°C):", min_value=-10.0, max_value=50.0, step=0.5, value=15.0)
pressure_alt = st.number_input("Inserisci l'altitudine di pressione (ft):", min_value=0, max_value=10000, step=100, value=0)

# Calcolo distanze
takeoff_ground_roll, takeoff_total = get_performance(temperature, pressure_alt, takeoff_data)
landing_ground_roll, landing_total = get_performance(temperature, pressure_alt, landing_data)

# Output risultati
if takeoff_ground_roll and landing_ground_roll:
    st.subheader("Risultati Calcolati:")
    st.write(f"**Takeoff Ground Roll:** {takeoff_ground_roll:.2f} m")
    st.write(f"**Takeoff Total Distance:** {takeoff_total:.2f} m")
    st.write(f"**Landing Ground Roll:** {landing_ground_roll:.2f} m")
    st.write(f"**Landing Total Distance:** {landing_total:.2f} m")
else:
    st.warning("Valori fuori dai limiti delle tabelle disponibili.")
