import random, subprocess, json, requests
with open('./info.json', 'r') as f:
    info = json.load(f)

data = round(random.uniform(1, 1.5), 2)
output = subprocess.Popen(['node', 'client/send.js', 'data', str(data)], stdout=subprocess.PIPE).communicate()[0].decode()
if output:
    txhash = json.loads(output.strip())['result']
    if 'Error' not in txhash:
        res = requests.post(info['data_server'] + '/api/iot/add', json={
            "iot" : info['device']['wallet'],
            "transaction" : txhash
        }).text
        print(res)
        if json.loads(res)['data']:
            print('[*] Success')
        exit(0)
print('[*] Error while executing')
