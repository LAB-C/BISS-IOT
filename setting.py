from klaytn import * 
klay = Klaytn('http://ubuntu.hanukoon.com:8551')
wallet = klay.newAccount('_labc')
klay.unlockAccount(wallet, '_labc', 30000)
print(klay.sendData(wallet, 'test1 by h4nuko0n'))
