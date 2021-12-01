from brownie import network, accounts, config
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000

LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork-dev"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS
        or network.show_active() in FORKED_LOCAL_ENVIROMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])
