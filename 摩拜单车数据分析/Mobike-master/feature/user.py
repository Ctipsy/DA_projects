# -*- coding:utf-8 -*-
import pandas as pd
import os
import numpy as np
from .other import get_distance
from .latlon import get_sloc_latlon, get_eloc_latlon, get_eloc_sloc_latlon_sub, get_eloc_sloc_slope, get_eloc_sloc_latlon_sub_divide_distance, get_bearing_array
os.path.join('..')
from utils import rank

'''
	获取用户特征
'''

# ----------------- 计数 -------------------

# 获取用户历史出行次数
def get_user_count(train, result):
    user_count = train.groupby('userid', as_index=False)['orderid'].agg({'user_count': 'count'})
    result = pd.merge(result, user_count, on=['userid'], how='left')
    return result

# 获取用户去过某个地点的历史出行次数
def get_user_eloc_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_count = train.groupby(['userid', 'geohashed_end_loc'], as_index=False)['userid'].agg({'user_eloc_count': 'count'})
    result = pd.merge(result, user_eloc_count, on=['userid', 'geohashed_end_loc'], how='left')
    return result

# 获取用户从某个地方出发的历史出行次数
def get_user_sloc_count(train, result):
    user_sloc_count = train.groupby(['userid', 'geohashed_start_loc'], as_index=False)['userid'].agg({'user_sloc_count': 'count'})
    result = pd.merge(result, user_sloc_count, on=['userid', 'geohashed_start_loc'], how='left')
    return result

