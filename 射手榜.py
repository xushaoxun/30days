# coding:utf-8
import requests, csv
from bs4 import BeautifulSoup
from selenium import webdriver

BASE_URL = 'http://soccer.stats.qq.com/goals.htm?type={}'
TYPES = {
    'yingchao':'英超',
    'xijia':'西甲',
    'yijia':'意甲',
    'dejia':'德甲',
    'fajia':'法甲',
    'zhongchao':'中超'
}

fields = ['联赛','排序','球员','球队','进球（点球）']



def save_data(league):
    url = BASE_URL.format(league)
    league_cn = TYPES[league]
    print('get [{}] {}'.format(league_cn, url))

    # driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    div = soup.find('div', attrs={'class':'jf-tab-con ssb-tab-con'})

    f = open('射手榜.csv', 'a')
    writer = csv.writer(f)

    all_trs = div.select('tbody tr')
    for tr in all_trs:
        num = tr.select('td.td-num span')[0].text
        player = tr.select('td.td-player a')[0].text
        team = tr.select('td.td-team a')[0].text
        goals = tr.select('td:nth-of-type(4)')[0].text

        row = [league_cn, num, player, team, goals]
        print(row)
        writer.writerow(row)

    f.close()
    print('end [{}]'.format(league_cn))

if __name__ == '__main__':
    with open('射手榜.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

    for league in TYPES:
        save_data(league)
