# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import pickle
import datetime
import fire
import gc
import warnings
warnings.filterwarnings('ignore')

from config import DefaultConfig
from dataset import get_train_data, get_test_data, get_sample
from feature import get_feat
from utils import get_label, get_score, load_model, predict, rank

def train(**kwargs):

	# ---------------------- 更新参数 ----------------------
	opt = DefaultConfig()
	opt.update(**kwargs)
	opt.printf()

	# ---------------------- 数据处理 ----------------------

	# 获取数据
	# train1, train2 = get_train_data(opt)
	# 获取样本
	# train_sample = get_sample(train1, train2, load=True)
	# 获取特征
	# train_feat = get_feat(train1, train_sample)
	# 获取标签
	# train_all = get_label(train_feat, opt)
	# gc.collect()

	# train_all.to_hdf('/home/xuwenchao/dyj-storage/all-feat/feat_23_24_label.hdf', 'w', complib='blosc', complevel=5)
	train_all = pd.read_hdf('/home/xuwenchao/dyj-storage/all-feat/feat_23_24_label.hdf')
	print(train_all.shape)
    
	# 取出需要用的特征
	# opt['model_name'] = 'lgb_1_2017-09-15#19:50:48_0.58820.pkl'
	# gbm, use_feat = load_model(opt)
	# predictors_100 = pd.DataFrame(data={'feature_name': gbm.feature_name(), 'feature_importance': gbm.feature_importance()})
	# predictors_100 = predictors_100.sort_values(by=['feature_importance'], ascending=False)['feature_name'].values[:100]
	# use_feat = list(predictors_100) + ['orderid', 'geohashed_end_loc', 'label'] + ['sloc_eloc_common_eloc_count', 'sloc_eloc_common_sloc_count', 'sloc_eloc_common_conn1_count', 'sloc_eloc_common_conn2_count', 'sloc_eloc_common_eloc_rate', 'sloc_eloc_common_sloc_rate', 'sloc_eloc_common_conn1_rate', 'sloc_eloc_common_conn2_rate', 'user_sloc_eloc_common_eloc_count', 'user_sloc_eloc_common_sloc_count', 'user_sloc_eloc_common_conn1_count', 'user_sloc_eloc_common_conn2_count', 'user_sloc_eloc_common_eloc_rate', 'user_sloc_eloc_common_sloc_rate', 'user_sloc_eloc_common_conn1_rate', 'user_sloc_eloc_common_conn2_rate']
	# train_all = train_all[use_feat]
	# gc.collect()
    
	# -------------------- 训练第一层 ------------------------

	# ********* 准备数据 **********
	# 划分验证集
	train, val = train_test_split(train_all, test_size=0.1)
	# 定义使用哪些特征
	# opt['model_name'] = 'lgb_1_2017-09-15#19:50:48_0.58820.pkl'
	# gbm, use_feat = load_model(opt)
	filters = set(['orderid', 'userid', 'biketype', 'geohashed_start_loc', 'bikeid', 'starttime', 'geohashed_end_loc', 'label'])
	predictors = list(filter(lambda x: x not in filters, train_all.columns.tolist()))
	# predictors = pd.DataFrame(data={'feature_name': gbm.feature_name(), 'feature_importance': gbm.feature_importance()})
	# predictors = predictors.sort_values(by=['feature_importance'], ascending=False)['feature_name'].values[:100]
	# use_feat = list(predictors) + ['orderid', 'geohashed_end_loc'] + ['sloc_eloc_common_eloc_count', 'sloc_eloc_common_sloc_count', 'sloc_eloc_common_conn1_count', 'sloc_eloc_common_conn2_count', 'sloc_eloc_common_eloc_rate', 'sloc_eloc_common_sloc_rate', 'sloc_eloc_common_conn1_rate', 'sloc_eloc_common_conn2_rate', 'user_sloc_eloc_common_eloc_count', 'user_sloc_eloc_common_sloc_count', 'user_sloc_eloc_common_conn1_count', 'user_sloc_eloc_common_conn2_count', 'user_sloc_eloc_common_eloc_rate', 'user_sloc_eloc_common_sloc_rate', 'user_sloc_eloc_common_conn1_rate', 'user_sloc_eloc_common_conn2_rate']
	# predictors = list(predictors_100) + ['sloc_eloc_common_eloc_count', 'sloc_eloc_common_sloc_count', 'sloc_eloc_common_conn1_count', 'sloc_eloc_common_conn2_count', 'sloc_eloc_common_eloc_rate', 'sloc_eloc_common_sloc_rate', 'sloc_eloc_common_conn1_rate', 'sloc_eloc_common_conn2_rate', 'user_sloc_eloc_common_eloc_count', 'user_sloc_eloc_common_sloc_count', 'user_sloc_eloc_common_conn1_count', 'user_sloc_eloc_common_conn2_count', 'user_sloc_eloc_common_eloc_rate', 'user_sloc_eloc_common_sloc_rate', 'user_sloc_eloc_common_conn1_rate', 'user_sloc_eloc_common_conn2_rate']
	print('使用的特征：{}维\n'.format(len(predictors)), predictors)
	# 定义数据集
	X_train = train[predictors]
	y_train = train['label']
	X_val = val[predictors]
	y_val = val['label']
	del train, val
	gc.collect()

	# ********* LightGBM *********
	# 数据集
	lgb_train = lgb.Dataset(X_train, y_train)
	lgb_val = lgb.Dataset(X_val, y_val, reference=lgb_train)
	# 配置
	params = {
	    'objective': 'binary',
	    'metric': {'auc', 'binary_logloss'},
	    'is_unbalance': True,
	    'num_leaves': opt['lgb_leaves'],
	    'learning_rate': opt['lgb_lr'],
	    'feature_fraction': 0.886,
	    'bagging_fraction': 0.886,
	    'bagging_freq': 5
	}
	gc.collect()    
	# ********** 开始训练 *********
	gbm1 = lgb.train(
				params,
                lgb_train,
                num_boost_round=1200,
                valid_sets=[lgb_train, lgb_val],
                early_stopping_rounds=5
	)
	gc.collect()
    
	# #  ********* 保存模型 *********

	cur_time = datetime.datetime.now().strftime('%Y-%m-%d#%H:%M:%S')
	# save_path = '{}/{}_{}_{:.5f}.pkl'.format(opt['model_dir'], 'lgb', cur_time, score[0])
	save_path = '{}/{}_{}.pkl'.format(opt['model_dir'], 'lgb', cur_time)
	with open(save_path, 'wb') as fout:
	    pickle.dump(gbm1, fout)
	print('保存模型：', save_path)
	gc.collect()    

	# #  ********* 评估  *********

	# # 在训练集上看效果
	del X_train, y_train, X_val, y_val
	gc.collect()    
	score = get_score(train_all, predictors, gbm1, opt)
	print('训练集分数：{}'.format(score))
    
	import sys
	sys.exit(0)
    
	# save_path = '{}/{}.pkl'.format(opt['model_dir'], 'lgb_1_300_top25')
	# with open(save_path, 'wb') as fout:
	#     pickle.dump(gbm1, fout)
	# print('保存模型(第一层)：', save_path)

	# ********* save predict *****

	# train_all[['orderid', 'geohashed_end_loc', 'pred']].to_hdf('/home/xuwenchao/dyj-storage/train2324_80_pred_res.hdf', 'w', complib='blosc', complevel=5)
	# print('Save train_pred_res.hdf successful!!!')

	# import sys
	# sys.exit(0)
    
	# -------------------- 训练第二层 ------------------------
    
	# opt['model_name'] = 'lgb_1_300_top25.pkl'
	# gbm1, use_feat1 = load_model(opt)
	# train_all.loc[:, 'pred'] = gbm1.predict(train_all[use_feat1])

	# 去掉重要性较低的特征，筛选出排名前十的候选样本，重新训练模型（后期可以载入模型finetune，尤其是对于样本量较少的情况，甚至可以选前5，但15可以覆盖99.5%的原始label，10可以覆盖98%的原始label，这两者可能会好一些，备选方案：5(+finetune)，10(+finetune)，15(+finetune)）
	predictors = pd.DataFrame(data={'feature_name': gbm1.feature_name(), 'feature_importance': gbm1.feature_importance()})
	predictors = predictors[predictors['feature_importance']>0]['feature_name'].values
	print('第二层使用的特征：{}维\n'.format(len(predictors)), predictors)
	train_all = train_all.sort_values(by=['orderid', 'pred'], ascending=False).groupby('orderid').head(15)
	# train_all = rank(train_all, 'orderid', 'pred', ascending=False)
	del train_all['pred']
	print('第二层数据：', train_all.shape)
    
	# ********* 准备数据 **********
	# 划分验证集
	train, val = train_test_split(train_all, test_size=0.1)
    
	# 定义数据集
	X_train = train[predictors]
	y_train = train['label']
	X_val = val[predictors]
	y_val = val['label']
	del train, val
	gc.collect()

	# 数据集
	lgb_train = lgb.Dataset(X_train, y_train)
	lgb_val = lgb.Dataset(X_val, y_val, reference=lgb_train)

	# ********** 开始训练 *********
	gbm2 = lgb.train(
				params,
                lgb_train,
                num_boost_round=1200,
                valid_sets=[lgb_train, lgb_val],
                early_stopping_rounds=5
                # init_model=gbm1 # finetune
	        )

	#  ********* 评估  *********

	# 在训练集上看效果    
	score = get_score(train_all, predictors, gbm2, opt)
	print('训练集分数(第二层)：{}'.format(score))

	#  ********* 保存模型 *********

	cur_time = datetime.datetime.now().strftime('%Y-%m-%d#%H:%M:%S')
	save_path = '{}/{}_{}_{:.5f}.pkl'.format(opt['model_dir'], 'lgb_2', cur_time, score[0])
	with open(save_path, 'wb') as fout:
	    pickle.dump(gbm2, fout)
	print('保存模型(第二层)：', save_path)
	# save_path = '{}/{}.pkl'.format(opt['model_dir'], 'lgb_2_300_top15')
	# with open(save_path, 'wb') as fout:
	#     pickle.dump(gbm2, fout)
	# print('保存模型(第二层)：', save_path)
    
	import sys
	sys.exit(0)
    
	# -------------------- 训练第三层 ------------------------
    
	# 筛选出排名前五的候选样本
	predictors = pd.DataFrame(data={'feature_name': gbm2.feature_name(), 'feature_importance': gbm2.feature_importance()})
	predictors = predictors[predictors['feature_importance']>0]['feature_name'].values
	print('第三层使用的特征：{}维\n'.format(len(predictors)), predictors)
	train_all = train_all.sort_values(by=['orderid', 'pred'], ascending=False).groupby('orderid').head(10)
	# train_all = rank(train_all, 'orderid', 'pred', ascending=False)
	del train_all['pred']
	print('第三层数据：', train_all.shape)
    
	# ********* 准备数据 **********
	# 划分验证集
	train, val = train_test_split(train_all, test_size=0.1)
    
	# 定义数据集
	X_train = train[predictors]
	y_train = train['label']
	X_val = val[predictors]
	y_val = val['label']
	del train, val
	gc.collect()

	# 数据集
	lgb_train = lgb.Dataset(X_train, y_train)
	lgb_val = lgb.Dataset(X_val, y_val, reference=lgb_train)

	# ********** 开始训练 *********
	gbm3 = lgb.train(
				params,
                lgb_train,
                num_boost_round=1200,
                valid_sets=[lgb_train, lgb_val],
                early_stopping_rounds=5
                # init_model=gbm2 # finetune
	        )

	#  ********* 评估  *********

	# 在训练集上看效果    
	score = get_score(train_all, predictors, gbm3, opt)
	print('训练集分数(第三层)：{}'.format(score))

	#  ********* 保存模型 *********

	cur_time = datetime.datetime.now().strftime('%Y-%m-%d#%H:%M:%S')
	save_path = '{}/{}_{}_{:.5f}.pkl'.format(opt['model_dir'], 'lgb_3', cur_time, score[0])
	with open(save_path, 'wb') as fout:
	    pickle.dump(gbm3, fout)
	print('保存模型(第三层)：', save_path)
	save_path = '{}/{}.pkl'.format(opt['model_dir'], 'lgb_3_300_top10')
	with open(save_path, 'wb') as fout:
	    pickle.dump(gbm3, fout) 
	print('保存模型(第三层)：', save_path)

    
	# -------------------- 训练第四层 ------------------------
    
	# 筛选出排名前三的候选样本
	predictors = pd.DataFrame(data={'feature_name': gbm3.feature_name(), 'feature_importance': gbm3.feature_importance()})
	predictors = predictors[predictors['feature_importance']>0]['feature_name'].values
	print('第四层使用的特征：{}维\n'.format(len(predictors)), predictors)
	train_all = train_all.sort_values(by=['orderid', 'pred'], ascending=False).groupby('orderid').head(5)
	# train_all = rank(train_all, 'orderid', 'pred', ascending=False)
	del train_all['pred']
	print('第四层数据：', train_all.shape)
    
	# ********* 准备数据 **********
	# 划分验证集
	train, val = train_test_split(train_all, test_size=0.1)
    
	# 定义数据集
	X_train = train[predictors]
	y_train = train['label']
	X_val = val[predictors]
	y_val = val['label']
	del train, val
	gc.collect()

	# 数据集
	lgb_train = lgb.Dataset(X_train, y_train)
	lgb_val = lgb.Dataset(X_val, y_val, reference=lgb_train)

	# ********** 开始训练 *********
	gbm4 = lgb.train(
				params,
                lgb_train,
                num_boost_round=1200,
                valid_sets=[lgb_train, lgb_val],
                early_stopping_rounds=5
                # init_model=gbm3 # finetune
	        )

	#  ********* 评估  *********

	# 在训练集上看效果    
	score = get_score(train_all, predictors, gbm4, opt)
	print('训练集分数(第四层)：{}'.format(score))

	#  ********* 保存模型 *********

	cur_time = datetime.datetime.now().strftime('%Y-%m-%d#%H:%M:%S')
	save_path = '{}/{}_{}_{:.5f}.pkl'.format(opt['model_dir'], 'lgb_4', cur_time, score[0])
	with open(save_path, 'wb') as fout:
	    pickle.dump(gbm4, fout)
	print('保存模型(第四层)：', save_path)
	save_path = '{}/{}.pkl'.format(opt['model_dir'], 'lgb_4_300_top5')
	with open(save_path, 'wb') as fout:
	    pickle.dump(gbm4, fout) 
	print('保存模型(第四层)：', save_path)

