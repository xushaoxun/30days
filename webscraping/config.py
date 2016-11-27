# coding:utf-8


DB_HOST = 'localhost'
DB_PORT = 27017
DATABASE_NAME = 'webscraping'
DB_URI = 'mongodb://localhost:27017/webscraping'

TIMEOUT = 3
FAKE_DATA_FILE = 'fake_useragent_0.1.2.json'
PROXY_RE = r'\d+\.\d+\.\d+\.\d+:\d{2,4}'


PROXY_SITES = [
    'http://cn-proxy.com',
    'http://www.xicidaili.com',
    'http://www.kuaidaili.com/free',
    'http://www.proxylists.net/?HTTP',
    # www.youdaili.net的地址随着日期不断更新
    'http://www.youdaili.net/Daili/http/4565.html',
    'http://www.youdaili.net/Daili/http/4562.html',
    'http://www.kuaidaili.com',
    'http://proxy.mimvp.com',
    'http://api.xicidaili.com/free2016.txt',
]

REFERER_LIST = [
    'http://www.google.com/',
    'http://www.bing.com/',
    'http://www.baidu.com/',
]

COUNTRY_URL = 'http://example.webscraping.com'

if __name__ == '__main__':
    import re
    print re.findall(PROXY_RE, '1.1.22.0:56')