from web3 import Web3
from solcx import compile_standard, install_solc
import json

# ---------------------------------------------
# CONNECT TO GANACHE
# ---------------------------------------------
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

print("Connected:", w3.is_connected())

# ---------------------------------------------
# INSTALL SOLIDITY COMPILER
# ---------------------------------------------
install_solc("0.8.0")

# ---------------------------------------------
# READ CONTRACT SOURCE FILE
# ---------------------------------------------
with open("contracts/EnergyTrading.sol", "r") as file:
    contract_source = file.read()

# ---------------------------------------------
# COMPILE CONTRACT
# ---------------------------------------------
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "EnergyTrading.sol": {
                "content": contract_source
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

# ---------------------------------------------
# EXTRACT ABI + BYTECODE
# IMPORTANT: CONTRACT NAME MUST MATCH .SOL FILE
# ---------------------------------------------
abi = compiled_sol["contracts"]["EnergyTrading.sol"]["EnergyTrading"]["abi"]
bytecode = compiled_sol["contracts"]["EnergyTrading.sol"]["EnergyTrading"]["evm"]["bytecode"]["object"]

# ---------------------------------------------
# DEPLOY CONTRACT USING FIRST GANACHE ACCOUNT
# ---------------------------------------------
account = w3.eth.accounts[0]

EnergyTrading = w3.eth.contract(
    abi=abi,
    bytecode=bytecode
)

tx_hash = EnergyTrading.constructor().transact({
    "from": account
})

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("\n✅ CONTRACT DEPLOYED")
print("Address:", tx_receipt.contractAddress)

# ---------------------------------------------
# SAVE CONTRACT DATA FOR app.py
# ---------------------------------------------
with open("contract_data.json", "w") as f:
    json.dump({
        "address": tx_receipt.contractAddress,
        "abi": abi
    }, f, indent=4)