def val(**kwargs):

	# ---------------------- 更新参数 ----------------------
	opt = DefaultConfig()
	opt.update(**kwargs)
	opt.printf()

	# ---------------------- 数据处理 ----------------------

	# 获取数据
	# train1, train2, train_test = get_train_data(opt)
	# 获取样本
	# train_sample = get_sample(train1, train2, load=True)
	# 获取特征
	# train_feat = get_feat(train_test, train_sample)
	# gc.collect()
    
	# train_feat.to_hdf('/home/xuwenchao/dyj-storage/all-feat/feat_{}.hdf'.format(opt['startday']), 'w', complib='blosc', complevel=5)
	train_feat = pd.read_hdf('/home/xuwenchao/dyj-storage/all-feat/feat_23_24_label.hdf')

    # ---------------------- 载入模型 ----------------------
	
	# opt['model_name'] = 'lgb_1_90_all.pkl'
	# gbm0, use_feat0 = load_model(opt)
	opt['model_name'] = 'lgb_1_2017-09-15#19:50:48_0.58820.pkl'
	gbm, use_feat = load_model(opt)
	opt['model_name'] = 'lgb_2017-09-23#20:14:52_0.58893.pkl'
	gbm1, use_feat1 = load_model(opt)
	# gbm2, use_feat2 = load_model(opt)
	# opt['model_name'] = 'lgb_2017-09-03#23:24:26_0.57836.pkl'
	# gbm3, use_feat3 = load_model(opt)
	# opt['model_name'] = ''
	# gbm4, use_feat4 = load_model(opt)

	# ---------------------- 评估 -------------------------

	train_feat.loc[:, 'pred'] = gbm.predict(train_feat[use_feat])
	gc.collect()
	train_feat[['orderid', 'geohashed_end_loc', 'pred']].to_csv('/home/xuwenchao/dyj-storage/pred/pred_23_24_0.58820.csv', index=None)
	train_feat.loc[:, 'pred'] = gbm1.predict(train_feat[use_feat1])
	gc.collect()
	train_feat[['orderid', 'geohashed_end_loc', 'pred']].to_csv('/home/xuwenchao/dyj-storage/pred/pred_23_24_0.58893.csv', index=None)
	# train_feat = train_feat.sort_values(by=['orderid', 'pred'], ascending=False).groupby('orderid').head(25)
	# train_feat[['orderid', 'geohashed_end_loc']].to_hdf('/home/xuwenchao/dyj-storage/sample_25_{}.hdf'.format(train.shape[0]), 'w', complib='blosc', complevel=5)
	# gc.collect()

	# score = get_score(train_feat, use_feat, gbm, opt)
	# print('day{}分数：{}'.format(opt['startday'], score))
	# score = get_score(train_feat, use_feat1, gbm1, opt)
	# print('day{}分数：{}'.format(opt['startday'], score)) 
	# train_feat = train_feat.sort_values(by=['orderid', 'pred'], ascending=False).groupby('orderid').head(15)
	# score = get_score(train_feat, use_feat1, gbm1, opt)
	# print('day{}分数：{}'.format(opt['startday'], score)) 
	# score1 = get_score(train_feat, use_feat1, gbm1, opt)
	# print('day{}分数: {}'.format(opt['startday'], score1))
	# score2 = get_score(train_feat, use_feat2, gbm2, opt)
	# print('day{}分数: {}'.format(opt['startday'], score2))
	# score3 = get_score(train_feat, use_feat3, gbm3, opt)
	# print('day{}分数: {}'.format(opt['startday'], score3))
	# score4 = get_score(train_feat, use_feat4, gbm4, opt)
	# print('day{}分数: {}'.format(opt['startday'], score4))

