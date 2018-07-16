# -*- coding: utf-8 -*-
'''
    明确任务：1.透视表分析pm2.5
'''

import os
import pandas as pd
import matplotlib.pyplot as plt

#数据文件的路径
datafile_path = './data/pm/Beijing_PM.csv'

#输出文件保存路径
output_path = './output/pm'

#保存存储路径
if not os.path.exists(output_path):
    os.makedirs(output_path)


def collect_data():
    '''
        读取数据
    '''
    
    data_df = pd.read_csv(datafile_path)   
    return data_df


def inspect_data(data_df):
    '''
        查看数据结果
    '''
    print('数据一共有{}行，{}列'.format(data_df.shape[0],data_df.shape[1]))
    #print('查看结果'）
    print(data_df) 
    
    print('查看前5行结果\n\n')
    print(data_df.head()) 
    
    print('查看前10行结果\n\n')
    print(data_df.head(10)) 
    
    print('查看数据的所有列类型\n\n')
    print(data_df.info()) 
    
    print('查看数据文件的类型\n\n')
    print(type(data_df))
    
    print('数据统计信息\n\n')
    print(data_df.describe())


def process_data(data_df):
    '''
        数据清洗
        1. 去除空值
    '''
    
    #去除空置
    cln_df = data_df.dropna()
    
    return cln_df
    

def analyze_data(data_df):
    '''
         数据分析
         1. 找出差别最大的10天的记录
         2. 中国环保部和美国使馆检测的每年平均PM2.5的值
    '''
    
   # 1. 按年月进行分组操作
    grouped_results = data_df.groupby(by=['year', 'month'])['PM_US'].mean()
    
    # 2. 按年月进行透视表操作
    pivot_results = pd.pivot_table(data_df, index='year', columns='month',
                               values='PM_US', aggfunc='mean')
    
    return grouped_results,pivot_results


def sava_and_show_results(grouped_results,pivot_results):
    '''
         数据可视化
         
    '''
    
    #保存数据
    grouped_results.to_csv(os.path.join(output_path,'grouped_results.csv'))
    
    pivot_results.to_csv(os.path.join(output_path,'pivot_results.csv'))
    
    #柱状图
    pivot_results.plot(kind='bar')
    plt.title('Beijing PM 2.5')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path,'pivot_results_nostacked.png'))
    plt.show()
    
    
    #堆叠柱状图可视化
    pivot_results.plot.bar(stacked=True)
    plt.title('Beijing PM 2.5')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path,'pivot_results_stacked.png'))
    plt.show()
    

def main() :
    '''
        主函数
    '''
    
    #读取数据
    data_df = collect_data()
    
    #查看数据
    inspect_data(data_df)
    
    #处理数据
    processed_data = process_data(data_df)
    
    #分析数据
    grouped_results,pivot_results = analyze_data(processed_data)
    
    #保存和显示数据
    sava_and_show_results(grouped_results,pivot_results)
    
if __name__ == '__main__':
    main()