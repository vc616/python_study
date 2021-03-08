import time, sys, getopt
from selenium import webdriver
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

import sys
sys.path.append("..")
from key import k

my_sender = "vc616@qq.com"  # 发件人邮箱账号
my_pass = k.email_pass  # 发件人邮箱密码
my_user = ["vc616@qq.com", ]  # 收件人邮箱账号

# dit = {'news' : '','daiban' : ''}
url = "https://account.xiaomi.com/pass/serviceLogin?callback=https%3A%2F%2Fi.mi.com%2Fsts%3Fsign%3DmF32YtfY7XReThOa0pZzXhZXJ0U%253D%26followup%3Dhttps%253A%252F%252Fi.mi.com%252F%26sid%3Di.mi.com&sid=i.mi.com&_locale=zh_CN&_snsNone=true"


# url = 'http://www.tdroa.com'
class check_OA():
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
            return "OK"
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print("邮件发送失败")
            return "err"

    def readOA(self):
        news = []
        daiban = []
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 设置option
        # driver = webdriver.Chrome(options=option)
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
        driver.find_element_by_id('username').clear()
        driver.find_element_by_id('username').send_keys(k.myphone)
        driver.find_element_by_id('pwd').clear()
        driver.find_element_by_id('pwd').send_keys(k.mi_pass)
        driver.find_element_by_id('login-button').click()
        # driver.implicitly_wait(10)          //*[@id="root"]/div/div/div[2]/a[7]
        time.sleep(10)
        # driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[2]/a[7]').click()
        # elements = driver.find_elements_by_link_text("查找设备")
        driver.get('https://i.mi.com/mobile/find#/')
        # driver.switch_to.frame("mainFrame")
        # print(driver.page_source)
        # elements = driver.find_elements_by_xpath('//*[@id="_contenttable_25"]/tbody/tr/td[2]/table/tbody/*/td[2]')
        # elements1 = driver.find_elements_by_xpath('//*[@id="_contenttable_19"]/tbody/tr/td[2]/table/tbody/*/td[2]')
        # elements = driver.find_elements_by_id('container_Table')
        # elements = driver.find_elements_by_class_name("docdetail")
        # print(elements)
        # print(elements1)

        # for t in elements:
        #     print(t.text)
        #     news.append(t.text)
        # for t in elements1:
        #     # print(t)
        #     # print(t.text)
        #     daiban.append(t.text)
        # # print(news)
        # # print(daiban)
        # # dit['news'] = news
        # # dit['daiban'] = daiban
        # dit = [news, daiban]
        #
        time.sleep(30)
        driver.close()
        # return dit

    def loop(self):
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
                if self.mail("OA有新消息", g) == "OK":
                    ne = ne1[:]
                    db = db1[:]
            else:
                print("没有变化！")
            time.sleep(3600)


w = check_OA()
w.readOA()
