## ⚡ P2P Renewable Energy Trading System

AI-powered peer-to-peer renewable energy trading platform that combines **energy demand forecasting**, **lightweight AI decision-making**, and **Ethereum smart contracts** with a live interactive dashboard.

This project demonstrates a full-stack integration of AI + Blockchain for decentralized energy markets.

---

## 🌱 Overview

Traditional energy markets are centralized and inefficient.  
This system enables decentralized trading where:

✔ Energy demand is predicted using AI  
✔ Prices are optimized dynamically  
✔ Trades are executed through blockchain smart contracts  

The platform simulates a real-world autonomous energy trading ecosystem.

---

## 🧠 Key Features

- 🔮 **LSTM Energy Demand Forecasting**
- 🤖 **Lightweight AI Trade Optimization**
- ⛓️ **Ethereum Smart Contract Trading**
- 📊 **Live Forecast Dashboard UI**
- ⚡ **Dynamic AI Pricing Based on Demand**
- 🔐 **Ganache Local Blockchain Integration**

---

## 🏗️ System Architecture
Frontend Dashboard (HTML/CSS/JS)
│
▼
Blockchain API (Flask + Web3.py)
│
▼
AI Forecast Microservice (TensorFlow LSTM)
│
▼
Ethereum Smart Contract (Ganache)

---

## 🛠️ Tech Stack

### AI & Backend
- Python
- TensorFlow / Keras
- Flask
- Web3.py

### Blockchain
- Solidity
- Hardhat
- Ganache

### Frontend
- HTML
- CSS
- JavaScript

---

## 📂 Project Structure
P2P_renewable_energy_trading/
│
├── EnergyForecasting/ # AI demand prediction microservice
│ ├── forecast_api.py
│ ├── predict.py
│
└── renewable_energy_trading/ # Blockchain backend + UI
├── app.py
├── ai_module.py
└── frontend/

---

## 🚀 How to Run Locally

  1️⃣ Clone Repository
  git clone https://github.com/sharminsheik47-wq/P2P_renewable_energy_trading.git
  cd P2P_renewable_energy_trading
  
  2️⃣ Setup Energy Forecasting Service
  cd EnergyForecasting
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  python forecast_api.py

  3️⃣ Setup Blockchain Backend
  Open new terminal:
  cd renewable_energy_trading
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  python app.py

  4️⃣ Start Ganache
  Run Ganache GUI with RPC
  Deploy smart contract using:
  deploy_contract.py

  5️⃣ Open Frontend
  Open:
  renewable_energy_trading/frontend/index.html

---

## 📊 How It Works

1.User inputs energy amount & price.
2.AI Forecast API predicts demand.
3.Lightweight AI adjusts pricing dynamically.
4.Backend sends transaction to Ethereum smart contract.
5.Trade executes on blockchain.
6.Dashboard updates with result.

---

## Contributing
Contributions are welcome!
Please fork the repository and submit a pull request with your improvements.

---

## Copyright
© 2026 Sharmin

---

## Author
sharminsheik47@gmail.com | Sharmin
