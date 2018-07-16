# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    print('原来数据有{}行，去除空值后有{}行'.format(data_df.shape[0],cln_df.shape[0]))
    
    return cln_df

    
def analyze_dual_variables(data_df,var1,var2):
    '''
        查看双变量的关系,散点图
    '''
    
    sns.jointplot(x=var1,y=var2,data=data_df)
    plt.savefig(os.path.join(output_path,var1+'_'+var2+'_sandian.png'))
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
    
    #盒类型图
    #analyze_data(processed_data,'PM_China')
    
    #散点图：
    #analyze_dual_variables(processed_data,'season','PM_US')
    
    #时间与pm2.5
    analyze_dual_variables(processed_data,'hour','PM_US')
    
    #月份与pm2.5
    analyze_dual_variables(processed_data,'month','PM_US')
    
    #年与pm2.5
    analyze_dual_variables(processed_data,'year','PM_US')
    
if __name__ == '__main__':
    main()
