from pypinyin import lazy_pinyin

chars = ['鑫','鹭','榕','柘','珈','骅','孚','迦','瀚','濮','浔','沱','泸','恺','怡','岷','萃','兖']
chars = "你好的"
chars.sort(key=lambda char: lazy_pinyin(char)[0][0])
print([lazy_pinyin(char) for char in chars])
print(chars)