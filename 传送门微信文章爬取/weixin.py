import requests
from requests.exceptions import RequestException
import re
import time
import json
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
    #pattern = re.compile('<title>(.*?)</title>', re.S)
    items = re.findall(pattern, html)      
    for item in items:
        print("找到关键字")
        print(item)
        yield
        {
        'link': 'http://chuansong.me'+item[0],
        'title': item[1],
        'time': item[2]                         
        }
    
def main(offset, i):    
#    url = 'http://chuansong.me/account/' + str(offset) + '?start=' + str(12*i)
#    print(url)
#    time.sleep(8)
#    html = get_one_page(url)
#    print(html)
#    for item in parse_one_page(html):
#        print(item)
    url = 'http://chuansong.me/account/' + str(offset) + '?start=' + str(12*i)
    #print(url)    
    html = open('html.txt', 'r', encoding='utf-8')
    for item4 in parse_one_page(html.read()):
        print(item4)
    #write_to_file(item4)        
    html.close()
    
if __name__ == "__main__":
    for i in range(1):
        main('almosthuman2014', i)
    