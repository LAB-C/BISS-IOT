from client.klaytn import Klaytn
from client.utils import *
import json, requests

import logging
logging.basicConfig(level=logging.DEBUG)

# check update
with open('./info.json', 'r') as f:
    info = json.load(f)

res = check_update(info)
if not res: # not updated
    exit(0)

# updated
klay = Klaytn(info['klaytn_node'])

# get file key
file_id = res['file_id']
txhash = res['txHash']
key = klay.getInputData(txhash)

# get public URL
url = get_realfirmwareurl(file_id, key, info)
print(url)
