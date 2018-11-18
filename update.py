from client.utils import *
import json, requests

import logging
logging.basicConfig(level=logging.DEBUG)

# check update
with open('./info.json', 'r') as f:
    print(check_update(json.load(f)))
