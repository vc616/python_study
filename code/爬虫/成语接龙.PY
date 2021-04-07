# 读取数据
import random

from xpinyin import Pinyin

file = open('idiom.txt', 'r', encoding='gbk')
line = file.readline()
data = []
while line:
    singledata = ''.join(line.split()).split('/')[0]
    # print(singledata)
    if len(singledata) == 4:
        data.append(singledata)
    line = file.readline()

file.close()
print(data)
# result = []
pin = Pinyin()
# for i in data:
#     result.append((pin.get_pinyin(i), i))
# print(result)
random.shuffle(data)
d = data[0]
d = "隔墙有耳"
n = 1
print(n, d, len(data))
new = []
n = n + 1
while 1:
    last = d[3]
    for i in data:
        if pin.get_pinyin(i[0]) == pin.get_pinyin(last):
            new.append(i)
    if len(new) > 0:
        random.shuffle(new)
        d = new[0]
        print(n, d, len(data))
        new = []
        data.remove(d)
        n = n + 1
    else:
        break
