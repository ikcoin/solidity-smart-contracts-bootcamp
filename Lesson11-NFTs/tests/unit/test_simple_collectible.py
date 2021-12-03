from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
    FORKED_LOCAL_ENVIROMENTS,
    get_account,
)
from scripts.deploy_and_mint import deploy_and_mint
from brownie import network
import pytest


def test_can_create_simple_collectible():
    if (
        network.show_active() not in FORKED_LOCAL_ENVIROMENTS
        and network.show_active() not in FORKED_LOCAL_ENVIROMENTS
    ):
        pytest.skip()

    simple_collectible = deploy_and_mint()
    assert simple_collectible.ownerOf(0) == get_account()
