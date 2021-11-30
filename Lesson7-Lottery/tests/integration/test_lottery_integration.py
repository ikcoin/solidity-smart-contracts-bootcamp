from brownie import Lottery, config, network, accounts
from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
)
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
import time

"""
def test_get_entrance_fee222():
    account = accounts[0]  # get_account()
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    assert lottery.getEntranceFee() > Web3.toWei(0.011, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.012, "ether")
"""


def test_can_pick_winner():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    account = get_account()
    lottery = deploy_lottery()

    # Act
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})

    fund_with_link(lottery.address)
    lottery.endLottery({"from": account})

    time.sleep(60)  # Wait for the Chainlink node to respons

    # Assert
    assert lottery.winner() == account
    assert lottery.balance() == 0
