import pandas as pd
import re
from pyecharts import Line, Geo
from snownlp import SnowNLP

fth = open('简版城市字典.txt', 'r', encoding='utf-8').read()

# 过滤字符串只保留中文
def translate(str):
    line = str.strip()
    p2 = re.compile('[^\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
    zh = " ".join(p2.split(line)).strip()
    zh = ",".join(zh.split())
    str = re.sub("[A-Za-z0-9!！，%\[\],。]", "", zh)
    return str


# 下面是按照列属性读取的
def count_sentiment(csv_file):
    d = pd.read_csv(csv_file)
    motion_list = []
    for i in d['content']:
        try:
            s = round(SnowNLP(i).sentiments, 2)
            motion_list.append(s)
        except TypeError:
            continue
    result = {}
    for i in set(motion_list):
        result[i] = motion_list.count(i)
    return result


def draw_sentiment_pic(csv_file):
    attr, val = [], []
    info = count_sentiment(csv_file)
    info = sorted(info.items(), key=lambda x: x[0], reverse=False)  # dict的排序方法
    for each in info[:-1]:
        attr.append(each[0])
        val.append(each[1])
    line = Line(csv_file+":影评情感分析")
    line.add("", attr, val, is_smooth=True, is_more_utils=True)
    line.render(csv_file+"_情感分析曲线图.html")


def count_city(csv_file):
    citys= []
    m = '[\u4e00-\u9fa5]'    # 匹配城市字符串中的中文
    d = pd.read_csv(csv_file)
    for i in d['city'].dropna():       # 过滤掉空的城市
        i = translate(i)  # 只保留中文
        if len(i) >2:
            if i in fth:   # 如果名称个数>2，先判断是否在字典里
                citys.append(i)
            else:
                i = i[-2:]  # 取城市名称后两个，去掉省份
                if i in fth:
                    citys.append(i)
                else:
                    continue
        else:
            if i in fth:   # 如果名称个数>2，先判断是否在字典里
                citys.append(i)
            else:
                continue
    result = {}
    #print(citys)
    while '' in citys:
        citys.remove('')  # 去掉字符串中的空值
    #print(citys)
    for i in set(citys):
        result[i] = citys.count(i)
    print(result)
    return result


def draw_citys_pic(csv_file):
    attr,  val = [], []
    info = count_city(csv_file)
    geo = Geo(csv_file+":评论城市来源分析", "Ctipsy原创",title_pos="center", width=1200,height=600, background_color='#404a59')
    attr, val = geo.cast(info)
    geo.add("",attr, val,visual_range=[0, 300], visual_text_color="#fff", is_geo_effect_show=False, geo_cities_coords=False, symbol_size=15, is_visualmap=True)
    geo.render(csv_file[:8]+"_城市点图.html")
    geo.add("", attr, val, type="heatmap", is_visualmap=True, visual_range=[0, 300],
            visual_text_color='#fff')
    geo.render(csv_file[:8]+"_城市热力图.html")  # 取CSV文件名的前8位数


def main(csv_file):
    # draw_sentiment_pic(csv_file)
    draw_citys_pic(csv_file)


if __name__ == '__main__':
    main('26752088.csv')




