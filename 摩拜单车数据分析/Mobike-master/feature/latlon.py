# -*- coding:utf-8 -*-
import pandas as pd
import Geohash as geohash
import numpy as np
import os
os.path.join('..')
from utils import rank

'''
    获取经纬度特征
'''

# ----------------- 经纬度 -------------------

# 获取目的地的经纬度
def get_eloc_latlon(result):
    eloc_latlon = result['geohashed_end_loc'].apply(lambda x: geohash.decode_exactly(x)[:2])
    result['eloc_lat'] = eloc_latlon.apply(lambda x: float(x[0]))
    result['eloc_lon'] = eloc_latlon.apply(lambda x: float(x[1]))
    return result

# 获取出发地的经纬度
def get_sloc_latlon(result):
    sloc_latlon = result['geohashed_start_loc'].apply(lambda x: geohash.decode_exactly(x)[:2])
    result['sloc_lat'] = sloc_latlon.apply(lambda x: float(x[0]))
    result['sloc_lon'] = sloc_latlon.apply(lambda x: float(x[1]))
    return result

# ----------------- 方向 -------------------

# 获取出发地与目的地的经纬度差
def get_eloc_sloc_latlon_sub(result):
    # sloc_latlon = result['geohashed_start_loc'].apply(lambda x: geohash.decode_exactly(x)[:2])
    # sloc_lat = sloc_latlon.apply(lambda x: float(x[0]))
    # sloc_lon = sloc_latlon.apply(lambda x: float(x[1]))
    # eloc_latlon = result['geohashed_end_loc'].apply(lambda x: geohash.decode_exactly(x)[:2])
    # eloc_lat = eloc_latlon.apply(lambda x: float(x[0]))
    # eloc_lon = eloc_latlon.apply(lambda x: float(x[1]))
    result['eloc_sloc_lat_sub'] = result['eloc_lat'] - result['sloc_lat']
    result['eloc_sloc_lon_sub'] = result['eloc_lon'] - result['sloc_lon']
    return result

# 获取出发地与目的地的斜率
def get_eloc_sloc_slope(result):
    result['eloc_sloc_latlon_slope'] = result['eloc_sloc_lat_sub'] / result['eloc_sloc_lon_sub']
    return result

# 获取经纬度差与距离的商
def get_eloc_sloc_latlon_sub_divide_distance(result):
    result['eloc_sloc_lat_sub_divide_distance'] = result['eloc_sloc_lat_sub'] / result['distance']
    result['eloc_sloc_lon_sub_divide_distance'] = result['eloc_sloc_lon_sub'] / result['distance']
    result['eloc_sloc_lat_sub_divide_manhattan'] = result['eloc_sloc_lat_sub'] / result['manhattan']
    result['eloc_sloc_lon_sub_divide_manhattan'] = result['eloc_sloc_lon_sub'] / result['manhattan']
    return result

# 获取方向角
def get_bearing_array(result):
    result['degree'] = np.arctan2(result['eloc_sloc_lat_sub'], result['eloc_sloc_lon_sub'])
    return result

# ----------------- 统计 -------------------

# 获取用户出发的距离统计
def get_user_latlon_sub_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_lat_sub_stat = train.groupby(['userid', 'geohashed_start_loc'], as_index=False)['eloc_sloc_lat_sub'].agg({'user_lat_sub_max': 'max', 'user_lat_sub_min': 'min', 'user_lat_sub_mean': 'mean'})
    result = pd.merge(result, user_lat_sub_stat, on=['userid', 'geohashed_start_loc'], how='left')
    user_lon_sub_stat = train.groupby(['userid', 'geohashed_start_loc'], as_index=False)['eloc_sloc_lon_sub'].agg({'user_lon_sub_max': 'max', 'user_lon_sub_min': 'min', 'user_lon_sub_mean': 'mean'})
    result = pd.merge(result, user_lon_sub_stat, on=['userid', 'geohashed_start_loc'], how='left')
    return result

