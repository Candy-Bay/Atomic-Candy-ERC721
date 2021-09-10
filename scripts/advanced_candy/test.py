from brownie import AdvancedCandy, accounts, config, network
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
    advanced_candy = AdvancedCandy[len(AdvancedCandy) - 1]
    number_of_advanced_candys = advanced_candy.tokenCounter()

    for token_id in range(number_of_advanced_candys):
        print(token_id, advanced_candy.tokenURI(token_id))
        #advanced_candy.setTokenURI

    #dev = accounts.add(config["wallets"]["from_key"])
    #advanced_candy.setTokenURI(0, advanced_candy.tokenURI(1), {"from": dev})