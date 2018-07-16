# -*- coding: utf-8 -*-
'''
    明确任务：使用柱状图可视化北京地区 PM2.5
'''
import os
import pandas as pd
import matplotlib.pyplot as plt


#数据文件的路径
datafile_path = './data/pm/Beijing_PM.csv'

#输出文件的路径
output_path = './output/pm'
if not os.path.exists(output_path):
    os.makedirs(output_path)

 
def collect_data():
    '''
        STEP1: 收集数据
    '''
    data_pd = pd.read_csv(os.path.join(datafile_path))
   
    return data_pd
    
    
def inspect_data(data_pd):
    '''
        STEP2: 描述数据
    '''
    print('数据文件中一共有{}行，{}列'.format(data_pd.shape[0],data_pd.shape[1]))
    
    print('数据预览')
    print(data_pd)
    
    print('数据的前5行')
    print(data_pd.head)
    
    print('数据文件的的基本信息')
    print(data_pd.info())
    
    print('数据内容的统计信息')
    print(data_pd.describe())
    
    
def ananlyze_data(data_pd):
    '''
        STEP3: 分析数据
    '''
    #按照年进行分组
    year_col = data_pd['year']
    year_grouped = data_pd.groupby(year_col)
    
    #分别计算出每年中国和美国给出的平均值
    pm_ch_mean =year_grouped['PM_China'].mean()
    pm_us_mean =year_grouped['PM_US'].mean()
    
    return pm_ch_mean,pm_us_mean
  
    
def save_and_show_data(pm_ch_mean,pm_us_mean):
    '''
        STEP4: 保存和可视化数据
    '''
    #保存数据集为csv文件
    pm_ch_mean.to_csv(os.path.join(output_path,'./pm_ch_mean.csv'))
    pm_us_mean.to_csv(os.path.join(output_path,'./pm_us_mean.csv'))

    #使用柱状图可视化
    pm_ch_mean.plot(kind='bar')
    plt.title('PM china mean')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path,'./pm_ch_mean.png'))
    
    
    pm_us_mean.plot(kind='bar')
    plt.title('PM us mean')
    plt.tight_layout()
    plt.savefig(os.path.join(output_path,'./pm_us_mean.png'))
    plt.show()
    

def main():
    #主函数
    
    #收集数据
    data_pd = collect_data()
    
    #描述数据
    inspect_data(data_pd)
    
    #分析数据
    pm_ch_mean,pm_us_mean = ananlyze_data(data_pd)
    
    #保存和可视化数据
    save_and_show_data(pm_ch_mean,pm_us_mean)


if __name__ == '__main__':
    main()
