from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time


def deploy_lottery():
    account = get_account()
    lottery_contract = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    print("Deployed Lottery contract at Addres: ", Lottery[-1].address)
    return lottery_contract


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    print("Lottery Started...")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]

    value = lottery.getEntranceFee() + 100000000
    print("The Actual minimum value to enter the lottery is ", value)
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("Lottery entered")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]

    # Send some LINK to contract
    tx = fund_with_link(lottery.address)
    tx.wait(1)

    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    time.sleep(60)
    print(lottery.winner(), " is the Winner")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()