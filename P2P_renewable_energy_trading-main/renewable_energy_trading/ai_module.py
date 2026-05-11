class EnergyTradingAI:

    def __init__(self):
        print("🤖 Lightweight AI module initialized")

    # ---------------------------------------------------
    # TRADE RECOMMENDATION
    # ---------------------------------------------------
    def recommend_trade(self, seller_data, buyer_data, market_conditions):

        forecast = market_conditions.get("forecast_demand", 0)
        price = market_conditions.get("current_price", 0)
        amount = seller_data.get("energy_available", 0)

        # PRICE + REASONING LOGIC
        if forecast >= 0.75:
            new_price = price * 1.20
            reasoning = "Very high demand detected — strong upward price pressure."

        elif forecast >= 0.55:
            new_price = price * 1.10
            reasoning = "High demand — increasing price."

        elif forecast >= 0.35:
            new_price = price * 1.03
            reasoning = "Moderate demand — slight price adjustment."

        elif forecast >= 0.20:
            new_price = price * 0.95
            reasoning = "Low demand — price reduction recommended."

        else:
            new_price = price * 0.85
            reasoning = "Very low demand — aggressive price drop suggested."

        return {
            "recommended_price": round(new_price, 2),
            "recommended_amount": amount,
            "confidence_score": round(min(1, forecast + 0.3), 2),
            "reasoning": reasoning
        }

    # ---------------------------------------------------
    # NEGOTIATION (LIGHTWEIGHT)
    # ---------------------------------------------------
    def simulate_negotiation(self, initial_offer, counter_offer, history):

        suggested_offer = (initial_offer + counter_offer) / 2

        return {
            "suggested_offer": suggested_offer,
            "negotiation_strategy": "Balanced compromise strategy",
            "predicted_outcome": "Trade likely successful"
        }

    # ---------------------------------------------------
    # ANOMALY DETECTION
    # ---------------------------------------------------
    def analyze_anomalies(self, transaction_data, historical_data):

        payment = transaction_data.get("payment", 0)

        if payment > 100000:
            return {
                "anomaly_detected": True,
                "anomaly_type": "Unusually large payment",
                "risk_score": 0.8,
                "explanation": "Payment exceeds normal trading range."
            }

        return {
            "anomaly_detected": False,
            "anomaly_type": None,
            "risk_score": 0.1,
            "explanation": "Transaction appears normal."
        }