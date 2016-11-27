# coding:utf-8
import sys, re
import threading, multiprocessing, time, requests
from multiprocessing.dummy import Pool
from Queue import Empty
from time import sleep
from utils import fetch, save_file
from models import Proxy, lazy_connect, Country
from config import COUNTRY_URL
from bs4 import BeautifulSoup
from mongoengine.connection import disconnect
from mongoengine import NotUniqueError



def process():
    queue = multiprocessing.JoinableQueue()
    num = multiprocessing.cpu_count()

    # for i in range(1,10):
    #     queue.put(i)
    queue.put('/index/0')

    for _ in range(1):
        p = multiprocessing.Process(target=do_with_queue, args=(queue,))
        p.start()

    queue.join()


def do_with_queue(queue):
    disconnect()
    lazy_connect()

    while True:
        try:
            page = queue.get(timeout=1)
        except Empty:
            break

        rv = fetch_country_data(page, queue)
        queue.task_done()
    print 'stop'

def fetch_country_data(page, queue, retry=0):
    if retry > 5:
        print 'retry>5'
        queue.put(page)
        return

    url = COUNTRY_URL + page
    proxy = Proxy.get_random_proxy()
    print 'fetch url:{} with proxy:{}'.format(url, proxy)

    try:
        r = fetch(url, proxy)
    except (requests.Timeout, requests.ConnectionError):
        print 'request exception, proxy invalid. retry'
        return fetch_country_data(page, queue, retry+1)
        Proxy.del_proxy(proxy)

    if r.status_code != 200:
        print 'status code invalid'
        return fetch_country_data(page, queue, retry+1)
        Proxy.del_proxy(proxy)

    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.find('div', attrs={'id': 'results'})
    if not results:
        print 'proxy invalid'
        Proxy.del_proxy(proxy)
        return fetch_country_data(page, queue, retry + 1)

    countries = results.find_all('div')
    for country in countries:
        a = country.find('a')
        url = COUNTRY_URL + a.attrs['href']
        flag_url = COUNTRY_URL + a.find('img').attrs['src']
        name = country.text

        country = Country(name=name, url=url, flag_url=flag_url)
        try:
            country.save()
        except NotUniqueError:
            continue

        print name, url, flag_url

    pn = soup.find('div', attrs={'id': 'pagination'}).find_all('a')
    for i in pn:
        if i.text == 'Next >':
            # queue.put(i.attrs['href'])
            print 'put page: ', i.attrs['href']

def update_country(country):
    '''
    :param country: Country
    :return:
    '''
    if country.updated:
        print 'country already updated'
        return

    url = country.url
    proxy = Proxy.get_random_proxy()
    try:
        print 'fetch {} using proxy[{}]'.format(url, proxy)
        r = fetch(url, proxy)
    except (requests.Timeout, requests.ConnectionError, requests.exceptions.ReadTimeout):
        print 'request exception, proxy invalid. retry'
        return update_country(country)

    if r.status_code != 200:
        print 'status code invalid'
        return update_country(country)

    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table')

    d = {
        'area': int(re.search(r'([,\d]+)',
                                     table.find(id='places_area__row').find(class_='w2p_fw').text).group().replace(',', '')),
        'population': int(re.search(r'([,\d]+)',
                                     table.find(id='places_population__row').find(class_='w2p_fw').text).group().replace(',', '')),


        'iso' : table.find(id='places_iso__row').find(class_='w2p_fw').text,
        'capital' : table.find(id='places_capital__row').find(class_='w2p_fw').text,
        'continent' : table.find(id='places_continent__row').find(class_='w2p_fw').text,
        'tld' : table.find(id='places_tld__row').find(class_='w2p_fw').text,
        'currency_code' : table.find(id='places_currency_code__row').find(class_='w2p_fw').text,
        'currency_name' : table.find(id='places_currency_name__row').find(class_='w2p_fw').text,
        'phone' : table.find(id='places_phone__row').find(class_='w2p_fw').text,
        'postal_code_format' : table.find(id='places_postal_code_format__row').find(class_='w2p_fw').text,
        'postal_code_regex' : table.find(id='places_postal_code_regex__row').find(class_='w2p_fw').text,
        'languages' : table.find(id='places_languages__row').find(class_='w2p_fw').text,
        'neighbours' : table.find(id='places_neighbours__row').find(class_='w2p_fw').text,
        'updated': True,
    }

    for k,v in d.items():
        setattr(country, k, v)

    country.save()

    # save image
    save_flag(country.flag_url, proxy)

    print '{} updated'.format(country.name)

def update_country_with_pool():
    pool = Pool(10)
    pool.map(update_country, Country.objects.filter(updated=False))
    pool.close()
    pool.join()

def save_flag(url, proxy):
    dir = 'flags'
    fname = url.rsplit('/', 1)[1]
    save_file(url, dir, fname, proxy)

if __name__ == '__main__':

    # process()

    update_country_with_pool()
