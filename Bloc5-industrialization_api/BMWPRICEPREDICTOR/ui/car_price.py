import streamlit as st
import requests
import json


def main():
    st.title("BMW CAR PRICE PREDICTOR")

    year = st.number_input("Year")

    mileage = st.number_input("Mileage (in mile)")

    price = st.number_input("Price (in £)")

    fuelType = st.selectbox("Fuel Type", ("Diesel", "Electric", "Hybrid", "Petrol"))
    if fuelType == "Diesel":
        fuelType = 0
    elif fuelType == "Electric":
        fuelType = 1
    elif fuelType == "Hybrid":
        fuelType = 2
    else:
        fuelType = 3

    transmission = st.selectbox("transmission", ("Automatic", "Semi-Auto", "Manual"))
    if transmission == "Automatic":
        transmission = 0
    elif transmission == "Semi-Auto":
        transmission = 1
    else:
        transmission = 2

    engineSize = st.number_input("Engine Size (in L)")


    input_data = {
        "year": year,
        "mileage": mileage,
        "price": price,
        "fuelType": fuelType,
        "transmission": transmission,
        "engineSize": engineSize
    }

    price = 0
    if st.button("Predict"):
        price = requests.post(url="http://127.0.0.1:8000/predict", data=json.dumps(input_data))
        price = price.json()
        p = price['prediction']
        st.success(f'The Price of the Car is {p} £')


if __name__ == '__main__':
    main()
