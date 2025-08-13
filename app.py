import streamlit as st
import pandas as pd
import joblib

model = joblib.load("best_co2_model.joblib")

st.set_page_config(page_title="CO₂ Emission Predictor", page_icon="🌍", layout="centered")
st.title("CO₂ Emission Predictor")
st.markdown("Select your car brand and model to estimate realistic CO₂ emissions (g/km).")


car_specs = pd.read_csv("archive/car_specs_cleaned.csv")
car_specs.columns = car_specs.columns.str.strip()


brand = st.selectbox("Select Car Brand", car_specs['Make'].unique())
model_name = st.selectbox("Select Car Model", car_specs[car_specs['Make'] == brand]['Model'].unique())  


car_data = car_specs[(car_specs['Make'] == brand) & (car_specs['Model'] == model_name)].iloc[0]

with st.form("prediction_form"):
    engine_size = st.slider(
        "Engine Size (L)", 0.5, 8.0, value=float(car_data['capacity_cm3']) / 1000, step=0.1
    )
    
    cylinders_value = car_data['number_of_cylinders']
    if pd.isna(cylinders_value):
        cylinders_value = 4  
    cylinders_value = int(cylinders_value)
    
    cylinders = st.selectbox(
        "Cylinders",
        [3, 4, 5, 6, 8, 12],
        index=[3, 4, 5, 6, 8, 12].index(cylinders_value)
    )
    
    fuel_city = st.slider(
        "Fuel Consumption City (L/100 km)", 4.0, 20.0,
        value=float(car_data['city_fuel_per_100km_l']), step=0.1
    )
    fuel_hwy = st.slider(
        "Fuel Consumption Hwy (L/100 km)", 3.0, 15.0,
        value=float(car_data['highway_fuel_per_100km_l']), step=0.1
    )
    fuel_comb = st.slider(
        "Fuel Consumption Combined (L/100 km)", 4.0, 20.0,
        value=float(car_data['mixed_fuel_consumption_per_100_km_l']), step=0.1
    )

    
    submit_button = st.form_submit_button("Predict CO₂")

if submit_button:
    input_df = pd.DataFrame([{
        "Make": brand,
        "Vehicle Class": "SUV - Small",  
        "Engine Size(L)": engine_size,
        "Cylinders": cylinders,
        "Transmission": car_data['transmission'],
        "Fuel Type": "Z",  
        "Fuel Consumption City (L/100 km)": fuel_city,
        "Fuel Consumption Hwy (L/100 km)": fuel_hwy,
        "Fuel Consumption Comb (L/100 km)": fuel_comb,
        "Fuel Consumption Comb (mpg)": 30  
    }])
    
    predicted_value = model.predict(input_df)[0]
    st.success(f"Predicted CO₂ Emissions for {brand} {model_name}: **{predicted_value:.2f} g/km**")

st.markdown("---")
