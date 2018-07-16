# -*- coding:utf-8 -*-
import pandas as pd

# 将用户的历史目的地加入为样本
def get_user_end_loc(train, test):
    user_eloc = train[['userid', 'geohashed_end_loc']]
    result = pd.merge(test[['orderid', 'userid']], user_eloc, on='userid', how='left')
    result = result[['orderid', 'geohashed_end_loc']].drop_duplicates()
    result['user_end_loc_sample'] = 1
    return result

# 将用户的历史出发地加入为样本
def get_user_start_loc(train, test):
    # user_sloc_train = train[['userid', 'geohashed_start_loc']]
    # user_sloc_test = test[['userid', 'geohashed_start_loc']]
    user_sloc_train = pd.read_csv('../../MOBIKE_CUP_2017/train.csv')[['userid', 'geohashed_start_loc']].drop_duplicates()
    user_sloc_test = pd.read_csv('../../MOBIKE_CUP_2017/test.csv')[['userid', 'geohashed_start_loc']].drop_duplicates()
    user_sloc = pd.concat([user_sloc_train, user_sloc_test])
    # user_sloc = train[['userid', 'geohashed_start_loc']].drop_duplicates()
    result = pd.merge(test[['orderid', 'userid']], user_sloc, on='userid', how='left')
    result.rename(columns={'geohashed_start_loc':'geohashed_end_loc'}, inplace=True)
    result = result[['orderid', 'geohashed_end_loc']].drop_duplicates()
    result['user_start_loc_sample'] = 1
    return result

# 将起始地点出发到的Top10地方加入为样本
def get_loc_to_loc(train, test):
    # sloc_eloc_count = train.groupby(['geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['geohashed_end_loc'].agg({'sloc_eloc_count':'count'})
    # sloc_eloc_count.sort_values('sloc_eloc_count', inplace=True)
    # if train['userid'].values[0] != -1: sloc_eloc_count = sloc_eloc_count.groupby('geohashed_start_loc').tail(15)
    sloc_eloc = train[['geohashed_start_loc', 'geohashed_end_loc']].drop_duplicates()
    result = pd.merge(test[['orderid', 'geohashed_start_loc']], sloc_eloc, on='geohashed_start_loc', how='left')
    # result = pd.merge(test[['orderid', 'geohashed_start_loc']], sloc_eloc_count, on='geohashed_start_loc', how='left')
    result = result[['orderid', 'geohashed_end_loc']].drop_duplicates()
    result['loc_to_loc_sample'] = 1
    return result

# 将热度大于2的地址对加入为样本
# def get_loc_to_loc2(train, test):
#     sloc_eloc_count = train.groupby(['geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['geohashed_end_loc'].agg({'sloc_eloc_count':'count'})
#     sloc_eloc_count = sloc_eloc_count[sloc_eloc_count['sloc_eloc_count']>=2]
#     result = pd.merge(test[['orderid', 'geohashed_start_loc']], sloc_eloc_count, on='geohashed_start_loc', how='left')
#     result = result[['orderid', 'geohashed_end_loc']].drop_duplicates()
#     result['loc_to_loc2_sample'] = 1
#     return result

# 将以起始地点作为结束地点出发的Top10地方加入为样本
# def get_loc_to_loc2(train, test):
#     sloc_eloc_count = train.groupby(['geohashed_start_loc', 'geohashed_end_loc'], as_index=False)['geohashed_end_loc'].agg({'sloc_eloc_count':'count'})
#     sloc_eloc_count.sort_values('sloc_eloc_count', inplace=True)
#     sloc_eloc_count.rename(columns={'geohashed_start_loc': 'geohashed_end_loc', 'geohashed_end_loc': 'geohashed_start_loc'}, inplace=True)
#     if train['userid'].values[0] != -1: sloc_eloc_count = sloc_eloc_count.groupby('geohashed_start_loc').tail(10)
#     result = pd.merge(test[['orderid', 'geohashed_start_loc']], sloc_eloc_count, on='geohashed_start_loc', how='left')
#     result = result[['orderid', 'geohashed_end_loc']]
#     return result

# 将热度最高的Top10目的地点加入为样本
# def get_hot_eloc(train, test):
#     hot_eloc = train.groupby('geohashed_end_loc', as_index=False)['orderid'].agg({'cnt': 'count'})
#     hot_eloc.sort_values(by='cnt', inplace=True)
#     hot_eloc = hot_eloc['geohashed_end_loc'].tail(10)
#     hot_eloc = pd.concat([hot_eloc] * test.shape[0]).reset_index()
#     result = pd.DataFrame({'orderid': pd.concat([test['orderid']] * 10)}).sort_values(by='orderid').reset_index()
#     result.loc[:, 'geohashed_end_loc'] = hot_eloc
#     return result

