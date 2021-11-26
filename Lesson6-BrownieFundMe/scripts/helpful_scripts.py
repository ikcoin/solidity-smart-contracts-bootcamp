from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000

LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local"]


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    account = get_account()

    print("Deploying Mocks...")
    print("----------", len(MockV3Aggregator))
    if len(MockV3Aggregator) <= 0:  # Contract not deployed yet
        MockV3Aggregator.deploy(
            DECIMALS,
            STARTING_PRICE,
            {"from": account},  # Web3.toWei(STARTING_PRICE, "ether")
        )
        print("MockV3Aggregator deployed at address: ", MockV3Aggregator[-1].address)

    return MockV3Aggregator[-1].address