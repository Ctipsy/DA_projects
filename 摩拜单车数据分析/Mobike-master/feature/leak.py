# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
from .other import get_distance

'''
    获取Leak特征
'''

# 获取目标地点与用户上一次、下一次出发地点的距离、时间差和速度
def get_eloc_user_sloc_leak(result):
    user_order = result[['orderid', 'userid', 'geohashed_start_loc', 'starttime', 'sloc_lat', 'sloc_lon']].drop_duplicates()
    user_order.sort_values(by=['userid', 'starttime'], inplace=True, ascending=True)
    user_order['last_userid'] = user_order.userid.shift(1)
    user_order['next_userid'] = user_order.userid.shift(-1)
    user_order['last_starttime'] = user_order.starttime.shift(1)
    user_order['user_last_order_time_diff'] = (pd.DatetimeIndex(user_order['starttime'])-pd.DatetimeIndex(user_order['last_starttime'])).total_seconds()
    user_order['next_starttime'] = user_order.starttime.shift(-1)
    user_order['user_next_order_time_diff'] = (pd.DatetimeIndex(user_order['starttime'])-pd.DatetimeIndex(user_order['next_starttime'])).total_seconds()
    user_order['last_sloc'] = user_order.geohashed_start_loc.shift(1)
    user_order['next_sloc'] = user_order.geohashed_start_loc.shift(-1)
    user_order['last_sloc_lat'] = user_order.sloc_lat.shift(1)
    user_order['next_sloc_lat'] = user_order.sloc_lat.shift(-1)
    user_order['last_sloc_lon'] = user_order.sloc_lon.shift(1)
    user_order['next_sloc_lon'] = user_order.sloc_lon.shift(-1)
    user_order.drop(['geohashed_start_loc', 'starttime', 'last_starttime', 'next_starttime', 'sloc_lat', 'sloc_lon'], axis=1, inplace=True)

    restmp = pd.merge(result[['orderid', 'geohashed_end_loc', 'eloc_lat', 'eloc_lon']], user_order, on='orderid', how='left')
    restmp.rename(columns={'last_sloc': 'geohashed_start_loc'}, inplace=True)
    distance = get_distance(restmp)
    restmp['eloc_user_last_sloc_distance'] = distance['distance']
    restmp['eloc_user_last_sloc_manhattan'] = distance['manhattan']

    restmp['eloc_user_last_sloc_lat_sub'] = restmp.eloc_lat - restmp.last_sloc_lat
    restmp['eloc_user_last_sloc_lon_sub'] = restmp.eloc_lon - restmp.last_sloc_lon
    restmp.drop(['geohashed_start_loc', 'distance', 'last_sloc_lat', 'last_sloc_lon', 'manhattan'], axis=1, inplace=True)
    restmp['eloc_user_last_sloc_speed'] = restmp.eloc_user_last_sloc_distance / restmp.user_last_order_time_diff
    restmp['eloc_user_last_sloc_manhattan_speed'] = restmp.eloc_user_last_sloc_manhattan / restmp.user_last_order_time_diff
    restmp['eloc_user_last_sloc_latlon_slope'] = restmp.eloc_user_last_sloc_lat_sub / restmp.eloc_user_last_sloc_lon_sub
    restmp['eloc_user_last_sloc_lat_sub_divide_distance'] = restmp.eloc_user_last_sloc_lat_sub / restmp.eloc_user_last_sloc_distance
    restmp['eloc_user_last_sloc_lon_sub_divide_distance'] = restmp.eloc_user_last_sloc_lon_sub / restmp.eloc_user_last_sloc_distance
    
    restmp.rename(columns={'next_sloc': 'geohashed_start_loc'}, inplace=True)
    distance = get_distance(restmp)
    restmp['eloc_user_next_sloc_distance'] = distance['distance']
    restmp['eloc_user_next_sloc_manhattan'] = distance['manhattan']
    restmp['eloc_user_next_sloc_lat_sub'] = restmp.eloc_lat - restmp.next_sloc_lat
    restmp['eloc_user_next_sloc_lon_sub'] = restmp.eloc_lon - restmp.next_sloc_lon
    restmp.drop(['geohashed_start_loc', 'distance', 'next_sloc_lat', 'next_sloc_lon', 'manhattan'], axis=1, inplace=True)
    restmp['eloc_user_next_sloc_speed'] = restmp.eloc_user_next_sloc_distance / restmp.user_next_order_time_diff
    restmp['eloc_user_next_sloc_manhattan_speed'] = restmp.eloc_user_next_sloc_manhattan / restmp.user_next_order_time_diff
    restmp['eloc_user_next_sloc_latlon_slope'] = restmp.eloc_user_next_sloc_lat_sub / restmp.eloc_user_next_sloc_lon_sub
    restmp['eloc_user_next_sloc_lat_sub_divide_distance'] = restmp.eloc_user_next_sloc_lat_sub / restmp.eloc_user_next_sloc_distance
    restmp['eloc_user_next_sloc_lon_sub_divide_distance'] = restmp.eloc_user_next_sloc_lon_sub / restmp.eloc_user_next_sloc_distance
    
    restmp.loc[restmp.userid != restmp.last_userid, 'user_last_order_time_diff'] = -1000000
    restmp.loc[restmp.userid != restmp.last_userid, 'eloc_user_last_sloc_distance'] = -1000000
    restmp.loc[restmp.userid != restmp.last_userid, 'eloc_user_last_sloc_manhattan'] = -1000000
    restmp.loc[restmp.userid != restmp.last_userid, 'eloc_user_last_sloc_speed'] = -1000000
    restmp.loc[restmp.userid != restmp.last_userid, 'eloc_user_last_sloc_manhattan_speed'] = -1000000
    restmp.loc[restmp.userid != restmp.last_userid, 'eloc_user_last_sloc_lat_sub'] = -1000000
    restmp.loc[restmp.userid != restmp.last_userid, 'eloc_user_last_sloc_lon_sub'] = -1000000
    restmp.loc[restmp.userid != restmp.last_userid, 'eloc_user_last_sloc_latlon_slope'] = -1000000
    restmp.loc[restmp.userid != restmp.last_userid, 'eloc_user_last_sloc_lat_sub_divide_distance'] = -1000000
    restmp.loc[restmp.userid != restmp.last_userid, 'eloc_user_last_sloc_lon_sub_divide_distance'] = -1000000
    
    restmp.loc[restmp.userid != restmp.last_userid, 'user_next_order_time_diff'] = -1000000
    restmp.loc[restmp.userid != restmp.next_userid, 'eloc_user_next_sloc_distance'] = -1000000
    restmp.loc[restmp.userid != restmp.next_userid, 'eloc_user_next_sloc_manhattan'] = -1000000
    restmp.loc[restmp.userid != restmp.next_userid, 'eloc_user_next_sloc_speed'] = -1000000
    restmp.loc[restmp.userid != restmp.next_userid, 'eloc_user_next_sloc_manhattan_speed'] = -1000000
    restmp.loc[restmp.userid != restmp.next_userid, 'eloc_user_next_sloc_lat_sub'] = -1000000
    restmp.loc[restmp.userid != restmp.next_userid, 'eloc_user_next_sloc_lon_sub'] = -1000000
    restmp.loc[restmp.userid != restmp.next_userid, 'eloc_user_next_sloc_latlon_slope'] = -1000000
    restmp.loc[restmp.userid != restmp.next_userid, 'eloc_user_next_sloc_lat_sub_divide_distance'] = -1000000
    restmp.loc[restmp.userid != restmp.next_userid, 'eloc_user_next_sloc_lon_sub_divide_distance'] = -1000000

    result['user_last_order_time_diff'] = restmp['user_last_order_time_diff'] # wc
    result['eloc_user_last_sloc_distance'] = restmp['eloc_user_last_sloc_distance'] # dui 90 wc
    result['eloc_user_last_sloc_manhattan'] = restmp['eloc_user_last_sloc_manhattan']
    result['eloc_user_last_sloc_speed'] = restmp['eloc_user_last_sloc_speed'] # dui 90 wc
    result['eloc_user_last_sloc_manhattan_speed'] = restmp['eloc_user_last_sloc_manhattan_speed']
    result['eloc_user_last_sloc_lat_sub'] = restmp['eloc_user_last_sloc_lat_sub']
    result['eloc_user_last_sloc_lon_sub'] = restmp['eloc_user_last_sloc_lon_sub']
    result['eloc_user_last_sloc_latlon_slope'] = restmp['eloc_user_last_sloc_latlon_slope']
    result['eloc_user_last_sloc_lat_sub_divide_distance'] = restmp['eloc_user_last_sloc_lat_sub_divide_distance']
    result['eloc_user_last_sloc_lon_sub_divide_distance'] = restmp['eloc_user_last_sloc_lon_sub_divide_distance']
    
    result['user_next_order_time_diff'] = restmp['user_next_order_time_diff']
    result['eloc_user_next_sloc_distance'] = restmp['eloc_user_next_sloc_distance'] # dui 90 wc
    result['eloc_user_next_sloc_manhattan'] = restmp['eloc_user_next_sloc_manhattan'] # wc
    result['eloc_user_next_sloc_speed'] = restmp['eloc_user_next_sloc_speed'] # dui 90 wc
    result['eloc_user_next_sloc_manhattan_speed'] = restmp['eloc_user_next_sloc_manhattan_speed'] # wc
    result['eloc_user_next_sloc_lat_sub'] = restmp['eloc_user_next_sloc_lat_sub'] # dui 90 wc
    result['eloc_user_next_sloc_lon_sub'] = restmp['eloc_user_next_sloc_lon_sub'] # dui 90 wc
    result['eloc_user_next_sloc_latlon_slope'] = restmp['eloc_user_next_sloc_latlon_slope']
    result['eloc_user_next_sloc_lat_sub_divide_distance'] = restmp['eloc_user_next_sloc_lat_sub_divide_distance']
    result['eloc_user_next_sloc_lon_sub_divide_distance'] = restmp['eloc_user_next_sloc_lon_sub_divide_distance']

    return result

