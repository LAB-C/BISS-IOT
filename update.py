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

    # check hash in blockchain
    output = subprocess.Popen(['node', 'firmware_server/send.js', 'hash', file_id, file_hash], stdout=subprocess.PIPE ).communicate()[0]
    result = json.loads(output.strip().decode())['result']

    if result:
        print('[*] Success: File Equal! (local-blockchain)')
        
        # upload
        if get_ext('./firms/' + file_name) == '.ino':
            print('[*] Success: Firmware file is .ino file!')
            upload_device('./firms/' + file_name)
        
        else:
            print('[*] Error: Firmware file is NOT .ino file!')
    else:
        print('[*] Error: File is Different! (local-blockchain)')  
except:
    pass

print('[*] Finish')
