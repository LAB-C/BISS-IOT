from klaytn import *
import os.path, json

klay = Klaytn('http://ubuntu.hanukoon.com:8551')

if not os.path.isfile('./info.json'):
    pass
    
wallet = klay.newAcc ount('_labc')
klay.unlockAccount(wallet, '_labc', 30000)
print(klay.sendData(wallet, 'test1 by h4nuko0n'))
