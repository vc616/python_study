from xpinyin import Pinyin

s = u"汉语拼音转换"
# 实例拼音转换对象
p = Pinyin()
# 进行拼音转换
ret = p.get_pinyin(s, tone_marks='marks')
ret1 = p.get_pinyin(s, tone_marks='numbers')
print(ret+'\n'+ret1)

