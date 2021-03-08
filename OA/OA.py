import time, sys, getopt, os
from selenium import webdriver
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import _thread
import threading
from selenium.webdriver.support.ui import Select
import sys
sys.path.append("..")
from key import k

my_sender = "vc616@qq.com"
my_pass = k.email_pass
my_user = ["vc616@qq.com", ]
OA_id = k.OA_id
OA_pass = k.OA_pass

# dit = {'news' : '','daiban' : ''}
class mailsend():
    def mail(self, t, c):  # 发送邮件
        try:
            msg = MIMEText(c, 'plain', 'utf-8')
            msg['From'] = formataddr(["TDR", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['Subject'] = t  # 邮件的主题，也可以说是标题
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, my_user, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            print("邮件发送成功")
            return "OK"
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print("邮件发送失败")
            return "err"

class check_OA():
    def readOA(self):
        news = []
        news2 = []
        daiban = []
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 设置option
        driver = webdriver.Chrome(options=option)
        # driver = webdriver.Chrome()
        driver.get('http://www.tdroa.com')
        driver.implicitly_wait(10)
        driver.find_element_by_id('loginid').clear()
        driver.find_element_by_id('loginid').send_keys(OA_id)
        driver.find_element_by_id('userpassword').clear()
        driver.find_element_by_id('userpassword').send_keys(OA_pass)
        driver.find_element_by_id('login').click()
        driver.implicitly_wait(30)
        driver.switch_to.frame("mainFrame")
        # print(driver.page_source)
        elements = driver.find_elements_by_xpath('//*[@id="_contenttable_25"]/tbody/tr/td[2]/table/tbody/*/td[2]')
        elements1 = driver.find_elements_by_xpath('//*[@id="_contenttable_19"]/tbody/tr/td[2]/table/tbody/*/td[2]')
        # elements = driver.find_elements_by_id('container_Table')
        # elements = driver.find_elements_by_class_name("docdetail")
        # print(elements)
        # print(elements1)
        for t in elements:
            news.append(t.text)
        for t in elements1:
            daiban.append(t.text)
        # for t in elements2:
        #     news2.append(t.text)
        dit = [news, daiban]
        # time.sleep(30)
        driver.close()
        # print(dit)
        return dit

    def loopoa(self,maileable):
        ne = []
        db = []
        while 1:
            result = self.readOA()
            ne1 = result[0][:]
            db1 = result[1][:]
            c = "新闻与公告:\n"
            e = ""
            a = ""
            for i in ne1:
                if (i in ne):
                    result[0].remove(i)
                else:
                    e = e + i + '\n'
            if len(e) > 0:
                a = c + e
            else:
                a = ""
            d = "待办事宜:\n"
            f = ""
            b = ""
            for i in db1:
                if (i in db):
                    result[1].remove(i)
                else:
                    f = f + i + '\n'
            if len(f) > 0:
                b = d + f
            else:
                b = ""
            g = a + b
            le = len(result[0]) + len(result[1])
            if le > 0:
                print(g)
                m = mailsend()
                if maileable == 1:
                    if m.mail("OA有新消息", g) == "OK":
                        ne = ne1[:]
                        db = db1[:]
            else:
                print("没有变化！")
            time.sleep(3600)

if __name__ == '__main__':
    w = check_OA()
    t = threading.Thread(target=w.loopoa(1), args=()) #
    t.start()


