from brownie import network, AdvancedCollectible
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    get_account,
    get_type,
)
from scripts.advanced_collectible.deploy_and_mint import deploy_and_mint


def test_can_create_advanced_collectible():
    # deploy the contract
    # create an NFT
    # get a random type back
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    # Act
    advanced_collectible, creation_transaction = deploy_and_mint()
    requestId = creation_transaction.events["requestedCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_collectible.address, {"from": get_account()}
    )
    # Assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToType(0) == random_number % 3


def test_get_type():
    # Arrange / Act
    nftType = get_type(0)
    # Assert
    assert nftType == "PUG"