import requests
import multiprocessing as mp
import json
import pymongo
import time
from config import *
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

proxy = ''
requests.packages.urllib3.disable_warnings()
fails = []
def get_proxy():
    try:
        res = requests.get(proxy_pool_url)
        if res.status_code == 200:
            return res.text
        return None
    except ConnectionError:
        return None

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print("Successfully saved:",result)
    else:
        print("Failed to save:",result)

def get_Info(tag_id,try_times=1):
    global proxy
    if tag_id == 0:
        return None
    if try_times >=5 :
        print('Fail to crawl,tag_id=',tag_id)
        return None
    try:
        url = 'https://api.bilibili.com/x/tag/info?&tag_id={}'.format(tag_id)
        proxies = {
            'https': 'https://' + proxy
        }
        res = requests.get(url,headers=headers,proxies=proxies,verify=False,timeout=20)
        if res.status_code == 200:
            data = json.loads(res.text)
            if data and 'data' in data.keys():
                return {
                    'tag_id': tag_id,
                    'tag_name': data.get('data').get('tag_name'),
                    'atten': data.get('data').get('count').get('atten'),
                    'use': data.get('data').get('count').get('use')
                }
            else:
                proxy = get_proxy()
                print('Using proxy:',proxy)
                #time.sleep(0.5)
                return get_Info(tag_id,try_times+1)
        else:
            proxy = get_proxy()
            print('Using proxy:', proxy)
            #time.sleep(0.5)
            return get_Info(tag_id,try_times+1)
    except:
        proxy = get_proxy()
        print('Using proxy:', proxy)
        #time.sleep(0.5)
        return get_Info(tag_id,try_times+1)

def main(tag_id):
    #time.sleep(0.5)
    global fails
    result = get_Info(tag_id)
    if result:
        save_to_mongo(result)
    else:
        print('Fail to get Info:',tag_id)
        fails.append(tag_id)

if __name__ == '__main__':
    for i in range(17,21):
        begin = time.clock()
        proxy = get_proxy()
        pool = mp.Pool()
        pool.map(main,range((i-1)*1000,i*1000))
        print('{0}-{1} Finished, Time used:{2}'.format((i-1)*1000,i*1000-1,time.clock()-begin))
        print(fails)


