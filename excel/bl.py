# -*-coding:utf-8-*-
import os
i = 0
# for root, dirs, files in os.walk("C:\Program Files\Git"):
for root, dirs, files in os.walk('/to_github/email\\test'):
    # print(root,"_______",dirs,"______",files)
    print(files)
    # for dir in dirs:
    #     print(os.path.join(root, dir))
    #     for file in files:
    #         print(os.path.join(root, file))
    #         i = i +1
os.chdir("/to_github/email\\test")
dir = os.getcwd()
for fn in os.listdir(dir):  ##返回字符串文件名
    print(fn)
# print(i)