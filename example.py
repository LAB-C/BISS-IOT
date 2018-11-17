import sys
from klaytn import *
from arduinoupload import *
klay = Klaytn('http://ubuntu.hanukoon.com:8551')

wallet = klay.newAccount('_labc') # create newAccount with '_labc' as passphrase
print(wallet)

print(klay.unlockAccount(wallet, '_labc', 30000)) # wallet to unlock, pass, time to unlock(sec)

print(klay.sendData(wallet, 'so what?')) # return txHash
