# -*- coding:utf-8 -*-

import pymysql
from datetime import datetime

import sys

sys.path.append("..")
# from key import k
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = "vc616@qq.com"  # 发件人邮箱账号
my_pass = "hcmjmmanwpiecadf"  # 发件人邮箱密码
my_user = ["vc616@qq.com", ]  # 收件人邮箱账号

sys.path.insert(0, "..")
mysql_host = "dtro.top"
mysql_user = "root"
mysql_password = "51660180"
mysql_db = "dt"
mysql_port = 3306
mailtexta = []
mailtextb = []
mailtext1 = []
emaileable = 1
dingshi = [9, 12, 15, 18]
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

        self.textc = []
        self.projectlist = {}
        self.t = "设备连线状态有更新："
        self.t2 = "设备状态定时发送"
        self.pn = []
        self.pncn = []

    def F_table(self, table):  # 在数据库dbn中查找名为table 的表格是否存在，返回True 或者 False

        sq = "SELECT	Count( * ) FROM	`TABLES` WHERE	`TABLES`.TABLE_NAME = '" + table + "' 	AND `TABLES`.TABLE_SCHEMA = '" + self.db1 + "'"
        try:
            db = pymysql.connect(host=self.host, user=self.user, password=self.password, database="information_schema",
                                 port=self.port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.commit()
            result = cursor.fetchone()
            db.close()
        except:
            pass
        try:
            if result[0] == 1:
                return True
            else:
                return False
        except:
            print("数据库连接失败，请检查参数,查找表格")
            return False

    def read_last(self, i):
        sq = "SELECT  Max(TIME) FROM  " + i
        # print(sq)
        mailtexta = []
        mailtextb = []
        texta = []
        textb = []
        try:
            db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.db1,
                                 port=self.port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.commit()
            result = cursor.fetchall()
            db.close()
            for row in result:
                u = (datetime.now() - row[0])
                # print(u.seconds)
                tt = u.seconds + u.days * 8400
                # print(tt)
                if tt > 300:
                    # print("异常断线，项目名称：" + i + "数据断线时长：" + str(u.seconds) )
                    mailtexta.append(i + "  时间：" + str(row[0]))
                    texta.append(i)
                else:
                    mailtextb.append(i + "  时间：" + str(row[0]))
                    textb.append(i)
            # return [mailtexta,mailtextb,texta,textb]
        except:
            print("错误3")
            # return False

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
            return True
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print("邮件发送失败")
            return False

    def read_prolist(self):  # 读取项目列表
        sq = "SELECT `ID` ,`项目名称`FROM config "
        localtime = time.localtime(time.time())
        global time_P
        global linkerr_p
        global linkerr_p1
        self.mailtext = []
        self.mailtexta = []
        self.mailtextb = []

        try:
            db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.db1,
                                 port=self.port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.commit()
            result = cursor.fetchall()
            db.close()
            for row in result:
                self.pn.append(row[0])
                self.pncn.append(row[1])
            # print("项目列表：", self.pn)
            # print("项目列表：", self.pncn)
            self.projectlist = dict(zip(self.pn, self.pncn))
            # print(self.projectlist)
            return (self.projectlist)

        except:
            # print(sys._getframe().f_code.co_name,"错误")
            return (False)

    def test_list(self, p):
        c = ""
        mailtexta = []
        mailtextb = []
        texta = []
        textb = []
        for i, k in p.items():
            i = i + "_r"
            if self.F_table(i):
                sq = "SELECT  Max(TIME) FROM  " + i
                # print(sq)
                try:
                    db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.db1,
                                         port=self.port)
                    cursor = db.cursor()
                    cursor.execute(sq)
                    db.commit()
                    result = cursor.fetchall()
                    db.close()
                    for row in result:
                        u = (datetime.now() - row[0])
                        # print(u.seconds)
                        tt = u.seconds + u.days * 8400
                        # print(tt)
                        i = p[i[:-2]]
                        if tt > 300:
                            # print("异常断线，项目名称：" + i + "数据断线时长：" + str(u.seconds) )
                            mailtexta.append(i + "  时间：" + str(row[0]))
                            texta.append(i)
                        else:
                            mailtextb.append(i + "  时间：" + str(row[0]))
                            textb.append(i)
                except:
                    print("错误3")
                    return False
        return [mailtexta, mailtextb, texta, textb]

    def do_text(self, w):
        mailtexta = w[0]
        mailtextb = w[1]
        texta = w[2]
        textb = w[3]

        c = ""
        n1 = "断线设备：( " + str(len(mailtexta)) + " )"
        n2 = "正常设备：( " + str(len(mailtextb)) + " )"
        if mailtexta == []:
            mailtexta = ["无"]
        if mailtextb == []:
            mailtextb = ["无"]
        mailtext = [n2] + mailtextb + [" "] + [n1] + mailtexta
        for i in range(len(mailtext)):
            c = c + mailtext[i] + """\r\n"""
        # print(c)
        if (self.textc != texta):
            print(self.textc)
            self.textc = texta[:]
            return [c, "1", len(mailtexta), len(mailtextb)]
        else:
            print("状态无变化")
            return [c, "0", len(mailtexta), len(mailtextb)]


