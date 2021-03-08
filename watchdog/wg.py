# -*- coding:utf-8 -*-
import wx
# from IPython import embed
# import csv
import pymysql
import time
import threading
import sys
import logging
# from opcua import Client
from datetime import datetime

import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = "vc616@qq.com"  # 发件人邮箱账号
my_pass = "hcmjmman"  # 发件人邮箱密码
my_user = ["vc616@qq.com", ]  # 收件人邮箱账号

sys.path.insert(0, "..")
mysql_host = "192.168.0.81"
mysql_user = "root"
mysql_password = "********"
mysql_db = "dtro"
mysql_port = 3306
mailtexta = []
mailtextb = []
mailtext1 = []
emaileable = 1
dingshi = [9, 15, 21]
time_P = 0
linkerr_p = 0
linkerr_p1 = 0


class data_check():
    def __init__(self):
        self.host = mysql_host
        self.user = mysql_user
        self.password = mysql_password
        self.db1 = mysql_db
        self.port = mysql_port
        self.mailtext = []
        self.mailtexta = []
        self.mailtextb = []
        self.mailtext1 = []
        self.projectlist = {}
        self.t = "设备连线状态有更新："
        self.t2 = "设备状态定时发送"
        self.pn = []
        self.pncn = []

    def read_last(self, i):
        sq = "SELECT  Max(TIME) FROM  " + i
        try:
            db = pymysql.connect(self.host, self.user, self.password, self.db1, self.port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.commit()
            result = cursor.fetchall()
            db.close()
            for row in result:
                u = (datetime.now() - row[0])
                # print(u.seconds)
                if (u.seconds + u.days * 8400) > 300:
                    # print("异常断线，项目名称：" + i + "数据断线时长：" + str(u.seconds) )
                    self.mailtexta.append(self.projectlist[i] + "  时间：" + str(row[0]))
                else:
                    self.mailtextb.append(self.projectlist[i] + "  时间：" + str(row[0]))
        except:
            print("错误3")

    def mail(self, t, c):  # 发送邮件
        try:
            msg = MIMEText(c, 'plain', 'utf-8')
            msg['From'] = formataddr(["TDR", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            # msg['To'] = formataddr(["VIP", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = t  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, my_user, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            print("邮件发送成功")
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print("邮件发送失败")

    def read_prolist(self):  # 读取项目列表
        sq = "SELECT `ID` ,`项目名称`FROM config "
        localtime = time.localtime(time.time())
        global time_P
        global linkerr_p
        global linkerr_p1
        self.mailtext = []
        self.mailtexta = []
        self.mailtextb = []
        c = ""
        try:
            db = pymysql.connect(self.host, self.user, self.password, self.db1, self.port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.commit()
            result = cursor.fetchall()
            db.close()

            for row in result:
                self.pn.append(row[0])
                self.pncn.append(row[1])
            print("项目列表：", self.pn)
            print("项目列表：", self.pncn)
            self.projectlist = dict(zip(self.pn, self.pncn))
            print(self.projectlist)
            for i in self.pn:
                # print(i)
                self.read_last(i)

            n1 = "断线设备：( " + str(len(self.mailtexta)) + " )"
            n2 = "正常设备：( " + str(len(self.mailtextb)) + " )"
            if self.mailtexta == []:
                self.mailtexta = ["无"]
            if self.mailtextb == []:
                self.mailtextb = ["无"]
            self.mailtext = [n1] + self.mailtexta + [" "] + [n2] + self.mailtextb
            for i in range(len(self.mailtext)):
                c = c + self.mailtext[i] + """
"""
            linkerr_p = 0
            linkerr_p1 = 0
        except:
            print("读取项目数据状态错误")
            t3 = "数据库连接失败"
            c3 = "请检查服务器状态，数据库无法连接！"
            if linkerr_p == 0:
                self.mail(t3, c3)
                linkerr_p = 1
            else:
                print("ok")
            if localtime.tm_hour in dingshi:
                if linkerr_p1 == 0:
                    self.mail(t3, c3)
                    print(localtime.tm_hour)
                    linkerr_p1 = 1
            else:
                linkerr_p1 = 0
                print(localtime.tm_hour)

        print(c)
        # print(self.mailtexta)
        # print(self.mailtext1)

        if self.mailtexta != self.mailtext1:
            if emaileable == 1:
                self.mail(self.t, c)
            self.mailtext1 = self.mailtexta
            # print(self.mailtext)

        else:
            print("状态无变化！")
            # print(self.mailtext)
        if localtime.tm_hour in dingshi:
            if time_P == 0:
                self.mail(self.t2, c)
                print(localtime.tm_hour)
                time_P = 1
        else:
            time_P = 0
            print(localtime.tm_hour)

        self.mailtext = []
        self.mailtexta = []
        self.mailtextb = []
        self.pn = []
        self.pncn = []


class DownThread:
    def __init__(self):
        self._running = True
        self._over = True

    def stp(self):
        self._running = False

    def sta(self):
        self._running = True

    def over(self):
        self._over = False

    def run(self):
        while self._over:
            if self._running:
                data.read_prolist()
                time.sleep(30)


class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, '数据采集系统插件', size=(400, 300))
        # 创建面板
        panel = wx.Panel(self)

        # 创建“确定”和“取消”按钮,并绑定事件
        self.bt_confirm = wx.Button(panel, label='开始监测')
        self.bt_confirm.Bind(wx.EVT_BUTTON, self.OnclickSubmit)
        self.bt_cancel = wx.Button(panel, label='停止')
        self.bt_cancel.Bind(wx.EVT_BUTTON, self.OnclickCancel)
        # 创建文本，左对齐
        self.title = wx.StaticText(panel, label="数据更新状态监测，点击下方按钮启动监测功能：")
        self.title1 = wx.StaticText(panel, label="监控中 √")
        """

        self.label_user = wx.StaticText(panel, label="用户名:")
        self.text_user = wx.TextCtrl(panel, style=wx.TE_LEFT)
        self.label_pwd = wx.StaticText(panel, label="密   码:")
        self.text_password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)

        # 添加容器，容器中控件横向排列
        hsizer_user = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_user.Add(self.label_user, proportion=0, flag=wx.ALL, border=5)
        hsizer_user.Add(self.text_user, proportion=1, flag=wx.ALL, border=5)

        hsizer_pwd = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_pwd.Add(self.label_pwd, proportion=0, flag=wx.ALL, border=5)
        hsizer_pwd.Add(self.text_password, proportion=1, flag=wx.ALL, border=5)
        """
        hsizer_button = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_button.Add(self.title1, proportion=0, flag=wx.ALIGN_CENTER, border=5)
        hsizer_button.Add(self.bt_confirm, proportion=0, flag=wx.ALIGN_CENTER, border=5)
        hsizer_button.Add(self.bt_cancel, proportion=0, flag=wx.ALIGN_CENTER, border=5)
        # 添加容器，容器中控件纵向排列
        vsizer_all = wx.BoxSizer(wx.VERTICAL)
        vsizer_all.Add(self.title, proportion=0, flag=wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER, border=15)
        vsizer_all.Add(hsizer_button, proportion=0, flag=wx.ALIGN_CENTER | wx.TOP, border=15)

        # vsizer_all.Add(hsizer_user, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
        # vsizer_all.Add(hsizer_pwd, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
        panel.SetSizer(vsizer_all)

    def OnclickSubmit(self, event):
        """ 单击确定按钮，执行方法 """
        self.title1.Label = "监控中 √"
        c.sta()

    def OnclickCancel(self, event):
        """ 单击取消按钮，执行方法 """
        self.title1.Label = "已停止 X"
        c.stp()


if __name__ == '__main__':
    data = data_check()

    c = DownThread()
    t = threading.Thread(target=c.run, args=())
    t.start()

    app = wx.App()  # 初始化
    frame = MyFrame(parent=None, id=-1)  # 实例化MyFrame类，并传递参数
    frame.Show()  # 显示窗口
    app.MainLoop()  # 调用主循环方法
    c.over()
