# 获取用户从某个地点出发的距离统计
def get_user_sloc_latlon_sub_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_sloc_lat_sub_stat = train.groupby(['userid', 'geohashed_start_loc'], as_index=False)['eloc_sloc_lat_sub'].agg({'user_sloc_lat_sub_max': 'max', 'user_sloc_lat_sub_min': 'min', 'user_sloc_lat_sub_mean': 'mean'}) # 8 7 kong
    # user_sloc_lat_sub_stat = train.groupby(['userid', 'geohashed_start_loc'], as_index=False)['eloc_sloc_lat_sub'].agg({'user_sloc_lat_sub_mean': 'mean'})
    result = pd.merge(result, user_sloc_lat_sub_stat, on=['userid', 'geohashed_start_loc'], how='left')
    user_sloc_lon_sub_stat = train.groupby(['userid', 'geohashed_start_loc'], as_index=False)['eloc_sloc_lon_sub'].agg({'user_sloc_lon_sub_max': 'max', 'user_sloc_lon_sub_min': 'min', 'user_sloc_lon_sub_mean': 'mean'})
    result = pd.merge(result, user_sloc_lon_sub_stat, on=['userid', 'geohashed_start_loc'], how='left')
    return result

# 获取用户到某个地点结束的距离统计
def get_user_eloc_latlon_sub_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_lat_sub_stat = train.groupby(['userid', 'geohashed_end_loc'], as_index=False)['eloc_sloc_lat_sub'].agg({'user_eloc_lat_sub_max': 'max', 'user_eloc_lat_sub_min': 'min', 'user_eloc_lat_sub_mean': 'mean'})
    result = pd.merge(result, user_eloc_lat_sub_stat, on=['userid', 'geohashed_end_loc'], how='left')
    user_eloc_lon_sub_stat = train.groupby(['userid', 'geohashed_end_loc'], as_index=False)['eloc_sloc_lon_sub'].agg({'user_eloc_lon_sub_max': 'max', 'user_eloc_lon_sub_min': 'min', 'user_eloc_lon_sub_mean': 'mean'})
    result = pd.merge(result, user_eloc_lon_sub_stat, on=['userid', 'geohashed_end_loc'], how='left')
    return result

# 获取用户从某个地点出发的小时段距离统计
def get_user_sloc_hour_latlon_sub_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_sloc_hour_lat_sub_stat = train.groupby(['userid', 'geohashed_start_loc', 'hour'], as_index=False)['eloc_sloc_lat_sub'].agg({'user_sloc_hour_lat_sub_max': 'max', 'user_sloc_hour_lat_sub_min': 'min', 'user_sloc_hour_lat_sub_mean': 'mean'})
    result = pd.merge(result, user_sloc_hour_lat_sub_stat, on=['userid', 'geohashed_start_loc', 'hour'], how='left')
    user_sloc_hour_lon_sub_stat = train.groupby(['userid', 'geohashed_start_loc', 'hour'], as_index=False)['eloc_sloc_lon_sub'].agg({'user_sloc_hour_lon_sub_max': 'max', 'user_sloc_hour_lon_sub_min': 'min', 'user_sloc_hour_lon_sub_mean': 'mean'})
    result = pd.merge(result, user_sloc_hour_lon_sub_stat, on=['userid', 'geohashed_start_loc', 'hour'], how='left')
    return result

# 获取用户到某个地点结束的小时段距离统计
def get_user_eloc_hour_latlon_sub_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_hour_lat_sub_stat = train.groupby(['userid', 'geohashed_end_loc', 'hour'], as_index=False)['eloc_sloc_lat_sub'].agg({'user_eloc_hour_lat_sub_max': 'max', 'user_eloc_hour_lat_sub_min': 'min', 'user_eloc_hour_lat_sub_mean': 'mean'}) # 4 4 6
    result = pd.merge(result, user_eloc_hour_lat_sub_stat, on=['userid', 'geohashed_end_loc', 'hour'], how='left')
    user_eloc_hour_lon_sub_stat = train.groupby(['userid', 'geohashed_end_loc', 'hour'], as_index=False)['eloc_sloc_lon_sub'].agg({'user_eloc_hour_lon_sub_max': 'max', 'user_eloc_hour_lon_sub_min': 'min', 'user_eloc_hour_lon_sub_mean': 'mean'}) # 2 7 6
    result = pd.merge(result, user_eloc_hour_lon_sub_stat, on=['userid', 'geohashed_end_loc', 'hour'], how='left')
    return result

# 获取从某个地点出发的距离统计
def get_sloc_latlon_sub_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_lat_sub_stat = train.groupby(['geohashed_start_loc'], as_index=False)['eloc_sloc_lat_sub'].agg({'sloc_lat_sub_max': 'max', 'sloc_lat_sub_min': 'min', 'sloc_lat_sub_mean': 'mean'})
    result = pd.merge(result, sloc_lat_sub_stat, on=['geohashed_start_loc'], how='left')
    sloc_lon_sub_stat = train.groupby(['geohashed_start_loc'], as_index=False)['eloc_sloc_lon_sub'].agg({'sloc_lon_sub_max': 'max', 'sloc_lon_sub_min': 'min', 'sloc_lon_sub_mean': 'mean'})
    result = pd.merge(result, sloc_lon_sub_stat, on=['geohashed_start_loc'], how='left')
    return result

