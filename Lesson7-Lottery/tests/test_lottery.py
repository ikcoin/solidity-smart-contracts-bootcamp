from brownie import Lottery, config, network, accounts
from scripts.helpful_scripts import get_account
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]  # get_account()
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    assert lottery.getEntranceFee() > Web3.toWei(0.011, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.012, "ether")
