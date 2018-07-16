# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 22:33:09 2018
通过读取爬取的公众号文章，获取链接，然后打开网页，获取html
去除非法命名字符，以文章标题命名保存的html
直接将请求获得的html代码，转换为pdf
@author: C_tipsy
"""


import pdfkit
import os
import pandas as pd
import time
import requests
import random
import re

def get_url_info(offset):
   path = get_path(offset)
   if path == "":
       print("缺少爬虫信息文件")
       return 
   else:
       print(path+'\\'+str(offset)+'.csv')
       file = open(path+'\\'+str(offset)+'.csv', encoding='utf-8') #如果路径中带有中文，则先open然后read，不然会报错
       data = pd.read_csv(file)       
       return data
 


def get_page(url):
    #需要加一个请求头部，不然会被网站封禁
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
    try:       
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status #若不为200，则引发HTTPError错误
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return "网页请求失败"

def get_path(offset):
    path = os.getcwd()+'\\'+str(offset)
    isExists = os.path.exists(path)
    if not isExists:
        print("还未爬取该公众号文章数据，请先爬取")
        return ""
    else: 
        return path    
    
    
def html_to_pdf(offset):
    wait = round(random.uniform(1,2),2) # 设置随机爬虫间隔，避免被封
    time.sleep(wait) 
    path = get_path(offset)
    if path == "" :
        print("尚未抓取该公众号")
    else:        
        info = get_url_info(offset)               
        for indexs in info.index:  
            url = info.loc[indexs]['链接']
            title = re.sub('[\\\\/:*?\"<>|]', '', info.loc[indexs]['标题'])
            date = info.loc[indexs]['日期']
            path_tmp = path + '//'+title+'.html'
            msg = get_page(url)            
            file = open(path_tmp, 'w', encoding='utf-8')
            file.write(msg)
            file.close
            path_wk = r'D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf = path_wk)
            pdfkit.from_string(msg, get_path(offset)+'\\'+ date+'_'+title+'.pdf', configuration=config)    

#def main(offset):
    
    
if __name__ == "__main__":    
    html_to_pdf('demo')
    



    