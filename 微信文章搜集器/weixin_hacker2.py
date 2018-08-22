# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 22:33:09 2018

@author: C_tipsy  
@location: WuHan_HUST NanYi Building
"""

import requests
from requests.exceptions import RequestException
import re
import time
import json
import random
import os



global count;
count=0;
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
    global count;
    path = os.getcwd()+'\\'+ str(offset)
    isExists = os.path.exists(path)
    path_csv = path +'\\'+ str(offset)+'.csv' 
    if not isExists:
        os.makedirs(path)  
        with open(path_csv, 'w', encoding='utf-8') as f: 
            f.write('链接,标题,日期' + '\n')  #注意，此处的逗号，应为英文格式
            f.close()        
    else:
        count+=1
        print("已下载链接数：",count)        
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
    
def judge_info(name):
    url = 'http://chuansong.me/account/' + str(name) + '?start=' + str(0)    
    wait = round(random.uniform(1,2),2) # 设置随机爬虫间隔，避免被封
    time.sleep(wait)    
    html = get_one_page(url) 
    
    pattern1 = re.compile('<h1>(Page Not Found.|该帐号还未审核或未审核通过。)</h1>', re.S)
    
    item1 = re.findall(pattern1, html)  # list类型
    
    pattern2 = re.compile('<a href="/account/.*?">(.\d+)</a>(\s*)</span>(\s*?)<a href="/account/.*" style="float: right">下一页</a>')
    item2 = re.findall(pattern2, html)  # list类型  
    
    if item1:
        print("\n---------该账号信息尚未收录--------\n") 
        name = input("\n---------退出请按y，继续请按m--------\n")
        if(name=='y'):
            exit();
        else:
            return 0;           
    else:
        print("\n---------该公众号目前已收录文章页数N为：",item2[0][0])
        return 1;

    
def main(offset, i):    
    url = 'http://chuansong.me/account/' + str(offset) + '?start=' + str(12*i)
    #print(url)
    wait = round(random.uniform(1,2),2) # 设置随机爬虫间隔，避免被封
    time.sleep(wait)    
    html = get_one_page(url)    
    for item in parse_one_page(html):
        info = 'http://chuansong.me'+item[0]+','+ item[1]+','+item[2]+'\n'
        info = repr(info.replace('\n', ''))
        write_to_file(info, offset)        
    
    
if __name__ == "__main__":
    print("\n说明：最便捷的微信文章下载器V1.0\n"
                     "\nAuthor:Ctipsy\n")
    while(1):            
        name = input("请输入公众号名称：")
        flag = judge_info(name);
        if flag: 
            pages = input("\n请输入需要抓取的文章页数(<N):")
            for i in range(int(pages)):
                main(name, i)
            print("\n---------已完成下载任务--------\n") 
            signal = input("\n---------退出请按y，下载其他公众号请按m--------\n")
            if(signal=='y'):
                break;
        

        
    