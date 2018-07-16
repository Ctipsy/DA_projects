# coding: utf-8
import re
import jieba
from scipy.misc import imread  # 这是一个处理图像的函数
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt
#选择背景图片，颜色最好对比分明，不然生成的词图，轮廓不明显
back_color = imread('chenli.jpg')  # 解析该图片

# WordCloud各含义参数请点击 wordcloud参数
wc = WordCloud(background_color='white',  # 背景颜色
               max_words=1000,  # 最大词数
               mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
               max_font_size=100,  # 显示字体的最大值
               stopwords=STOPWORDS.add(' '),  # 使用内置的屏蔽词，再添加'苟利国'
               font_path="C:/Windows/Fonts/msyhbd.ttc",  # 显示中文，从属性里复制字体名称，不能直接看windows显示的字体名
               random_state=42,  # 为每个词返回一个PIL颜色
               # width=1000,  # 图片的宽
               # height=860  #图片的长
               )


# 添加自己的词库分词，比如添加'陈粒啊'到jieba词库后，当你处理的文本中含有“陈粒啊”这个词，
# 就会直接将'陈粒啊'当作一个词，而不会得到'陈粒'或'粒啊'这样的词
jieba.add_word('陈粒啊')

# 打开词源的文本文件，加read以字符串的形式
txt = open('all_outputs.txt','r',encoding='UTF-8').read()
# 去除文本中的英文，特殊符号等，只保留中文
txt = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", txt)

# 该函数的作用就是把屏蔽词去掉，使用这个函数就不用在WordCloud参数中添加stopwords参数了
# 把你需要屏蔽的词全部放入一个stopwords文本文件里即可
def stop_words(texts):
    words_list = []
    word_generator = jieba.cut(texts, cut_all=False)  # 返回的是一个迭代器
    with open('stop_word.txt','r',encoding='UTF-8') as f:
        str_text = f.read()
        #print(str_text)  #如果不知道解码是否正确，可print一下，看输出的中文是否乱码
        f.close()  # stopwords文本中词的格式是'一词一行'
    for word in word_generator:
        if word.strip() not in str_text:
            words_list.append(word)
    return ' '.join(words_list)  # 注意是空格

text = stop_words(txt)
#print(text)  ##如果不知道解码是否正确，可print一下，看输出的中文是否乱码
wc.generate(text)
# 基于背景图像生成相应彩色
image_colors = ImageColorGenerator(back_color) 
# 显示图片
plt.imshow(wc)
# 关闭坐标轴
plt.axis('off')
# 绘制词云
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis('off')
# 保存图片
wc.to_file('result.png')
plt.imshow(wc.recolor())
plt.axis('off')
# 保存图片
wc.to_file('result2.png')