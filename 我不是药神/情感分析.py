import pandas as pd
import re
from pyecharts import Line, Geo
from snownlp import SnowNLP

# fth = open('简版城市字典.txt', 'r', encoding='utf-8')
# print(fth)
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
        tmp = re.compile(m).match(i)   # 过滤掉海外城市（非中文）
        if tmp is not None:
            if i != "关注此人":        # 过滤掉主页中不存在的城市信息
                if i == "台湾"or"香港"or"澳门":
                    continue
                citys.append(i)
            else:
                continue
        else:
            continue
    result = {}
    print(citys)
    for i in set(citys):
        result[i] = citys.count(i)
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
    geo.render(csv_file[:8]+"_城市热力图.html")


def main(csv_file):
    # draw_sentiment_pic(csv_file)
    draw_citys_pic(csv_file)


if __name__ == '__main__':
    main('26752088.csv')




