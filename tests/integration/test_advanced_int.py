import pytest
from brownie import network, AdvancedCandy
from scripts.utils import (
    get_account,
    get_contract,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
import time


def test_can_create_advanced_candy_integration(
    get_keyhash,
    chainlink_fee,
):
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
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
    advanced_candy.createCandy("None", {"from": get_account()})
    time.sleep(75)
    # Assert
    assert advanced_candy.tokenCounter() > 0
