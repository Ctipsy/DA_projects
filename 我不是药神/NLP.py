import numpy as np
import re
from snownlp import SnowNLP
import matplotlib
import matplotlib.pyplot as plt
from itertools import  islice
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

f = open('comments.csv', 'r', encoding='UTF-8')
sentimentslist = []
m = '[\d]+'
for line in islice(f, 1, None):   # 跳过csv文件表头
    match = re.compile(m).match(line)
    if match is not None:         # 跳过不规则换行的评论
        print(line.split(",")[2])
        # s = SnowNLP(line.split(",")[2])
        # print(s.sentiments)
        # sentimentslist.append(s.sentiments)
    else:
        continue
plt.hist(sentimentslist, bins=np.arange(0, 1, 0.01), facecolor='g')
plt.xlabel('文本情感概率值')
plt.ylabel('数量')
plt.title('情感分析')
plt.show()