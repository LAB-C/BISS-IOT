from client.klaytn import Klaytn
from client.utils import *
import urllib.request
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
file_url = get_realfirmwareurl(file_id, key, info)
print(file_url)

file_name = file_url[file_url.rfind("/")+1:]
print(file_name)

try:
    # download file
    urllib.request.urlretrieve(file_url, './firms/' + file_name)

    # get file checksum
    file_hash = hash_file('./firms/' + file_name)

    # check hash(reporting)
    res = requests.post(info['firmware_server'] + '/api/check/hash/' + str(file_id), json={
        'hash': file_hash, 
        'wallet': info['device']['wallet']
    })
    print(res.text)
    data = json.loads(res.text)
    print(data)
    if data['equal']:
        print('[*] Success: File Equal!')
    else:
        print('[*] Error: File is Different!')        
except:
    pass
