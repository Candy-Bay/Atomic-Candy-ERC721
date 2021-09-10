#!/usr/bin/python3
from brownie import AdvancedCandy, accounts, network, config, interface
import json


def main():
    flatten()


def flatten():
    file = open("./AdvancedCandy_flattened.json", "w")
    json.dump(AdvancedCandy.get_verification_info(), file)
    file.close()
