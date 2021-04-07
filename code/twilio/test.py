import time
from twilio.rest import Client  # 需要装twilio库
import sys

sys.path.append("..")
from key import k

# 获取当前时间并格式化显示方式：
send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def send_message(to, content):
    account_sid = k.twilio_account_sid  # api参数 复制粘贴过来
    auth_token = k.twilio_auth_token  # api参数 复制粘贴过来
    client = Client(account_sid, auth_token)  # 账户认证
    message = client.messages.create(
        to="+86" + to,  # 接受短信的手机号 注意写中国区号 +86
        from_="+12705183514",  # api参数 Number(领取的虚拟号码
        body=content)  # 自定义短信内容
    print('接收短信号码：' + message.to)
    # 打印发送时间和发送状态：
    print('发送时间：%s \n状态：发送成功！' % send_time)
    print('短信内容：\n' + message.body)  # 打印短信内容
    print('短信SID：' + message.sid)  # 打印SID


send_message(k.myphone, "123456789012345678901234567890123456789012345678901234567890")  # 调用执行函数
