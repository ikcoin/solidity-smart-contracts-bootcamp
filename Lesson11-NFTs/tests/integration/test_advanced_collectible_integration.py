from brownie import network, AdvancedCollectible
import time
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
)
from scripts.advanced_collectible.deploy_and_mint import deploy_and_mint


def test_can_create_advanced_collectible_integration():
    # deploy the contract
    # create an NFT
    # get a random type back
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    # Act
    advanced_collectible, creation_transaction = deploy_and_mint()
    time.sleep(60)
    # Assert
    assert advanced_collectible.tokenCounter() == 1