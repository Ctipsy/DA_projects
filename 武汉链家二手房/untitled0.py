# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 22:28:58 2018

@author: C_tipsy
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests


def generate_web_link(districts):
    '''
    此函数生成武汉地区所有区域二手房网页链接地址
    '''
    page_urls = [] 
    base_url = 'https://wh.lianjia.com/ershoufang/{}'
    for district in districts:
        district_url = base_url.format(district)
        res = requests.get(district_url).content.decode('utf-8')
        soup = BeautifulSoup(res,'lxml')
        totalpage = int(eval(soup.find('div',{'class':'page-box house-lst-page-box'})['page-data'])['totalPage'])#找出每个区域总共有多少页
        #eval函数将字符转化为表达式，find找出的内容是字符串形式的字典'{"totalPage":100,"curPage":1}'
        for page in range(1,totalpage+1):
            page_url = district_url + '/pg{}'.format(page)
            page_urls.append((district,page_url))
    return page_urls

def house_info_spider(page_links):
    district_dicts = {'jiangan':'江岸','jianghan':'江汉','qiaokou':'硚口',
                    'dongxihu':'东西湖','wuchang':'武昌','qingshan':'青山',
                    'hongshan':'洪山','hanyang': '汉阳','donghugaoxin':'东湖高新',
                    'jiangxia':'江夏'}
    infos = pd.DataFrame()
    for page_link in page_links:
        res = requests.get(page_link[1]).content.decode('utf-8')
        soup = BeautifulSoup(res,'lxml')
        house_infos = [i.text for i in soup.find_all('div',{'class':'houseInfo'})]
        floors = [i.text for i in soup.find_all('div',{'class':'positionInfo'})]
        total_prices = [i.text for i in soup.find_all('div',{'class':'totalPrice'})]
        unit_prices = [i.text for i in soup.find_all('div',{'class':'unitPrice'})]
        house_districts = [district_dicts[page_link[0]]]*len(house_infos)
        for house_info,floor,total_price,unit_price,district in zip(house_infos,floors,total_prices,unit_prices,house_districts):
            infos = infos.append([[house_info,floor,total_price,unit_price,district]])
    infos.columns = ['信息','楼层','售价','单价','地区']
    return infos

    #开始采集数据
if __name__ == '__main__':
    districts = ['jiangan','jianghan','qiaokou','dongxihu','wuchang','qingshan',
                 'hongshan','hanyang','donghugaoxin','jiangxia']
    page_links = generate_web_link(districts)
    house_datas = house_info_spider(page_links)

# house_datas = house_datas.reset_index(drop=True)
# house_datas.to_csv('lianjia_house.csv',index=False)     #数据保存到电脑
