from client.utils import *
import json, requests

import logging
logging.basicConfig(level=logging.DEBUG)

# check update
with open('./info.json', 'r') as f:
    info = json.load(f)

res = check_update(info)
if not res: # not updated
    exit(0)

# updated
print(res)
