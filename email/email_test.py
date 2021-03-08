# 发送文件夹中的所有文件到邮箱
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.application import MIMEApplication
from email.header import Header
import smtplib
import sys
import os

sys.path.append("..")
from key import k

my_sender = "vc616@qq.com"
my_pass = k.email_pass
my_user = ["vc616@qq.com", ]
path = r"C:\Users\vm\PycharmProjects\Pycharm_all\to_github\email\附件"


class mailsend():

    def mail(self, t, c):  # 发送邮件
        try:
            multipart = MIMEMultipart()
            # msg = MIMEText(c, 'plain', 'utf-8')
            multipart['From'] = my_sender  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            multipart['Subject'] = t  # 邮件的主题，也可以说是标题
            multipart["To"] = my_sender
            part = MIMEText(c)
            multipart.attach(part)

            os.chdir(path)
            dir = os.getcwd()

            for fn in os.listdir(dir):  ##返回字符串文件名
                print(fn)
                attachment = MIMEApplication(open(fn, 'rb').read())
                # attach["Content-Type"] = 'application/octet-stream'
                # attach["Content-Disposition"] = 'attachment; filename=' + fn
                attachment.add_header('Content-Disposition', 'attachment', filename=fn)
                multipart.attach(attachment)

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, my_user, multipart.as_bytes())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            # server.sendmail(my_sender, my_user, msg.as_string())
            server.quit()  # 关闭连接
            print("邮件发送成功")
            return "OK"
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print("邮件发送失败")
            return "err"


r = mailsend()
r.mail("测试附件", "文件已解密")
