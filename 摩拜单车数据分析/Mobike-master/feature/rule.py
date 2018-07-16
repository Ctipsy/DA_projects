# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np

'''
    获取自定义规则
'''

def get_user_rule(result):
    result['user_rule'] = (1 + result['user_eloc_count']) * result['eloc_user_count'] / (0.01 * result['distance'])
    return result

def get_user_didi(train, result):
    result['user_hour_count_rate'] = result['user_hour_count'] / train.shape[0]
    train = train[~train.geohashed_end_loc.isnull()]
    result['user_eloc_count_rate'] = result['user_eloc_count'] / train.shape[0]
    result['user_hour_eloc_rate'] = result['user_eloc_hour_count'] / result['user_eloc_count']
    result['user_hour_eloc_distribute'] = result['user_eloc_count_rate'] * result['user_hour_eloc_rate'] / result['user_hour_count_rate']
    return result

def get_loc_rule(result):
    result['loc_rule'] = result['eloc_count'] / (0.01 * result['distance'])
    result['loc_rule2'] = np.sqrt(result['distance'] / (result['eloc_count'] ** 1.1))
    return result

def get_loc_didi(train, result):
    result['hour_count_rate'] = result['hour_count'] / train.shape[0]
    train = train[~train.geohashed_end_loc.isnull()]
    result['eloc_count_rate'] = result['eloc_count'] / train.shape[0]
    result['hour_eloc_rate'] = result['eloc_hour_count'] / result['eloc_count']
    result['hour_eloc_distribute'] = result['eloc_count_rate'] * result['hour_eloc_rate'] / result['hour_count_rate']
    return result