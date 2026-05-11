from flask import Flask, jsonify, request
from flask_cors import CORS
from predict import predict_next_hour
import random

# ⭐ CREATE FLASK APP FIRST
app = Flask(__name__)
CORS(app)

# -----------------------------------------
# FORECAST ROUTE (PUT THIS BELOW app=Flask)
# -----------------------------------------
@app.route('/forecast', methods=['GET'])
def forecast():

    amount = float(request.args.get("amount", 10))
    price = float(request.args.get("price", 5))

    base_prediction = float(predict_next_hour())

    adjusted = base_prediction
    adjusted += (amount * 0.05)
    adjusted -= (price * 0.04)
    adjusted += random.uniform(-0.02, 0.02)

    adjusted = max(0.5, min(0.95, adjusted))

    return jsonify({
        "predicted_demand": adjusted
    })


# -----------------------------------------
# RUN SERVER
# -----------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5001)