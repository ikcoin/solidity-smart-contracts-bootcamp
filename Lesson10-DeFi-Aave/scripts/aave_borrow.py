from brownie import network, config, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from scripts.withdraw_weth import withdrawy_weth
from web3 import Web3

AMOUNT = Web3.toWei(0.1, "ether")


def get_lending_pool():
    # ABI, Address
    lending_pool_AddressProvider_contract = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_contract_address = (
        lending_pool_AddressProvider_contract.getLendingPool()
    )
    lending_pool_contract = interface.ILendingPool(lending_pool_contract_address)
    return lending_pool_contract


def approve_erc20(amount, spender, erc20_address, account):
    # ABI, Address
    erc20_token = interface.IERC20(erc20_address)
    print("Approving ERC20 token..")
    tx = erc20_token.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Erc20 token consumption approved.")
    return tx


def main():
    account = get_account()
    weth_contract_address = config["networks"][network.show_active()]["weth_token"]

    # get 0.1 WETH
    get_weth()

    lending_pool_contract = get_lending_pool()
    print(lending_pool_contract)

    # Deposit 0.1 WETH to the lending_pool_contract
    #   1. Approve ERC20 token
    approve_erc20(AMOUNT, lending_pool_contract.address, weth_contract_address, account)
    #   2. Deposit

    # Return 0.1 WETH for the 0.1 ETH
    withdrawy_weth()
