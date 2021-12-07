from scripts.helpful_scripts import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from scripts.deploy import deploy_tokenFarm_and_dappToken
from brownie import network, exceptions
import pytest


def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_tokenFarm_and_dappToken()

    # Act
    token_farm.setPriceFeedContract(
        dapp_token.address, get_contract("eth_usd_price_feed"), {"from": account}
    )

    # Assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == get_contract(
        "eth_usd_price_feed"
    )
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(
            dapp_token.address, get_contract("eth_usd_price_feed"), {"from": non_owner}
        )
