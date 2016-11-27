# coding:utf-8

import requests, csv, re
from bs4 import BeautifulSoup


def remove_space(str):
    return re.sub(r'\s', '', str)

base_url = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc={loc}&start={start}'
loc = 'Ximending,Taipei,Taiwan'
start = 0


def save_data(url, loc, start):
    url = base_url.format(loc=loc, start=start)
    res = requests.get(url)
    status_code = res.status_code

    soup = BeautifulSoup(res.text, 'lxml')
    with open('loc-{}.csv'.format(loc), 'a') as f:
        csvf = csv.writer(f)

        for biz in soup.findAll('div', {'class', 'biz-listing-large'}):
            title = biz.findAll('a', {'class': 'biz-name'})[0]
            address = biz.findAll('address')[0]
            phone = biz.findAll('span', {'class': 'biz-phone'})[0]
            print(title.contents)
            # print(title.text, address.text.replace(' ', ''), phone.text.replace(' ', ''))
            csvf.writerow([remove_space(t) for t in [title.text, address.text, phone.text]])

if __name__ == '__main__':
    with open('loc-{}.csv'.format(loc), 'w') as f:
        csvf = csv.writer(f)
        csvf.writerow(['title', 'address', 'phone'])

    start = 0
    while start<11:
        save_data(base_url, loc, start)
        start += 10