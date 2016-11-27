# coding:utf-8

from datetime import datetime
from requests.exceptions import Timeout, ConnectionError
from gevent import monkey, GreenletExit
from gevent.queue import Queue, Empty
from gevent.pool import Pool
from time import sleep
monkey.patch_all()
from pymongo.errors import InvalidBSON
from mongoengine import NotUniqueError, DoesNotExist
from bs4 import BeautifulSoup

from utils import fetch
from models import Proxy, Article, Publisher

SEARCH_URL = 'http://weixin.sogou.com/weixin?query={}&type=2&page={}'
SEARCH_TEXT = 'Python'


def save_search_result(page, queue, retry=0):
    if retry > 5:
        print 'retry>5'
        queue.put(page)
        raise GreenletExit()

    proxy = Proxy.get_random_proxy()['address']
    url = SEARCH_URL.format(SEARCH_TEXT, page)
    print 'save_search_result {} with proxy:{}'.format(url, proxy)
    try:
        cookies = {
            'SUV':'0',
            'SNUID':'34F2F7C2BFBAFD9FDEC4161FBFDBAF1A',
        }
        r = fetch(url, proxy=proxy, cookies=cookies)
        print r.status_code
    except (Timeout, ConnectionError):
        print 'Proxy timeout'
        p = Proxy.del_proxy(proxy)
        sleep(0.1)
        retry += 1
        return save_search_result(page, queue, retry)

    print 'return status=', r.status_code
    if r.status_code != 200:
        p = Proxy.del_proxy(proxy)
        sleep(0.1)
        retry += 1
        return save_search_result(page, queue, retry)

    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.find('div', class_='news-box')

    if results is None:
        print 'proxy is blocked'
        p = Proxy.del_proxy(proxy)
        #代理被封
        sleep(0.1)
        retry += 1
        return save_search_result(page, queue, retry)

    articles = results.find_all('li')
    print 'articles=', len(articles)

    for article in articles:
        save_article(article)


def save_article(article):
    try:
        img_url = article.find(class_='img-box').find('img').attrs['src'].split('url=')[1]
    except:
        print 'no img_url'
        return
    text_box = article.find(class_='txt-box')
    title = text_box.find('h3').find('a').text
    article_url = text_box.find('h3').find('a').attrs['href']
    summary = text_box.find('p').text
    create_at = datetime.fromtimestamp(float(
        text_box.find(class_='s-p').attrs['t']
    ))
    publisher_name = text_box.find(class_='s-p').find('a').text

    article = Article(img_url=img_url, title=title, url=article_url,
                      summary=summary, create_at=create_at,
                      publisher=Publisher.get_or_create(publisher_name))
    try:
        article.save()
        print 'article saved'
    except (NotUniqueError, InvalidBSON):
        pass

def save_search_result_with_queue(queue):
    while True:
        try:
            p = queue.get(timeout=0)
        except Empty:
            break

        save_search_result(p, queue)
    print 'stopping crawler....'


def use_gevent_with_queue():
    queue = Queue()
    pool = Pool(5)

    for p in range(1, 10):
        queue.put(p)

    while pool.free_count():
        pool.spawn(save_search_result_with_queue, queue)

    pool.join()


if __name__ == '__main__':
    use_gevent_with_queue()

    # url = 'http://weixin.sogou.com/weixin?query=Python&type=2&page=1'
    # url = 'http://weixin.sogou.com/weixin?oq=&query=Python&_sug_type_=1&sut=0&lkt=0%2C0%2C0&ri=1&_sug_=n&type=2&sst0=1480083181477&page=2&ie=utf8&p=40040108&dp=1&w=01015002&dr=1'
    # cookies = {
    #     'SUV': '0',
    #     'SNUID': '34F2F7C2BFBAFD9FDEC4161FBFDBAF1A',
    # }
    # r = fetch(url, cookies=cookies)
    # print r.text

    # url = 'http://weixin.sogou.com/weixin?oq=&query=Python&_sug_type_=1&sut=0&lkt=0%2C0%2C0&ri=1&_sug_=n&type=2&sst0=1480083181477&page=2&ie=utf8&p=40040108&dp=1&w=01015002&dr=1'
    # # url = 'http://httpbin.org/get'
    # # url = 'http://www.phei.com.cn/'
    # # necessary cookies
    # cookies = {
    #     'SUV':'0',
    #     'SNUID':'34F2F7C2BFBAFD9FDEC4161FBFDBAF1A',
    # }
    # r = fetch(url, cookies=cookies)
    # print r.text
