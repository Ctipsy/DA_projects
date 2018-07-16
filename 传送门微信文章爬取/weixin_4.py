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
import os
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

def mkdir(offset):
    path = os.getcwd()+'\\'+ str(offset)
    isExists = os.path.exists(path)
    path_csv = path +'\\'+ str(offset)+'.csv' 
    if not isExists:
        os.makedirs(path)  
        with open(path_csv, 'w', encoding='utf-8') as f: 
            f.write('链接,标题,日期' + '\n')  #注意，此处的逗号，应为英文格式
            f.close()        
    else:
        print("已创建公众号对应的文件夹")        
    return path
    
def write_to_file(content, offset):
    path = mkdir(offset) +'\\'+ str(offset)+'.csv'    
    with open(path, 'a', encoding='utf-8') as f:  #追加存储形式，content是字典形式
        f.write(str(json.dumps(content, ensure_ascii=False).strip('\'\"') + '\n'))  #在写入
        f.close()
        
        

def parse_one_page(html):
    pattern = re.compile('<div class="feed_item_question">.*?<span>.*?<a class="question_link" href="(.*?)".*?_blank">(.*?)</a>.*?"timestamp".*?">(.*?)</span>', re.S)
    items = re.findall(pattern, html)      
    return items
    
def main(offset, i):    
    url = 'http://chuansong.me/account/' + str(offset) + '?start=' + str(12*i)
    print(url)
    wait = round(random.uniform(1,2),2) # 设置随机爬虫间隔，避免被封
    time.sleep(wait)    
    html = get_one_page(url)    
    for item in parse_one_page(html):
        info = 'http://chuansong.me'+item[0]+','+ item[1]+','+item[2]+'\n'
        info = repr(info.replace('\n', ''))
        print(info)
        #info.strip('\"')  #这种去不掉首尾的“        
        #info = info[1:-1]  #这种去不掉首尾的“ 
        #info.Trim("".ToCharArray())
        #info.TrimStart('\"').TrimEnd('\"')
        write_to_file(info, offset)        
    
    
if __name__ == "__main__":
#    for i in range(35):
#        main('wzdata', i)
        
#    for i in range(35):
#        main('wzdata', i)
  
#    for i in range(147):
#        main('ecshujufenxi', i)  
#        
#     for i in range(94):
#         main('sjfxjx', i)   
 

#    for i in range(71):
#        main('DataScienceWeMedia', i)
        
#    for i in range(14):
#        main('metrodatateam', i)  
        
#    for i in range(97):
#        main('datadw', i) 
    for i in range(168):
        main('datakong', i)
        

        
    