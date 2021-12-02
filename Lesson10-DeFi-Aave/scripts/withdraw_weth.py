from brownie import interface, config, network
from scripts.helpful_scripts import get_account
from web3 import Web3


def withdrawy_weth(collateral):

    account = get_account()

    # To interact with the WETH Contract, we need the ABI and the Address
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.withdraw(Web3.toWei(collateral, "ether"), {f"from": account})
    tx.wait(1)
    print("Received ", collateral, " ETH")


def main():
    withdrawy_weth()