from brownie import network, config, ikcoin
from scripts.helpful_scripts import get_account

INITIAL_SUPPLY = 1000_000_000_000_000_000_000


def deploy_ikcoin():
    account = get_account()
    ikcoin_contract = ikcoin.deploy(
        INITIAL_SUPPLY,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    print("Deployed Lottery contract at Addres: ", ikcoin[-1].address)
    return ikcoin_contract


def main():
    deploy_ikcoin()