# 获取到某个地点结束的距离统计
def get_eloc_latlon_sub_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_lat_sub_stat = train.groupby(['geohashed_end_loc'], as_index=False)['eloc_sloc_lat_sub'].agg({'eloc_lat_sub_max': 'max', 'eloc_lat_sub_min': 'min', 'eloc_lat_sub_mean': 'mean'})
    result = pd.merge(result, eloc_lat_sub_stat, on=['geohashed_end_loc'], how='left')
    eloc_lon_sub_stat = train.groupby(['geohashed_end_loc'], as_index=False)['eloc_sloc_lon_sub'].agg({'eloc_lon_sub_max': 'max', 'eloc_lon_sub_min': 'min', 'eloc_lon_sub_mean': 'mean'})
    result = pd.merge(result, eloc_lon_sub_stat, on=['geohashed_end_loc'], how='left')
    return result

# 获取从某个地点出发的小时段距离统计
def get_sloc_hour_latlon_sub_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_hour_lat_sub_stat = train.groupby(['geohashed_start_loc', 'hour'], as_index=False)['eloc_sloc_lat_sub'].agg({'sloc_hour_lat_sub_max': 'max', 'sloc_hour_lat_sub_min': 'min', 'sloc_hour_lat_sub_mean': 'mean'})
    result = pd.merge(result, sloc_hour_lat_sub_stat, on=['geohashed_start_loc', 'hour'], how='left')
    sloc_hour_lon_sub_stat = train.groupby(['geohashed_start_loc', 'hour'], as_index=False)['eloc_sloc_lon_sub'].agg({'sloc_hour_lon_sub_max': 'max', 'sloc_hour_lon_sub_min': 'min', 'sloc_hour_lon_sub_mean': 'mean'})
    result = pd.merge(result, sloc_hour_lon_sub_stat, on=['geohashed_start_loc', 'hour'], how='left')
    return result

# 获取到某个地点结束的小时段距离统计
def get_eloc_hour_latlon_sub_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_hour_lat_sub_stat = train.groupby(['geohashed_end_loc', 'hour'], as_index=False)['eloc_sloc_lat_sub'].agg({'eloc_hour_lat_sub_max': 'max', 'eloc_hour_lat_sub_min': 'min', 'eloc_hour_lat_sub_mean': 'mean'})
    result = pd.merge(result, eloc_hour_lat_sub_stat, on=['geohashed_end_loc', 'hour'], how='left')
    eloc_hour_lon_sub_stat = train.groupby(['geohashed_end_loc', 'hour'], as_index=False)['eloc_sloc_lon_sub'].agg({'eloc_hour_lon_sub_max': 'max', 'eloc_hour_lon_sub_min': 'min', 'eloc_hour_lon_sub_mean': 'mean'})
    result = pd.merge(result, eloc_hour_lon_sub_stat, on=['geohashed_end_loc', 'hour'], how='left')
    return result

# ----------------- 排序 -------------------

# 获取用户出行距离的排序
def get_user_latlon_sub_rank(result):
    result = rank(result, 'userid', 'eloc_sloc_lat_sub', rank_name='user_lat_sub_rank', ascending=False)
    result = rank(result, 'userid', 'eloc_sloc_lon_sub', rank_name='user_lon_sub_rank', ascending=False)
    return result

# 获取用户到某个目的地的距离排序
def get_user_eloc_latlon_sub_rank(result):
    result = rank(result, ['userid', 'geohashed_end_loc'], 'eloc_sloc_lat_sub', rank_name='user_eloc_lat_sub_rank', ascending=False)
    result = rank(result, ['userid', 'geohashed_end_loc'], 'eloc_sloc_lon_sub', rank_name='user_eloc_lon_sub_rank', ascending=False)
    return result

# 获取用户从某个地点出发的距离排序
def get_user_sloc_latlon_sub_rank(result):
    result = rank(result, ['userid', 'geohashed_start_loc'], 'eloc_sloc_lat_sub', rank_name='user_sloc_lat_sub_rank', ascending=False)
    result = rank(result, ['userid', 'geohashed_start_loc'], 'eloc_sloc_lon_sub', rank_name='user_sloc_lon_sub_rank', ascending=False)
    return result