# 将自行车下一个出发地点(在全部测试集中寻找)加入为样本
def get_bike_next_sloc(train, test):
    train_set = pd.read_csv('../../MOBIKE_CUP_2017/train.csv')
    test_set = pd.read_csv('../../MOBIKE_CUP_2017/test.csv')
    all_set = pd.concat([train_set, test_set])
    bike_sloc = all_set[['orderid', 'bikeid', 'geohashed_start_loc', 'starttime']]
    bike_sloc.sort_values(by=['bikeid', 'starttime'], inplace=True, ascending=True)
    bike_sloc['next_bikeid'] = bike_sloc['bikeid'].shift(-1)
    bike_sloc['geohashed_end_loc'] = bike_sloc['geohashed_start_loc'].shift(-1)
    result = bike_sloc[(bike_sloc['bikeid'] == bike_sloc['next_bikeid']) & (bike_sloc['starttime'] >= test['starttime'].min()) & (bike_sloc['starttime'] <= test['starttime'].max())]
    result = result[['orderid', 'geohashed_end_loc']].drop_duplicates()
    result['bike_next_sloc_sample'] = 1
    # bike_sloc = test[['orderid', 'bikeid', 'geohashed_start_loc', 'starttime']].drop_duplicates()
    # bike_sloc.sort_values(by=['bikeid', 'starttime'], inplace=True, ascending=True)
    # bike_sloc['next_bikeid'] = bike_sloc['bikeid'].shift(-1)
    # bike_sloc['geohashed_end_loc'] = bike_sloc['geohashed_start_loc'].shift(-1)
    # result = bike_sloc[bike_sloc['bikeid'] == bike_sloc['next_bikeid']]
    # result = result[['orderid', 'geohashed_end_loc']]
    return result

# 寻找用户的下一个出发地点(在全部测试集中寻找)加入为样本
def get_user_next_sloc(train, test):
    train_set = pd.read_csv('../../MOBIKE_CUP_2017/train.csv')
    test_set = pd.read_csv('../../MOBIKE_CUP_2017/test.csv')
    all_set = pd.concat([train_set, test_set])
    user_sloc = all_set[['orderid', 'userid', 'geohashed_start_loc', 'starttime']]
    user_sloc.sort_values(by=['userid', 'starttime'], inplace=True, ascending=True)
    user_sloc['next_userid'] = user_sloc['userid'].shift(-1)
    user_sloc['geohashed_end_loc'] = user_sloc['geohashed_start_loc'].shift(-1)
    result = user_sloc[(user_sloc['userid'] == user_sloc['next_userid']) & (user_sloc['starttime'] >= test['starttime'].min()) & (user_sloc['starttime'] <= test['starttime'].max())]
    result = result[['orderid', 'geohashed_end_loc']].drop_duplicates()
    return result

# 构造样本
def get_sample(train, test, load=False):
    user_start_loc = get_user_start_loc(train, test)
    user_end_loc = get_user_end_loc(train, test)
    loc_to_loc = get_loc_to_loc(train, test)
    bike_next_sloc = get_bike_next_sloc(train, test)
    # 汇总
    result = pd.concat([user_end_loc[['orderid', 'geohashed_end_loc']],
                        user_start_loc[['orderid', 'geohashed_end_loc']],
                        loc_to_loc[['orderid', 'geohashed_end_loc']],
                        bike_next_sloc[['orderid', 'geohashed_end_loc']]
                       ]).drop_duplicates()

    restmp = pd.concat([user_end_loc,
                        user_start_loc,
                        loc_to_loc,
                        bike_next_sloc
                       ])
    restmp.fillna(0, inplace=True)
    restmp = restmp.groupby(['orderid', 'geohashed_end_loc'], as_index=False).sum()

    result = pd.merge(result, restmp, on=['orderid', 'geohashed_end_loc'], how='left')
    # 添加负样本
    result = pd.merge(result, test, on='orderid', how='left')
    # 删除出发点和目的点相同的样本 以及 异常值
    result = result[result['geohashed_end_loc'] != result['geohashed_start_loc']]
    result = result[(~result['geohashed_start_loc'].isnull()) & (~result['geohashed_end_loc'].isnull())]
    # print("原始样本数目：", result.shape)
    # sample_leak = bike_next_sloc[['orderid', 'geohashed_end_loc']].drop_duplicates()
    # print("Leak样本数目：", sample_leak.shape)
    # sample_leak['leak'] = 1
    # result = pd.merge(result, sample_leak, on=['orderid', 'geohashed_end_loc'], how='left')
    # result = result[result.leak.isnull()]
    # print("过滤Leak之后的样本数目：", result.shape)
    # del result['leak']
    if load:
        sample_27 = pd.read_pickle('/home/xuwenchao/dyj-storage/wc-sample/sample_filter_{}.pickle'.format(test.shape[0]))[['orderid', 'geohashed_end_loc', 'userid', 'bikeid', 'biketype', 'starttime', 'geohashed_start_loc']]
        # sample_27 = pd.concat([pd.read_pickle('/home/xuwenchao/dyj-storage/wc-sample/sample_filter_23_1_27_.pickle'), pd.read_pickle('/home/xuwenchao/dyj-storage/wc-sample/sample_filter_24_1_27_.pickle')])[['orderid', 'geohashed_end_loc', 'userid', 'bikeid', 'biketype', 'starttime', 'geohashed_start_loc']]
        result = pd.merge(sample_27, result[['orderid', 'geohashed_end_loc', 'user_end_loc_sample', 'user_start_loc_sample', 'loc_to_loc_sample', 'bike_next_sloc_sample']], on=['orderid', 'geohashed_end_loc'], how='left')
    print('构造样本完成：', result.shape, result[result.geohashed_start_loc.isnull()].shape)
    return result