from brownie import network, TokenFarm, DappToken, config
from scripts.helpful_scripts import get_account, INITIAL_VALUE, get_contract


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        tx = token_farm.addAllowedTokens(token.address, {"from": account})
        tx.wait(1)

        tx = token_farm.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token], {"from": account}
        )
        tx.wait(1)


def deploy_tokenFarm_and_dappToken():
    account = get_account()
    dapp_token = DappToken.deploy(INITIAL_VALUE, {"from": account})
    token_farm = TokenFarm.deploy(
        dapp_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    tx = dapp_token.transfer(token_farm.address, INITIAL_VALUE / 2)
    tx.wait(1)

    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    dict_of_allowed_tokens = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }
    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)
    return token_farm, dapp_token


def main():
    deploy_tokenFarm_and_dappToken()
    account = get_account()
