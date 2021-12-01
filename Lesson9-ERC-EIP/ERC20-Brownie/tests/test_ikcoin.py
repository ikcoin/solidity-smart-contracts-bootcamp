from brownie import network, exceptions
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIROMENTS, get_account
from scripts.deploy_token import deploy_ikcoin
from web3 import Web3
import pytest


def test_get_tottal_supply():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()

    # Arrange
    account = get_account()
    ikcoin = deploy_ikcoin()

    # Act
    expected_total_supply = Web3.toWei(1000, "ether")
    minter_balance = ikcoin.balanceOf(account)
    # Assert
    assert expected_total_supply == minter_balance


def test_get_name_symbol():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()

    # Arrange
    account = get_account()
    ikcoin = deploy_ikcoin()

    # Act
    expected_name = "ikcoin"
    expected_symbol = "IKC"
    name = ikcoin.name()
    symbol = ikcoin.symbol()
    # Assert
    assert expected_name == name
    assert expected_symbol == symbol