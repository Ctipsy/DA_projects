## Ctipsy原创分享，转载或修改请务必提前联系我

---------------------------
**更新**  

emmm，我的豆瓣帐号又被封了
跑代码的同学，需要先在浏览器登录豆瓣获取cookies，然后手动把它放到代码里(我已经作注释)，否则代码不能正常运行。

---------------------------


### 使用说明
#### **1、第三方库支持**

pyecharts  
snownlp  
jieba  
wordcloud  


#### **2、data_scrapy.py为爬虫获取数据脚本**
步骤：
* 登录豆瓣获取自己的cookies
* 先搜索想要分析的电影，然后通过URL获取ID例如《[我不是药神](https://movie.douban.com/subject/26752088/?from=showing)》ID为26752088
* 输入想要爬取的页数（最大为49）
* run

#### **3、visualization_analysis.py为数据可视化分析脚本**
步骤
* 输入电影名称(爬虫完成后，会自动生成相应的  电影名.csv  文件)
* 输入停用词条名(自行创建txt文件)
* 输入需要设置为词云背景的图片(自行创建) 

#### 4、欢迎PR
如您有更好的代码实现或者更妙的分析思路，欢迎`Issue`和`Pull Request`

#### 5、注
* pyecharts生成的渲染图片为html源文件，可以在浏览器中直接另存为图片即可
* 录制视频采用chrome插件神器“Loom”，[官网](https://www.useloom.com)
