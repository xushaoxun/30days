# coding:utf-8
import re, requests, urlparse, threading
from models import Proxy
from utils import fetch
from config import PROXY_RE, PROXY_SITES
from mongoengine import NotUniqueError
# from gevent.pool import Pool
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

def clean_up():
    Proxy.drop_collection()

def save_cool_proxy_net():
    url = 'http://www.cool-proxy.net/proxies/http_proxy_list/page:1/sort:score/direction:desc'
    # url = 'http://httpbin.org/get'
    proxy_url = '202.73.53.22'
    proxy_port = 80
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', proxy_url)
    profile.set_preference('network.proxy.http_port', proxy_port)
    profile.set_preference('network.proxy.ssl', proxy_url)
    profile.set_preference('network.proxy.ssl_port', proxy_port)
    profile.update_preferences()
    driver = webdriver.Firefox(profile)

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'xml')
    driver.quit()

    trs = soup.find_all('tr')

    for tr in trs:
        ip_tr = tr.find('td', attrs={'style': 'text-align:left; font-weight:bold;'})
        port_tr = ip_tr.next_sibling
        print ip_tr
        print port_tr



def save_proxy(url):
    print threading.currentThread().getName()

    from_site = urlparse.urlsplit(url).netloc
    proxies = []
    try:
        r = fetch(url)
        print r.status_code
    except requests.exceptions.RequestException:
        print 'Request Exception'
        return None

    addresses = re.findall(PROXY_RE, r.text)
    for addr in addresses:
        proxy = Proxy(address = addr, from_site=from_site)
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
    pool.close()
    pool.join()

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
    pool.close()
    pool.join()


if __name__ == '__main__':
    # save_proxy_with_pool()
    check_proxy_with_pool()

    # check_proxy_with_pool()
    # print check_proxy('120.52.73.98:93')
    # save_cool_proxy_net()