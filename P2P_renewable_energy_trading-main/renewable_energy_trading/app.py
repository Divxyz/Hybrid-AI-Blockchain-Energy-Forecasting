from flask import Flask, request, jsonify
from flask_cors import CORS
from web3 import Web3
from ai_module import EnergyTradingAI
import requests
import json

app = Flask(__name__)
CORS(app)

# ---------------------------------------------
#  BLOCKCHAIN SETUP  (CONNECT TO GANACHE HERE)
# ---------------------------------------------
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

if w3.is_connected():
    print("🔗 Connected to Ganache blockchain")
else:
    print("❌ Connection failed. Check Ganache RPC URL")

# ---------------------------------------------
#  LOAD DEPLOYED SMART CONTRACT
# ---------------------------------------------
with open("contract_data.json") as f:
    contract_data = json.load(f)

contract_address = contract_data["address"]
contract_abi = contract_data["abi"]

contract = w3.eth.contract(
    address=contract_address,
    abi=contract_abi
)

print("📦 Smart Contract Loaded:", contract_address)

# ---------------------------------------------
#  AI SETUP (LIGHTWEIGHT AI)
# ---------------------------------------------
ai = EnergyTradingAI()

# ---------------------------------------------
#  FORECAST API INTEGRATION
# ---------------------------------------------
def get_energy_forecast(amount, price):
    try:
        url = f"http://127.0.0.1:5001/forecast?amount={amount}&price={price}"
        res = requests.get(url)
        data = res.json()
        return data.get("predicted_demand")
    except Exception as e:
        print("Forecast API error:", e)
        return None

# ---------------------------------------------
#  ENDPOINT: PROPOSE TRADE
# ---------------------------------------------
@app.route('/propose_trade', methods=['POST'])
def propose_trade():

    data = request.json

    seller = data['seller']
    buyer = data['buyer']
    amount = data['amount']
    price = data['price']

    # 🔥 NOW variables exist — safe to call forecast
    forecast_value = get_energy_forecast(amount, price)

    print("⚡ Predicted Demand from Forecast API:", forecast_value)

    recommendation = ai.recommend_trade(
        seller_data={'address': seller, 'energy_available': amount},
        buyer_data={'address': buyer, 'energy_needed': amount},
        market_conditions={
            'current_price': price,
            'forecast_demand': forecast_value
        }
    )

    price = int(round(recommendation["recommended_price"]))

    tx_hash = contract.functions.proposeTrade(
        buyer, amount, price
    ).transact({'from': seller})

    return jsonify({
        'forecast_value': forecast_value,
        'ai_recommendation': recommendation,
        'final_price_used': price,
        'transaction_hash': tx_hash.hex()
    })

# ---------------------------------------------
#  ENDPOINT: EXECUTE TRADE
# ---------------------------------------------
@app.route('/execute_trade', methods=['POST'])
def execute_trade():

    data = request.json
    trade_id = data['trade_id']
    buyer = data['buyer']
    payment = data['payment']

    anomaly_check = ai.analyze_anomalies(
        transaction_data={'trade_id': trade_id, 'buyer': buyer, 'payment': payment},
        historical_data=[]
    )

    if anomaly_check.get('anomaly_detected'):
        return jsonify({'error': 'Anomaly detected', 'details': anomaly_check}), 400

    tx_hash = contract.functions.executeTrade(
        trade_id
    ).transact({'from': buyer, 'value': payment})

    return jsonify({
        'anomaly_analysis': anomaly_check,
        'transaction_hash': tx_hash.hex()
    })

# ---------------------------------------------
#  ENDPOINT: NEGOTIATE
# ---------------------------------------------
@app.route('/negotiate', methods=['POST'])
def negotiate():

    data = request.json
    initial_offer = data['initial_offer']
    counter_offer = data['counter_offer']
    history = data.get('history', [])

    negotiation_result = ai.simulate_negotiation(
        initial_offer,
        counter_offer,
        history
    )

    return jsonify(negotiation_result)

# ---------------------------------------------
#  ENDPOINT: TRADE HISTORY
# ---------------------------------------------
@app.route('/trade_history', methods=['GET'])
def get_trade_history():

    trade_id = request.args.get('trade_id')

    if trade_id:
        trade = contract.functions.getTrade(int(trade_id)).call()
        return jsonify({
            'seller': trade[0],
            'buyer': trade[1],
            'amount': trade[2],
            'price': trade[3],
            'timestamp': trade[4],
            'executed': trade[5]
        })
    else:
        return jsonify({'message': 'Trade history endpoint - implement pagination'})

# ---------------------------------------------
#  APP RUNNER
# ---------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
