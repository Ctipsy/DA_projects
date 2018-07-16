# -*- coding:utf-8 -*-
import pandas as pd
import Geohash as geohash
import numpy as np
import os
os.path.join('..')
from utils import rank

'''
	获取地理位置特征
'''

# ----------------- 计数 -------------------

# 获取目的地的热度
def get_eloc_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_count = train.groupby('geohashed_end_loc', as_index=False)['userid'].agg({'eloc_count': 'count'})
    result = pd.merge(result, eloc_count, on='geohashed_end_loc', how='left')
    return result

# 获取出发地热度
def get_sloc_count(train, result):
    sloc_count = train.groupby('geohashed_start_loc', as_index=False)['userid'].agg({'sloc_count': 'count'})
    result = pd.merge(result, sloc_count, on='geohashed_start_loc', how='left')
    return result

# 获取出发地作为目的地的热度
def get_sloc_as_eloc_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_as_eloc_count = train.groupby('geohashed_end_loc', as_index=False)['userid'].agg({'sloc_as_eloc_count': 'count'})
    sloc_as_eloc_count.rename(columns={'geohashed_end_loc': 'geohashed_start_loc'}, inplace=True)
    result = pd.merge(result, sloc_as_eloc_count, on='geohashed_start_loc', how='left')
    return result

# 获取目的地作为出发地的热度
def get_eloc_as_sloc_count(train, result):
    eloc_as_sloc_count = train.groupby('geohashed_start_loc', as_index=False)['userid'].agg({'eloc_as_sloc_count': 'count'})
    eloc_as_sloc_count.rename(columns={'geohashed_start_loc': 'geohashed_end_loc'}, inplace=True)
    result = pd.merge(result, eloc_as_sloc_count, on='geohashed_end_loc', how='left')
    return result

