import pandas as pd
import re
from pyecharts import Line, Geo, Bar
from snownlp import SnowNLP

fth = open('pyecharts_citys_supported.txt', 'r', encoding='utf-8').read() # pyecharts支持城市列表

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
    d = pd.read_csv(csv_file)
    for i in d['city'].dropna():       # 过滤掉空的城市
        i = translate(i)  # 只保留中文
        if len(i)>1 and len(i)<5:  # 如果名称个数2~4，先判断是否在字典里
            if i in fth:
                citys.append(i)
            else:
                i = i[-2:]  # 取城市名称后两个，去掉省份
                if i in fth:
                    citys.append(i)
                else:
                    continue
        if len(i) > 4:
            if i in fth:   # 如果名称个数>2，先判断是否在字典里
                citys.append(i)
            if i[-5:] in fth:
                citys.append(i[-5:])
                continue
            if i[-4:] in fth:
                citys.append(i[-4:])
                continue
            if i[-3:] in fth:
                citys.append(i[-3:])
            else:
                continue
    result = {}
    while '' in citys:
        citys.remove('')  # 去掉字符串中的空值
    print("城市总数量为：",len(citys))
    for i in set(citys):
        result[i] = citys.count(i)
    return result


def draw_citys_pic(csv_file):
    info = count_city(csv_file)
    geo = Geo(csv_file[:8]+":评论城市来源分析", "Ctipsy原创",title_pos="center", width=1200,height=600, background_color='#404a59', title_color="#fff")
    flag = 0
    while True:   # 二次筛选，和pyecharts支持的城市库进行匹配，如果报错则删除该城市对应的统计
        try:
            attr, val = geo.cast(info)
            geo.add("", attr, val, visual_range=[0, 300], visual_text_color="#fff", is_geo_effect_show=False,
                    is_piecewise=True, visual_split_number=6, symbol_size=15, is_visualmap=True)
            flag =1
        except ValueError as e:
            e = str(e)
            e = e.split("No coordinate is specified for ")[1]  # 获取不支持的城市名称
            info.pop(e)
        if flag == 1:
            break
    info = sorted(info.items(), key=lambda x: x[1], reverse=False)  # list排序
    # print(info)
    info = dict(info)   #list转dict
    # print(info)
    attr, val = [], []
    for key in info:
        attr.append(key)
        val.append(info[key])
    print(attr)
    print(val)



    geo = Geo(csv_file[:8] + ":评论城市来源分析", "Ctipsy原创", title_pos="center", width=1200, height=600,
              background_color='#404a59', title_color="#fff")
    geo.add("", attr, val, visual_range=[0, 300], visual_text_color="#fff", is_geo_effect_show=False,
            is_piecewise=True, visual_split_number=10, symbol_size=15, is_visualmap=True, is_more_utils=True)
    geo.render(csv_file[:8] + "_城市点图.html")

    geo = Geo(csv_file[:8]+":评论城市来源分析", "Ctipsy原创",title_pos="center", width=1200,height=600, background_color='#404a59', title_color="#fff",)
    geo.add("", attr, val, type="heatmap", is_visualmap=True, visual_range=[0, 50],visual_text_color='#fff', is_more_utils=True)
    geo.render(csv_file[:8]+"_城市热力图.html")  # 取CSV文件名的前8位数

    bar = Bar(csv_file[:8] + ":评论城市来源分析", "Ctipsy原创", title_pos="center", width=1200, height=600,
              background_color='#404a59', title_color="#fff", )
    bar.add("", attr, val, is_visualmap=True, visual_range=[0, 300], visual_text_color='#fff',
            is_more_utils=True)
    bar.render(csv_file[:8]+"_城市评论排行.html")  # 取CSV文件名的前8位数

def main(csv_file):
    # draw_sentiment_pic(csv_file)
    draw_citys_pic(csv_file)


if __name__ == '__main__':
    main('26366496.csv')




