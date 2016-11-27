# coding:utf-8
import sys
if 'threading' in sys.modules:
    del sys.modules['threading']
from gevent import monkey, GreenletExit
from gevent.queue import Queue, Empty
from gevent.pool import Pool
from time import sleep
from utils import fetch
from models import Proxy
from config import COUNTRY_URL
from bs4 import BeautifulSoup
import requests

monkey.patch_all()

def use_gevent_with_queue():
    queue = Queue()
    pool = Pool(10)

    # for i in range(1,10):
    #     queue.put(i)
    queue.put(0)

    while pool.free_count():
        sleep(0.1)
        pool.spawn(do_with_queue, queue)

    pool.join()

def do_with_queue(queue):
    while True:
        try:
            page = queue.get(timeout=0)
        except Empty:
            break

        fetch_country_data(page, queue)
    print 'stop'

def fetch_country_data(page, queue, retry=0):

    if retry > 5:
        print 'retry>5'
        queue.put(page)
        raise GreenletExit()

    url = COUNTRY_URL.format(page)
    proxy = Proxy.get_random_proxy()
    print 'fetch url:{} with proxy:{}'.format(url, proxy)

    try:
        r = fetch(url, proxy)
    except (requests.Timeout, requests.ConnectionError):
        print 'request exception, proxy invalid. retry'
        return fetch_country_data(page, queue, retry+1)
        # proxy.delete()

    if r.status_code != 200:
        print 'status code invalid'
        return fetch_country_data(page, queue, retry+1)
        # proxy.delete()

    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.find('div', attrs={'id': 'results'})
    countries = results.find_all('div')

    print results




if __name__ == '__main__':
    use_gevent_with_queue()