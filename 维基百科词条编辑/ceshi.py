# import math
#
# def move(x, y, step, angle=0):
#     nx = x + step * math.cos(angle)
#     ny = y - step * math.sin(angle)
#     nz = 1+3
#     return nx, ny, nz
#
#
# y = move(100, 100, 60, math.pi / 6)
# print(y[2])


# import re
#
# ip1 = "2405:204:8088:c6bc:882d:3c33:7aa2:6ba0"
# ip2 = "1.152.110.187"
# ip3 = "103.206.131.178"
# ip4 = "703jun"
# m = '([a-f0-9]{1,4}(:[a-f0-9]{1,4}){7}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){0,7}::[a-f0-9]{0,4}(:[a-f0-9]{1,4}){0,7})|' \
#     '(((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))'
# pattern = re.compile(m)
# match = pattern.match(ip4)
# print(match)
# if match is not None:
#     print("是IP")
# else:
#     print("是")

# import ctypes
#
# ctypes.windll.user32.MessageBoxA(0, r"尚未收录该词条！".encode('gb2312'), r'提示'.encode('gb2312'), 0)




