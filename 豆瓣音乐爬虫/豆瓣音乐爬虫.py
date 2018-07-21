# !/usr/bin/env python3
# -*- coding:utf-8-*-
# 参考文献链接：https://mp.weixin.qq.com/s/_WpjpY0mgr1_5kPGM26WfA
# 导入需要使用的库
import requests
import re
from urllib import request
from bs4 import BeautifulSoup as bs
import requests
import json
import time
import random

# 随机生成user-agent
def process_request():
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",]
    user_header=random.choice(USER_AGENTS)

    return user_header
# 输入需要获取的页数和风格
def main():
    user_header = process_request()
    search_keywords = input('please input your search_keywords:')
    user_in_nub = input('please input your pages:')
    for i in generate_allurl(user_in_nub,search_keywords,user_header):
        # print(i)
        ls_url =  get_allurl(i,user_header)
        for j in ls_url:
            info_text = open_url(j,user_header)
            writer_to_text(info_text)


# 构建url
def generate_allurl(user_in_nub,search_keywords,user_header):
    # 最外页网址
    url1 = "https://music.douban.com/tag/"
    header ={
        "Host":"music.douban.com",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":user_header
    }
    time.sleep(5)
    get_url = requests.get(url1,headers = header)
    soup = bs(get_url.content,'lxml')
    j = 0
    info = {}

    for i in range(0,len(soup.select('table.tagCol'))):
        x=soup.select('table.tagCol')[i]
        for q in range (0,len(x.select('tbody tr td a'))):
            lsdirx =str(i) + str(q)
            info[lsdirx] = x.select('tbody tr td a')[q].text
            a = list(info.values())
    # print(a)

    # print(search_keywords)
    url = "https://music.douban.com/tag/" + search_keywords + "?start={}&type=T"
    # print(url)
    # url = 'https://music.douban.com/tag/OST?start={}&type=T'
    next_page = int(user_in_nub)*20
    for url_next in range(0,next_page,20):
        # url_next =url_next + 20
        yield url.format(url_next)



# 正则匹配链接url
def get_allurl(generate_allurl,user_header):
    header ={
        "Host":"music.douban.com",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":user_header
    }
    time.sleep(5)
    get_url = requests.get(generate_allurl,headers = header)

    if get_url.status_code == 200:
        re_set = re.compile('<a.*?class="nbg".*?href="(.*?)"')
        re_get = re.findall(re_set,get_url.text)
        return re_get
        # print(get_url.text)
        # print(re_get)


# 获取所需要的信息
def open_url(re_get,user_header):
    header ={
        "Host":"music.douban.com",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":user_header
    }
    time.sleep(5)
    res = requests.get(re_get,headers = header)

    if res.status_code == 200:
        info = {'歌名': '', '其他属性': '', '评分': '', '评价人数': '', '推荐常用标签': '', '推荐歌手': '','推荐歌曲':''}
        soup = bs(res.text, 'lxml')
        if (soup.select('#wrapper h1 span')):
            info['歌名'] = str(soup.select('#wrapper h1 span')[0].text)
        if(soup.select('div#info')):
            info['其他属性'] = str(soup.select('div#info')[0].text).split("\n")
        if(soup.select('strong.ll.rating_num')):
            info['评分'] = str(soup.select('strong.ll.rating_num')[0].text)
        if (soup.select('.rating_people span')):
            info['评价人数'] = str(soup.select('.rating_people span')[0].text)
            # info['评价人数'] = str(soup.select('.rating_people span')[0].text)
        if (soup.select('.tags-body')):
            info["推荐常用标签"] = soup.select('.tags-body')[0].text.split("\n")
        if (soup.select('div#db-rec-artist-section div.content.clearfix dl.subject-rec-list dd a') != None):

        #    print(len(soup.select('.content.clearfix .subject-rec-list dd a')))
            j = 0
            for i in soup.select('div#db-rec-artist-section div.content.clearfix dl.subject-rec-list dd a'):
                lsdir = str('推荐歌手' + str(j))
                info[lsdir] = soup.select('div#db-rec-artist-section div.content.clearfix dl.subject-rec-list dd a')[j].text
                j += 1

        if (soup.select('div#db-rec-section div dl dd a') != None):

            #    print(len(soup.select('.content.clearfix .subject-rec-list dd a')))
            j = 0
            for i in soup.select('div#db-rec-section div dl dd a'):
                lsdir = str('推荐歌曲' + str(j))
                info[lsdir] = soup.select('div#db-rec-section div dl dd a')[j].text
                j += 1

        return info


def writer_to_text(text):  # 储存到text
    with open('豆瓣音乐.txt', 'a', encoding='utf-8')as f:
         f.write(json.dumps(text, ensure_ascii=False) + '\n')
         f.close()

if __name__ == '__main__':
    main()