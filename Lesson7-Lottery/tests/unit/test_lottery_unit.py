from brownie import Lottery
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3


def test_get_entrance_fee():
    # Arrange
    lottery = deploy_lottery()
    # Act
    # 2,000 eth/usd
    # usdEntryFee is 50
    # 200/1==50/x == 0.025
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert entrance_fee == expected_entrance_fee
