# -*- coding:utf-8 -*-
import pandas as pd
import datetime

result_dir = '../result'

test25 = pd.read_csv(result_dir + '/day25_2017-09-24#05:02:10_wc_sample_0.58893.csv')
test26 = pd.read_csv(result_dir + '/day26_2017-09-24#09:27:13_wc_sample_0.58893.csv')
test27 = pd.read_csv(result_dir + '/day27_2017-09-24#16:49:10_wc_sample_0.58893.csv')
test28 = pd.read_csv(result_dir + '/day28_2017-09-24#20:18:04_wc_sample_0.58893.csv')
test29 = pd.read_csv(result_dir + '/day29_2017-09-24#23:26:19_wc_sample_0.58893.csv')
test30 = pd.read_csv(result_dir + '/day30_2017-09-25#02:02:54_wc_sample_0.58893.csv')
test31 = pd.read_csv(result_dir + '/day31_2017-09-25#08:46:58_wc_sample_0.58893.csv')

# 生成全部测试结果
test = pd.read_csv('../../MOBIKE_CUP_2017/test.csv')
res = pd.concat([test25, test26, test27, test28, test29, test30, test31])
print(res.shape)
res = pd.merge(test[['orderid']], res, on='orderid', how='left')
res.fillna('0', inplace=True)

# 生成提交文件
cur_time = datetime.datetime.now().strftime('%Y-%m-%d#%H:%M:%S')
res_path = '{}/result_{}_{}.csv'.format(result_dir, '0.58893_wc_sample', cur_time)
res.to_csv(res_path, header=False, index=False)
print('保存提交结果至：', res_path)