# 获取用户到某个目的地的小时段距离排序
def get_user_eloc_hour_latlon_sub_rank(result):
    result = rank(result, ['userid', 'geohashed_end_loc', 'hour'], 'eloc_sloc_lat_sub', rank_name='user_eloc_hour_lat_sub_rank', ascending=False)
    result = rank(result, ['userid', 'geohashed_end_loc', 'hour'], 'eloc_sloc_lon_sub', rank_name='user_eloc_hour_lon_sub_rank', ascending=False)
    return result

# 获取从某个目的地出发的小时段距离排序
def get_user_sloc_hour_latlon_sub_rank(result):
    result = rank(result, ['userid', 'geohashed_start_loc', 'hour'], 'eloc_sloc_lat_sub', rank_name='user_sloc_hour_lat_sub_rank', ascending=False)
    result = rank(result, ['userid', 'geohashed_start_loc', 'hour'], 'eloc_sloc_lon_sub', rank_name='user_sloc_hour_lon_sub_rank', ascending=False)
    return result

# 获取到某个目的地的距离排序
def get_eloc_latlon_sub_rank(result):
    result = rank(result, 'geohashed_end_loc', 'eloc_sloc_lat_sub', rank_name='eloc_lat_sub_rank', ascending=False)
    result = rank(result, 'geohashed_end_loc', 'eloc_sloc_lon_sub', rank_name='eloc_lon_sub_rank', ascending=False)
    return result

# 获取从某个地点出发的距离排序
def get_sloc_latlon_sub_rank(result):
    result = rank(result, 'geohashed_start_loc', 'eloc_sloc_lat_sub', rank_name='sloc_lat_sub_rank', ascending=False)
    result = rank(result, 'geohashed_start_loc', 'eloc_sloc_lon_sub', rank_name='sloc_lon_sub_rank', ascending=False)
    return result

# 获取到某个目的地的小时段距离排序
def get_eloc_hour_latlon_sub_rank(result):
    result = rank(result, ['geohashed_end_loc', 'hour'], 'eloc_sloc_lat_sub', rank_name='eloc_hour_lat_sub_rank', ascending=False)
    result = rank(result, ['geohashed_end_loc', 'hour'], 'eloc_sloc_lon_sub', rank_name='eloc_hour_lon_sub_rank', ascending=False)
    return result

# 获取从某个目的地出发的小时段距离排序
def get_sloc_hour_latlon_sub_rank(result):
    result = rank(result, ['geohashed_start_loc', 'hour'], 'eloc_sloc_lat_sub', rank_name='sloc_hour_lat_sub_rank', ascending=False)
    result = rank(result, ['geohashed_start_loc', 'hour'], 'eloc_sloc_lon_sub', rank_name='sloc_hour_lon_sub_rank', ascending=False)
    return result

# ----------------- 交叉 -------------------

# 获取距离与用户出行距离统计值的(绝对)差值
def get_user_latlon_sub_stat_sub(result):
    result['user_lat_sub_mean_sub'] = (result['distance'] - result['user_lat_sub_mean'])
    result['user_lon_sub_mean_sub'] = (result['distance'] - result['user_lon_sub_mean'])
    result['user_lat_sub_mean_sub_abs'] = (result['distance'] - result['user_lat_sub_mean']).abs() # 6
    result['user_lon_sub_mean_sub_abs'] = (result['distance'] - result['user_lon_sub_mean']).abs() # 1
    return result

# 获取距离与用户从某个点出发距离统计值的(绝对)差值
def get_user_sloc_latlon_sub_stat_sub(result):
    # result['user_sloc_lat_sub_mean_sub'] = (result['distance'] - result['user_sloc_lat_sub_mean']) # 0
    result['user_sloc_lon_sub_mean_sub'] = (result['distance'] - result['user_sloc_lon_sub_mean']) # 2
    # result['user_sloc_lat_sub_mean_sub_abs'] = (result['distance'] - result['user_sloc_lat_sub_mean']).abs() # 0
    # result['user_sloc_lon_sub_mean_sub_abs'] = (result['distance'] - result['user_sloc_lon_sub_mean']).abs() # 0
    return result

# 获取距离与用户到某个点结束距离统计值的(绝对)差值
def get_user_eloc_latlon_sub_stat_sub(result):
    result['user_eloc_lat_sub_mean_sub'] = (result['distance'] - result['user_eloc_lat_sub_mean'])
    result['user_eloc_lon_sub_mean_sub'] = (result['distance'] - result['user_eloc_lon_sub_mean'])
    result['user_eloc_lat_sub_mean_sub_abs'] = (result['distance'] - result['user_eloc_lat_sub_mean']).abs()
    result['user_eloc_lon_sub_mean_sub_abs'] = (result['distance'] - result['user_eloc_lon_sub_mean']).abs()
    return result

