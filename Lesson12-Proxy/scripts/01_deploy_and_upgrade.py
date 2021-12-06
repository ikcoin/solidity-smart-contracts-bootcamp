from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    network,
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
)


def main():
    account = get_account()
    print("Deploying to ", network.show_active())
    box = Box.deploy({"from": account}, publish_source=True)
    print(box.retrieve())

    # Hooking up a proxy to out implementation contract (Box.sol)
    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=True)
    # initializer = box.store, 1 # In this case, the contrcutor is to call the store function with value 1
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,  # Logic contract address,
        proxy_admin.address,  # Admin address,
        box_encoded_initializer_function,  # encoded function call
        {"from": account, "gas_limit": 1000000},
        publish_source=False,
    )
    print("Proxy deployed to ", proxy, " We can now upgrade to V2.")

    # Assign the proxy address the abi of the Box contract. This will work because the proxy will
    # delegate all the calls to the box contract
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    tx = proxy_box.store(5, {"from": account})
    tx.wait(1)
    print(proxy_box.retrieve())

    """
    -----UPGRADE-BOXV2-----
    """
    box_v2 = BoxV2.deploy({"from": account}, publish_source=True)
    upgrade_transaction = upgrade(account, proxy, box_v2.address, proxy_admin)
    print("Proxy has been updated.")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())
