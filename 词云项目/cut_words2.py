#!/usr/bin/env python3
#遇到的编码字符流问题参考了如下博客的解决方案
#https://blog.csdn.net/zhangyunfei_happy/article/details/47169939
import jieba
import re
# jieba.load_userdict('userdict.txt')
# 创建停用词list
jieba.load_userdict('usr_dict.txt')
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r',encoding='utf-8').readlines()]
    return stopwords

# 对句子进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('stop_word.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

if __name__ == '__main__':
    
   
    inputs = open('all.txt', 'r',encoding='ansi')  #源文件是'utf-8'编码，
    outputs = open('all_outputs.txt', 'w',encoding='utf-8')  #保存为utf8编码
    for line in inputs:
        line_seg = seg_sentence(line)  # 这里的返回值是字符串
        #注意有些符号是中英文两种格式，所以都要包含进去
        line_seg = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\：\（\）\，\。]", "", line_seg)
        outputs.write(line_seg)
        outputs.write('\n')
    outputs.close()
    inputs.close()
