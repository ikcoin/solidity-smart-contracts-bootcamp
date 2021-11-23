from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv
import os
import json

# load .env
load_dotenv()

# install_solc("0.8.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile the Smart Contracts
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_sol.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# Ganache blockchain connection
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x5cAAd74bD53A90Dc6BbC6644A97812a5A7891333"
private_key = os.getenv("PRIVATE_KEY")

# contract creation
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get account current nonce
nonce = w3.eth.getTransactionCount(my_address)

# Deply contract transaction built
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key
)

tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# Interacting with the contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call() --> Simulate making the call and getting a return value
# transact() --> Making a state change

nonce = w3.eth.getTransactionCount(my_address)
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
print(simple_storage.functions.retrieve().call())