# 获取出发地->目的地地址对的热度
def get_sloc_eloc_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_eloc_count = train.groupby(['geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['userid'].agg({'sloc_eloc_count': 'count'})
    result = pd.merge(result, sloc_eloc_count, on=['geohashed_start_loc', 'geohashed_end_loc'], how='left')
    return result

# 获取目的地->出发地地址对的热度（返程次数）
def get_eloc_sloc_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_sloc_count = train.groupby(['geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['userid'].agg({'eloc_sloc_count': 'count'})
    eloc_sloc_count.rename(columns={'geohashed_start_loc': 'geohashed_end_loc', 'geohashed_end_loc': 'geohashed_start_loc'}, inplace=True)
    result = pd.merge(result, eloc_sloc_count, on=['geohashed_start_loc', 'geohashed_end_loc'], how='left')
    return result

# 获取目的地的用户热度
def get_eloc_user_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_user_count = train.groupby(['geohashed_end_loc'], as_index=False)['userid'].agg({'eloc_user_count': lambda x: np.unique(x).size})
    result = pd.merge(result, eloc_user_count, on='geohashed_end_loc', how='left')
    return result

# 获取出发地的用户热度
def get_sloc_user_count(train, result):
    sloc_user_count = train.groupby(['geohashed_start_loc'], as_index=False)['userid'].agg({'sloc_user_count': lambda x: np.unique(x).size})
    result = pd.merge(result, sloc_user_count, on='geohashed_start_loc', how='left')
    return result

# 获取出发地作为目的地的用户热度
def get_sloc_as_eloc_user_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_as_eloc_user_count = train.groupby('geohashed_end_loc', as_index=False)['userid'].agg({'sloc_as_eloc_user_count': lambda x: np.unique(x).size})
    sloc_as_eloc_user_count.rename(columns={'geohashed_end_loc': 'geohashed_start_loc'}, inplace=True)
    result = pd.merge(result, sloc_as_eloc_user_count, on='geohashed_start_loc', how='left')
    return result

# 获取目的地作为出发地的用户热度
def get_eloc_as_sloc_user_count(train, result):
    eloc_as_sloc_user_count = train.groupby('geohashed_start_loc', as_index=False)['userid'].agg({'eloc_as_sloc_user_count': lambda x: np.unique(x).size})
    eloc_as_sloc_user_count.rename(columns={'geohashed_start_loc': 'geohashed_end_loc'}, inplace=True)
    result = pd.merge(result, eloc_as_sloc_user_count, on='geohashed_end_loc', how='left')
    return result

# 获取出发地->目的地地址对的用户热度
def get_sloc_eloc_user_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_eloc_user_count = train.groupby(['geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['userid'].agg({'sloc_eloc_user_count': lambda x: np.unique(x).size})
    result = pd.merge(result, sloc_eloc_user_count, on=['geohashed_start_loc', 'geohashed_end_loc'], how='left')
    return result

# 获取目的地->出发地地址对的用户热度（返程用户数）
def get_eloc_sloc_user_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_sloc_user_count = train.groupby(['geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['userid'].agg({'eloc_sloc_user_count': lambda x: np.unique(x).size})
    eloc_sloc_user_count.rename(columns={'geohashed_start_loc': 'geohashed_end_loc', 'geohashed_end_loc': 'geohashed_start_loc'}, inplace=True)
    result = pd.merge(result, eloc_sloc_user_count, on=['geohashed_start_loc', 'geohashed_end_loc'], how='left')
    return result

# 获取从某个地方出发的目的地个数
def get_sloc_eloccount(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_eloccount = train.groupby('geohashed_start_loc', as_index=False)['geohashed_end_loc'].agg({'sloc_eloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, sloc_eloccount, on='geohashed_start_loc', how='left')
    return result

# 获取到某个地方结束的出发地个数
def get_eloc_sloccount(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_sloccount = train.groupby('geohashed_end_loc', as_index=False)['geohashed_start_loc'].agg({'eloc_sloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, eloc_sloccount, on='geohashed_end_loc', how='left')
    return result

# 获取目的地在各小时段的订单数
def get_eloc_hour_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_hour_count = train.groupby(['geohashed_end_loc', 'hour'], as_index=False)['orderid'].agg({'eloc_hour_count': 'count'})
    result = pd.merge(result, eloc_hour_count, on=['geohashed_end_loc', 'hour'], how='left')
    return result

# 获取出发地在各小时段的订单数
def get_sloc_hour_count(train, result):
    sloc_hour_count = train.groupby(['geohashed_start_loc', 'hour'], as_index=False)['orderid'].agg({'sloc_hour_count': 'count'})
    result = pd.merge(result, sloc_hour_count, on=['geohashed_start_loc', 'hour'], how='left')
    return result

# 获取出发地->目的地地址对的小时热度
def get_sloc_eloc_hour_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_eloc_hour_count = train.groupby(['geohashed_start_loc', 'geohashed_end_loc', 'hour'], as_index=False)['userid'].agg({'sloc_eloc_hour_count': 'count'})
    result = pd.merge(result, sloc_eloc_hour_count, on=['geohashed_start_loc', 'geohashed_end_loc', 'hour'], how='left')
    return result

# 获取目的地->出发地地址对的小时热度（返程次数）
def get_eloc_sloc_hour_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_sloc_hour_count = train.groupby(['geohashed_start_loc', 'geohashed_end_loc', 'hour'], as_index=False)['userid'].agg({'eloc_sloc_hour_count': 'count'})
    eloc_sloc_hour_count.rename(columns={'geohashed_start_loc': 'geohashed_end_loc', 'geohashed_end_loc': 'geohashed_start_loc'}, inplace=True)
    result = pd.merge(result, eloc_sloc_hour_count, on=['geohashed_start_loc', 'geohashed_end_loc', 'hour'], how='left')
    return result

# 获取目的地在各小时段的用户数
def get_eloc_hour_user_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_hour_user_count = train.groupby(['geohashed_end_loc', 'hour'], as_index=False)['userid'].agg({'eloc_hour_user_count': 
                                                                                    lambda x: np.unique(x).size})
    result = pd.merge(result, eloc_hour_user_count, on=['geohashed_end_loc', 'hour'], how='left')
    return result

# 获取出发地在各小时段的用户数
def get_sloc_hour_user_count(train, result):
    sloc_hour_user_count = train.groupby(['geohashed_start_loc', 'hour'], as_index=False)['userid'].agg({'sloc_hour_user_count': 
                                                                                    lambda x: np.unique(x).size})
    result = pd.merge(result, sloc_hour_user_count, on=['geohashed_start_loc', 'hour'], how='left')
    return result

# 获取出发地->目的地地址对的用户小时热度
def get_sloc_eloc_hour_user_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_eloc_hour_user_count = train.groupby(['geohashed_start_loc', 'geohashed_end_loc', 'hour'], as_index=False)['userid'].agg({'sloc_eloc_hour_user_count': lambda x: np.unique(x).size})
    result = pd.merge(result, sloc_eloc_hour_user_count, on=['geohashed_start_loc', 'geohashed_end_loc', 'hour'], how='left')
    return result

# 获取目的地->出发地地址对的用户小时热度（返程用户数）
def get_eloc_sloc_hour_user_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_sloc_hour_user_count = train.groupby(['geohashed_start_loc', 'geohashed_end_loc', 'hour'], as_index=False)['userid'].agg({'eloc_sloc_hour_user_count': lambda x: np.unique(x).size})
    eloc_sloc_hour_user_count.rename(columns={'geohashed_start_loc': 'geohashed_end_loc', 'geohashed_end_loc': 'geohashed_start_loc'}, inplace=True)
    result = pd.merge(result, eloc_sloc_hour_user_count, on=['geohashed_start_loc', 'geohashed_end_loc', 'hour'], how='left') # 9
    return result

# 获取从某个地方出发每个小时的目的地个数
def get_sloc_hour_eloccount(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_hour_eloccount = train.groupby(['geohashed_start_loc', 'hour'], as_index=False)['geohashed_end_loc'].agg({'sloc_hour_eloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, sloc_hour_eloccount, on=['geohashed_start_loc', 'hour'], how='left')
    return result

# 获取到某个地方结束每个小时的出发地个数
def get_eloc_hour_sloccount(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_hour_sloccount = train.groupby(['geohashed_end_loc', 'hour'], as_index=False)['geohashed_start_loc'].agg({'eloc_hour_sloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, eloc_hour_sloccount, on=['geohashed_end_loc', 'hour'], how='left')
    return result

# ----------------- 统计 -------------------

# 获取从某个地点出发的距离统计
def get_sloc_distance_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_distance_stat = train.groupby(['geohashed_start_loc'], as_index=False)['distance'].agg({'sloc_distance_max': 'max', 'sloc_distance_min': 'min', 'sloc_distance_mean': 'mean'})
    result = pd.merge(result, sloc_distance_stat, on=['geohashed_start_loc'], how='left')
    return result

# 获取到某个地点结束的距离统计
def get_eloc_distance_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_distance_stat = train.groupby(['geohashed_end_loc'], as_index=False)['distance'].agg({'eloc_distance_max': 'max', 'eloc_distance_min': 'min', 'eloc_distance_mean': 'mean'})
    result = pd.merge(result, eloc_distance_stat, on=['geohashed_end_loc'], how='left')
    return result

# 获取从某个地点出发的小时段距离统计
def get_sloc_hour_distance_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_hour_distance_stat = train.groupby(['geohashed_start_loc', 'hour'], as_index=False)['distance'].agg({'sloc_hour_distance_max': 'max', 'sloc_hour_distance_min': 'min', 'sloc_hour_distance_mean': 'mean'})
    result = pd.merge(result, sloc_hour_distance_stat, on=['geohashed_start_loc', 'hour'], how='left')
    return result

# 获取到某个地点结束的小时段距离统计
def get_eloc_hour_distance_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_hour_distance_stat = train.groupby(['geohashed_end_loc', 'hour'], as_index=False)['distance'].agg({'eloc_hour_distance_max': 'max', 'eloc_hour_distance_min': 'min', 'eloc_hour_distance_mean': 'mean'})
    result = pd.merge(result, eloc_hour_distance_stat, on=['geohashed_end_loc', 'hour'], how='left')
    return result

# 获取从某个地点出发的小时均值
def get_sloc_hour_mean(train, result):
    sloc_hour_mean = train.groupby(['geohashed_start_loc'], as_index=False)['hour'].agg({'sloc_hour_mean': 'mean'})
    result = pd.merge(result, sloc_hour_mean, on=['geohashed_start_loc'], how='left')
    return result

# 获取到某个地点结束的小时均值
def get_eloc_hour_mean(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    eloc_hour_mean = train.groupby(['geohashed_end_loc'], as_index=False)['hour'].agg({'eloc_hour_mean': 'mean'})
    result = pd.merge(result, eloc_hour_mean, on=['geohashed_end_loc'], how='left')
    return result

# 获取从某个点出发到某个地点结束的小时均值
def get_sloc_eloc_hour_mean(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    sloc_eloc_hour_mean = train.groupby(['geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['hour'].agg({'sloc_eloc_hour_mean': 'mean'})
    result = pd.merge(result, sloc_eloc_hour_mean, on=['geohashed_start_loc', 'geohashed_end_loc'], how='left')
    return result

# ----------------- 排序 -------------------

# 获取到某个目的地的距离排序
def get_eloc_distance_rank(result):
    result = rank(result, 'geohashed_end_loc', 'distance', rank_name='eloc_distance_rank', ascending=False)
    return result

# 获取从某个地点出发的距离排序
def get_sloc_distance_rank(result):
    result = rank(result, 'geohashed_start_loc', 'distance', rank_name='sloc_distance_rank', ascending=False)
    return result

# 获取到某个目的地的小时段距离排序
def get_eloc_hour_distance_rank(result):
    result = rank(result, ['geohashed_end_loc', 'hour'], 'distance', rank_name='eloc_hour_distance_rank', ascending=False)
    return result

# 获取从某个目的地出发的小时段距离排序
def get_sloc_hour_distance_rank(result):
    result = rank(result, ['geohashed_start_loc', 'hour'], 'distance', rank_name='sloc_hour_distance_rank', ascending=False)
    return result

# 获取从某个地点出发的小时段排序
def get_sloc_hour_rank(result):
    result = rank(result, 'geohashed_start_loc', 'hour', rank_name='sloc_hour_rank', ascending=False)
    return result

# 获取到某个目的地结束的小时段排序
def get_eloc_hour_rank(result):
    result = rank(result, 'geohashed_end_loc', 'hour', rank_name='eloc_hour_rank', ascending=False)
    return result

# 获取从某个地点出发到某个地点结束的小时段排序
def get_sloc_eloc_hour_rank(result):
    result = rank(result, ['geohashed_start_loc', 'geohashed_end_loc'], 'hour', rank_name='sloc_eloc_hour_rank', ascending=False)
    return result

# ----------------- 差值 -------------------

# 获取距离与从某个点出发距离统计值的绝对差值
def get_sloc_distance_stat_sub(result):
    result['sloc_distance_mean_sub'] = (result['distance'] - result['sloc_distance_mean'])
    result['sloc_distance_mean_sub_abs'] = (result['distance'] - result['sloc_distance_mean']).abs()
    return result

# 获取距离与到某个点结束距离统计值的绝对差值
def get_eloc_distance_stat_sub(result):
    result['eloc_distance_mean_sub'] = (result['distance'] - result['eloc_distance_mean'])
    result['eloc_distance_mean_sub_abs'] = (result['distance'] - result['eloc_distance_mean']).abs()
    return result

# 获取距离与从某个点出发距离统计值的各小时段绝对差值
def get_sloc_hour_distance_stat_sub(result):
    result['sloc_hour_distance_mean_sub'] = (result['distance'] - result['sloc_hour_distance_mean'])
    result['sloc_hour_distance_mean_sub_abs'] = (result['distance'] - result['sloc_hour_distance_mean']).abs()
    return result

# 获取距离与到某个点结束距离统计值的各小时段绝对差值
def get_eloc_hour_distance_stat_sub(result):
    result['eloc_hour_distance_mean_sub'] = (result['distance'] - result['eloc_hour_distance_mean'])
    result['eloc_hour_distance_mean_sub_abs'] = (result['distance'] - result['eloc_hour_distance_mean']).abs()
    return result

# 获取小时段与从某个点出发的小时均值的绝对差值
def get_hour_sloc_hour_mean_sub(result):
    result['hour_sloc_hour_mean_sub'] = (result['hour'] - result['sloc_hour_mean'])
    result['hour_sloc_hour_mean_sub_abs'] = (result['hour'] - result['sloc_hour_mean']).abs()
    return result

# 获取小时段与到某个点结束的小时均值的绝对差值
def get_hour_eloc_hour_mean_sub(result):
    result['hour_eloc_hour_mean_sub'] = (result['hour'] - result['eloc_hour_mean'])
    result['hour_eloc_hour_mean_sub_abs'] = (result['hour'] - result['eloc_hour_mean']).abs()
    return result

# 获取小时段与从某个点出发到某个点结束的小时均值的绝对差值
def get_hour_sloc_eloc_hour_mean_sub(result):
    result['hour_sloc_eloc_hour_mean_sub'] = (result['hour'] - result['sloc_eloc_hour_mean'])
    result['hour_sloc_eloc_hour_mean_sub_abs'] = (result['hour'] - result['sloc_eloc_hour_mean']).abs()
    return result

# ----------------- 比例 ------------------- 

# 获取从某个地点出发到某个地点结束的个数与从这个点出发的个数的比例
def get_sloc_eloc_count_ratio(result):
    result['sloc_eloc_count_ratio'] = result['sloc_eloc_count'] / result['sloc_count']
    return result;

# 获取从某个地点出发的小时段个数与从这个地方出发的个数的比例
def get_sloc_hour_count_ratio(result):
    result['sloc_hour_count_ratio'] = result['sloc_hour_count'] / result['sloc_count']
    return result

# 获取到某个目的地的小时段个数与到某个目的地的个数的比例
def get_eloc_hour_count_ratio(result):
    result['eloc_hour_count_ratio'] = result['eloc_hour_count'] / result['eloc_count']
    return result