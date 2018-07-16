# -*- coding:utf-8 -*-
import gc

from .user import *
from .location import *
from .latlon import *
from .other import *
from .leak import *
from .rule import *
from .filter import *

# 获取全部特征
def get_feat(train, sample):
    result = sample
    # 获取协同过滤特征：
    result = get_loc_filter(train, result)
    result = get_user_loc_filter(train, result)
    print('协同过滤特征构造完成！')
    gc.collect()
    result.fillna(-1000000, inplace=True)
    gc.collect()
    print('所有特征构造完成：\ncolumns:\n{}'.format(result.columns))
    return result
    
    # 获取距离特征：
    result = get_distance(result) # distance # dui 90 wc
    # result = result[(result['distance'] < 7200) & (result['distance'] > 100)]
    # print('过滤大小距离之后：', result.shape)
    # result = result[result['distance'] < 10000]
    # print('过滤大距离之后：', result.shape)
    print('距离特征构造完成！')
    
    # 获取小时特征：
    result = get_hour(result) # hour # dui 90 wc
    result = get_hour_count(train, result) # hour_fre # dui 90 wc
    print('小时特征构造完成！')

    # 获取用户特征
    result = get_user_count(train, result) # user_count # dui 90 wc 
    result = get_user_eloc_count(train, result) # user_eloc_count # dui 90 wc
    result = get_user_sloc_count(train, result) 
    result = get_user_sloc_eloc_count(train, result) # user_sloc_eloc_count
    result = get_user_eloc_sloc_count(train, result) # user_eloc_sloc_count
    result = get_user_eloc_sloc_rate(train, result) # dui 90 wc
    result = get_user_eloc_as_sloc_count(train, result) # user_sloc_count # dui 90 wc 
    result = get_user_sloc_as_eloc_count(train, result) # 1
    result = get_user_eloc_in_sloc_count(result) # eloc_in_sloc_count
    result = get_user_loccount(train, result)
    result = get_user_sloccount(train, result)
    result = get_user_eloccount(train, result) # dui 90 wc
    result = get_user_sloc_eloccount(train, result)
    result = get_user_eloc_sloccount(train, result)
    gc.collect()
    print('1 done!')
    result = get_user_hour_count(train, result) # user_hour_fre # dui 90 wc
    result = get_user_eloc_hour_count(train, result) # user_eloc_hour_fre # dui 90 wc
    result = get_user_sloc_hour_count(train, result) # user_sloc_hour_fre
    result = get_user_sloc_eloc_hour_count(train, result) # user_sloc_eloc_hour_fre
    result = get_user_eloc_sloc_hour_count(train, result)
    result = get_user_hour_loccount(train, result)
    result = get_user_hour_sloccount(train, result)
    result = get_user_hour_eloccount(train, result)
    result = get_user_sloc_hour_eloccount(train, result)
    result = get_user_eloc_hour_sloccount(train, result)
    gc.collect()
    print('2 done!')
    result = get_user_distance_stat(train, result) # user_dis_min, user_dis_max, user_dis_med # dui 90 wc
    result = get_user_distance_quantile(train, result) # wc
    result = get_user_eloc_distance_stat(train, result) # user_eloc_dis_max, user_eloc_dis_min, user_eloc_dis_med # dui 90 wc
    result = get_user_sloc_distance_stat(train, result) # user_sloc_dis_min, user_sloc_dis_max, user_sloc_dis_med # dui 90 wc
    result = get_user_hour_distance_stat(train, result) # dui 90 wc
    result = get_user_sloc_hour_distance_stat(train, result) # dui 90 wc
    result = get_user_eloc_hour_distance_stat(train, result)
    result = get_user_hour_stat(train, result) # 1 # dui 90 wc
    result = get_user_sloc_hour_stat(train, result) # 1
    result = get_user_eloc_hour_stat(train, result) # 1 # dui 90 wc
    result = get_user_sloc_eloc_hour_stat(train, result)
    result = get_user_most_freq_eloc(train, result) # wc
    result = get_user_eloc_lasttime(train, result) # wc
    gc.collect()
    print('3 done!')
    result = get_user_eloc_distance_rank(result) # user_sloc_dis_rank
    result = get_user_sloc_distance_rank(result) # user_eloc_dis_rank
    result = get_user_eloc_hour_distance_rank(result) # dui 90 wc
    result = get_user_sloc_hour_distance_rank(result)
    result = get_user_hour_rank(result) # 1 # dui 90 wc
    result = get_user_sloc_hour_rank(result) # 1
    result = get_user_eloc_hour_rank(result)
    result = get_user_sloc_eloc_hour_rank(result)
    gc.collect()
    print('4 done!')
    result = get_user_distance_stat_sub(result) # 1 # dui 90 wc
    result = get_user_sloc_distance_stat_sub(result) # 1 # dui 90 wc
    result = get_user_eloc_distance_stat_sub(result) # 1
    result = get_user_hour_distance_stat_sub(result) # dui 90 wc
    result = get_user_sloc_hour_distance_stat_sub(result) # dui 90 wc
    result = get_user_eloc_hour_distance_stat_sub(result)
    result = get_hour_user_hour_stat_sub(result) # 1 # dui 90 wc
    result = get_hour_user_sloc_hour_stat_sub(result) # 1
    result = get_hour_user_eloc_hour_stat_sub(result) # 1 # dui 90 wc
    result = get_hour_user_sloc_eloc_hour_stat_sub(result)
    gc.collect()
    print('5 done!')
    result = get_global_user_sloc_count_ratio(result) # wc
    result = get_user_eloc_count_ratio(result) # wc
    gc.collect()
    print('用户特征构造完成！')
    
    # # 获取地理位置特征
    result = get_eloc_count(train, result) # eloc_count # dui 90 wc
    result = get_sloc_count(train, result) # eloc_as_sloc_count # dui 90 wc
    result = get_sloc_as_eloc_count(train, result)
    result = get_eloc_as_sloc_count(train, result) # dui 90 wc
    result = get_sloc_eloc_count(train, result) # dui 90 wc
    result = get_eloc_sloc_count(train, result)
    result = get_eloc_user_count(train, result) # eloc_usercount # dui 90 wc
    result = get_sloc_user_count(train, result) # eloc_as_sloc_usercount # dui 90 wc
    result = get_sloc_as_eloc_user_count(train, result)
    result = get_eloc_as_sloc_user_count(train, result) # dui 90 wc
    result = get_sloc_eloc_user_count(train, result) # user_sloc_eloc_usercount # dui 90 wc
    result = get_eloc_sloc_user_count(train, result) # user_eloc_sloc_usercount
    result = get_sloc_eloccount(train, result) # sloc_eloccount # dui 90 wc
    result = get_eloc_sloccount(train, result) # eloc_sloccount
    gc.collect()
    print('1 done!')
    result = get_eloc_hour_count(train, result) # eloc_hour_fre # dui 90 wc
    result = get_sloc_hour_count(train, result) # sloc_hour_fre # 90 wc 最后删掉
    result = get_sloc_eloc_hour_count(train, result) # sloc_eloc_hour_fre
    result = get_eloc_sloc_hour_count(train, result)
    result = get_eloc_hour_user_count(train, result)
    result = get_sloc_hour_user_count(train, result)
    result = get_sloc_eloc_hour_user_count(train, result)
    result = get_eloc_sloc_hour_user_count(train, result)
    result = get_sloc_hour_eloccount(train, result)
    result = get_eloc_hour_sloccount(train, result)
    gc.collect()
    print('2 done!')
    result = get_sloc_distance_stat(train, result) # sloc_dis_med, sloc_dis_min, sloc_dis_max # dui 90 wc
    result = get_eloc_distance_stat(train, result) # eloc_dis_max, eloc_dis_min, eloc_dis_med # dui 90 wc
    result = get_sloc_hour_distance_stat(train, result)
    result = get_eloc_hour_distance_stat(train, result)
    result = get_sloc_hour_mean(train, result) # 1 # dui 90 wc
    result = get_eloc_hour_mean(train, result) # 1 # dui 90 wc
    result = get_sloc_eloc_hour_mean(train, result) # 1 # dui 90 wc
    gc.collect()
    print('3 done!')
    result = get_eloc_distance_rank(result) # sloc_dis_rank
    result = get_sloc_distance_rank(result) # eloc_dis_rank
    result = get_eloc_hour_distance_rank(result)
    result = get_sloc_hour_distance_rank(result)
    result = get_sloc_hour_rank(result) # 1
    result = get_eloc_hour_rank(result) # 1
    result = get_sloc_eloc_hour_rank(result) # 1
    gc.collect()
    print('4 done!')
    result = get_sloc_distance_stat_sub(result) # 1 # dui 90 wc
    result = get_eloc_distance_stat_sub(result) # 1 # dui 90 wc
    result = get_sloc_hour_distance_stat_sub(result)
    result = get_eloc_hour_distance_stat_sub(result)
    result = get_hour_sloc_hour_mean_sub(result) # 1 # dui 90 wc
    result = get_hour_eloc_hour_mean_sub(result) # 1 # dui 90 wc
    result = get_hour_sloc_eloc_hour_mean_sub(result) # 1 # dui 90 wc
    gc.collect()
    print('5 done!')
    result = get_sloc_eloc_count_ratio(result) # wc
    result = get_sloc_hour_count_ratio(result) # wc
    result = get_eloc_hour_count_ratio(result) # wc
    gc.collect()
    print('地理位置特征构造完成！')
    
    # 获取协同过滤特征：
    result = get_loc_filter(train, result)
    result = get_user_loc_filter(train, result)
    print('协同过滤特征构造完成！')

    # # 获取经纬度特征
    result = get_eloc_latlon(result) # dui 90 wc
    result = get_sloc_latlon(result) # dui 90 wc
    gc.collect()
    print('1 done!')
    result = get_eloc_sloc_latlon_sub(result) # sloc_eloc_lon_sub, sloc_eloc_lat_sub # dui 90 wc
    result = get_eloc_sloc_slope(result) # 1 # dui 90 wc
    result = get_eloc_sloc_latlon_sub_divide_distance(result) # 1 # dui 90 wc
    result = get_bearing_array(result) # wc
    gc.collect()
    print('2 done!')
    result = get_user_latlon_sub_stat(train, result) # dui 90 wc
    result = get_user_sloc_latlon_sub_stat(train, result)
    result = get_user_eloc_latlon_sub_stat(train, result) # dui 90 wc
    result = get_user_sloc_hour_latlon_sub_stat(train, result)
    result = get_user_eloc_hour_latlon_sub_stat(train, result)
    gc.collect()
    print('3 done!')
    result = get_sloc_latlon_sub_stat(train, result) # dui 90 wc
    result = get_eloc_latlon_sub_stat(train, result) # dui 90 wc
    result = get_sloc_hour_latlon_sub_stat(train, result)
    result = get_eloc_hour_latlon_sub_stat(train, result) # dui 90 wc
    gc.collect()
    print('4 done!')
    result = get_user_latlon_sub_rank(result) # dui 90 wc
    result = get_user_eloc_latlon_sub_rank(result)
    result = get_user_sloc_latlon_sub_rank(result) # dui 90 wc
    result = get_user_eloc_hour_latlon_sub_rank(result)
    result = get_user_sloc_hour_latlon_sub_rank(result) # dui 90 wc
    gc.collect()
    print('5 done!')
    result = get_eloc_latlon_sub_rank(result) # dui 90 wc
    result = get_sloc_latlon_sub_rank(result)
    result = get_eloc_hour_latlon_sub_rank(result)
    result = get_sloc_hour_latlon_sub_rank(result)
    gc.collect()
    print('6 done!')
    result = get_user_latlon_sub_stat_sub(result)
    result = get_user_sloc_latlon_sub_stat_sub(result)
    result = get_user_eloc_latlon_sub_stat_sub(result)
    result = get_user_sloc_hour_latlon_sub_stat_sub(result)
    result = get_user_eloc_hour_latlon_sub_stat_sub(result)
    gc.collect()
    print('7 done!')
    result = get_sloc_latlon_sub_stat_sub(result)
    result = get_eloc_latlon_sub_stat_sub(result)
    result = get_sloc_hour_latlon_sub_stat_sub(result)
    result = get_eloc_hour_latlon_sub_stat_sub(result)
    gc.collect()
    print('经纬度特征构造完成！')
    
    # 获取Leak特征：
    result = get_eloc_user_sloc_leak(result) # 1 # dui 90 wc
    result = get_eloc_bike_sloc_leak(result) # 1 # dui 90 wc
    print('Leak特征构造完成！')
    
    # 获取规则特征
    result = get_user_rule(result) # dui 90 wc
    result = get_user_didi(train, result) # dui 90 wc
    gc.collect()
    print('1 done!')
    result = get_loc_rule(result) # dui 90 wc
    result = get_loc_didi(train, result) # dui 90 wc
    gc.collect()
    print('规则特征构造完成！')
    
    # 删除无用特征
    # result.drop(['sloc_lon_sub_max', 'user_hour_distance_mean', 'user_sloc_distance_mean', 'user_eloc_hour_max', 'sloc_lat_sub_max', 'eloc_bike_last_sloc_distance', 'hour', 'eloc_bike_last_sloc_speed', 'user_eloc_hour_min', 'eloc_hour_count', 'user_lon_sub_max', 'eloc_hour_lon_sub_max', 'user_hour_max', 'user_lat_sub_max', 'eloc_hour_lat_sub_min', 'hour_count', 'eloc_hour_lat_sub_max', 'eloc_hour_lon_sub_min', 'user_eloc_distance_min', 'user_hour_count_rate', 'user_eloc_distance_mean', 'user_hour_min', 'user_hour_eloc_rate', 'eloc_lon_sub_min', 'user_eloc_lon_sub_mean', 'user_eloc_lat_sub_mean', 'user_eloc_hour_mean', 'user_eloc_lon_sub_min', 'user_eloc_lat_sub_min', 'user_eloc_lon_sub_max', 'sloc_lat_sub_min', 'user_eloc_hour_count', 'eloc_lat_sub_min', 'user_eloc_count_rate', 'eloc_count_rate', 'sloc_lon_sub_min', 'user_eloc_lat_sub_max', 'hour_count_rate', 'user_end_loc_sample', 'sloc_lat', 'user_lat_sub_mean', 'sloc_lon', 'user_hour_distance_mean_sub', 'sloc_distance_max', 'user_lon_sub_mean', 'user_distance_mean', 'sloc_distance_mean_sub_abs', 'user_sloc_distance_min', 'sloc_lat_sub_mean', 'eloc_lon_sub_max', 'user_sloc_distance_max', 'eloc_distance_max', 'hour_user_hour_mean_sub', 'eloc_as_sloc_count', 'sloc_distance_min', 'eloc_lat_sub_max', 'bike_next_sloc_sample', 'user_rule', 'eloc_distance_mean_sub_abs', 'user_lat_sub_min', 'user_lon_sub_min', 'loc_to_loc_sample', 'user_sloc_hour_distance_min', 'user_sloc_hour_distance_max', 'user_sloc_hour_distance_mean', 'user_sloc_hour_distance_mean_sub', 'sloc_hour_count'], axis=1, inplace=True)
    
    # 删除无用特征
    # result.drop(['user_eloc_hour_lon_sub_mean_sub_abs', 'user_sloc_lon_sub_mean_sub'], axis=1, inplace=True)
    
    result.fillna(-1000000, inplace=True)
    print('所有特征构造完成：\ncolumns:\n{}'.format(result.columns))
    return result