# 获取距离与用户从某个点出发距离统计值的各小时段(绝对)差值
def get_user_sloc_hour_latlon_sub_stat_sub(result):
    result['user_sloc_hour_lat_sub_mean_sub'] = (result['distance'] - result['user_sloc_hour_lat_sub_mean'])
    result['user_sloc_hour_lon_sub_mean_sub'] = (result['distance'] - result['user_sloc_hour_lon_sub_mean'])
    result['user_sloc_hour_lat_sub_mean_sub_abs'] = (result['distance'] - result['user_sloc_hour_lat_sub_mean']).abs() # 5
    result['user_sloc_hour_lon_sub_mean_sub_abs'] = (result['distance'] - result['user_sloc_hour_lon_sub_mean']).abs() # 8
    return result

# 获取距离与用户到某个点结束距离统计值的各小时段(绝对)差值
def get_user_eloc_hour_latlon_sub_stat_sub(result):
    result['user_eloc_hour_lat_sub_mean_sub'] = (result['distance'] - result['user_eloc_hour_lat_sub_mean']) # 43
    result['user_eloc_hour_lon_sub_mean_sub'] = (result['distance'] - result['user_eloc_hour_lon_sub_mean']) # 18
    # result['user_eloc_hour_lat_sub_mean_sub_abs'] = (result['distance'] - result['user_eloc_hour_lat_sub_mean']).abs() # 0
    result['user_eloc_hour_lon_sub_mean_sub_abs'] = (result['distance'] - result['user_eloc_hour_lon_sub_mean']).abs() # 3
    return result

# 获取距离与从某个点出发距离统计值的(绝对)差值
def get_sloc_latlon_sub_stat_sub(result):
    result['sloc_lat_sub_mean_sub'] = (result['distance'] - result['sloc_lat_sub_mean'])
    result['sloc_lon_sub_mean_sub'] = (result['distance'] - result['sloc_lon_sub_mean'])
    result['sloc_lat_sub_mean_sub_abs'] = (result['distance'] - result['sloc_lat_sub_mean']).abs() # 4
    result['sloc_lon_sub_mean_sub_abs'] = (result['distance'] - result['sloc_lon_sub_mean']).abs() # 4
    return result

# 获取距离与到某个点结束距离统计值的(绝对)差值
def get_eloc_latlon_sub_stat_sub(result):
    result['eloc_lat_sub_mean_sub'] = (result['distance'] - result['eloc_lat_sub_mean'])
    result['eloc_lon_sub_mean_sub'] = (result['distance'] - result['eloc_lon_sub_mean'])
    result['eloc_lat_sub_mean_sub_abs'] = (result['distance'] - result['eloc_lat_sub_mean']).abs() # 7
    result['eloc_lon_sub_mean_sub_abs'] = (result['distance'] - result['eloc_lon_sub_mean']).abs()
    return result

# 获取距离与从某个点出发距离统计值的各小时段(绝对)差值
def get_sloc_hour_latlon_sub_stat_sub(result):
    result['sloc_hour_lat_sub_mean_sub'] = (result['distance'] - result['sloc_hour_lat_sub_mean'])
    result['sloc_hour_lon_sub_mean_sub'] = (result['distance'] - result['sloc_hour_lon_sub_mean'])
    result['sloc_hour_lat_sub_mean_sub_abs'] = (result['distance'] - result['sloc_hour_lat_sub_mean']).abs() # 7
    result['sloc_hour_lon_sub_mean_sub_abs'] = (result['distance'] - result['sloc_hour_lon_sub_mean']).abs() # 6
    return result

# 获取距离与到某个点结束距离统计值的各小时段(绝对)差值
def get_eloc_hour_latlon_sub_stat_sub(result):
    result['eloc_hour_lat_sub_mean_sub'] = (result['distance'] - result['eloc_hour_lat_sub_mean'])
    result['eloc_hour_lon_sub_mean_sub'] = (result['distance'] - result['eloc_hour_lon_sub_mean'])
    result['eloc_hour_lat_sub_mean_sub_abs'] = (result['distance'] - result['eloc_hour_lat_sub_mean']).abs() # 9
    result['eloc_hour_lon_sub_mean_sub_abs'] = (result['distance'] - result['eloc_hour_lon_sub_mean']).abs()
    return result