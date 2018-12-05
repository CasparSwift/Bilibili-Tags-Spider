import re
import requests
from bs4 import BeautifulSoup as bs
from config import *
proxy = None
def get_proxy():
    try:
        res = requests.get(proxy_pool_url)
        if res.status_code == 200:
            return res.text
        return None
    except ConnectionError:
        return None

def get_html(tag_number,try_time=1):
    if try_time >= 5:
        print('Failed to Crawl')
        return None
    try:
        proxies = {
            'http': 'http://'+get_proxy()
        }
        res = requests.get('https://www.bilibili.com/tag/{}/'.format(tag_number),proxies=proxies)
        if res.status_code == 200:
            return res.text
        else:
            return get_html(tag_number,try_time+1)
    except ConnectionError:
        return get_html(tag_number,try_time+1)

if __name__ == '__main__':
    for i in range(5):
        html = get_html(i)
        if not html: continue
        soup = bs(get_html(i),'lxml')
        title = soup.select('#app > div.top-header > div > div.top-contain > div.top-title > div.top-text')[0].string
        follow_number_tag = soup.select('#app > div.top-header > div > div.top-contain > div.top-title > div.concern-num')
        follow_number = str(re.search('(.*?)人已关注', follow_number_tag[0].string).group(1))
        if '万' in follow_number:
            follow_number = int(float(follow_number.replace('万', '')) * 10000)
        else:
            follow_number = int(follow_number)
        data = {
            'tag_number': i,
            'title': title,
            'follow_number': follow_number
        }
        print(data)
