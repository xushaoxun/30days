# coding:utf-8
import re, requests
from models import Proxy
from utils import fetch
from config import PROXY_RE, PROXY_SITES
from mongoengine import NotUniqueError
from gevent.pool import Pool

def clean_up():
    Proxy.drop_collection()

def save_proxy(url):
    proxies = []
    try:
        r = fetch(url)
        print r.status_code
    except requests.exceptions.RequestException:
        print 'Request Exception'
        return None

    addresses = re.findall(PROXY_RE, r.text)
    for addr in addresses:
        proxy = Proxy(address = addr)
        try:
            proxy.save()
            print 'proxy {} saved'.format(addr)
        except NotUniqueError:
            pass
        proxies.append(addr)

    return proxies

def save_proxy_with_pool():
    clean_up()

    pool = Pool(5)
    pool.map(save_proxy, PROXY_SITES)

def check_proxy(proxy):
    if isinstance(proxy, str):
        address = proxy
    elif isinstance(proxy, Proxy):
        address = proxy.address
    else:
        raise BaseException

    print 'check proxy {}'.format(address)
    try:
        r = fetch('http://httpbin.org/get', proxy=address)
        if r.status_code != 200:
            if isinstance(proxy, Proxy):
                proxy.delete()
            raise requests.exceptions.ConnectionError
        print r.status_code, r.text
    except Exception as e:
        print e
        print 'invalid proxy {}, delete!'.format(address)
        if isinstance(proxy, Proxy):
            proxy.delete()

# 好像很慢
def check_proxy_with_pool():
    pool = Pool(10)
    pool.map(check_proxy, Proxy.objects.all())


if __name__ == '__main__':
    # save_proxy_with_pool()
    # check_proxy_with_pool()

    check_proxy_with_pool()

