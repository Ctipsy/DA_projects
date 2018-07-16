import requests
import json
from bs4 import BeautifulSoup
from urllib.request import urljoin
import collections
from pyecharts import Map

def get_view_history_link(search_word):
    """该函数用来获取历史编辑连接地址"""
    root_url = 'https://en.wikipedia.org'
    url = root_url + '/wiki/' + search_word
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    relavtiv_link = soup.find('li', {'id':'ca-history'}).span.a['href']
    return urljoin(root_url, relavtiv_link)

def get_ip(search_word):
    """该函数用来获取匿名修改的IP地址"""
    url = get_view_history_link(search_word)
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    page_500_link = urljoin('https://en.wikipedia.org', soup.find_all('a', {'class': 'mw-numlink'})[-1]['href'])
    soup = BeautifulSoup(requests.get(page_500_link).text, 'lxml')
    ips = soup.find_all('a', {'class': 'mw-anonuserlink'})
    set_ips = set()
    for ip in ips:
        set_ips.add(ip.text)
    return set_ips


def get_country(ip):
    """该函数用来获取ip所对应的国家"""
    try:
        res = requests.get('http://api.ipstack.com/' + ip + '?access_key=9f7745fbfbec55bd8d91dbab0f2ff3bd', verify=False)
    except:
        print('无效的ip地址')
    data_json = json.loads(res.text)
    country = data_json.get('country_name')
    return(ip, country)

def write_to_csv(word, source):
    with open(word+".csv", 'w', encoding='utf-8') as f:
        for i in source:
            f.write(str(i[0]))
            f.write(",")
            f.write(str(i[1])+'\n')
    f.close()

def draw_map(results, word):
    names = []
    values = []
    countrys = [i[1] for i in results]
    stats = collections.Counter(countrys)  # 统计来自各相同国家的IP地址数量
    datas = sorted(dict(stats).items(), key=lambda x: x[1], reverse=True)  # dict的排序方法
    write_to_csv(word + "_ip", results)   # 按【 原始IP：国家 】结果写入csv文件
    for each in datas:
        names.append(each[0])
        values.append(each[1])
    write_to_csv(word + "_order", datas)  # 按【 国家：数量 】 排序序后的结果写入csv文件

    word_map = Map("维基词条: "+word+" 各国编辑量统计", width=800, height=400)
    word_map.add("", names, values, maptype="world", is_visualmap=True,
                 is_piecewise=True, visual_text_color='#000', is_map_symbol_show=False,
                 pieces=[{"min": 25, "label": ">25"}, {"max": 25, "min": 15, "label": "15-25"}, {"max": 15, "min": 5, "label": "5-15"},
                        {"max": 5, "min": 2, "label": "2-5"},{"max": 1, "min": 0, "label": "<2"}], is_more_utils=True)
    file_name = word+"_chart.html"
    word_map.render(file_name)



def main(word):
    ips = get_ip(word)
    results = []
    for ip in ips:
        result = get_country(ip)
        results.append(result)
    draw_map(results, word)

if __name__ == '__main__':
    main("Artificial_intelligence")









