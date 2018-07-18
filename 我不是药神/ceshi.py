from pyecharts import ThemeRiver, Bar, Page
import pandas as pd
from pandas import DataFrame
import numpy as np
csv_file = "26683723.csv"

def date_transform(date):
    pass


def score_draw(csv_file):
    page = Page(csv_file[:8]+":评论等级分析")
    score, date, val, score_list = [], [], [], []
    result = {}
    d = pd.read_csv(csv_file)[['score', 'date']].dropna()  # 读取CSV转为dataframe格式，并丢弃评论为空的记录
    for indexs in d.index:  # 一种遍历df行的方法（下面还有第二种，iterrows）
        score_list.append(tuple(d.loc[indexs].values[:])) # 目前只找到转换为tuple然后统计相同元素个数的方法
    #print("有效评分总数量为：",len(score_list), " 条")
    for i in set(list(score_list)):
        result[i] = score_list.count(i)  # dict类型 ('很差', '2018-04-28'): 55
    info = []
    for key in result:
        score= key[0]
        date = key[1]
        val = result[key]
        info.append([score, date, val])
    info_new = DataFrame(info)  # 将字典转换成为数据框
    info_new.columns = ['score', 'date', 'votes']
    info_new.sort_values('date', inplace=True)    # 按日期升序排列df，便于找最早date和最晚data，方便后面插值
    #print("first df", info_new)
    # 以下代码用于插入空缺的数据，每个日期的评分类型应该有5中，依次遍历判断是否存在，若不存在则往新的df中插入新数值
    mark = 0
    creat_df = pd.DataFrame(columns = ['score', 'date', 'votes']) # 创建空的dataframe
    for i in list(info_new['date']):
        location = info_new[(info_new.date==i)&(info_new.score=="力荐")].index.tolist()
        if location == []:
            creat_df.loc[mark] = ["力荐", i, 0]
            mark += 1
        location = info_new[(info_new.date==i)&(info_new.score=="推荐")].index.tolist()
        if location == []:
            creat_df.loc[mark] = ["推荐", i, 0]
            mark += 1
        location = info_new[(info_new.date==i)&(info_new.score=="还行")].index.tolist()
        if location == []:
            creat_df.loc[mark] = ["还行", i, 0]
            mark += 1
        location = info_new[(info_new.date==i)&(info_new.score=="较差")].index.tolist()
        if location == []:
            creat_df.loc[mark] = ["较差", i, 0]
            mark += 1
        location = info_new[(info_new.date==i)&(info_new.score=="很差")].index.tolist()
        if location == []:
            creat_df.loc[mark] = ["很差", i, 0]
            mark += 1
    info_new = info_new.append(creat_df.drop_duplicates(), ignore_index=True)
    score_list = []
    info_new.sort_values('date', inplace=True)    # 按日期升序排列df，便于找最早date和最晚data，方便后面插值
    #print(info_new)
    for index, row in info_new.iterrows():   # 第二种遍历df的方法
        score_list.append([row['date'], row['votes'], row['score']])
    tr = ThemeRiver()
    tr.add(['力荐', '推荐', '还行', '较差', '很差'], score_list, is_label_show=True, is_more_utils=True)
    page.add_chart(tr)

    attr, v1, v2, v3, v4, v5 = [], [], [], [], [], []
    attr = list(sorted(set(info_new['date'])))
    bar = Bar()
    for i in attr:
        v1.append(int(info_new[(info_new['date']==i)&(info_new['score']=="力荐")]['votes']))
        v2.append(int(info_new[(info_new['date']==i)&(info_new['score']=="推荐")]['votes']))
        v3.append(int(info_new[(info_new['date']==i)&(info_new['score']=="还行")]['votes']))
        v4.append(int(info_new[(info_new['date']==i)&(info_new['score']=="较差")]['votes']))
        v5.append(int(info_new[(info_new['date']==i)&(info_new['score']=="很差")]['votes']))
    bar.add("力荐", attr, v1, is_stack=True)
    bar.add("推荐", attr, v2, is_stack=True)
    bar.add("还行", attr, v3, is_stack=True)
    bar.add("较差", attr, v4, is_stack=True)
    bar.add("很差", attr, v5, is_stack=True, is_convert=True, mark_line=["average"])
    page.add_chart(bar)
    page.render(csv_file[:8] + "_日投票量分析汇总.html")

score_draw(csv_file)