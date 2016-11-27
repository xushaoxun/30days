# coding:utf-8
import requests, re, threading
from utils import fetch
from config import PROXY_REGEX, PROXY_SITES
from models import Proxy
from mongoengine import NotUniqueError
# from multiprocessing.dummy import Pool
import Queue
from gevent.pool import Pool

def save_proxies(url):
    proxies = []
    try:
        r = fetch(url)
    except requests.exceptions.RequestException:
        return False

    addresses = re.findall(PROXY_REGEX, r.text)
    for addr in addresses:
        proxy = Proxy(address=addr)
        try:
            proxy.save()
            print 'save proxy {}'.format(addr)
        except NotUniqueError:
            pass
        else:
            proxies.append(proxy)

    return proxies

def cleanup():
    Proxy.drop_collection()


def non_thread():
    cleanup()
    for url in PROXY_SITES:
        save_proxies(url)


def use_thread():
    cleanup()

    threads = []
    for url in PROXY_SITES:
        t = threading.Thread(target=save_proxies, args=(url,))
        t.setDaemon(True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def use_gevent_pool():
    cleanup()

    pool = Pool(10)
    pool.map(save_proxies, PROXY_SITES)



def save_proxies_with_queue(queue):
    while True:
        url = queue.get()
        save_proxies(url)
        queue.task_done()


def use_thread_with_queue():
    cleanup()
    queue = Queue.Queue()
    for i in range(5):
        t = threading.Thread(target=save_proxies_with_queue, args=(queue,))
        t.setDaemon(True)
        t.start()

    for url in PROXY_SITES:
        queue.put(url)

    queue.join()


def save_proxies_with_queue2(in_queue, out_queue):
    while True:
        url = in_queue.get()
        rs = save_proxies(url)
        out_queue.put(rs)
        in_queue.task_done()

def append_result(out_queue, result):
    while True:
        rs = out_queue.get()
        if rs:
            result.append(rs)
        out_queue.task_done()


def use_thread_with_queue2():
    cleanup()
    in_queue = Queue.Queue()
    out_queue = Queue.Queue()

    for i in range(5):
        t = threading.Thread(target=save_proxies_with_queue2, args=(in_queue, out_queue))
        t.setDaemon(True)
        t.start()

    for url in PROXY_SITES:
        in_queue.put(url)

    result = []

    for i in range(5):
        t = threading.Thread(target=append_result, args=(out_queue, result))
        t.setDaemon(True)
        t.start()

    in_queue.join()
    out_queue.join()

    print result


def check_proxy(proxy):
    '''
    check if proxy is valid
    :param proxy: Proxy
    :return:
    '''
    try:
        print 'check proxy', proxy.address
        fetch('http://www.baidu.com', proxy.address)
        print 'proxy {} is valid'.format(proxy.address)
    except requests.RequestException:
        print 'proxy invalid'
        proxy.delete()

def check_proxy_with_gevent():
    pool = Pool(10)
    pool.map(check_proxy, Proxy.objects.all())

if __name__ == '__main__':
    # 获取代理
    # use_thread_with_queue2()
    use_gevent_pool()
    print 'proxy count=', Proxy.objects.count()

    check_proxy_with_gevent()
    print 'proxy count after check:', Proxy.objects.count()
    # 验证代理
    # print 'proxy count=', Proxy.objects.count()
    # pool = Pool(5)
    # pool.map(check_proxy, Proxy.objects.all())
    # print 'proxy count=', Proxy.objects.count()

