# import requests
# import re
# import json
# from bs4 import BeautifulSoup
# from urllib.request import urljoin
# import collections
# from pyecharts import Map
#
# def get_view_history_link(search_word):
#     "该函数用来获取历史编辑连接地址"
#     root_url = 'https://en.wikipedia.org'
#     url = root_url + '/wiki/' + search_word
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#                              '(KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
#     res = requests.get(url, headers=headers)
#     soup = BeautifulSoup(res.text, 'lxml')
#     relavtiv_link = soup.find('li', {'id':'ca-history'}).span.a['href']
#     return urljoin(root_url, relavtiv_link)
#
# def get_ip(search_word):
#     """该函数用来获取匿名修改的IP地址"""
#     url = get_view_history_link(search_word)
#     soup = BeautifulSoup(requests.get(url).text,'lxml')
#     page_500_link = urljoin('https://en.wikipedia.org',soup.find_all('a',{'class':'mw-numlink'})[-1]['href'])
#     soup = BeautifulSoup(requests.get(page_500_link).text,'lxml')
#     ips = soup.find_all('a',{'class':'mw-anonuserlink'})
#     set_ips = set()
#     for ip in ips:
#         set_ips.add(ip.text)
#     return set_ips
#
#
# def get_country(ip):
#     '该函数用来获取ip所对应的国家'
#     try:
#         res = requests.get('http://api.ipstack.com/' + ip + '?access_key=9f7745fbfbec55bd8d91dbab0f2ff3bd', verify=False)
#     except:
#         print('无效的ip地址')
#     data_json = json.loads(res.text)
#     country = data_json.get('country_name')
#     return(ip, country)
#
#
#
#
# def draw_map(results):
#     # 转换国家中英文名称
#     tmp = results
#     country_ab = {}
#     names = []
#     values = []
#     f = open(r'E:\CZK\工作\数据分析\我的练习项目\维基百科词条编辑\国家.txt', 'r', encoding='UTF-8')
#     for line in f:
#         if len(line) > 1:
#             country_ab[re.findall('(.*?):', line)[0]] = ' '.join(re.findall('[\u4e00-\u9fa5]+', line))
# #             country_ab[re.findall('[a-zA-Z]+', line)[0]] = ' '.join(re.findall('[a-zA-Z]+', line)[1:])
#     f.close()
#     countrys = []
#     countrys = [i[1] for i in results]
#     stats = []
#     stats = collections.Counter(countrys)
#     for each in stats.items():
#         (name, value) = each
#         names.append(name)
#         value.append(value)
#
#     word_map = Map("维基词条编辑每个国家贡献", width=800, height=400)
#     word_map.add("", names, values, maptype="world", is_visualmap=True,
#                  is_piecewise=True, visual_text_color='#000', is_map_symbol_show=False,
#                  pieces=[{"max": 25, "min": 25, "label": "25"}, {"max": 24, "min": 10, "label": "24-10"},
#                         {"max": 10, "min": 0, "label": "<10"}])
#
#
# if __name__ == '__main__':
#     ips = get_ip('Python_(programming_language)')
#     results = []
#     for ip in ips:
#         result = get_country(ip)
#         results.append(result)
#     draw_map(results)



