from brownie import FundMe, network, accounts, exceptions
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIROMENTS
from scripts.deploy import deploy_fund_me
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = 25000000000000000  # fund_me.getEntranceFee()

    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)  # wait 1 block
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    tx = fund_me.withdraw({"from": account})
    tx.wait(1)  # wait 1 block
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip("Only for local network testing")

    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
