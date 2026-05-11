import pytest
from unittest.mock import patch, MagicMock
import json
from renewable_energy_trading.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Mock AI module methods
def mock_recommend_trade(*args, **kwargs):
    return {
        "recommended_price": 100,
        "recommended_amount": 50,
        "confidence_score": 0.9,
        "reasoning": "Optimal trade based on demand"
    }

def mock_simulate_negotiation(*args, **kwargs):
    return {
        "suggested_offer": 90,
        "negotiation_strategy": "Compromise",
        "predicted_outcome": "Trade accepted"
    }

def mock_analyze_anomalies_no_anomaly(*args, **kwargs):
    return {
        "anomaly_detected": False,
        "anomaly_type": None,
        "risk_score": 0,
        "explanation": "No anomaly detected"
    }

def mock_analyze_anomalies_with_anomaly(*args, **kwargs):
    return {
        "anomaly_detected": True,
        "anomaly_type": "Fraud",
        "risk_score": 0.95,
        "explanation": "Suspicious payment pattern"
    }

# Mock blockchain contract functions
class MockContractFunction:
    def transact(self, transaction):
        return b"\x12\x34"

    def call(self):
        # Return dummy trade data:
        return (
            "0xSellerAddress",
            "0xBuyerAddress",
            100,
            10,
            1627849200,
            False
        )

@pytest.fixture
def mock_contract_functions():
    mock_contract = MagicMock()
    mock_contract.functions.proposeTrade.return_value = MockContractFunction()
    mock_contract.functions.executeTrade.return_value = MockContractFunction()
    mock_contract.functions.getTrade.return_value = MockContractFunction()
    return mock_contract

@patch('renewable_energy_trading.app.contract', new_callable=MagicMock)
@patch('renewable_energy_trading.app.ai', autospec=True)
def test_propose_trade(mock_ai, mock_contract, client):
    mock_ai.recommend_trade.side_effect = mock_recommend_trade
    mock_contract.functions.proposeTrade.return_value.transact.return_value = b'\x12\x34'

    data = {
        "seller": "0xseller",
        "buyer": "0xbuyer",
        "amount": 50,
        "price": 100
    }

    response = client.post('/propose_trade', json=data)
    json_data = response.get_json()

    assert response.status_code == 200
    assert "ai_recommendation" in json_data
    assert json_data["ai_recommendation"]["recommended_price"] == 100
    assert "transaction_hash" in json_data

@patch('renewable_energy_trading.app.contract', new_callable=MagicMock)
@patch('renewable_energy_trading.app.ai', autospec=True)
def test_execute_trade_no_anomaly(mock_ai, mock_contract, client):
    mock_ai.analyze_anomalies.side_effect = mock_analyze_anomalies_no_anomaly
    mock_contract.functions.executeTrade.return_value.transact.return_value = b'\x12\x34'

    data = {
        "trade_id": 1,
        "buyer": "0xbuyer",
        "payment": 100
    }

    response = client.post('/execute_trade', json=data)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["anomaly_analysis"]["anomaly_detected"] is False
    assert "transaction_hash" in json_data

@patch('renewable_energy_trading.app.ai', autospec=True)
def test_execute_trade_with_anomaly(mock_ai, client):
    mock_ai.analyze_anomalies.side_effect = mock_analyze_anomalies_with_anomaly

    data = {
        "trade_id": 1,
        "buyer": "0xbuyer",
        "payment": 100
    }

    response = client.post('/execute_trade', json=data)
    json_data = response.get_json()

    assert response.status_code == 400
    assert json_data["error"] == "Anomaly detected"

@patch('renewable_energy_trading.app.ai', autospec=True)
def test_negotiate(mock_ai, client):
    mock_ai.simulate_negotiation.side_effect = mock_simulate_negotiation

    data = {
        "initial_offer": 100,
        "counter_offer": 90,
        "history": []
    }

    response = client.post('/negotiate', json=data)
    json_data = response.get_json()

    assert response.status_code == 200
    assert "suggested_offer" in json_data

@patch('renewable_energy_trading.app.contract', new_callable=MagicMock)
def test_get_trade_history_single_trade(mock_contract, client):
    mock_contract.functions.getTrade.return_value.call.return_value = (
        "0xSeller",
        "0xBuyer",
        100,
        10,
        1627849200,
        False
    )

    response = client.get('/trade_history', query_string={"trade_id": 1})
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["seller"] == "0xSeller"
    assert json_data["price"] == 10

@patch('renewable_energy_trading.app.contract', new_callable=MagicMock)
def test_get_trade_history_no_trade_id(mock_contract, client):
    response = client.get('/trade_history')
    json_data = response.get_json()

    assert response.status_code == 200
    assert "message" in json_data
