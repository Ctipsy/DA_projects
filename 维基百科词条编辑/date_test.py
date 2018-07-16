import  os
# print(os.getcwd()) #获取当前工作目录路径
# print(os.path.abspath('.')) #获取当前工作目录路径
# print(os.path.abspath('test.txt')) #获取当前目录文件下的工作目录路径
# print(os.path.abspath('..')) #获取当前工作的父目录 ！注意是父目录路径
# print(os.path.abspath(os.curdir)) #获取当前工作目录路径

def write_to_csv(word, pre, source):
    path = os.getcwd()+"\\"+word
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    with open(path + "\\" + word + pre + ".csv", 'w', encoding='utf-8') as f:
        for i in source:
            f.write(str(i[0]))
            f.write(",")
            f.write(str(i[1])+'\n')
    f.close()


def main(word, source):
    write_to_csv(word, "_ceshi", source)


if __name__ == '__main__':
    main("AI", ["可以，不错"])
