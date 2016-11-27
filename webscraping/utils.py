# coding:utf-8

import requests,tempfile, os, shutil
from fake_useragent import UserAgent
from config import FAKE_DATA_FILE, TIMEOUT

def get_user_agent():
    if not os.path.exists(os.path.join(tempfile.gettempdir(), FAKE_DATA_FILE)):
        shutil.copy(FAKE_DATA_FILE, os.path.join(tempfile.gettempdir(), FAKE_DATA_FILE))

    ua = UserAgent()
    return ua.random


def fetch(url, proxy=None):
    headers = {
        'user-agent': get_user_agent()
    }

    proxies = None
    if proxy:
        proxies = {
            'http': proxy
        }

    r = requests.get(url, timeout=TIMEOUT, headers=headers, proxies=proxies)
    return r

if __name__ == '__main__':
    pass
