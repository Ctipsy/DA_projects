# -*- coding:utf-8 -*-
import sys, jieba, jieba.analyse, xlwt
if __name__ == "__main__":
    wbk = xlwt.Workbook(encoding='ascii')
    sheet = wbk.add_sheet("wordCount")  # Excel单元格名字
    word_lst = []
    key_list = []
    for line in open('all_outputs.txt', 'rb'):  # 1.txt是需要分词统计的文档
        item = line.strip('\n\r'.encode('utf-8')).split('\t'.encode('utf-8'))  # 制表格切分
       
        tags = jieba.analyse.extract_tags(item[0])  # jieba分词
        for t in tags:
            word_lst.append(t)
    word_dict = {}
    with open("wordCount.txt", 'bw') as wf2:  # 打开文件
        for item in word_lst:
            if item not in word_dict:  # 统计数量
                word_dict[item] = 1
            else:
                word_dict[item] += 1
        orderList = list(word_dict.values())
        orderList.sort(reverse=True)
        # print orderList
        for i in range(len(orderList)):
            for key in word_dict:
                if word_dict[key] == orderList[i]:
                    wf2.write((key + ' ' + str(word_dict[key])).encode('utf-8'))  # 写入txt文档
                    wf2.write('\n'.encode('utf-8'))  # 写入txt文档
                    key_list.append(key)
                    word_dict[key] = 0
    #为了便于tableau限量统计，可把range(len(key_list)): 改为range(200)，限定200个词 
    for i in range(200):  
        sheet.write(i, 1, label=orderList[i])
        sheet.write(i, 0, label=key_list[i])
    wbk.save('wordCount.xls')  # 保存为 wordCount.xls文件
