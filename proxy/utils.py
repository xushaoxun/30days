# coding:utf-8
import random, requests
from fake_useragent import UserAgent
from config import REFERER_LIST, TIMEOUT

def get_referer():
    return random.choice(REFERER_LIST)

def get_user_agent():
    check_fake_useragent_file()

    ua = UserAgent()
    return ua.random

def check_fake_useragent_file():
    fake_data = 'fake_useragent_0.1.2.json'
    # save fake_useragent data file
    import os, tempfile, shutil

    p = os.path.join(tempfile.gettempdir(), fake_data)

    if not os.path.exists(p):
        shutil.copyfile(fake_data, p)

def fetch(url, proxy=None, cookies=None):
    '''
    :param url: str
    :param proxy: str
    :return: request.Response
    :except: requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError
    '''
    # s = requests.Session()
    # s.headers.update({'user-agent': get_user_agent()})

    headers = {
        'User-Agent': get_user_agent(),
    }

    proxies = None
    if proxy:
        proxies = {
            'http': proxy
        }

    return requests.get(url, headers=headers, proxies=proxies, cookies=cookies)

    # return s.get(url, timeout=TIMEOUT, proxies=proxies)

if __name__ == '__main__':
    # r = requests.get('http://httpbin.org/get')
    # print r.text
    check_fake_useragent_file()
    # res = fetch('http://httpbin.org/get')
    # print (res.text)