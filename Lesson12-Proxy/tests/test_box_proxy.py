from scripts.helpful_scripts import get_account, encode_function_data
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_proxy_delegates_calls():
    # Arrange
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()

    # Act
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)

    # Assert
    assert proxy_box.retrieve() == 0
    proxy_box.store(7, {"from": account})
    assert proxy_box.retrieve() == 7