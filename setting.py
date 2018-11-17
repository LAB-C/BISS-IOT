from klaytn import *
import os.path, requests, json

url = input('[*] Input Firmware-server URL: ')
klay = Klaytn(url)

def make_info():
    wallet = klay.newAccount('_labc')
    info = {
        'device': {
            'name': input('[*] Input device name: '),
            'wallet': wallet
        },
        'klaytn-node': input('[*] Input Klaytn node URL: '),
        'firmware-server': url
    }
    klay.unlockAccount(wallet, '_labc', 30000)
    with open('./info.json', 'w') as f:
        json.dump(info, f, indent=4)
    return info

def report_info(info):
    # 1. Check if same wallet exists in server
    r = requests.post(url, data={'wallet': info['device']['wallet']})
    if json.loads(r.text)['message'] == False: # does not exist(new)
        # 2. Report device information
        r = requests.post(url, data=info['device'])
        if 'Success' in r.text:
            return True
    return False

if not os.path.isfile('./info.json'): # 존재 x
    info = make_info()
    report_info(info)
else:
    try:
        with open('./info.json', 'r') as f:
            info = json.load(f)
        report_info(info)
    except:
        pass
