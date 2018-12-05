import requests
import multiprocessing as mp
import json
import time
import random
from config import *
requests.packages.urllib3.disable_warnings()
def get_proxy():
    try:
        res = requests.get(proxy_pool_url)
        if res.status_code == 200:
            return res.text
        return None
    except ConnectionError:
        return None
def save_to_txt(results):
    with open('output54146yihou.txt','a') as f:
        for result in results:
            #result = json.dumps(result)
            if result:
                try:
                    f.write(str(result))
                    f.write('\n')
                    print('Successfully saved:',result)
                except UnicodeEncodeError:
                    print('UnicodeEncodeError:',result)
                    f.write('UnicodeEncodeError!\n')
        f.close()

def get_Info(tag_id,proxy='',try_times=1):
    if tag_id % 2 == 1:
        return 'No Tag'
    if try_times >= 3 :
        print('Fail to crawl,tag_id=',tag_id)
        return None
    try:
        url = 'http://api.bilibili.com/x/tag/info?&tag_id={}'.format(tag_id)
        headers['User-Agent']=random.choice(user_agent_list)
        if enable_proxy:
            res = requests.get(url,headers=headers,verify=False,proxies={'http':'http://'+proxy},timeout=6)
        else:
            res = requests.get(url,headers=headers,verify=False,timeout=6)
        time.sleep(TIME_SLEEP)
        if res.status_code == 200:
            data = json.loads(res.text)
            print(tag_id)
            if 'data' in data.keys():
                return {
                    'tag_id': tag_id,
                    'tag_name': data["data"]["tag_name"],
                    'atten': data["data"]["count"]["atten"],
                    'use': data["data"]["count"]["use"]
                }
            else: return 'No Tag'
        if res.status_code == 403:
            #proxy = get_proxy()
            #p = get_proxy()
            #print('Using proxy:', p)
            print('403')
            return get_Info(tag_id,proxy,try_times+1)
    except Exception as e:
        #p = get_proxy()
        #print('Using proxy:', p)
        #time.sleep(0.5)
        print(e)
        return get_Info(tag_id,proxy,try_times+1)

def main(args):
    result = get_Info(args)
    if result:
        return result
    else:
        print('Fail to get Info:',args)
        return None

def crawl(begin,end):
    pool = mp.Pool()
    for i in range(begin, end):
        begin = time.time()
        step = 100
        # proxy = get_proxy()
        # print(proxy)
        # proxy = random.choice(ips)
        # proxy = ''
        # args = [[tag_id,proxy] for tag_id in range(i*step+1,(i+1)*step+1)]
        results = pool.map(main, range(i * step + 1, (i + 1) * step + 1))
        # with futures.ThreadPoolExecutor(64) as executor:
        # results = executor.map(main,args)
        for result in results:
            if not result:
                print('403 Error, Please wait 20 minutes!')
                return i,False
        save_to_txt(results)
        time.sleep(1.05)
        print('{0}-{1} Finished, Time used:{2}'.format(i * step + 1, (i + 1) * step, time.time() - begin))
    return end,True

if __name__ == '__main__':
    finished = False
    begin = BEGIN
    end = END
    now = begin
    while not finished:
        now,finished = crawl(now,end)
        if not finished:
            for i in range(1,20):
                time.sleep(60)
                print(str(20-i)+' minutes left...')