# import collections
# from pyecharts import Map
# import re
# #转换国家中英文名称
# results = [('50.53.1.33', 'United States'), ('27.7.33.30', 'India'), ('8.37.96.36', 'United States'), ('50.109.75.78', 'United States'), ('90.221.222.69', 'United Kingdom'), ('37.39.199.13', 'Kuwait'), ('119.235.50.170', 'India'), ('37.106.181.109', 'Saudi Arabia'), ('134.193.238.227', 'United States'), ('2405:204:1389:e5c2:8c1c:39fc:8605:a898', 'India'), ('41.239.21.3', 'Egypt'), ('192.54.144.229', 'France'), ('68.57.254.129', 'United States'), ('216.80.103.176', 'United States'), ('49.205.216.210', 'India'), ('62.255.128.67', 'United Kingdom'), ('111.92.46.179', 'India'), ('2.218.17.222', 'United Kingdom'), ('117.224.233.3', 'India'), ('1.22.102.23', 'India'), ('183.82.37.234', 'India'), ('2602:306:3796:abd0:bc72:1033:4871:7dd1', 'United States'), ('2405:204:d087:d48e:d4ba:1788:612f:977c', 'India'), ('85.86.231.102', 'Spain'), ('77.131.79.194', 'France'), ('46.188.158.93', 'Croatia'), ('27.154.219.75', 'China'), ('220.227.205.189', 'India'), ('2003:c3:5f14:4d00:adf2:9703:2ef2:a770', 'Germany'), ('85.193.242.133', 'Poland'), ('70.184.214.35', 'United States'), ('24.142.209.86', 'United States'), ('73.162.65.52', 'United States'), ('70.24.205.94', 'Canada'), ('103.15.62.18', 'India'), ('76.14.39.29', 'United States'), ('134.193.69.220', 'United States'), ('85.56.120.25', 'Spain'), ('71.242.244.146', 'United States'), ('112.134.39.136', 'Sri Lanka'), ('2600:8800:7b01:880:7850:da8d:4342:7bc6', 'United States'), ('62.203.35.109', 'Switzerland'), ('141.131.2.3', 'United States'), ('114.29.237.80', 'India'), ('108.179.38.243', 'United States'), ('2601:183:847f:e15b:f841:b4fd:f8bc:e57', 'United States'), ('27.106.92.189', 'India'), ('106.51.26.242', 'India'), ('131.152.137.48', 'Switzerland'), ('98.65.194.191', 'United States'), ('187.189.102.199', 'Mexico'), ('176.51.204.190', 'Russia'), ('81.247.46.88', 'Belgium'), ('154.122.62.116', 'Kenya'), ('105.151.170.37', 'Morocco'), ('188.23.105.235', 'Austria'), ('81.106.240.17', 'United Kingdom'), ('2600:100d:b00d:9e44:2165:cd79:1ed3:7d18', 'United States'), ('115.114.50.215', 'India'), ('213.97.248.159', 'Spain'), ('85.92.160.163', 'United Kingdom'), ('2001:630:212:de0:583e:6fad:64ad:886a', 'United Kingdom'), ('130.92.255.36', 'Switzerland'), ('47.8.142.195', 'India'), ('78.48.131.210', 'Germany'), ('95.172.232.240', 'United Kingdom'), ('50.53.1.21', 'United States'), ('203.163.252.26', 'India'), ('220.94.163.15', 'Republic of Korea'), ('85.255.237.147', 'United Kingdom'), ('160.127.15.38', 'United States'), ('103.16.71.19', 'India'), ('87.66.197.101', 'Belgium'), ('192.140.221.149', 'India'), ('2001:5b0:4ec5:4608:d982:b293:4e60:af15', 'United States'), ('187.189.246.28', 'Mexico'), ('77.65.100.186', 'Poland'), ('182.65.122.82', 'India'), ('80.249.56.118', 'United Kingdom'), ('61.12.45.214', 'India'), ('122.172.173.70', 'India'), ('150.107.25.212', 'India'), ('85.95.189.104', 'Russia'), ('12.156.20.2', 'United States'), ('81.136.225.91', 'United Kingdom'), ('2a00:23c5:6e09:c400:3547:6914:5b6:cb5a', 'United Kingdom'), ('175.136.38.52', 'Malaysia'), ('210.212.247.38', 'India'), ('183.83.82.2', 'India'), ('103.21.77.58', 'India'), ('213.168.107.162', 'Germany'), ('195.194.86.66', 'United Kingdom'), ('86.120.91.155', 'Romania'), ('103.241.244.36', 'India'), ('180.190.43.58', 'Philippines'), ('199.172.169.86', 'United States'), ('31.147.240.138', 'Croatia'), ('182.72.162.3', 'India'), ('146.163.156.200', 'United States'), ('24.80.84.36', 'Canada'), ('77.178.142.167', 'Germany'), ('140.193.113.207', 'Canada'), ('202.153.45.19', 'India')]
# country_ab = {}
# names = []
# values = []
# f = open(r'E:\CZK\工作\数据分析\我的练习项目\维基百科词条编辑\国家.txt', 'r', encoding='UTF-8')
# for line in f:
#     if len(line) > 1:
#         country_ab[re.findall('(.*?):', line)[0]] = ' '.join(re.findall('[\u4e00-\u9fa5]+', line))
#         country_ab[re.findall('[a-zA-Z]+', line)[0]] = ' '.join(re.findall('[a-zA-Z]+', line)[1:])
# f.close()
# countrys = [i[1] for i in results]
# stats = collections.Counter(countrys)
# for each in stats.items():
#     (name, value) = each
#     names.append(name)
#     values.append(value)
# print(names, values)
# word_map = Map("维基词条编辑每个国家贡献", width=800, height=400)
# word_map.add("", names, values, maptype="world", is_visualmap=True,
#              is_piecewise=True, visual_text_color='#000', is_map_symbol_show=False,
#              pieces=[{"min": 25, "label": ">25"}, {"max": 25, "min": 15, "label": "15-25"}, {"max": 15, "min": 5, "label": "5-15"},
#                     {"max": 5, "min": 2, "label": "2-5"},{"max": 1, "min": 0, "label": "<2"}])
# word_map.render()





