from scripts.helpful_scripts import get_account, OPENSEA_URL, get_contract
from brownie import AdvancedCollectible, config, network

sample_token_uri = "https://ipfs.io/ipfs/QmQDsRGjhhWUvTHiRaQ69F6TndWuMS2tNTapAPyZn6zE3r?filename=0-SHIB.json"


def deploy_and_mint():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        "Advanced NFT",
        "ANFT",
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    """
    tx = advanced_collectible.createCollectible(sample_token_uri, {"from": account})

    tx.wait(1)
    print(
        f"NFT available at {OPENSEA_URL.format(advanced_collectible.address, advanced_collectible.tokenCounter()-1)}"
    )
    return advanced_collectible
    """


def main():
    deploy_and_mint()
