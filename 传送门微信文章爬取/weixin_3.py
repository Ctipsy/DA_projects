# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 22:57:04 2018

@author: C_tipsy
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 22:33:09 2018

@author: C_tipsy
"""

import requests
from requests.exceptions import RequestException
import re
import time
import json
import random
def get_one_page(url):
    #需要加一个请求头部，不然会被网站封禁
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    try:       
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status #若不为200，则引发HTTPError错误
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return "产生异常"

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:  #追加存储形式，content是字典形式
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

def parse_one_page(html):
    pattern = re.compile('<div class="feed_item_question">.*?<span>.*?<a class="question_link" href="(.*?)".*?_blank">(.*?)</a>.*?"timestamp".*?">(.*?)</span>', re.S)
    items = re.findall(pattern, html)      
    return items
    
def main(offset, i):    
    url = 'http://chuansong.me/account/' + str(offset) + '?start=' + str(12*i)
    print(url)
    wait = round(random.uniform(1,2),2)
    time.sleep(wait)
    
    html = get_one_page(url)    
    for item in parse_one_page(html):
        info = 'http://chuansong.me'+item[0]+','+ item[1]+','+item[2]+'\n'
        info = info.replace('\n', '') 
        info.strip('\"')
        write_to_file(info)        
    
    
if __name__ == "__main__":
    for i in range(160, 167):
        main('datakong', i)
    