# 获取目标地点与车辆上一次、下一次出发地点的距离、时间差、速度及经纬度信息等
def get_eloc_bike_sloc_leak(result):
    bike_order = result[['orderid', 'bikeid', 'geohashed_start_loc', 'starttime', 'sloc_lat', 'sloc_lon']].drop_duplicates()
    bike_order.sort_values(by=['bikeid', 'starttime'], inplace=True, ascending=True)
    bike_order['last_bikeid'] = bike_order.bikeid.shift(1)
    bike_order['next_bikeid'] = bike_order.bikeid.shift(-1)
    bike_order['last_starttime'] = bike_order.starttime.shift(1)
    bike_order['bike_last_order_time_diff'] = (pd.DatetimeIndex(bike_order['starttime'])-pd.DatetimeIndex(bike_order['last_starttime'])).total_seconds()
    bike_order['next_starttime'] = bike_order.starttime.shift(-1)
    bike_order['bike_next_order_time_diff'] = (pd.DatetimeIndex(bike_order['starttime'])-pd.DatetimeIndex(bike_order['next_starttime'])).total_seconds()
    bike_order['last_sloc'] = bike_order.geohashed_start_loc.shift(1)
    bike_order['next_sloc'] = bike_order.geohashed_start_loc.shift(-1)
    bike_order['last_sloc_lat'] = bike_order.sloc_lat.shift(1)
    bike_order['next_sloc_lat'] = bike_order.sloc_lat.shift(-1)
    bike_order['last_sloc_lon'] = bike_order.sloc_lon.shift(1)
    bike_order['next_sloc_lon'] = bike_order.sloc_lon.shift(-1)
    bike_order.drop(['geohashed_start_loc', 'starttime', 'last_starttime', 'next_starttime', 'sloc_lat', 'sloc_lon'], axis=1, inplace=True)

    restmp = pd.merge(result[['orderid', 'geohashed_end_loc', 'eloc_lat', 'eloc_lon']], bike_order, on='orderid', how='left')
    restmp.rename(columns={'last_sloc': 'geohashed_start_loc'}, inplace=True)
    distance = get_distance(restmp)
    restmp['eloc_bike_last_sloc_distance'] = distance['distance']
    restmp['eloc_bike_last_sloc_manhattan'] = distance['manhattan']
    restmp['eloc_bike_last_sloc_lat_sub'] = restmp.eloc_lat - restmp.last_sloc_lat
    restmp['eloc_bike_last_sloc_lon_sub'] = restmp.eloc_lon - restmp.last_sloc_lon
    restmp.drop(['geohashed_start_loc', 'distance', 'last_sloc_lat', 'last_sloc_lon', 'manhattan'], axis=1, inplace=True)
    restmp['eloc_bike_last_sloc_speed'] = restmp.eloc_bike_last_sloc_distance / restmp.bike_last_order_time_diff
    restmp['eloc_bike_last_sloc_manhattan_speed'] = restmp.eloc_bike_last_sloc_manhattan / restmp.bike_last_order_time_diff
    restmp['eloc_bike_last_sloc_latlon_slope'] = restmp.eloc_bike_last_sloc_lat_sub / restmp.eloc_bike_last_sloc_lon_sub
    restmp['eloc_bike_last_sloc_lat_sub_divide_distance'] = restmp.eloc_bike_last_sloc_lat_sub / restmp.eloc_bike_last_sloc_distance
    restmp['eloc_bike_last_sloc_lon_sub_divide_distance'] = restmp.eloc_bike_last_sloc_lon_sub / restmp.eloc_bike_last_sloc_distance
    
    restmp.rename(columns={'next_sloc': 'geohashed_start_loc'}, inplace=True)
    distance = get_distance(restmp)
    restmp['eloc_bike_next_sloc_distance'] = distance['distance']
    restmp['eloc_bike_next_sloc_manhattan'] = distance['manhattan']
    restmp['eloc_bike_next_sloc_lat_sub'] = restmp.eloc_lat - restmp.next_sloc_lat
    restmp['eloc_bike_next_sloc_lon_sub'] = restmp.eloc_lon - restmp.next_sloc_lon
    restmp.drop(['geohashed_start_loc', 'distance', 'next_sloc_lat', 'next_sloc_lon', 'manhattan'], axis=1, inplace=True)
    restmp['eloc_bike_next_sloc_speed'] = restmp.eloc_bike_next_sloc_distance / restmp.bike_next_order_time_diff
    restmp['eloc_bike_next_sloc_manhattan_speed'] = restmp.eloc_bike_next_sloc_manhattan / restmp.bike_next_order_time_diff
    restmp['eloc_bike_next_sloc_latlon_slope'] = restmp.eloc_bike_next_sloc_lat_sub / restmp.eloc_bike_next_sloc_lon_sub
    restmp['eloc_bike_next_sloc_lat_sub_divide_distance'] = restmp.eloc_bike_next_sloc_lat_sub / restmp.eloc_bike_next_sloc_distance
    restmp['eloc_bike_next_sloc_lon_sub_divide_distance'] = restmp.eloc_bike_next_sloc_lon_sub / restmp.eloc_bike_next_sloc_distance
    
    restmp.loc[restmp.bikeid != restmp.last_bikeid, 'eloc_bike_last_sloc_distance'] = -1000000
    restmp.loc[restmp.bikeid != restmp.last_bikeid, 'eloc_bike_last_sloc_manhattan'] = -1000000
    restmp.loc[restmp.bikeid != restmp.last_bikeid, 'eloc_bike_last_sloc_speed'] = -1000000
    restmp.loc[restmp.bikeid != restmp.last_bikeid, 'eloc_bike_last_sloc_manhattan_speed'] = -1000000
    restmp.loc[restmp.bikeid != restmp.last_bikeid, 'eloc_bike_last_sloc_lat_sub'] = -1000000
    restmp.loc[restmp.bikeid != restmp.last_bikeid, 'eloc_bike_last_sloc_lon_sub'] = -1000000
    restmp.loc[restmp.bikeid != restmp.last_bikeid, 'eloc_bike_last_sloc_latlon_slope'] = -1000000
    restmp.loc[restmp.bikeid != restmp.last_bikeid, 'eloc_bike_last_sloc_lat_sub_divide_distance'] = -1000000
    restmp.loc[restmp.bikeid != restmp.last_bikeid, 'eloc_bike_last_sloc_lon_sub_divide_distance'] = -1000000
    
    restmp.loc[restmp.bikeid != restmp.next_bikeid, 'eloc_bike_next_sloc_distance'] = -1000000
    restmp.loc[restmp.bikeid != restmp.next_bikeid, 'eloc_bike_next_sloc_manhattan'] = -1000000
    restmp.loc[restmp.bikeid != restmp.next_bikeid, 'eloc_bike_next_sloc_speed'] = -1000000
    restmp.loc[restmp.bikeid != restmp.next_bikeid, 'eloc_bike_next_sloc_manhattan_speed'] = -1000000
    restmp.loc[restmp.bikeid != restmp.next_bikeid, 'eloc_bike_next_sloc_lat_sub'] = -1000000
    restmp.loc[restmp.bikeid != restmp.next_bikeid, 'eloc_bike_next_sloc_lon_sub'] = -1000000
    restmp.loc[restmp.bikeid != restmp.next_bikeid, 'eloc_bike_next_sloc_latlon_slope'] = -1000000
    restmp.loc[restmp.bikeid != restmp.next_bikeid, 'eloc_bike_next_sloc_lat_sub_divide_distance'] = -1000000
    restmp.loc[restmp.bikeid != restmp.next_bikeid, 'eloc_bike_next_sloc_lon_sub_divide_distance'] = -1000000

    result['eloc_bike_last_sloc_distance'] = restmp['eloc_bike_last_sloc_distance'] # dui 90 wc
    result['eloc_bike_last_sloc_manhattan'] = restmp['eloc_bike_last_sloc_manhattan']
    result['eloc_bike_last_sloc_speed'] = restmp['eloc_bike_last_sloc_speed'] # dui 90 wc
    result['eloc_bike_last_sloc_manhattan_speed'] = restmp['eloc_bike_last_sloc_manhattan_speed']
    result['eloc_bike_last_sloc_lat_sub'] = restmp['eloc_bike_last_sloc_lat_sub'] # 90
    result['eloc_bike_last_sloc_lon_sub'] = restmp['eloc_bike_last_sloc_lon_sub'] # 90
    result['eloc_bike_last_sloc_latlon_slope'] = restmp['eloc_bike_last_sloc_latlon_slope'] # 90
    result['eloc_bike_last_sloc_lat_sub_divide_distance'] = restmp['eloc_bike_last_sloc_lat_sub_divide_distance'] # 90
    result['eloc_bike_last_sloc_lon_sub_divide_distance'] = restmp['eloc_bike_last_sloc_lon_sub_divide_distance'] # 90
    
    result['eloc_bike_next_sloc_distance'] = restmp['eloc_bike_next_sloc_distance'] # dui 90 wc
    result['eloc_bike_next_sloc_manhattan'] = restmp['eloc_bike_next_sloc_manhattan']
    result['eloc_bike_next_sloc_speed'] = restmp['eloc_bike_next_sloc_speed'] # dui 90 wc
    result['eloc_bike_next_sloc_manhattan_speed'] = restmp['eloc_bike_next_sloc_manhattan_speed']
    result['eloc_bike_next_sloc_lat_sub'] = restmp['eloc_bike_next_sloc_lat_sub'] # 90
    result['eloc_bike_next_sloc_lon_sub'] = restmp['eloc_bike_next_sloc_lon_sub'] # 90
    result['eloc_bike_next_sloc_latlon_slope'] = restmp['eloc_bike_next_sloc_latlon_slope'] # 90
    result['eloc_bike_next_sloc_lat_sub_divide_distance'] = restmp['eloc_bike_next_sloc_lat_sub_divide_distance'] # 90
    result['eloc_bike_next_sloc_lon_sub_divide_distance'] = restmp['eloc_bike_next_sloc_lon_sub_divide_distance'] # 90
    
    return result