#
#             linkerr_p = 0
#             linkerr_p1 = 0
#         except:
#             print("读取项目数据状态错误")
#             t3 = "数据库连接失败"
#             c3 = "请检查服务器状态，数据库无法连接！"
#             if linkerr_p == 0:
#                 self.mail(t3, c3)
#                 linkerr_p = 1
#             else:
#                 print("ok")
#             if localtime.tm_hour in dingshi:
#                 if linkerr_p1 == 0:
#                     self.mail(t3, c3)
#                     print(localtime.tm_hour)
#                     linkerr_p1 = 1
#             else:
#                 linkerr_p1 = 0
#                 print(localtime.tm_hour)
#
#         print(c)
#         # print(self.mailtexta)
#         # print(self.mailtext1)
#
#         if self.mailtexta != self.mailtext1:
#             if emaileable == 1:
#                 # self.mail(self.t, c)
#                 print(self.t,c)
#             self.mailtext1 = self.mailtexta
#             # print(self.mailtext)
#
#         else:
#             print("状态无变化！")
#             # print(self.mailtext)
#         if localtime.tm_hour in dingshi:
#             if time_P == 0:
#                 self.mail(self.t2, c)
#                 print(localtime.tm_hour)
#                 time_P = 1
#         else:
#             time_P = 0
#             print(localtime.tm_hour)
#
#         self.mailtext = []
#         self.mailtexta = []
#         self.mailtextb = []
#         self.pn = []
#         self.pncn = []


# class DownThread:
#     def __init__(self):
#         self._running = True
#         self._over = True
#
#     def stp(self):
#         self._running = False
#
#     def sta(self):
#         self._running = True
#
#     def over(self):
#         self._over = False
#
#     def run(self):
#         while self._over:
#             if self._running:
#                 p = data.read_prolist()
#                 if p:
#                     q = data.test_list(p)
#                     if q:
#                         r = data.do_text(q)
#                         if r[1] == "1":
#                             data.mail("设备状态变化", r[0])
#                             print(r[0])
#                         localtime = time.localtime(time.time())
#
#                         if localtime.tm_hour in dingshi:
#                             if linkerr_p1 == 0:
#                                 s = data.mail("定时发送", r[0])
#                                 if s:
#                                     linkerr_p1 = 1
#                                     print(localtime.tm_hour)
#
#                         else:
#                             linkerr_p1 = 0
#                             # print(localtime.tm_hour)
#
#                     # for i in q:
#                     #     print(i)
#
#                 else:
#                     print("读取配置文件错误")
#
#                 time.sleep(60)


