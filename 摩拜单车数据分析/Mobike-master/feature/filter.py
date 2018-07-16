# -*- coding:utf-8 -*-
import pandas as pd
import Geohash as geohash
import numpy as np
import os
import tqdm
os.path.join('..')
from utils import rank

'''
	获取协同过滤特征
'''

# ----------------- 计数 -------------------

# 获取地址对的协同过滤信息
def get_loc_filter(train, result):
    sloc_elocs, eloc_slocs = {}, {}
    for i in tqdm.tqdm(train[['geohashed_start_loc', 'geohashed_end_loc']].values):
        if i[0] not in sloc_elocs:
            sloc_elocs[i[0]] = {}
        if i[1] not in sloc_elocs[i[0]]:
            sloc_elocs[i[0]][i[1]] = 0
        sloc_elocs[i[0]][i[1]] += 1
        if i[1] not in eloc_slocs:
            eloc_slocs[i[1]] = {}
        if i[0] not in eloc_slocs[i[1]]:
            eloc_slocs[i[1]][i[0]] = 0;
        eloc_slocs[i[1]][i[0]] += 1
    sloc_list, eloc_list, sloc_eloc_common_eloc_count, sloc_eloc_common_sloc_count, sloc_eloc_common_conn1_count, sloc_eloc_common_conn2_count = [], [], [], [], [], []
    for i in tqdm.tqdm(result[['geohashed_start_loc', 'geohashed_end_loc']].drop_duplicates().values):
        sloc_list.append(i[0])
        eloc_list.append(i[1])
        # 获取地址对在历史记录中共有的目的地数目
        common_eloc_count = 0
        if (i[0] in sloc_elocs) and (i[1] in sloc_elocs):
            sloc_eloc_common_eloc_set = sloc_elocs[i[0]].keys() & sloc_elocs[i[1]].keys()
            for common_eloc in sloc_eloc_common_eloc_set:
                common_eloc_count = common_eloc_count + sloc_elocs[i[0]][common_eloc] + sloc_elocs[i[1]][common_eloc]
        sloc_eloc_common_eloc_count.append(common_eloc_count)
        # 获取地址对在历史记录中共有的出发地数目
        common_sloc_count = 0
        if (i[0] in eloc_slocs) and (i[1] in eloc_slocs):
            sloc_eloc_common_sloc_set = eloc_slocs[i[0]].keys() & eloc_slocs[i[1]].keys()
            for common_sloc in sloc_eloc_common_sloc_set:
                common_sloc_count = common_sloc_count + eloc_slocs[i[0]][common_sloc] + eloc_slocs[i[1]][common_sloc]
        sloc_eloc_common_sloc_count.append(common_sloc_count)
        # 获取地址对在历史记录中共有的连接点数目(出发点->xx->目的地)
        common_conn1_count = 0
        if (i[0] in sloc_elocs) and (i[1] in eloc_slocs):
            sloc_eloc_common_conn1_set = sloc_elocs[i[0]].keys() & eloc_slocs[i[1]].keys()
            for common_conn1 in sloc_eloc_common_conn1_set:
                common_conn1_count = common_conn1_count + sloc_elocs[i[0]][common_conn1] + eloc_slocs[i[1]][common_conn1]
        sloc_eloc_common_conn1_count.append(common_conn1_count)
        # 获取地址对在历史记录中共有的连接点数目(出发点<-xx<-目的地)
        common_conn2_count = 0
        if (i[0] in eloc_slocs) and (i[1] in sloc_elocs):
            sloc_eloc_common_conn2_set = eloc_slocs[i[0]].keys() & sloc_elocs[i[1]].keys()
            for common_conn2 in sloc_eloc_common_conn2_set:
                common_conn2_count = common_conn2_count + eloc_slocs[i[0]][common_conn2] + sloc_elocs[i[1]][common_conn2]
        sloc_eloc_common_conn2_count.append(common_conn2_count)
    loc_filter = pd.DataFrame({"geohashed_start_loc": sloc_list, "geohashed_end_loc": eloc_list, "sloc_eloc_common_eloc_count": sloc_eloc_common_eloc_count, "sloc_eloc_common_sloc_count": sloc_eloc_common_sloc_count, "sloc_eloc_common_conn1_count": sloc_eloc_common_conn1_count, "sloc_eloc_common_conn2_count": sloc_eloc_common_conn2_count})
    result = pd.merge(result, loc_filter, on=['geohashed_start_loc', 'geohashed_end_loc'], how='left')
    result['sloc_eloc_common_eloc_rate'] = result['sloc_eloc_common_eloc_count']/(result['sloc_count']+result['eloc_as_sloc_count'])
    result['sloc_eloc_common_sloc_rate'] = result['sloc_eloc_common_sloc_count']/(result['sloc_as_eloc_count']+result['eloc_count'])
    result['sloc_eloc_common_conn1_rate'] = result['sloc_eloc_common_conn1_count']/(result['sloc_count']+result['eloc_count'])
    result['sloc_eloc_common_conn2_rate'] = result['sloc_eloc_common_conn2_count']/(result['sloc_as_eloc_count']+result['eloc_as_sloc_count'])
    return result

