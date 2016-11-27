# coding:utf-8
import urllib, urlparse, requests
import utils, json
from models import Proxy
from config import TIMEOUT, COMMENT_JS_URL
from simplejson.scanner import JSONDecodeError
import simplejson

def gen_js_url(url):
    query_dict = urlparse.parse_qs(urlparse.urlsplit(url).query)
    query_dict = {k: v[0] for k, v in query_dict.items()}
    query_dict.update({
        'uin': '',
        'key': '',
        'pass_ticket': '',
        'wxtoken': '',
        'devicetype': '',
        'clientversion': 0,
        'x5': 0
    })

    return '{}?{}'.format(COMMENT_JS_URL, urllib.urlencode(query_dict))

def fetch(url):
    s = requests.Session()
    s.headers.update({'user-agent': utils.get_user_agent()})
    proxies = {
        'http': Proxy.get_random_proxy()['address'],
    }

    html_text = s.get(url, timeout=TIMEOUT, proxies=proxies)
    js_url = gen_js_url(url)

    js_data = s.get(js_url, timeout=TIMEOUT, proxies=proxies)
    # try:
    #     js_data = s.get(js_url, timeout=TIMEOUT, proxies=proxies).json()
    # except JSONDecodeError:
    #     raise requests.RequestException

    return html_text, js_data

if __name__ == '__main__':

    url = 'http://mp.weixin.qq.com/s?src=3&timestamp=1480133089&ver=1&signature=at24GKibwNNoE9VsETitURyMHzXYeytp1MoUyAFx-2XgIFa3OneSFrKV6rNwLaI5ADq7SRWO-2BXF6KtlEw3vwdJDAMyg9U4Fq72eFa3zsSsZs5i5rGT0*04nIiAHcW6ckSndyZ5gYyj91sZOakctnEzoBJuzUA1uKP2IIxQUF4='
    html, js = fetch(url)
    print html.text
    j = '{"comment": 1}'
    print j
    # j = '{"a":1}'
    print simplejson.loads(j)
    # print json.loads(j)
