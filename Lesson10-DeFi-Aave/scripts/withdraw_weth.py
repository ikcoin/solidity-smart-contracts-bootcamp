from brownie import interface, config, network
from scripts.helpful_scripts import get_account
from web3 import Web3


def withdrawy_weth():

    account = get_account()

    # To interact with the WETH Contract, we need the ABI and the Address
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.withdraw(Web3.toWei(0.1, "ether"), {f"from": account})
    tx.wait(1)
    print("Received 0.1 ETH")


def main():
    withdrawy_weth()