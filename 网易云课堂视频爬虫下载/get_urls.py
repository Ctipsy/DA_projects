import requests
import re
import sys
import getopt

opts, args = getopt.getopt(sys.argv[1:], '-h-g-d:-n:', ['help','generate', 'dir=', 'name='])

def GetInfo(Vid):
    print("正在获取课程信息...")
    data={'callCount':1,
    'scriptSessionId':'${scriptSessionId}190',
    'c0-scriptName':'PlanNewBean',
    'c0-methodName':'getPlanCourseDetail',
    'c0-id':'0',
    'c0-param0':'string:'+Vid,
    'c0-param1':'number:0',
    'c0-param2':'null:null',
    'batchId':"1506324769538"}

    html=requests.post('http://study.163.com/dwr/call/plaincall/PlanNewBean.getPlanCourseDetail.dwr?1506324769538',data=data,headers=headers)

    #s16.lessonName="\u8BBE\u7F6E\u5750\u6807\u8F741";s16.leve
    LessonName=re.findall(r's\w*?\.id=(.*?);.*?s(\w*?)\.lessonName="(.*?)";',html.text)
    return LessonName



def GetVideoUrl(LessonName, Vid):
    print("正在获取课件信息：")
    Lists = []
    for i in range(0,len(LessonName)):

        Vnum =  LessonName[i][0]
        VName = LessonName[i][2].encode('utf-8').decode('unicode_escape','ignore')
        print(VName)

        data={'callCount':'1',
        'scriptSessionId':'${scriptSessionId}190',
        'c0-scriptName':'LessonLearnBean',
        'c0-methodName':'getVideoLearnInfo',
        'c0-id':'0',
        'c0-param0':'string:'+ Vnum,
        'c0-param1':'string:'+ Vid,
        'batchId':'1506324769538'}

        video=requests.post("http://study.163.com/dwr/call/plaincall/LessonLearnBean.getVideoLearnInfo.dwr?1506327358812",data=data,headers=headers)
        try:
            Vurl = re.findall(r'flvHdUrl="(.*?)"',video.text)[0]
        except:
            pass
        Value = [VName,Vurl]
        Lists.append(Value)
    return Lists

def MakeTxt(Lists):
    print("正在生成视频地址...")
    AllLinks = ""

    for i in range(0,len(Lists)):
    #    Lists[i][1] = Lists[i][1].replace("http://","")
        Links = '<div class="down"><a href="'+Lists[i][1]+'">'+Lists[i][0]+'</a></div>'+"\n"
        AllLinks = AllLinks + Links
    filename = Vid+".html"
    with open(filename,'w',encoding='utf-8') as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="x-ua-compatible" content="IE=edge,chrome=1"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <title>视频下载页面</title>
    <link rel="stylesheet" type="text/css" href="http://www.lz1y.cn/css/download.css">
</head>
<body>
<div class="download">
    <div class="head">
    <div class="logo"><img src="http://www.lz1y.cn/wordpress/wp-content/uploads/2017/06/cropped-C977239D-7B8E-2709-E8CB-A03DD1E6FAF9.png@236w_0e_1l-180x180.png" alt="logo"></div>
    <div class="logo-title">网易云课堂视频下载 <br /> Author: Lz1y</div>
    </div><br/><br/><br/><br/><br/><br/><br/>
        <div class="down-column">
    <div class="down1"><a href="">课程下载</a></div>
    """+AllLinks+"""
    </div>
    <div class="foot"><p><a href="http://www.lz1y.cn/wordpress" target="_blank"><font color="black">Lz1y'Blog | Coding My world</a></p>
    </div>
</div>
</body>
</html>
    """)

def MakeHtml(Lists):
    print(Lists[i][1])
    AllLinks = ""

    filename = Vid + "_name.txt"
    for i in range(0,len(Lists)):
        Links = '<div class ="down"><font color="black"><a href="'+Lists[i][1]+'"> '+Lists[i][0]+' </font></a></div>'
        AllLinks = AllLinks + Links

        with open(filename,'a',encoding='utf-8') as f:
            f.write(Lists[i][0])

    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>视频下载页面</title>
    <link rel="stylesheet" type="text/css" href="http://www.lz1y.cn/css/download.css">
</head>
<body>
<div class="app-download">
    <div class="logo"><img src="//www.lz1y.cn/wordpress/wp-content/uploads/2017/06/cropped-C977239D-7B8E-2709-E8CB-A03DD1E6FAF9.png@236w_0e_1l-180x180.png" alt="logo"></div>
    <div class="logo-title">网易云课堂视频下载 <br /> Author: Lz1y</div><br>"""+AllLinks+"""
    <br><p><a href="http://www.lz1y.cn/wordpress" target="_blank"><font color="black">Lz1y'Blog | Coding My world</a></p>
</div>
</body>
</html>
    """
    filename = Vid+".html"
    with open(filename,'w',encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/61.0"}  
    Vid = input("\n请输入CourseId，然后按回车:\n")
    LessonName = GetInfo(Vid)
    Lists = GetVideoUrl(LessonName, Vid)
    MakeTxt(Lists)
"""
    for opt_name, opt_value in opts:
        if opt_name in ('-d', '--dir'):
            dir = opt_value

        if opt_name in ('-n', '--name'):
            name = opt_value
            with open(name,'w',encoding='utf-8') as f:
                names = f.readlines()
            files = os.listdir(dir)
            for i in range(0,len(files)):
                os.rename(dir+"/"+files[i],dir+"/"+names[i])


        if opt_name in ('-g','--generate'):
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0"}

            Vid = input("请输入CourseId:\n")
            LessonName = GetInfo(Vid)
            Lists = GetVideoUrl(LessonName, Vid)
            MakeTxt(Lists)

        if opt_name in ('-h', '--help'):
            print("-g --generate   生成web页面")
            



    #    MakeHtml(Lists)
"""
