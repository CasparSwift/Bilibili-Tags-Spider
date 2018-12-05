from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import multiprocessing as mp
from config import *
import re
import requests
import time

def get_proxy():
    try:
        res = requests.get(proxy_pool_url)
        if res.status_code == 200:
            return res.text
        return None
    except ConnectionError:
        return None

option = Options()
option.add_argument('-headless')
browser = webdriver.Chrome(chrome_options=option)
wait = WebDriverWait(browser,2.5)
def get_info(tag_number,try_times=1):
    if try_times >= 5:
        print('该页面无法爬取')
        return None
    try:
        print('正在爬取...')
        #option.add_argument('--proxy-server=http://{}'.format(get_proxy()))
        browser.get('https://www.bilibili.com/tag/{}/'.format(tag_number))
        title = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,'#app > div.top-header > div > div.top-contain > div.top-title > div.top-text')
        ))
        follow_number_tag = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,'#app > div.top-header > div > div.top-contain > div.top-title > div.concern-num')
        ))
        follow_number=str(re.search('(.*?)人已关注',follow_number_tag.text).group(1))
        if '万' in follow_number:
            follow_number = int(float(follow_number.replace('万',''))*10000)
        else: follow_number = int(follow_number)
        data = {
            'tag_number': tag_number,
            'follow_number': follow_number
        }
        print(data)
        return data
    except TimeoutException:
        try_times += 1
        return get_info(tag_number,try_times)

if __name__ == '__main__':
    pool = mp.Pool()
    pool.map(get_info,range(76000,77000))
    #for i in range(1,10000):
        #print(get_info(i))
        #time.sleep(0.5)
