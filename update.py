from client.klaytn import Klaytn
from client.utils import *
import urllib.request
import json, requests, subprocess

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

# download file
urllib.request.urlretrieve(file_url, './firms/' + file_name)

# get file checksum
file_hash = hash_file('./firms/' + file_name)

# check hash in blockchain
output = subprocess.Popen(['node', 'client/send.js', 'hash', str(file_id), file_hash], stdout=subprocess.PIPE ).communicate()[0]
result = json.loads(output.strip().decode())['result']

try:
    if result:
        print('[*] Success: File Equal! (local-blockchain)')

        # check hash(reporting)
        res = requests.post(info['firmware_server'] + '/api/check/hash/' + str(file_id), json={
            'hash': file_hash, 
            'wallet': info['device']['wallet']
        })
        print(res.text)
        data = json.loads(res.text)

        if data['equal']:
            print('[*] Success: File Equal! (local-server)')
        
            # upload to arduino
            if get_ext('./firms/' + file_name) == '.ino':
                print('[*] Success: Firmware file is .ino file!')
                upload_device('./firms/' + file_name)
            
            else:
                print('[*] Error: Firmware file is NOT .ino file!')
        else:
            print('[*] Error: File is Different! (local-server)')
    else:
        print('[*] Error: File is Different! (local-blockchain)')  
except:
    print('[*] Error while executing')

print('[*] Finish')
