from klaytn import *
import os.path, requests, json

import logging
logging.basicConfig(level=logging.DEBUG)

url = input('[*] Input Firmware-server URL: ')
klay = Klaytn(url)
logging.debug('Firmware-server URL: ' + url)

def make_info():
    wallet = klay.newAccount('_labc')
    logging.debug('New Wallet: ' + wallet)
    info = {
        'device': {
            'name': input('[*] Input device name: '),
            'wallet': wallet
        },
        'klaytn-node': input('[*] Input Klaytn node URL: '),
        'firmware-server': url
    }
    logging.debug(info)
    klay.unlockAccount(wallet, '_labc', 30000)
    logging.debug('Unlocked wallet: ' + wallet)
    with open('./info.json', 'w') as f:
        json.dump(info, f, indent=4)
    return info

def report_info(info):
    # 1. Check if same wallet exists in server
    r = requests.post(url + '/check/update', data={'wallet': info['device']['wallet']})
    logging.debug('URL: ' + url + '/check/update')
    logging.debug('response: ' + r.text)
    if json.loads(r.text)['message'] == False: # does not exist(new)
        # 2. Report device information
        r = requests.post(url + '/register', data=info['device'])
        logging.debug('URL: ' + url + '/register')
        logging.debug('response: ' + r.text)
        if 'Success' in r.text:
            return True
    return False

if not os.path.isfile('./info.json'): # 존재 x
    logging.debug('info.json: file not found -> calling make_info()')
    info = make_info()
    report_info(info)
else:
    try:
        with open('./info.json', 'r') as f:
            logging.debug('info.json: file found')
            info = json.load(f)
        report_info(info)
    except:
        logging.debug('info.json: parsing error -> calling make_info()')
        info = make_info()
        report_info(info)
