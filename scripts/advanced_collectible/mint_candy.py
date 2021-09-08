from brownie import AdvancedCollectible, accounts, config, network
from scripts.utils import fund_with_link, upload_to_ipfs, upload_to_pinata
import time
import os
from metadata import metadata_template
from pathlib import Path
import requests
import json
import time
import sys 

'''
!!EXAMPLE!!

image_dic = {
    'hydrogen-#FFFFFF.png': 'https://ipfs.io/ipfs/QmekYjK3ZH5PM3zkMXbSmHxSB95oymSVwbQSbaCLfNvmTm?filename=hydrogen-#FFFFFF.png'
    }

local_metadata_dict = {
    "hydrogen-#FFFFFF.png.json": {
        "name": "hydrogen-#FFFFFF.png",
        "description": "hydrogen-#FFFFFF.png",
        "image": "https://ipfs.io/ipfs/QmekYjK3ZH5PM3zkMXbSmHxSB95oymSVwbQSbaCLfNvmTm?filename=hydrogen-#FFFFFF.png",
        "attributes": [
            {
                "trait_type": "Found on the laboratory floor",
                "value": true
            },
            {
                "trait_type": "story",
                "value": "suisuss slipped on a bored banana at the Candy Bay Research Lab and found this candy underneath a table."
            },
            {
                "trait_type": "Probability of containing some narcotic",
                "value": 0.1
            }
        ]
    }
}

ipfs_metadata_dict = {
    'hydrogen-#FFFFFF.json': 'https://ipfs.io/ipfs/QmekYjK3ZH5PM3zkMXbSsadfsdfddVwbQSbaCLfNvmTm?filename=hydrogen-#FFFFFF.json'
}

'''

def main():

    stdoutOrigin=sys.stdout 
    sys.stdout = open(f"./reports/{network.show_active()}/batches/{config['batch']}.report", "w")

    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    print(advanced_collectible.address)
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    calc_number_of_advanced_collectibles = ((config['batch'] - 1) * 4)

    print(f"Expecting to have deployed {calc_number_of_advanced_collectibles} candys")
    print(f"Have deployed {number_of_advanced_collectibles} candys")

    if calc_number_of_advanced_collectibles == number_of_advanced_collectibles:
        print("Uploading Images")
        image_dic = dict()
        upload_files(f"./img/{network.show_active()}/batches/{config['batch']}", image_dic)
        print("\n")
        print(json.dumps(image_dic, indent=4))
        print("\n")

        time.sleep(30)

        print("Creating metadata files")
        local_metadata_dic = dict()
        create_metadata(local_metadata_dic, image_dic, number_of_advanced_collectibles)
        print("\n")
        print(json.dumps(local_metadata_dic, indent=4))
        print("\n")

        print("Uploading metadata files")
        ipfs_metadata_dic = dict()
        upload_files(f"./metadata/{network.show_active()}/batches/{config['batch']}", ipfs_metadata_dic)
        print("\n")
        print(json.dumps(ipfs_metadata_dic, indent=4))
        print("\n")


        print("Minting collectibles")
        create_collectibles(ipfs_metadata_dic)

    else: 
        print("Your batch number is for a batch that has already roled out.")

    sys.stdout.close()
    sys.stdout=stdoutOrigin


def upload_files(path_of_the_directory, dic):
    files = []
    for filename in os.listdir(path_of_the_directory):
        if filename.endswith(('.png', '.json')):
            print(filename)
            files.append(filename)
    
    if len(files) == 4:
        for i, filename in enumerate(files):
            print(f"Uploading metadata file #{i}: {filename}")
            dic[filename] = upload_to_ipfs(f"{path_of_the_directory}/{filename}")
    else:
        print(f"Theres are {len(files)} files in that directory, there must be 4")




def create_metadata(local_metadata_list, image_dic, number_of_advanced_collectibles):

    if len(image_dic) == 4:
        for i, (key, value) in enumerate(image_dic.items()):
            metadata_file_name = (f"./metadata/{network.show_active()}/batches/{config['batch']}/{key}.json")
            collectible_metadata = metadata_template.metadata_template

            print(f"Creating metadata file #{i}: {metadata_file_name}")
            collectible_metadata["name"] = number_of_advanced_collectibles + i + 1

           # collectible_metadata["description"] = key NO DESCRIPTION

            collectible_metadata["image"] = value
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file, indent=4)

            local_metadata_list[metadata_file_name] = collectible_metadata


def create_collectibles(ipfs_metadata_dic):
    dev = accounts.add(config["wallets"]["from_key"])
    # Get most recent deployment of Advanced Collectible
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    fund_with_link(advanced_collectible.address)
    # Create collectible with no URI. Will add URI with set_tokenuri.py later

    for key, uri in ipfs_metadata_dic.items():
        transaction = advanced_collectible.createCollectible(uri, {"from": dev})
        print("Waiting on second transaction...")
        # wait for the 2nd transaction
        transaction.wait(1)
        time.sleep(45)

        requestId = transaction.events["requestedCollectible"]["requestId"] # Get request ID from transaction
        token_id = advanced_collectible.requestIdToTokenId(requestId) # Get token ID
        print(f"TokenId for {key} is {token_id}")