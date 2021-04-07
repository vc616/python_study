import requests, json
# https://cp.xuthus.cc/                        #消息推送服务器

spkey = 'b6bc04c871161bc97e5811841f78233b'     #CPkey，填上自己的

qq = 'https://push.xuthus.cc/send/' + spkey    #推送到个人QQ
qqg = 'https://push.xuthus.cc/group/' + spkey  #推送到个人QQ群
wx = "https://push.xuthus.cc/wx/" + spkey      #推送到个微信
tdwt = "123456789，1234567890，1234567890，1234567890，1234567890，1234567890，1234567890，1234567890，1234567890，"
# print(cpurl)
requests.post(qq, tdwt.encode('utf-8'))
requests.post(qqg, tdwt.encode('utf-8'))
requests.post(wx, tdwt.encode('utf-8'))
