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


def get_borrowable_data(lending_pool_contract, account):
    (
        totalCollateralETH,
        totalDebtETH,
        availableBorrowsETH,
        currentLiquidationThreshold,
        ltv,
        healthFactor,
    ) = lending_pool_contract.getUserAccountData(account)

    availableBorrowsETH = Web3.fromWei(availableBorrowsETH, "ether")
    totalDebtETH = Web3.fromWei(totalDebtETH, "ether")
    totalCollateralETH = Web3.fromWei(totalCollateralETH, "ether")

    print("You have ", totalCollateralETH, " worth of ETH deposited.")
    print("You have ", totalDebtETH, " worth of ETH borrowed.")
    print("You can borrow ", availableBorrowsETH, " worth of ETH.")

    return (float(availableBorrowsETH), float(totalCollateralETH))


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.IAggregatorV3(price_feed_address)
    (
        roundId,
        answer,  # price
        startedAt,
        updatedAt,
        answeredInRound,
    ) = dai_eth_price_feed.latestRoundData()
    print("The DAI/ETH price is ", Web3.fromWei(answer, "ether"))
    return float(Web3.fromWei(answer, "ether"))


def repay_all(amount, lending_pool_contract, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool_contract.address,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )

    repay_tx = lending_pool_contract.repay(
        config["networks"][network.show_active()]["dai_token"],  # asset
        amount,
        1,  # RateMode
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)
    print("Borrowed amount repayed.")


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
    tx = lending_pool_contract.deposit(
        weth_contract_address, AMOUNT, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Amount deposited. ")

    borrowable_eth, total_collateral = get_borrowable_data(
        lending_pool_contract, account
    )

    # DAI in terms of ETH
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_usd_price_feed"]
    )
    dai_address = config["networks"][network.show_active()]["dai_token"]
    amount_dai_to_borrow = (1 / dai_eth_price) * (
        borrowable_eth * 0.95
    )  # 95% of the ETH to not get liquidated
    print("Wer are going to borrow ", amount_dai_to_borrow, " DAI")
    borrow_tx = lending_pool_contract.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,  # interestRateMode
        0,  # referralCode
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("Some DAI borrowed.")
    get_borrowable_data(lending_pool_contract, account)

    # Repay everithing borrowed
    repay_all(amount_dai_to_borrow, lending_pool_contract, account)
    borrowable_eth, total_collateral = get_borrowable_data(
        lending_pool_contract, account
    )
    print("Deposited, borrowed and repayed back with Aave & Chainlink.")

    # Return 0.1 WETH for the 0.1 ETH
    # withdrawy_weth(total_collateral)

    get_borrowable_data(lending_pool_contract, account)
