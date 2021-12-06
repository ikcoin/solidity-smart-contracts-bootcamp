from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    Box,
    BoxV2,
    exceptions,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
)
import pytest


def test_proxy_upgrades():
    # Arrange
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account},
    )

    # Act
    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})
    # Since we didn't upgrade the proxy yet, proxy shouldn't delegate the function increment to BoxV2 but Box(V1)

    upgrade(account, proxy, box_v2.address, proxy_admin)
    assert proxy_box.retrieve() == 0
    proxy_box.store(7, {"from": account})
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 8