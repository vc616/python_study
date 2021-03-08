import re

s = "db113_40_3"
n = re.findall(r"(\d+)", s)
print(n)

content = 'Hello 123456789 Word_This is just a test 666 Test'
result = re.search('(\d+)', content)

print(result)
print(result.group())  # print(result.group(0)) 同样效果字符串
print(result.groups())
print(result.group(1))