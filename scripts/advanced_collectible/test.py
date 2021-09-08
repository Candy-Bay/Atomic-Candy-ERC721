from brownie import AdvancedCollectible, accounts, config, network
from scripts.utils import fund_with_link
import time
import os
from metadata import metadata_template
from pathlib import Path
import requests
import json
import time
import sys 


def main():
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()

    for token_id in range(number_of_advanced_collectibles):
        print(token_id, advanced_collectible.tokenURI(token_id))
        #advanced_collectible.setTokenURI

    #dev = accounts.add(config["wallets"]["from_key"])
    #advanced_collectible.setTokenURI(0, advanced_collectible.tokenURI(1), {"from": dev})