# 获取用户地址对的协同过滤信息
def get_user_loc_filter(train, result):
    user_sloc_elocs, user_eloc_slocs = {}, {}
    for i in tqdm.tqdm(train[['userid', 'geohashed_start_loc', 'geohashed_end_loc']].values):
        if i[0] not in user_sloc_elocs:
            user_sloc_elocs[i[0]] = {}
        if i[1] not in user_sloc_elocs[i[0]]:
            user_sloc_elocs[i[0]][i[1]] = {}
        if i[2] not in user_sloc_elocs[i[0]][i[1]]:
            user_sloc_elocs[i[0]][i[1]][i[2]] = 0
        user_sloc_elocs[i[0]][i[1]][i[2]] += 1
        if i[0] not in user_eloc_slocs:
            user_eloc_slocs[i[0]] = {}
        if i[2] not in user_eloc_slocs[i[0]]:
            user_eloc_slocs[i[0]][i[2]] = {};
        if i[1] not in user_eloc_slocs[i[0]][i[2]]:
            user_eloc_slocs[i[0]][i[2]][i[1]] = 0
        user_eloc_slocs[i[0]][i[2]][i[1]] += 1
    user_list, user_sloc_list, user_eloc_list, user_sloc_eloc_common_eloc_count, user_sloc_eloc_common_sloc_count, user_sloc_eloc_common_conn1_count, user_sloc_eloc_common_conn2_count = [], [], [], [], [], [], []
    for i in tqdm.tqdm(result[['userid', 'geohashed_start_loc', 'geohashed_end_loc']].drop_duplicates().values):
        user_list.append(i[0])
        user_sloc_list.append(i[1])
        user_eloc_list.append(i[2])
        # 获取地址对在用户历史记录中共有的目的地数目
        user_common_eloc_count = 0
        if (i[0] in user_sloc_elocs) and (i[1] in user_sloc_elocs[i[0]]) and (i[2] in user_sloc_elocs[i[0]]):
            user_sloc_eloc_common_eloc_set = user_sloc_elocs[i[0]][i[1]].keys() & user_sloc_elocs[i[0]][i[2]].keys()
            for user_common_eloc in user_sloc_eloc_common_eloc_set:
                user_common_eloc_count = user_common_eloc_count + user_sloc_elocs[i[0]][i[1]][user_common_eloc] + user_sloc_elocs[i[0]][i[2]][user_common_eloc]
        user_sloc_eloc_common_eloc_count.append(user_common_eloc_count)
        # 获取地址对在用户历史记录中共有的出发地数目
        user_common_sloc_count = 0
        if (i[0] in user_eloc_slocs) and (i[1] in user_eloc_slocs[i[0]]) and (i[2] in user_eloc_slocs[i[0]]):
            user_sloc_eloc_common_sloc_set = user_eloc_slocs[i[0]][i[1]].keys() & user_eloc_slocs[i[0]][i[2]].keys()
            for user_common_sloc in user_sloc_eloc_common_sloc_set:
                user_common_sloc_count = user_common_sloc_count + user_eloc_slocs[i[0]][i[1]][user_common_sloc] + user_eloc_slocs[i[0]][i[2]][user_common_sloc]
        user_sloc_eloc_common_sloc_count.append(user_common_sloc_count)
        # 获取地址对在用户历史记录中共有的连接点数目(出发点->xx->目的地)
        user_common_conn1_count = 0
        if (i[0] in user_sloc_elocs) and (i[1] in user_sloc_elocs[i[0]]) and (i[0] in user_eloc_slocs) and (i[2] in user_eloc_slocs[i[0]]):
            user_sloc_eloc_common_conn1_set = user_sloc_elocs[i[0]][i[1]].keys() & user_eloc_slocs[i[0]][i[2]].keys()
            for user_common_conn1 in user_sloc_eloc_common_conn1_set:
                user_common_conn1_count = user_common_conn1_count + user_sloc_elocs[i[0]][i[1]][user_common_conn1] + user_eloc_slocs[i[0]][i[2]][user_common_conn1]
        user_sloc_eloc_common_conn1_count.append(user_common_conn1_count)
        # 获取地址对在用户历史记录中共有的连接点数目(出发点<-xx<-目的地)
        user_common_conn2_count = 0
        if (i[0] in user_eloc_slocs) and (i[1] in user_eloc_slocs[i[0]]) and (i[0] in user_sloc_elocs) and (i[2] in user_sloc_elocs[i[0]]):
            user_sloc_eloc_common_conn2_set = user_eloc_slocs[i[0]][i[1]].keys() & user_sloc_elocs[i[0]][i[2]].keys()
            for user_common_conn2 in user_sloc_eloc_common_conn2_set:
                user_common_conn2_count = user_common_conn2_count + user_eloc_slocs[i[0]][i[1]][user_common_conn2] + user_sloc_elocs[i[0]][i[2]][user_common_conn2]
        user_sloc_eloc_common_conn2_count.append(user_common_conn2_count)
    user_loc_filter = pd.DataFrame({"userid": user_list, "geohashed_start_loc": user_sloc_list, "geohashed_end_loc": user_eloc_list, "user_sloc_eloc_common_eloc_count": user_sloc_eloc_common_eloc_count, "user_sloc_eloc_common_sloc_count": user_sloc_eloc_common_sloc_count, "user_sloc_eloc_common_conn1_count": user_sloc_eloc_common_conn1_count, "user_sloc_eloc_common_conn2_count": user_sloc_eloc_common_conn2_count})
    result = pd.merge(result, user_loc_filter, on=['userid', 'geohashed_start_loc', 'geohashed_end_loc'], how='left')
    result['user_sloc_eloc_common_eloc_rate'] = result['user_sloc_eloc_common_eloc_count']/(result['user_sloc_count']+result['user_eloc_as_sloc_count'])
    result['user_sloc_eloc_common_sloc_rate'] = result['user_sloc_eloc_common_sloc_count']/(result['user_sloc_as_eloc_count']+result['user_eloc_count'])
    result['user_sloc_eloc_common_conn1_rate'] = result['user_sloc_eloc_common_conn1_count']/(result['user_sloc_count']+result['user_eloc_count'])
    result['user_sloc_eloc_common_conn2_rate'] = result['user_sloc_eloc_common_conn2_count']/(result['user_sloc_as_eloc_count']+result['user_eloc_as_sloc_count'])
    return result