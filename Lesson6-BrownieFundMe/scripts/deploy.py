from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account


def deploy_fund_me():
    account = get_account()

    if network.show_active() != "development":
        price_feed_address = config["netwoks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:  # mock
        print("Deploying Mocks...")
        mock_aggregator = MockV3Aggregator.deploy(
            18, 2000000000000000000000, {"from": account}
        )
        print("MockV3Aggregator deployed at address: ", mock_aggregator.address)
        price_feed_address = mock_aggregator.address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print("FundMe deployed on addres: ", fund_me.address)


def main():
    deploy_fund_me()