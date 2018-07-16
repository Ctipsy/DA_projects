# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 15:04:06 2018

@author: C_tipsy
"""

import requests
import json
from requests.exceptions import RequestException
import re

def get_one_page(url):
    #需要加一个请求头部，不然会被网站封禁
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    try:       
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:  #任何异常都可以被捕捉到，不用区分特定的异常
        return None
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>'
                         +'(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?"integer">(.*?)</i>'
                         +'.*?fraction">(.*?)</i>.*?</dd>', re.S)  #加re.S那么符号.就可以匹配换行符了
    items = re.findall(pattern, html)
    #print(items)
    for item in items:
        yield
        {
        'index': item[0],
        'image': item[1],
        'title': item[2],
        'actor': item[3].strip()[3:],
        'time' : item[4].strip()[5:],
        'score': item[5]+item[6]                          
        }
    
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:  #追加存储形式，content是字典形式
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

    
def main():
    url = 'http://maoyan.com/board/4?'
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
    
    
if __name__ == "__main__":
    main()
    