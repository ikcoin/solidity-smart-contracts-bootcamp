from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible

sample_token_uri = "https://ipfs.io/ipfs/QmQDsRGjhhWUvTHiRaQ69F6TndWuMS2tNTapAPyZn6zE3r?filename=0-SHIB.json"


def deploy_and_mint():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"NFT available at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter()-1)}"
    )
    return simple_collectible


def main():
    deploy_and_mint()
