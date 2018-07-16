# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import os
os.path.join('..')
from feature.other import get_distance, get_hour, get_latlon

# 获取训练数据
def get_train_data(opt):
	train = pd.read_csv(opt['train_csv'])
	train1 = train[(train['starttime'] < opt['starttime']) | (train['starttime'] >= opt['endtime'])]
	train2 = train[(train['starttime'] >= opt['starttime']) & (train['starttime'] < opt['endtime'])]
	# train2_old = train2[train2.userid.isin(train1.userid)]
	# train2_new = train2[~train2.userid.isin(train1.userid)]
	# train2_old_sample = train2_old.sample(frac=0.8)
	# train2 = pd.concat([train2_old_sample, train2_new])
	# train2_newuser = train2[~train2.userid.isin(train1['userid'])]
	# train2 = pd.concat([train2, train2_newuser, train2_newuser])
	# train1 = train[(train['starttime'] < '2017-05-18 00:00:00') | ((train['starttime'] >= '2017-05-20 00:00:00') & (train['starttime'] < '2017-05-22 00:00:00'))]
	# train2 = train[((train['starttime'] >= '2017-05-18 00:00:00') & (train['starttime'] < '2017-05-20 00:00:00')) | (train['starttime'] >= '2017-05-22 00:00:00')]
	del train2['geohashed_end_loc']
	train1 = add_info(train1) # 添加小时信息、距离信息和经纬度信息
	#test = pd.read_csv(opt['test_csv']) # add
	#train2 = get_hour(train2) # add
	#train2 = get_latlon(train2, end=False) # add
	#test = get_hour(test) # add
	#test = get_latlon(test, end=False) # add
	#train_all = pd.concat([train1, train2, test]) # add
	print('训练数据加载完成：', train1.shape, train2.shape)#, train_all.shape)
	return train1, train2#, train_all

# 获取测试数据
def get_test_data(opt):
	train = pd.read_csv(opt['train_csv'])
	test = pd.read_csv(opt['test_csv'])
	# test_all = test.copy()
	if opt['test_endtime'] < opt['test_starttime']: test = test[(test['starttime'] >= opt['test_starttime'])]
	else: test = test[(test['starttime'] >= opt['test_starttime']) & (test['starttime'] < opt['test_endtime'])]
	train = add_info(train) # 添加小时信息、距离信息和经纬度信息
	# test_all = get_hour(test_all)
	# test_all = get_latlon(test_all, end=False)
	# train_all = pd.concat([train, test_all])
	print('测试数据加载完成：', train.shape, test.shape)#, train_all.shape)
	return train, test#, train_all

def add_info(res):
    res = get_distance(res)
    res = get_hour(res)
    res = get_latlon(res)
    return res