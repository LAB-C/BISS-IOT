from client.utils import *
import os.path, json

import logging
logging.basicConfig(level=logging.DEBUG)

if not os.path.isfile('./info.json'): # 존재 x
    logging.debug('info.json: file not found -> calling make_info()')
    info = make_info()
    report_info(info)
else:
    # try:
        with open('./info.json', 'r') as f:
            logging.debug('info.json: file found')
            info = json.load(f)
        report_info(info)
    # except:
    #     logging.debug('info.json: parsing error -> calling make_info()')
    #     info = make_info()
    #     report_info(info)

print('[*] Finish')
