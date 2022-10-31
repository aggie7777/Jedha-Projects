from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pickle

# load model
model=pickle.load(open("model\car_price_predictor_model.pkl",'rb'))

app=FastAPI()
# ["year", "mileage", "price", "fuelType", "transmission", "engineSize", "selling_price"]
class Input(BaseModel):
    year:int
    mileage:int
    price:int
    fuelType:int
    transmission:int
    engineSize:float

@app.get("/")
def read_root():
    return {"msg":"Car Price Predictor"}

@app.post("/predict")
def predict_price(input:Input):
    data = input.dict()
    data_in = [[data['year'], data['mileage'], data['price'], data['fuelType'],
                    data['transmission'], data['engineSize']]]

    prediction = model.predict(data_in)
    return {
        'prediction': prediction[0]
        }

if __name__=="__main__":
    uvicorn.run(app, host="http://localhost/", port=8000)