def test(**kwargs):
	
	# ---------------------- 更新参数 ----------------------
	opt = DefaultConfig()
	opt.update(**kwargs)
	opt.printf()

    # ---------------------- 数据处理 ----------------------

    # 获取数据
	train, test = get_test_data(opt)
	gc.collect()
 #    # 获取样本
	# test_sample = get_sample(train, test, load=True)
	# gc.collect()
 #    # 获取特征
	# test_feat = get_feat(train, test_sample)
	# gc.collect()

	# 保存特征至文件
	# test_feat.to_hdf('/home/xuwenchao/dyj-storage/all-feat/feat_{}.hdf'.format(test.shape[0]), 'w', complib='blosc', complevel=5)
	test_feat = pd.read_hdf('/home/xuwenchao/dyj-storage/all-feat/feat_{}.hdf'.format(test.shape[0]))
	test_feat = get_feat(train, test_feat)
	gc.collect()
	test_feat.to_hdf('/home/xuwenchao/dyj-storage/all-feat/feat_{}_filter.hdf'.format(test.shape[0]), 'w', complib='blosc', complevel=5)

    # ---------------------- 载入模型 ----------------------

	# opt['model_name'] = 'lgb_1_90_all.pkl'
	# gbm0, use_feat0 = load_model(opt)
	opt['model_name'] = 'lgb_2017-09-23#20:14:52_0.58893.pkl'
	gbm1, use_feat1 = load_model(opt)
	# opt['model_name'] = 'lgb_2_300_top15.pkl'
	# gbm2, use_feat2 = load_model(opt)
	# opt['model_name'] = 'lgb_3_300_top10.pkl'
	# gbm3, use_feat3 = load_model(opt)
	# opt['model_name'] = 'lgb_4_300_top5.pkl'
	# gbm4, use_feat4 = load_model(opt)
    
	# ---------------------- 保存预测结果 -------------------

	# test_feat.loc[:, 'pred'] = gbm0.predict(test_feat[use_feat0])
	# gc.collect()
	# res = test_feat[['orderid', 'geohashed_end_loc', 'pred']].sort_values(by=['orderid', 'pred'], ascending=False).groupby('orderid').head(25)
	# res[['orderid', 'geohashed_end_loc']].to_hdf('/home/xuwenchao/dyj-storage/sample_25_{}_filter_leak_sample.hdf'.format(test.shape[0]), 'w', complib='blosc', complevel=5)
	# gc.collect()

	# test_feat.loc[:, 'pred'] = gbm1.predict(test_feat[use_feat1])
	# test_feat[['orderid', 'geohashed_end_loc', 'pred']].to_hdf('/home/xuwenchao/dyj-storage/pred/pred_{}_0.58820.hdf'.format(test.shape[0]), 'w', complib='blosc', complevel=5)

	res = predict(test_feat, use_feat1, gbm1)
	test_feat[['orderid', 'geohashed_end_loc', 'pred']].to_hdf('/home/xuwenchao/dyj-storage/pred/pred_{}_0.58893.hdf'.format(test.shape[0]), 'w', complib='blosc', complevel=5)
	gc.collect()
	cur_time = datetime.datetime.now().strftime('%Y-%m-%d#%H:%M:%S')
	res_path = '{}/day{}_{}_wc_sample_0.58893.csv'.format(opt['result_dir'], opt['test_startday'], cur_time)
	res.to_csv(res_path, index=False)
	print('保存测试结果至：', res_path)
# 	test_feat = test_feat.sort_values(by=['orderid', 'pred'], ascending=False).groupby('orderid').head(15)
# 	del test_feat['pred']
# 	gc.collect()

# 	res = predict(test_feat, use_feat2, gbm2)
# 	gc.collect()
# 	test_feat = test_feat.sort_values(by=['orderid', 'pred'], ascending=False).groupby('orderid').head(10)
# 	del test_feat['pred']
# 	gc.collect()

# 	res = predict(test_feat, use_feat3, gbm3)
# 	gc.collect()
# 	test_feat = test_feat.sort_values(by=['orderid', 'pred'], ascending=False).groupby('orderid').head(5)
# 	del test_feat['pred']
# 	gc.collect()

# 	res = predict(test_feat, use_feat4, gbm4)
# 	gc.collect()
# 	cur_time = datetime.datetime.now().strftime('%Y-%m-%d#%H:%M:%S')
# 	res_path = '{}/day{}_{}_5.csv'.format(opt['result_dir'], opt['test_startday'], cur_time)
# 	res.to_csv(res_path, index=False)
# 	print('保存测试结果至：', res_path)

if __name__ == '__main__':
    fire.Fire()