import requests, subprocess, json

class Klaytn:
    def __init__(self, url):
        self.url = url
        self.header = {'Content-Type':'application/json'}
    
    def _request(self, method, jsonrp='2.0', params=[], id=1):
        return requests.post(self.url, headers=self.header, 
            json={'jsonrpc':jsonrp, 'method':method, 'params':params, 'id':id}
        ).json()

    def newAccount(self, passphrase):
        wallet = self._request('personal_newAccount', params=[passphrase])['result']
        print('[*]', requests.get('https://apiwallet.klaytn.com/faucet?address=' + wallet).text) # get first klay from faucet
        return wallet
    
    def unlockAccount(self, address, passphrase, duration):
        return True if self._request('personal_unlockAccount', params=[address, passphrase, duration])=='true' else False

    def sendData(self, data):
        output = subprocess.Popen(['node', 'firmware_server/send.js', 'data', data], stdout=subprocess.PIPE ).communicate()[0]
        result = json.loads(output.strip().decode())['result']
        if 'Error' in result:
            return False
        return result
    
    def getInputData(self, txhash):
        url = 'https://apiscope.klaytn.com/api/transaction/' + txhash
        res = json.loads(requests.get(url).text)
        if res['status'] == 'FAIL':
            return False
        print(bytes.fromhex(res['result']['input'][2:]).replace(b'\x00', b''))
        return bytes.fromhex(res['result']['input'][2:]).replace(b'\x00', b'').replace(b'\x1b\xc2t\x16\x11@\x1e', b'').decode()
