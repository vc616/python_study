# server酱网址：http://sc.ftqq.com/?c=code
#
import requests
url = "https://sc.ftqq.com/SCU98381T86c11dea8f3d0d012833692fb247f9ee5fbf09db5a105.send"
data = {"text":"99999","desp":"555",}
res = requests.post(url=url,data=data)
print(res.text)