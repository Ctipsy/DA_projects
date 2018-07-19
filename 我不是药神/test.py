import pandas as pd
def score_draw(csv_file):
    score, date, val, score_list, date_start, date_end = [], [], [], [], [], []
    result = {}
    d = pd.read_csv(csv_file)[['score', 'date']]
    tmp = sorted(d['date'])
    date_start = tmp[0]
    date_end = tmp[1]
    print(date)
    for indexs in d.index:
        score_list.append(tuple(d.loc[indexs].values[:])) # 目前只找到转换为tuple然后统计的方法
    print("有效评分总数量为：",len(score_list), " 条")
    for i in set(list(score_list)):
        result[i] = score_list.count(i)  # dict类型 ('很差', '2018-04-28'): 55
    info = []
    for key in result:
        score= key[0]
        date = key[1]
        val = result[key]
        info.append([score, date, val])
    #print(info)
    return info

score_draw("26683723.csv")