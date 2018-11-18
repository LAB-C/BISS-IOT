import requests
import sys
import json
from pprint import pprint
import os

with open('info.json') as f:
        data = json.load(f)

check1 = requests.post('http://ubuntu.hanukoon.com:5000/api/check/exist', json={'wallet' : data['device']['wallet']})
parsed1 = json.loads(check1)

if parsed1['exist'] == false:
	os.system("python3 setting.py")
os.system("sudo ./start.sh")