# class MyFrame(wx.Frame):
#     def __init__(self, parent, id):
#         wx.Frame.__init__(self, parent, id, '数据采集系统插件', size=(400, 300))
#         # 创建面板
#         panel = wx.Panel(self)
#
#         # 创建“确定”和“取消”按钮,并绑定事件
#         self.bt_confirm = wx.Button(panel, label='开始监测')
#         self.bt_confirm.Bind(wx.EVT_BUTTON, self.OnclickSubmit)
#         self.bt_cancel = wx.Button(panel, label='停止')
#         self.bt_cancel.Bind(wx.EVT_BUTTON, self.OnclickCancel)
#         # 创建文本，左对齐
#         self.title = wx.StaticText(panel, label="数据更新状态监测，点击下方按钮启动监测功能：")
#         self.title1 = wx.StaticText(panel, label="监控中 √")
#         """
#
#         self.label_user = wx.StaticText(panel, label="用户名:")
#         self.text_user = wx.TextCtrl(panel, style=wx.TE_LEFT)
#         self.label_pwd = wx.StaticText(panel, label="密   码:")
#         self.text_password = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
#
#         # 添加容器，容器中控件横向排列
#         hsizer_user = wx.BoxSizer(wx.HORIZONTAL)
#         hsizer_user.Add(self.label_user, proportion=0, flag=wx.ALL, border=5)
#         hsizer_user.Add(self.text_user, proportion=1, flag=wx.ALL, border=5)
#
#         hsizer_pwd = wx.BoxSizer(wx.HORIZONTAL)
#         hsizer_pwd.Add(self.label_pwd, proportion=0, flag=wx.ALL, border=5)
#         hsizer_pwd.Add(self.text_password, proportion=1, flag=wx.ALL, border=5)
#         """
#         hsizer_button = wx.BoxSizer(wx.HORIZONTAL)
#         hsizer_button.Add(self.title1, proportion=0, flag=wx.ALIGN_CENTER, border=5)
#         hsizer_button.Add(self.bt_confirm, proportion=0, flag=wx.ALIGN_CENTER, border=5)
#         hsizer_button.Add(self.bt_cancel, proportion=0, flag=wx.ALIGN_CENTER, border=5)
#         # 添加容器，容器中控件纵向排列
#         vsizer_all = wx.BoxSizer(wx.VERTICAL)
#         vsizer_all.Add(self.title, proportion=0, flag=wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER, border=15)
#         vsizer_all.Add(hsizer_button, proportion=0, flag=wx.ALIGN_CENTER | wx.TOP, border=15)
#
#         # vsizer_all.Add(hsizer_user, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
#         # vsizer_all.Add(hsizer_pwd, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=45)
#         panel.SetSizer(vsizer_all)
#
#     def OnclickSubmit(self, event):
#         """ 单击确定按钮，执行方法 """
#         self.title1.Label = "监控中 √"
#         c.sta()
#
#     def OnclickCancel(self, event):
#         """ 单击取消按钮，执行方法 """
#         self.title1.Label = "已停止 X"
#         c.stp()


if __name__ == '__main__':
    data = data_check()
    while 1:
        p = data.read_prolist()
        # print(p)
        if p:
            q = data.test_list(p)
            if q:
                r = data.do_text(q)
                if r[1] == "1":
                    # data.mail("设备状态变化:" + str(r[3]) + "/" + str(r[3] + r[2]), r[0])
                    print(r[0])
                localtime = time.localtime(time.time())

                if localtime.tm_hour in dingshi:
                    if linkerr_p1 == 0:
                        s = data.mail("定时发送:" + str(r[3]) + "/" + str(r[3] + r[2]), r[0])
                        if s:
                            print(r[0])
                            linkerr_p1 = 1
                            print(localtime.tm_hour)
                else:
                    linkerr_p1 = 0
        time.sleep(60)
