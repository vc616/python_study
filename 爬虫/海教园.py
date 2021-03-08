import time, sys, getopt, os
from selenium import webdriver
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import sys
sys.path.append("..")
from key import k

my_sender = "vc616@qq.com"  # 发件人邮箱账号1
my_pass = k.email_pass  # 发件人邮箱密码
my_user = ["vc616@qq.com", ]  # 收件人邮箱账号


# dit = {'news' : '','daiban' : ''}

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

    def read(self):
        news = []
        daiban = []
        a = 1
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 设置option
        if a == 1:
            driver = webdriver.Chrome(options=option)
        else:
            driver = webdriver.Chrome()
        driver.get('https://tj.ke.com/ershoufang/rs鲁能泰山7号/')
        driver.implicitly_wait(10)
        # driver.find_element_by_id('loginid').clear()
        # driver.find_element_by_id('loginid').send_keys('id')
        # driver.find_element_by_id('userpassword').clear()
        # driver.find_element_by_id('userpassword').send_keys('pass')
        # driver.find_element_by_id('login').click()
        # driver.implicitly_wait(10)
        time.sleep(10)
        # driver.switch_to.frame("mainFrame")
        # print(driver.page_source)
        # elements  = driver.find_elements_by_xpath('//*[@id="beike"]/div[1]/div[4]/div[1]/div[4]/ul/*/div[1]/div[1]/a')

        elements1 = driver.find_elements_by_xpath('//*[@id="beike"]/div[1]/div[4]/div[1]/div[5]/div[2]/div')
        # elements = driver.find_elements_by_id('container_Table')
        # elements = driver.find_elements_by_class_name("docdetail")
        # print(elements)
        # print(elements1)

        for t in elements1:
            print(t.text)
            news.append(t.text)
        # for t in elements1:
        # print(t)
        # print(t.text)
        # daiban.append(t.text)
        # print(news)
        # print(daiban)
        # dit['news'] = news
        # dit['daiban'] = daiban
        # dit = [news, daiban]

        driver.close()
        print(news)
        return news


w = check_OA()
w.read()
