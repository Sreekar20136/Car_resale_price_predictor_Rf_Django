import pickle
from django.shortcuts import render
from .forms import CarPriceForm
import pandas as pd

# Load the model and label encoders once when the server starts
def load_model():
    with open('carPrice/model/car_price_predictor_final.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

model_data = load_model()
model = model_data['model']
label_encoders = model_data['label_encoders']

def get_car_choices():
    df = pd.read_csv('carPrice/model/car_prediction_data.csv')
    car_names = df['Car_Name'].unique()
    car_choices = [(car, car) for car in car_names]
    return car_choices

def predict_price(data):
    # Extract the input values
    car_name = data['car_name']
    present_price = data['present_price']
    kms_driven = data['kms_driven']
    fuel_type = data['fuel_type']
    seller_type = data['seller_type']
    transmission = data['transmission']
    owner = data['owner']
    
    # Ensure you include all features used during training
    # Encode categorical variables
    car_name_encoded = label_encoders['Car_Name'].transform([car_name])[0]
    fuel_type_encoded = label_encoders['Fuel_Type'].transform([fuel_type])[0]
    seller_type_encoded = label_encoders['Seller_Type'].transform([seller_type])[0]
    transmission_encoded = label_encoders['Transmission'].transform([transmission])[0]

    # Add the feature(s) that might be missing
    # For example, if you have a feature like `Car_Age`:
    car_age = 2024 - int(data['year'])  # Assuming `year` is included
    # Or use any other features you used in training

    # Create input data array with all required features
    input_data = [[
        car_name_encoded,
        present_price,
        kms_driven,
        fuel_type_encoded,
        seller_type_encoded,
        transmission_encoded,
        owner,
        car_age  # Ensure all features used during training are included
    ]]
    
    # Predict price
    predicted_price = model.predict(input_data)[0]
    return round(predicted_price, 2)

 



def index(request):
    if request.method == 'POST':
        form = CarPriceForm(request.POST, car_choices=get_car_choices())
        if form.is_valid():
            prediction = predict_price(form.cleaned_data)
            return render(request, 'carPrice/index.html', {'form': form, 'prediction': prediction})
    else:
        form = CarPriceForm(car_choices=get_car_choices())

    return render(request, 'carPrice/index.html', {'form': form})
