from client.klaytn import Klaytn
import logging, requests, json

def strip_url(_url):
    return _url[:-1] if _url.endswith('/') else _url

def make_info():
    # klaytn node
    klay_url = strip_url(input('[*] Input Klaytn node URL: '))
    klay = Klaytn(klay_url)
    logging.debug('Klaytn node URL: ' + klay_url)

    # firmware server
    server_url = strip_url(input('[*] Input Firmware server URL: '))

    wallet = klay.newAccount('_labc')
    logging.debug('New Wallet: ' + wallet)
    info = {
        'device': {
            'name': input('[*] Input device name: '),
            'wallet': wallet
        },
        'klaytn_node': klay_url,
        'firmware_server': server_url
    }
    logging.debug(info)
    klay.unlockAccount(wallet, '_labc', 30000)
    logging.debug('Unlocked wallet: ' + wallet)
    with open('./info.json', 'w') as f:
        json.dump(info, f, indent=4)
    return info

def report_info(info):
    server_url = info['firmware_server']

    # 1. Check if same wallet exists in server
    r = requests.post(server_url + '/check/exist', data={'wallet': info['device']['wallet']})
    logging.debug('URL: ' + server_url + '/check/exist')
    logging.debug('response: ' + r.text)

    if json.loads(r.text)['exist'] == False:
        # 2. Report device information

        r = requests.post(server_url + '/register', data=info['device'])
        logging.debug('URL: ' + server_url + '/register')
        logging.debug('response: ' + r.text)

        if 'Success' in r.text:
            print('[*] Register success')
            return True
    return False

def check_update(info):
    wallet = info['device']['wallet']
    server_url = info['firmware_server']

    r = requests.post(server_url + '/check/update', data={'wallet': wallet})
    logging.debug('URL: ' + server_url + '/check/update')
    logging.debug('response: ' + r.text)
    
    return True if json.loads(r.text)['update'] else False
    