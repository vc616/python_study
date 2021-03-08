import wget
import tempfile

url = 'https://down.qq.com/qqweb/PCQQ/PCQQ_EXE/PCQQ2020.exe'

# 获取文件名
file_name = wget.filename_from_url(url)
print(file_name)  #1106F5849B0A2A2A03AAD4B14374596C76B2BDAB_w1000_h626.jpg
file_name = wget.download(url)
print(file_name)