# -*- coding:utf-8 -*-
import Geohash as geohash
import pandas as pd
import numpy as np
import os
os.path.join('..')
from utils import cal_distance, rank, manhattan

'''
	获取小时特征
'''

# 获取小时段
def get_hour(result):
    result['hour'] = pd.to_datetime(result['starttime']).dt.hour
    return result

# 获取每个小时段的出行订单数
def get_hour_count(train, result):
    hour_count = train.groupby(['hour'], as_index=False)['userid'].agg({'hour_count': 'count'})
    result = pd.merge(result, hour_count, on='hour', how='left')
    return result

'''
	获取距离特征
'''

# 获取出发地到目的地的欧氏距离和曼哈顿距离
def get_distance(result):
    locs = list(set(result['geohashed_start_loc']) | set(result['geohashed_end_loc']))
    if np.nan in locs: 
        locs.remove(np.nan)
    deloc = []
    for loc in locs:
        deloc.append(geohash.decode_exactly(loc))
    loc_dict = dict(zip(locs, deloc))
    geohashed_loc = result[['geohashed_start_loc', 'geohashed_end_loc']].values
    distance = []
    manhattan_distance = []
    for i in geohashed_loc:
        if i[0] is not np.nan and i[1] is not np.nan:
            lat1, lon1, _, _ = loc_dict[i[0]]
            lat2, lon2, _, _ = loc_dict[i[1]]
            distance.append(cal_distance(float(lat1), float(lon1), float(lat2), float(lon2)))
            manhattan_distance.append(manhattan(float(lat1), float(lon1), float(lat2), float(lon2)))
        else:
            distance.append(np.nan)
            manhattan_distance.append(np.nan)
    result.loc[:, 'distance'] = distance
    result.loc[:, 'manhattan'] = manhattan_distance
    return result

'''
	获取经纬度特征
'''
def get_latlon(result, end=True):
    if end:
        eloc_latlon = result['geohashed_end_loc'].apply(lambda x: geohash.decode_exactly(x))
        result['eloc_lat'] = eloc_latlon.apply(lambda x: float(x[0]))
        result['eloc_lon'] = eloc_latlon.apply(lambda x: float(x[1]))
    sloc_latlon = result['geohashed_start_loc'].apply(lambda x: geohash.decode_exactly(x))
    result['sloc_lat'] = sloc_latlon.apply(lambda x: float(x[0]))
    result['sloc_lon'] = sloc_latlon.apply(lambda x: float(x[1]))
    if end:
        result['eloc_sloc_lat_sub'] = result['eloc_lat'] - result['sloc_lat']
        result['eloc_sloc_lon_sub'] = result['eloc_lon'] - result['sloc_lon']
    return result