from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
)
from web3 import Web3


def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        price_feed_address = config["netwoks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:  # mock
        price_feed_address = deploy_mocks()

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print("FundMe deployed on addres: ", fund_me.address)
    return fund_me


def main():
    deploy_fund_me()