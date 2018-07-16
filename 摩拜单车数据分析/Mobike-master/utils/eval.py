# -*- coding:utf-8 -*-
import os
import pandas as pd
import numpy as np
import pickle
from .helper import rank

# 获取真实标签
def get_label(data, opt):
    result_path = opt['cache_dir'] + '/true.pkl'
    if os.path.exists(result_path):
        true = pickle.load(open(result_path, 'rb+'))
    else:
        train = pd.read_csv(opt['train_csv'])
        test = pd.read_csv(opt['test_csv'])
        test['geohashed_end_loc'] = np.nan
        data_all = pd.concat([train, test])
        true = dict(zip(data_all['orderid'].values, data_all['geohashed_end_loc']))
        pickle.dump(true, open(result_path, 'wb+'))
    data['label'] = data['orderid'].map(true)
    if data.get('geohashed_end_loc', None) is not None:
        data['label'] = (data['label'] == data['geohashed_end_loc']).astype('int')
    return data

# 整合预测结果
def reshape(pred):
    result = pred[["orderid", "pred", "geohashed_end_loc"]].copy()
    result = rank(result, 'orderid', 'pred', ascending=False)
    result = result[result['rank']<3][['orderid', 'geohashed_end_loc', 'rank']]
    result = result.set_index(['orderid', 'rank']).unstack()
    result.reset_index(inplace=True)
    result.columns = ['orderid', 0, 1, 2]
    return result

# 评估函数
def map_score(result):
    '''
        result: orderid, 0, 1, 2, label
    '''
    data = result.copy()
    acc1 = sum(data['label'] == data[0]) # 第一个位置上正确的个数
    acc2 = sum(data['label'] == data[1]) # 第二个位置上正确的个数
    acc3 = sum(data['label'] == data[2]) # 第三个位置上正确的个数
    score = (acc1+acc2/2+acc3/3)/data.shape[0]
    return score, acc1, acc2, acc3, data.shape[0]

# 预测结果
def predict(data, feat, model):
    data.loc[:, 'pred'] = model.predict(data[feat])
    res = reshape(data)
    res.fillna('0', inplace=True)
    return res

# 获取分数
def get_score(data, feat, model, opt):
    res = predict(data, feat, model)
    res = get_label(res, opt)
    score = map_score(res)
    return score
