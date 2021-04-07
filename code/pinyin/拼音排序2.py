from xpinyin import Pinyin
s = """大小鸟上下早牙刷起山水火木马四个人羊七八手太工才有一向中用们九只十二月六齿
江南鱼西北可以树叶正在你去飞来我的怎么空船国回游东晚
白云儿泥土子方头电广是五光色式亮了播视塔巨天河里祖家阳从升
他背心怀抱听见丰满时不说和气好出生面口开知风道浮毛全鹅雪看闹浪笑
虫害昆田地野园庄蚂蚁冬今当牛皮沙渔民村宝贝壳扇泉音乐林荫公交车通胶焦点朋友相及
写字书文古代候老先领后到日言长久法壮信青草岛年万干花对住房助分为入三裂散活主杯外强"""

def my_function(lis):  # 输入一个名字的列表
    pin = Pinyin()
    result = []
    for item in lis:
        result.append((pin.get_pinyin(item), item))
    print(result)
    result.sort()
    print(result)
    for i in range(len(result)):
        result[i] = result[i][1]
    result = ''.join(result)  # 将排好序的结果使用空格连接，方便输出
    print(result)  # 输出结果


my_function(s)