# 获取用户从某个地方出发到某个地方结束的历史出行次数
def get_user_sloc_eloc_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_sloc_eloc_count = train.groupby(['userid', 'geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['userid'].agg({'user_sloc_eloc_count': 'count'})
    result = pd.merge(result, user_sloc_eloc_count, on=['userid', 'geohashed_start_loc', 'geohashed_end_loc'], how='left')
    return result

# 获取用户从某个目的地出发到某个出发地结束的历史返程次数
def get_user_eloc_sloc_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_sloc_count = train.groupby(['userid', 'geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['userid'].agg({'user_eloc_sloc_count': 'count'})
    user_eloc_sloc_count.rename(columns={'geohashed_start_loc':'geohashed_end_loc', 'geohashed_end_loc':'geohashed_start_loc'}, inplace=True)
    result = pd.merge(result, user_eloc_sloc_count, on=['userid', 'geohashed_start_loc', 'geohashed_end_loc'], how='left')
    return result

# 获取用户的返程比例
def get_user_eloc_sloc_rate(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_sloc_count = train.groupby(['userid', 'geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['userid'].agg({'user_eloc_sloc_count': 'count'})
    user_eloc_sloc_count.rename(columns={'geohashed_start_loc':'geohashed_end_loc', 'geohashed_end_loc':'geohashed_start_loc'}, inplace=True)
    restmp = pd.merge(train, user_eloc_sloc_count, on=['userid', 'geohashed_start_loc', 'geohashed_end_loc'], how='left')
    restmp = restmp.groupby('userid', as_index=False)['user_eloc_sloc_count'].agg({'user_eloc_sloc_rate': lambda x: np.sum(x>0)/np.size(x)})
    result = pd.merge(result, restmp, on='userid', how='left')
    return result

# 获取用户目的地点作为出发地的次数
def get_user_eloc_as_sloc_count(train, result):
    user_eloc_as_sloc_count = train.groupby(['userid', 'geohashed_start_loc'], as_index=False)['userid'].agg({'user_eloc_as_sloc_count': 'count'})
    user_eloc_as_sloc_count.rename(columns={'geohashed_start_loc': 'geohashed_end_loc'}, inplace=True)
    result = pd.merge(result, user_eloc_as_sloc_count, on=['userid', 'geohashed_end_loc'], how='left')
    return result

# 获取用户出发地点作为目的地的次数
def get_user_sloc_as_eloc_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_sloc_as_eloc_count = train.groupby(['userid', 'geohashed_end_loc'], as_index=False)['userid'].agg({'user_sloc_as_eloc_count': 'count'})
    user_sloc_as_eloc_count.rename(columns={'geohashed_end_loc': 'geohashed_start_loc'}, inplace=True)
    result = pd.merge(result, user_sloc_as_eloc_count, on=['userid', 'geohashed_start_loc'], how='left')
    return result

# 获取用户目的地出现在出发地中的个数
def get_user_eloc_in_sloc_count(result):
    user_eloc_in_sloc_count = result.groupby(['userid', 'geohashed_start_loc'], as_index=False)['orderid'].agg({'user_eloc_in_sloc_count': lambda x: np.unique(x).size})
    user_eloc_in_sloc_count.rename(columns={'geohashed_start_loc': 'geohashed_end_loc'}, inplace=True)
    result = pd.merge(result, user_eloc_in_sloc_count, on=['userid', 'geohashed_end_loc'], how='left')
    return result

# 获取用户涉及到的地点个数
def get_user_loccount(train, result):
    user_sloc = train[['userid', 'geohashed_start_loc']]
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc = train[['userid', 'geohashed_end_loc']].rename(columns={'geohashed_end_loc': 'geohashed_start_loc'}, inplace=True)
    user_loc = pd.concat([user_sloc, user_eloc])
    user_loccount = user_loc.groupby('userid', as_index=False)['geohashed_start_loc'].agg({'user_loccount': lambda x: np.unique(x).size})
    result = pd.merge(result, user_loccount, on=['userid'], how='left')
    return result

# 获取用户出发的出发地个数
def get_user_sloccount(train, result):
    user_sloccount = train.groupby('userid', as_index=False)['geohashed_start_loc'].agg({'user_sloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, user_sloccount, on=['userid'], how='left')
    return result

# 获取用户到达的目的地个数
def get_user_eloccount(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloccount = train.groupby('userid', as_index=False)['geohashed_end_loc'].agg({'user_eloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, user_eloccount, on=['userid'], how='left')
    return result

# 获取用户从某个地方出发到的目的地数目
def get_user_sloc_eloccount(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_sloc_eloccount = train.groupby(['userid', 'geohashed_start_loc'], as_index=False)['geohashed_end_loc'].agg({'user_sloc_eloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, user_sloc_eloccount, on=['userid', 'geohashed_start_loc'], how='left')
    return result

# 获取用户到某个地方结束的出发地数目
def get_user_eloc_sloccount(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_sloccount = train.groupby(['userid', 'geohashed_end_loc'], as_index=False)['geohashed_start_loc'].agg({'user_eloc_sloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, user_eloc_sloccount, on=['userid', 'geohashed_end_loc'], how='left')
    return result

# 获取用户在每个小时段的出行订单数
def get_user_hour_count(train, result):
    user_hour_count = train.groupby(['userid', 'hour'], as_index=False)['orderid'].agg({'user_hour_count': 'count'})
    result = pd.merge(result, user_hour_count, on=['userid', 'hour'], how='left')
    return result

# 获取用户在每个小时段从某个地方出发的订单数
def get_user_sloc_hour_count(train, result):
    user_sloc_hour_count = train.groupby(['userid', 'geohashed_start_loc', 'hour'], as_index=False)['orderid'].agg({'user_sloc_hour_count': 'count'})
    result = pd.merge(result, user_sloc_hour_count, on=['userid', 'geohashed_start_loc', 'hour'], how='left')
    return result

# 获取用户在每个小时段到某个地方结束的订单数
def get_user_eloc_hour_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_hour_count = train.groupby(['userid', 'geohashed_end_loc', 'hour'], as_index=False)['orderid'].agg({'user_eloc_hour_count': 'count'})
    result = pd.merge(result, user_eloc_hour_count, on=['userid', 'geohashed_end_loc', 'hour'], how='left')
    return result

# 获取用户在每个小时段从某个地方出发到某个地方结束的订单数
def get_user_sloc_eloc_hour_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_sloc_eloc_hour_count = train.groupby(['userid', 'geohashed_start_loc', 'geohashed_end_loc', 'hour'], as_index=False)['orderid'].agg({'user_sloc_eloc_hour_count': 'count'})
    result = pd.merge(result, user_sloc_eloc_hour_count, on=['userid', 'geohashed_start_loc', 'geohashed_end_loc', 'hour'], how='left')
    return result

# 获取用户在每个小时段从某个地方出发到某个地方结束的返程订单数
def get_user_eloc_sloc_hour_count(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_sloc_hour_count = train.groupby(['userid', 'geohashed_start_loc', 'geohashed_end_loc', 'hour'], as_index=False)['orderid'].agg({'user_eloc_sloc_hour_count': 'count'})
    user_eloc_sloc_hour_count.rename(columns={'geohashed_start_loc': 'geohashed_end_loc', 'geohashed_end_loc': 'geohashed_start_loc'}, inplace=True)
    result = pd.merge(result, user_eloc_sloc_hour_count, on=['userid', 'geohashed_start_loc', 'geohashed_end_loc', 'hour'], how='left') # 1
    return result

# 获取用户每个小时段涉及到的地点数
def get_user_hour_loccount(train, result):
    user_hour_sloc = train[['userid', 'hour', 'geohashed_start_loc']]
    train = train[~train.geohashed_end_loc.isnull()]
    user_hour_eloc = train[['userid', 'hour', 'geohashed_end_loc']].rename(columns={'geohashed_end_loc': 'geohashed_start_loc'}, inplace=True)
    user_hour_loc = pd.concat([user_hour_sloc, user_hour_eloc])
    user_hour_loccount = user_hour_loc.groupby(['userid', 'hour'], as_index=False)['geohashed_start_loc'].agg({'user_hour_loccount': lambda x: np.unique(x).size})
    result = pd.merge(result, user_hour_loccount, on=['userid', 'hour'], how='left')
    return result

# 获取用户每个小时段出发的出发地个数
def get_user_hour_sloccount(train, result):
    user_hour_sloccount = train.groupby(['userid', 'hour'], as_index=False)['geohashed_start_loc'].agg({'user_hour_sloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, user_hour_sloccount, on=['userid', 'hour'], how='left') # 4
    return result

# 获取用户每个小时段到达的目的地个数
def get_user_hour_eloccount(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_hour_eloccount = train.groupby(['userid', 'hour'], as_index=False)['geohashed_end_loc'].agg({'user_hour_eloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, user_hour_eloccount, on=['userid', 'hour'], how='left')
    return result

# 获取用户每个小时段从某个地方出发到的目的地数目
def get_user_sloc_hour_eloccount(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_sloc_hour_eloccount = train.groupby(['userid', 'geohashed_start_loc', 'hour'], as_index=False)['geohashed_end_loc'].agg({'user_sloc_hour_eloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, user_sloc_hour_eloccount, on=['userid', 'geohashed_start_loc', 'hour'], how='left')
    return result

# 获取用户每个小时段到某个地方结束的出发地数目
def get_user_eloc_hour_sloccount(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_hour_sloccount = train.groupby(['userid', 'geohashed_end_loc', 'hour'], as_index=False)['geohashed_start_loc'].agg({'user_eloc_hour_sloccount': lambda x: np.unique(x).size})
    result = pd.merge(result, user_eloc_hour_sloccount, on=['userid', 'geohashed_end_loc', 'hour'], how='left') # 9
    return result

# ----------------- 统计 -------------------

# 获取用户出行距离的统计值
def get_user_distance_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_distance_stat = train.groupby('userid', as_index=False)['distance'].agg({'user_distance_max': 'max', 'user_distance_min': 'min', 'user_distance_mean': 'mean'})
    result = pd.merge(result, user_distance_stat, on=['userid'], how='left')
    user_manhattan_stat = train.groupby('userid', as_index=False)['manhattan'].agg({'user_manhattan_max': 'max', 'user_manhattan_min': 'min', 'user_manhattan_mean': 'mean'})
    result = pd.merge(result, user_manhattan_stat, on=['userid'], how='left')
    return result

# 获取用户出行距离的分位点
def get_user_distance_quantile(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_distance_quantile = train.groupby('userid')['distance'].quantile(0.2).reset_index()
    user_distance_quantile.rename(columns={'distance': 'user_distance_quantile_2'}, inplace=True)
    result = pd.merge(result, user_distance_quantile, on='userid', how='left')
    user_manhattan_quantile = train.groupby('userid')['manhattan'].quantile(0.2).reset_index()
    user_manhattan_quantile.rename(columns={'manhattan': 'user_manhattan_quantile_2'}, inplace=True)
    result = pd.merge(result, user_manhattan_quantile, on='userid', how='left')
    user_distance_quantile = train.groupby('userid')['distance'].quantile(0.8).reset_index()
    user_distance_quantile.rename(columns={'distance': 'user_distance_quantile_8'}, inplace=True)
    result = pd.merge(result, user_distance_quantile, on='userid', how='left')
    return result

# 获取用户从某个地点出发的出行距离统计值
def get_user_sloc_distance_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_sloc_distance_stat = train.groupby(['userid', 'geohashed_start_loc'], as_index=False)['distance'].agg({'user_sloc_distance_max': 'max', 'user_sloc_distance_min': 'min', 'user_sloc_distance_mean': 'mean'})
    result = pd.merge(result, user_sloc_distance_stat, on=['userid', 'geohashed_start_loc'], how='left')
    user_sloc_manhattan_stat = train.groupby(['userid', 'geohashed_start_loc'], as_index=False)['manhattan'].agg({'user_sloc_manhattan_max': 'max', 'user_sloc_manhattan_min': 'min', 'user_sloc_manhattan_mean': 'mean'})
    result = pd.merge(result, user_sloc_manhattan_stat, on=['userid', 'geohashed_start_loc'], how='left')
    return result

# 获取用户到某个地点结束的出行距离统计值
def get_user_eloc_distance_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_distance_stat = train.groupby(['userid', 'geohashed_end_loc'], as_index=False)['distance'].agg({'user_eloc_distance_max': 'max', 'user_eloc_distance_min': 'min', 'user_eloc_distance_mean': 'mean'})
    result = pd.merge(result, user_eloc_distance_stat, on=['userid', 'geohashed_end_loc'], how='left')
    return result

# 获取用户各时间段出行距离的统计值
def get_user_hour_distance_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_hour_distance_stat = train.groupby(['userid', 'hour'], as_index=False)['distance'].agg({'user_hour_distance_max': 'max', 'user_hour_distance_min': 'min', 'user_hour_distance_mean': 'mean'})
    result = pd.merge(result, user_hour_distance_stat, on=['userid', 'hour'], how='left')
    user_hour_manhattan_stat = train.groupby(['userid', 'hour'], as_index=False)['manhattan'].agg({'user_hour_manhattan_max': 'max', 'user_hour_manhattan_min': 'min', 'user_hour_manhattan_mean': 'mean'})
    result = pd.merge(result, user_hour_manhattan_stat, on=['userid', 'hour'], how='left')
    return result

# 获取用户各时间段从某个地点出发的出行距离统计值
def get_user_sloc_hour_distance_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_sloc_hour_distance_stat = train.groupby(['userid', 'geohashed_start_loc', 'hour'], as_index=False)['distance'].agg({'user_sloc_hour_distance_max': 'max', 'user_sloc_hour_distance_min': 'min', 'user_sloc_hour_distance_mean': 'mean'})
    result = pd.merge(result, user_sloc_hour_distance_stat, on=['userid', 'geohashed_start_loc', 'hour'], how='left')
    user_sloc_hour_manhattan_stat = train.groupby(['userid', 'geohashed_start_loc', 'hour'], as_index=False)['manhattan'].agg({'user_sloc_hour_manhattan_max': 'max', 'user_sloc_hour_manhattan_min': 'min', 'user_sloc_hour_manhattan_mean': 'mean'})
    result = pd.merge(result, user_sloc_hour_manhattan_stat, on=['userid', 'geohashed_start_loc', 'hour'], how='left')
    return result

# 获取用户各时间段到某个地点结束的出行距离统计值
def get_user_eloc_hour_distance_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_hour_distance_stat = train.groupby(['userid', 'geohashed_end_loc', 'hour'], as_index=False)['distance'].agg({'user_eloc_hour_distance_max': 'max', 'user_eloc_hour_distance_min': 'min', 'user_eloc_hour_distance_mean': 'mean'})
    result = pd.merge(result, user_eloc_hour_distance_stat, on=['userid', 'geohashed_end_loc', 'hour'], how='left')
    return result

# 获取用户出行的小时段统计值
def get_user_hour_stat(train, result):
    user_hour_stat = train.groupby(['userid'], as_index=False)['hour'].agg({'user_hour_max': 'max', 'user_hour_min': 'min', 'user_hour_mean': 'mean'})
    result = pd.merge(result, user_hour_stat, on=['userid'], how='left')
    return result

# 获取用户从某个地点出行的小时段统计值
def get_user_sloc_hour_stat(train, result):
    user_sloc_hour_stat = train.groupby(['userid', 'geohashed_start_loc'], as_index=False)['hour'].agg({'user_sloc_hour_max': 'max', 'user_sloc_hour_min': 'min', 'user_sloc_hour_mean': 'mean'})
    result = pd.merge(result, user_sloc_hour_stat, on=['userid', 'geohashed_start_loc'], how='left')
    return result

# 获取用户到某个地点结束的小时段统计值
def get_user_eloc_hour_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_hour_stat = train.groupby(['userid', 'geohashed_end_loc'], as_index=False)['hour'].agg({'user_eloc_hour_max': 'max', 'user_eloc_hour_min': 'min', 'user_eloc_hour_mean': 'mean'})
    result = pd.merge(result, user_eloc_hour_stat, on=['userid', 'geohashed_end_loc'], how='left')
    return result

# 获取用户从某个地点出发到某个地点结束的小时段统计值
def get_user_sloc_eloc_hour_stat(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_sloc_eloc_hour_stat = train.groupby(['userid', 'geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['hour'].agg({'user_sloc_eloc_hour_max': 'max', 'user_sloc_eloc_hour_min': 'min', 'user_sloc_eloc_hour_mean': 'mean'}) # 6
    # user_sloc_eloc_hour_stat = train.groupby(['userid', 'geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['hour'].agg({'user_sloc_eloc_hour_min': 'min', 'user_sloc_eloc_hour_mean': 'mean'})
    result = pd.merge(result, user_sloc_eloc_hour_stat, on=['userid', 'geohashed_start_loc', 'geohashed_end_loc'], how='left')
    return result

# 获取用户到过最多的地点的各信息
def get_user_most_freq_eloc(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    user_eloc_count = train.groupby(['userid', 'geohashed_end_loc'], as_index=False)['userid'].agg({'user_eloc_count': 'count'})
    user_most_freq_eloc = user_eloc_count.sort_values(by=['userid', 'user_eloc_count']).groupby('userid', as_index=False).last()[['userid', 'geohashed_end_loc']]
    user_most_freq_eloc.rename(columns={'geohashed_end_loc': 'user_most_freq_eloc'}, inplace=True)
    result = pd.merge(result, user_most_freq_eloc, on='userid', how='left')
    restmp = result[['orderid', 'geohashed_start_loc', 'user_most_freq_eloc']];
    restmp.rename(columns={'user_most_freq_eloc': 'geohashed_end_loc'}, inplace=True)
    restmp = get_distance(restmp)
    restmp = get_sloc_latlon(restmp)
    restmp = pd.merge(restmp, get_eloc_latlon(restmp[~restmp.geohashed_end_loc.isnull()][['orderid', 'geohashed_end_loc']]), on=['orderid', 'geohashed_end_loc'], how='left')
    restmp = get_eloc_sloc_latlon_sub(restmp)
    restmp = get_eloc_sloc_slope(restmp)
    restmp = get_eloc_sloc_latlon_sub_divide_distance(restmp)
    restmp = get_bearing_array(restmp)
    result['user_most_freq_eloc_distance'] = restmp['distance']
    result['user_most_freq_eloc_distance_sub'] = result['distance'] - result['user_most_freq_eloc_distance']
    result['user_most_freq_eloc_distance_sub_abs'] = (result['distance'] - result['user_most_freq_eloc_distance']).abs()
    result['user_most_freq_eloc_manhattan_distance'] = restmp['manhattan']
    result['user_most_freq_eloc_manhattan_sub'] = result['manhattan'] - result['user_most_freq_eloc_manhattan_distance']
    result['user_most_freq_eloc_manhattan_sub_abs'] = (result['manhattan'] - result['user_most_freq_eloc_manhattan_distance']).abs()
    result['user_most_freq_eloc_lon_sub'] = restmp['eloc_sloc_lon_sub']
    result['user_most_freq_eloc_lat_sub'] = restmp['eloc_sloc_lat_sub']
    result['user_most_freq_eloc_slope'] = restmp['eloc_sloc_latlon_slope']
    result['user_most_freq_eloc_lat_sub_divide_distance'] = restmp['eloc_sloc_lat_sub_divide_distance']
    result['user_most_freq_eloc_lon_sub_divide_distance'] = restmp['eloc_sloc_lon_sub_divide_distance']
    result['user_most_freq_eloc_degree'] = restmp['degree']
    result.drop(['user_most_freq_eloc'], axis=1, inplace=True)
    return result

# 获取用户到某个地点的最后一次时间与当前的时间差
def get_user_eloc_lasttime(train, result):
    train = train[~train.geohashed_end_loc.isnull()]
    train = train.sort_values(by='starttime')
    user_eloc_last = train.groupby(['userid','geohashed_end_loc'], as_index=False).last()[['userid','geohashed_end_loc', 'starttime']]
    user_eloc_last.rename(columns={'starttime': 'user_eloc_lasttime'}, inplace=True)
    result = pd.merge(result, user_eloc_last, on=['userid', 'geohashed_end_loc'], how='left')
    result['user_eloc_lasttime'] = (pd.DatetimeIndex(result.starttime) - pd.DatetimeIndex(result.user_eloc_lasttime)).total_seconds().values
    return result

# ----------------- 排序 -------------------

# 获取用户到某个地点结束的距离排序
def get_user_eloc_distance_rank(result):
    result = rank(result, ['userid', 'geohashed_end_loc'], 'distance', rank_name='user_eloc_distance_rank', ascending=False)
    return result

# 获取用户从某个地点出发的距离排序
def get_user_sloc_distance_rank(result):
    result = rank(result, ['userid', 'geohashed_start_loc'], 'distance', rank_name='user_sloc_distance_rank', ascending=False)
    return result

# 获取用户各小时段到某个地点结束的距离排序
def get_user_eloc_hour_distance_rank(result):
    result = rank(result, ['userid', 'geohashed_start_loc', 'hour'], 'distance', rank_name='user_eloc_hour_distance_rank', ascending=False)
    return result

# 获取用户各小时段从某个地点出发的距离排序
def get_user_sloc_hour_distance_rank(result):
    result = rank(result, ['userid', 'geohashed_end_loc', 'hour'], 'distance', rank_name='user_sloc_hour_distance_rank', ascending=False)
    return result

# 获取用户出行时间的小时段排序
def get_user_hour_rank(result):
    result = rank(result, 'userid', 'hour', rank_name='user_hour_rank', ascending=False)
    return result

# 获取用户从某个地点出发的出行时间的小时段排序
def get_user_sloc_hour_rank(result):
    result = rank(result, ['userid', 'geohashed_start_loc'], 'hour', rank_name='user_sloc_hour_rank', ascending=False)
    return result

# 获取用户到某个地点结束的出行时间的小时段排序
def get_user_eloc_hour_rank(result):
    result = rank(result, ['userid', 'geohashed_end_loc'], 'hour', rank_name='user_eloc_hour_rank', ascending=False)
    return result

# 获取用户从某个地点出发到某个地点结束的出行时间的小时段排序
def get_user_sloc_eloc_hour_rank(result):
    result = rank(result, ['userid', 'geohashed_start_loc', 'geohashed_end_loc'], 'hour', rank_name='user_sloc_eloc_hour_rank', ascending=False) # 5
    return result

# ----------------- 差值 -------------------

# 获取实际距离与用户出行距离统计值的(绝对)差值
def get_user_distance_stat_sub(result):
    result['user_distance_mean_sub'] = (result['distance'] - result['user_distance_mean'])
    result['user_distance_mean_sub_abs'] = (result['distance'] - result['user_distance_mean']).abs()
    result['user_manhattan_mean_sub'] = (result['manhattan'] - result['user_manhattan_mean'])
    result['user_manhattan_mean_sub_abs'] = (result['manhattan'] - result['user_manhattan_mean']).abs()
    return result

# 获取实际距离与用户从某个点出发距离统计值的(绝对)差值
def get_user_sloc_distance_stat_sub(result):
    result['user_sloc_distance_mean_sub'] = (result['distance'] - result['user_sloc_distance_mean'])
    result['user_sloc_distance_mean_sub_abs'] = (result['distance'] - result['user_sloc_distance_mean']).abs()
    result['user_sloc_manhattan_mean_sub'] = (result['manhattan'] - result['user_sloc_manhattan_mean'])
    result['user_sloc_manhattan_mean_sub_abs'] = (result['manhattan'] - result['user_sloc_manhattan_mean']).abs()
    return result

# 获取实际距离与用户到某个点结束距离统计值的(绝对)差值
def get_user_eloc_distance_stat_sub(result):
    result['user_eloc_distance_mean_sub'] = (result['distance'] - result['user_eloc_distance_mean'])
    result['user_eloc_distance_mean_sub_abs'] = (result['distance'] - result['user_eloc_distance_mean']).abs()
    return result

# 获取实际距离与用户出行距离统计值的各小时段(绝对)差值
def get_user_hour_distance_stat_sub(result):
    result['user_hour_distance_mean_sub'] = (result['distance'] - result['user_hour_distance_mean'])
    result['user_hour_distance_mean_sub_abs'] = (result['distance'] - result['user_hour_distance_mean']).abs()
    result['user_hour_manhattan_mean_sub'] = (result['manhattan'] - result['user_hour_manhattan_mean'])
    result['user_hour_manhattan_mean_sub_abs'] = (result['manhattan'] - result['user_hour_manhattan_mean']).abs()
    return result

# 获取实际距离与用户从某个点出发距离统计值的各小时段(绝对)差值
def get_user_sloc_hour_distance_stat_sub(result):
    result['user_sloc_hour_distance_mean_sub'] = (result['distance'] - result['user_sloc_hour_distance_mean'])
    result['user_sloc_hour_distance_mean_sub_abs'] = (result['distance'] - result['user_sloc_hour_distance_mean']).abs()
    result['user_sloc_hour_manhattan_mean_sub'] = (result['manhattan'] - result['user_sloc_hour_manhattan_mean'])
    result['user_sloc_hour_manhattan_mean_sub_abs'] = (result['manhattan'] - result['user_sloc_hour_manhattan_mean']).abs()
    return result

# 获取实际距离与用户到某个点结束距离统计值的各小时段(绝对)差值
def get_user_eloc_hour_distance_stat_sub(result):
    result['user_eloc_hour_distance_mean_sub'] = (result['distance'] - result['user_eloc_hour_distance_mean'])
    result['user_eloc_hour_distance_mean_sub_abs'] = (result['distance'] - result['user_eloc_hour_distance_mean']).abs()
    return result

# 获取小时段与用户出行的小时段统计值的(绝对)差值
def get_hour_user_hour_stat_sub(result):
    result['hour_user_hour_mean_sub'] = (result['hour'] - result['user_hour_mean'])
    result['hour_user_hour_mean_sub_abs'] = (result['hour'] - result['user_hour_mean']).abs()
    return result

# 获取小时段与用户从某个地方出发的小时段统计值的(绝对)差值
def get_hour_user_sloc_hour_stat_sub(result):
    result['hour_user_sloc_hour_mean_sub'] = (result['hour'] - result['user_sloc_hour_mean'])
    result['hour_user_sloc_hour_mean_sub_abs'] = (result['hour'] - result['user_sloc_hour_mean']).abs()
    return result

# 获取小时段与用户到某个地方结束的小时段统计值的(绝对)差值
def get_hour_user_eloc_hour_stat_sub(result):
    result['hour_user_eloc_hour_mean_sub'] = (result['hour'] - result['user_eloc_hour_mean'])
    result['hour_user_eloc_hour_mean_sub_abs'] = (result['hour'] - result['user_eloc_hour_mean']).abs()
    return result

# 获取小时段与用户从某个地点出发到某个地方结束的小时段统计值的(绝对)差值
def get_hour_user_sloc_eloc_hour_stat_sub(result):
    result['hour_user_sloc_eloc_hour_mean_sub'] = (result['hour'] - result['user_sloc_eloc_hour_mean'])
    result['hour_user_sloc_eloc_hour_mean_sub_abs'] = (result['hour'] - result['user_sloc_eloc_hour_mean']).abs()
    return result

# ----------------- 比例 -------------------

# 获取全局中用户目的地出现在出发地中的个数占用户出行次数的比例
def get_global_user_sloc_count_ratio(result):
    train = pd.read_csv('../../MOBIKE_CUP_2017/train.csv')
    test = pd.read_csv('../../MOBIKE_CUP_2017/test.csv')
    train = pd.concat([train, test])
    user_sloc_count = train.groupby(['userid','geohashed_start_loc'])['userid'].agg({'global_user_sloc_count_ratio': 'count'})
    user_count = train.groupby(['userid'])['userid'].agg({'global_user_sloc_count_ratio': 'count'})  
    user_sloc_count = user_sloc_count.div(user_count).reset_index()
    user_sloc_count.rename(columns={'geohashed_start_loc':'geohashed_end_loc'},inplace=True)
    result = pd.merge(result, user_sloc_count, on=['userid', 'geohashed_end_loc'], how='left')
    return result

# 获取用户到某个目的地的个数占用户出行总数的比例
def get_user_eloc_count_ratio(result):
    result['user_eloc_count_ratio'] = result['user_eloc_count'] / result['user_count']
    return result