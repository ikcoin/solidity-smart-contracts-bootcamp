from brownie import accounts, config, SimpleStorage, network
import os


def get_account():
    if network.show_active() == "development":
        return accounts[0]  # Local Ganache Brownie generated accounts
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_simple_storage():
    account = get_account()

    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)
    simple_storage.store(15, {"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)


def main():
    deploy_simple_storage()
