from client.klaytn import Klaytn
import logging, requests, json, hashlib, os.path

def strip_url(_url):
    return _url[:-1] if _url.endswith('/') else _url

def make_info():
    # klaytn node
    klay_url = strip_url(input('[*] Input Klaytn node URL: '))
    klay = Klaytn(klay_url)
    logging.debug('Klaytn node URL: ' + klay_url)

    wallet = klay.newAccount('_labc')
    logging.debug('New Wallet: ' + wallet)
    info = {
        'device': {
            'name': input('[*] Input device name: '),
            'wallet': wallet,
            'desc': input('[*] Input device description: ')
        },
        'klaytn_node': klay_url,
        'firmware_server': strip_url(input('[*] Input Firmware server URL: ')),
        'data_server': strip_url(input('[*] Input Data server URL: '))
    }
    logging.debug(info)
    klay.unlockAccount(wallet, '_labc', 30000)
    logging.debug('Unlocked wallet: ' + wallet)
    with open('./info.json', 'w') as f:
        json.dump(info, f, indent=4)
    return info

def report_info(info):
    # [*] REPORT to firmware_server
    server_url = info['firmware_server']

    # 1. Check if same wallet exists in server
    r = requests.post(server_url + '/api/check/exist', json={'wallet': info['device']['wallet']})
    logging.debug('URL: ' + server_url + '/api/check/exist')
    logging.debug('response: ' + r.text)

    if json.loads(r.text)['exist'] == False:
        logging.debug('Info not in Firmware Server')
        # 2. Report device information

        r = requests.post(server_url + '/api/register', json=info['device'])
        logging.debug('URL: ' + server_url + '/api/register')
        logging.debug('response: ' + r.text)

        if 'Success' in r.text:
            print('[*] Firmware-Server: Register success')
        else:
            print('[*] Firmware-Server: Register failed')

    # [*] REPORT to data_server
    server_url = info['data_server']

    # 1. Check duplicate -> data server iot device
    r = requests.get(server_url + '/api/iot/regist/' + info['device']['wallet'])
    logging.debug('URL: ' + server_url + '/api/iot/regist/' + info['device']['wallet'])
    logging.debug('response: ' + r.text)

    if not json.loads(r.text)['data']: # not in server
        # 2. register iot device
        logging.debug('Info not in Data Server')
        r = requests.post(server_url + '/api/iot/regist', json={
            'uuid': info['device']['wallet'], # wallet
            'key': info['device']['wallet'], # wallet
            'name': info['device']['name'],
            'desc': info['device']['desc']
        })
        logging.debug('URL: ' + server_url + '/api/iot/regist')
        logging.debug('response: ' + r.text)
        if json.loads(r.text)['data']:
            print('[*] Data-Server: Device Register success')   
        else:         
            print('[*] Data-Server: Device Register failed')        

    # 3. Check duplicate -> data server wallet
    r = requests.get(server_url + '/api/iot/' + info['device']['wallet'])
    logging.debug('URL: ' + server_url + '/api/iot/' + info['device']['wallet'])
    logging.debug('response: ' + r.text)

    if not json.loads(r.text)['data']: # not in server
        # 4. register wallet
        logging.debug('Info not in Data Server')
        r = requests.post(server_url + '/api/iot', json={
            'iot': info['device']['wallet'], # wallet
        })
        logging.debug('URL: ' + server_url + '/api/iot')
        logging.debug('response: ' + r.text)
        if json.loads(r.text)['data']:
            print('[*] Data-Server: Wallet Register success')   
        else:         
            print('[*] Data-Server: Wallet Register failed')
            
    return False

def check_update(info):
    wallet = info['device']['wallet']
    server_url = info['firmware_server']

    r = requests.post(server_url + '/api/check/update', json={'wallet': wallet})
    logging.debug('URL: ' + server_url + '/api/check/update')
    logging.debug('response: ' + r.text)

    res = json.loads(r.text)
    return res if res['update'] else False

def get_realfirmwareurl(file_id, key, info):
    res = requests.post(info['firmware_server'] + '/api/download/' + str(file_id), json ={'key': key})
    logging.info(res.text)
    data = json.loads(res.text)
    try:
        return data['result']['url']
    except:
        return False

def hash_file(filepath):
    md5_hash = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            md5_hash.update(buf)
            buf = f.read(65536)
    return md5_hash.hexdigest()

def get_ext(filepath):
    _, ext = os.path.splitext(filepath)
    return ext

def upload_device(filepath):
    os.system('arduino-sketch -u ' + filepath)
    os.system('rm -rf ' + filepath)
