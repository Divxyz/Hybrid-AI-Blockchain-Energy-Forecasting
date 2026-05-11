import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Load trained model
model = load_model("models/trained_model.h5", compile=False)

def predict_next_hour():
    # Load latest data
    df = pd.read_csv("data/energy_features.csv")

    # Select features (adjust if different)
    features = ["demand", "temp", "humidity", "wind_speed"]
    data = df[features].values

    # Scale data (same as training)
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    # Take last 24 rows (your LSTM window)
    last_window = data_scaled[-24:]
    last_window = np.reshape(last_window, (1, last_window.shape[0], last_window.shape[1]))

    # Predict
    prediction = model.predict(last_window)

    return float(prediction[0][0])