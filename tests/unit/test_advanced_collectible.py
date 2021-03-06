import pytest
from brownie import network, AdvancedCandy
from scripts.utils import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def test_can_create_advanced_candy(
    get_keyhash,
    chainlink_fee,
):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    advanced_candy = AdvancedCandy.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        get_keyhash,
        {"from": get_account()},
    )
    get_contract("link_token").transfer(
        advanced_candy.address, chainlink_fee * 3, {"from": get_account()}
    )
    # Act
    transaction_receipt = advanced_candy.createCandy(
        "None", {"from": get_account()}
    )
    requestId = transaction_receipt.events["requestedCollectible"]["requestId"]
    assert isinstance(transaction_receipt.txid, str)
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, 777, advanced_candy.address, {"from": get_account()}
    )
    # Assert
    assert advanced_candy.tokenCounter() > 0
    assert isinstance(advanced_candy.tokenCounter(), int)
