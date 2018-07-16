# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import pickle

# 计算相差的分钟数
def diff_of_minutes(time1, time2):
    d = {'5': 0, '6': 31, }
    try:
        days = (d[time1[6]] + int(time1[8:10])) - (d[time2[6]] + int(time2[8:10]))
        try:
            minutes1 = int(time1[11:13]) * 60 + int(time1[14:16])
        except:
            minutes1 = 0
        try:
            minutes2 = int(time2[11:13]) * 60 + int(time2[14:16])
        except:
            minutes2 = 0
        return (days * 1440 - minutes2 + minutes1)
    except:
        return np.nan

# 计算两点之间距离
def haversine(lat1, lng1, lat2, lng2):
    """function to calculate haversine distance between two co-ordinates"""
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    AVG_EARTH_RADIUS = 6371  # in km
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = np.sin(lat * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * np.arcsin(np.sqrt(d))
    return(h)

def manhattan(lat1, lng1, lat2, lng2):
    """function to calculate manhatten distance between pick_drop"""
    a = haversine(lat1, lng1, lat1, lng2)
    b = haversine(lat1, lng1, lat2, lng1)
    return a + b

# 计算两个经纬度之间的距离
def cal_distance(lat1,lon1,lat2,lon2):
    dx = np.abs(lon1 - lon2)
    dy = np.abs(lat1 - lat2)
    b = (lat1 + lat2) / 2.0
    Lx = 6371004.0 * (dx / 57.2958) * np.cos(b / 57.2958)
    Ly = 6371004.0 * (dy / 57.2958)
    L = (Lx**2 + Ly**2) ** 0.5
    return L

# 计算两个经纬度之间的方向角
def bearing_array(lat1, lng1, lat2, lng2):
    """ function was taken from beluga's notebook as this function works on array
    while my function used to work on individual elements and was noticably slow"""
    AVG_EARTH_RADIUS = 6371  # in km
    lng_delta_rad = np.radians(lng2 - lng1)
    lat1, lng1, lat2, lng2 = map(np.radians, (lat1, lng1, lat2, lng2))
    y = np.sin(lng_delta_rad) * np.cos(lat2)
    x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(lng_delta_rad)
    return np.degrees(np.arctan2(y, x))

# 分组排序
def rank(data, feat1, feat2, rank_name='rank', ascending=True):
    if type(feat1) == list: feat = feat1 + [feat2]
    else: feat = [feat1, feat2]
    use_feat = list(set(feat + ['orderid', 'geohashed_end_loc']))
    datatmp = data[use_feat]
    datatmp.sort_values(feat, inplace=True, ascending=ascending)
    datatmp[rank_name] = range(datatmp.shape[0])
    min_rank = datatmp.groupby(feat1, as_index=False)[rank_name].agg({'min_rank': 'min'})
    datatmp = pd.merge(datatmp, min_rank, on=feat1, how='left')
    datatmp[rank_name] = datatmp[rank_name] - datatmp['min_rank']
    data = pd.merge(data, datatmp[['orderid', 'geohashed_end_loc', rank_name]], on=['orderid', 'geohashed_end_loc'], how='left')
    # del data['min_rank']
    return data

# 载入模型
def load_model(opt):
    with open('{}/{}'.format(opt['model_dir'], opt['model_name']), 'rb') as fin:
        gbm = pickle.load(fin)
    use_feat = gbm.feature_name()
    print('载入模型成功：', len(use_feat), use_feat)
    return gbm, use_feat
