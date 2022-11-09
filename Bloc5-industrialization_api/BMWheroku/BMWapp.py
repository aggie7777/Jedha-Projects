import streamlit as st
import numpy as np
import pandas as pd
import pickle

from sklearn.tree import DecisionTreeRegressor
html_temp = """
<div style="background-color:yellow;padding:1.5px">
<h1 style="color:black;text-align:center;">Used Car Price Prediction</h1>
</div><br>"""
st.markdown(html_temp, unsafe_allow_html=True)

st.write("\n\n"*2)

# load model
@st.cache
model = pickle.load(open("C:/Users/Administrateur/Desktop/car_Api/car_price_predictor_model.pkl",'rb'))


with st.sidebar:
    st.subheader('Car Specs to Predict Price')

year = st.sidebar.number_input("Model year:",min_value=1996, max_value=2020, value=1996, step=1)
mileage = st.sidebar.number_input("km Traveled:",min_value=1000, max_value=200000, value=1000, step=5000)
price = st.sidebar.number_input("The price at the time of purchase:",min_value=1000, max_value=100000, value=1000, step=1000)
fuelType = st.sidebar.selectbox("Fuel Type Selection", ("Diesel", "Petrol", "Hybrid", "Electric"))
if fuelType == "Diesel":
    fuelType = 0
elif fuelType == "Electric":
    fuelType = 1
elif fuelType == "Hybrid":
    fuelType = 2
else:
    fuelType = 3
transmission = st.sidebar.radio("Transmission", ("Manual", "Automatic", "Semi-Auto"))
if transmission == "Automatic":
    transmission = 0
elif transmission == "Semi-Auto":
    transmission = 1
else:
    transmission = 2
engineSize = st.sidebar.number_input("Engine Size:",min_value=1.0, max_value=6.0, value=1.0, step=0.5)

input_data = {
        "year": year,
        "mileage": mileage,
        "price": price,
        "fuelType": fuelType,
        "transmission": transmission,
        "engineSize": engineSize
    }

df = pd.DataFrame.from_dict([input_data])

cols = {
    "year": "Model year",
    "mileage": "km Traveled",
    "price": "price of purchase",
    "fuelType": "Fuel Type",
    "transmission": "Transmission",
    "engineSize": "Engine Size"
}

df_show = df.copy()
df_show.rename(columns = cols, inplace = True)
st.write("Spécifications sélectionnées: \n")
st.table(df_show)

if st.button("Predict"):
    pred = model.predict(df)
    col1, col2 = st.columns(2)
    col1.write(f"La valeur estimée du prix de la voiture est de £ :")
    col2.write(pred[0].astype(int))


st.write("\n\n")
