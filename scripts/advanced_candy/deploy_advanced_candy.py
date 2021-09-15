#!/usr/bin/python3
from brownie import AdvancedCandy, accounts, network, config


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    # publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False # Currently having an issue with this
    publish_source = False
    advanced_candy = AdvancedCandy.deploy({"from": dev}, publish_source=publish_source)
    return advanced_candy
