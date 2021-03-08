from IPython import embed
import csv
import pymysql
import time
import threading
import sys
import logging
from opcua import Client
from datetime import datetime
from datetime import timedelta

sys.path.insert(0, "..")
mysql_host = "192.168.0.81"
mysql_user = "root"
mysql_password = "******"
mysql_db = "dtro"
mysql_port = 3306
sn = []
device = []
name = []
ard = []
typ = []
trend_y = []
sn_list = []
ip_list = []
device_list = []
con = []
dabase = "dtro"
insert_str_key = []
insert_str_value = []


def sum_FI(pro, sn):
    y = (sn - 1) // 12
    m = (sn - 1) % 12 + 1
    ny = str(y) + "年" + str(m) + "月"
    s1 = str(y) + "-" + str(m) + "-01 00:00:00"
    s2 = str(y) + "-" + str(m + 1) + "-01 00:00:00"
    sq = "SELECT TIME, FI28021, subtime FROM " + pro + " WHERE TIME BETWEEN '" + s1 + "' AND '" + s2 + "'"
    host = mysql_host
    user = mysql_user
    password = mysql_password
    db = mysql_db
    port = mysql_port
    sum = 0.0
    try:
        db = pymysql.connect(host, user, password, db, port)
        cursor = db.cursor()
        cursor.execute(sq)
        db.commit()
        result = cursor.fetchall()
        db.close()
        for row in result:
            f1 = row[1]
            t1 = row[2]
            # print(row[0], f1, t1)
            if t1 != None:
                if t1 < 600:
                    sum = sum + f1 * t1
    except:
        print("错误0 读取流量记录错误")

    # print(sum/3600)
    sum = str(sum / 3600)
    print(sum)
    sn = str(sn)
    sq = "SELECT `项目名称`, `月份序号` FROM analysis WHERE `项目名称` = '" + pro + "' AND `月份序号` = '" + sn + "' "
    # print(sq)
    host = mysql_host
    user = mysql_user
    password = mysql_password
    db1 = mysql_db
    port = mysql_port
    try:
        db = pymysql.connect(host, user, password, db1, port)
        cursor = db.cursor()
        cursor.execute(sq)
        db.commit()
        result = cursor.fetchall()
        db.close()
    except:
        print("错误1 ")

    # print(len(result))

    if len(result) > 0:
        sq = "UPDATE `analysis` SET `月度累计水量`='" + sum + "' WHERE (`项目名称`='" + pro + "') AND (`月份序号`='" + sn + "') LIMIT 1"
        print(sq)
    else:
        sq = "INSERT INTO `analysis` (`项目名称`, `月份序号`, `月度累计水量`,`年月`) VALUES ('" + pro + "', '" + sn + "', '" + sum + "','" + ny + "')"
        print(sq)
    try:
        db = pymysql.connect(host, user, password, db1, port)
        cursor = db.cursor()
        cursor.execute(sq)
        db.commit()
        db.close()
    except:
        print("错误2 写入汇总表格错误")


def select(p):
    host = mysql_host
    user = mysql_user
    password = mysql_password
    db1 = mysql_db
    port = mysql_port
    sq = "SELECT TIME, FI28021, subtime FROM " + p + " WHERE FI28021 IS NOT NULL AND subtime IS NOT NULL ORDER BY TIME ASC"
    print(sq)
    day_text = []
    day_sn = []
    day_sum = 0
    day_sum_list = []
    try:
        db = pymysql.connect(host, user, password, db1, port)
        cursor = db.cursor()
        cursor.execute(sq)
        db.commit()
        result = cursor.fetchall()
        db.close()
    except:
        print("select(p)_错误3")

    for row in result:
        d = str(row[0].year) + "年" + str(row[0].month) + "月" + str(row[0].day) + "日"
        d_sn = row[0].toordinal()
        if row[2] < 600:
            day_sum = float(row[1]) * float(row[2])
        # else:
        # print(row[2])
        l = len(day_sum_list) - 1
        if d not in day_text:
            day_text.append(d)
            day_sn.append(d_sn)
            day_sum_list.append(day_sum)
        else:
            day_sum_list[l] = day_sum_list[l] + day_sum

    print(day_text)
    print(day_sum_list)
    print(day_sn)
    for i in range(len(day_sn)):
        sq = "SELECT `项目名称`, `日序号` FROM analysis_days WHERE `项目名称` = '" + p + "' AND `日序号` = '" + str(day_sn[i]) + "' "
        # print(sq)
        host = mysql_host
        user = mysql_user
        password = mysql_password
        db1 = mysql_db
        port = mysql_port
        try:
            db = pymysql.connect(host, user, password, db1, port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.commit()
            result = cursor.fetchall()
            db.close()
        except:
            print("错误1 ")

        # print(len(result))

        if len(result) > 0:
            sq = "UPDATE `analysis_days` SET `日累计水量`='" + str(
                day_sum_list[i] / 3600) + "' WHERE (`项目名称`='" + p + "') AND (`日序号`='" + str(day_sn[i]) + "') LIMIT 1"
            print(sq)
        else:
            sq = "INSERT INTO `analysis_days` (`项目名称`, `日序号`, `日累计水量`,`年月日`) VALUES ('" + p + "', '" + str(
                day_sn[i]) + "', '" + str(day_sum_list[i] / 3600) + "','" + day_text[i] + "')"
            print(sq)

        try:
            db = pymysql.connect(host, user, password, db1, port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.commit()
            db.close()
        except:
            print("错误2 写入汇总表格错误")


def read_prolist():
    prolist = []
    host = mysql_host
    user = mysql_user
    password = mysql_password
    db1 = mysql_db
    port = mysql_port
    pn = []
    sq = "SELECT `ID` FROM config "

    try:
        db = pymysql.connect(host, user, password, db1, port)
        cursor = db.cursor()
        cursor.execute(sq)
        db.commit()
        result = cursor.fetchall()
        db.close()
    except:
        print("read_prolist_错误3")
    for row in result:
        pn.append(row[0])
    # print(pn)
    # print(pn)

    return pn


pro = read_prolist()
t = ['guangchanga', 'guangchangb', 'hengyang', 'jingxing', 'nanjing', 'zhongxiang']

for i in pro:
    if i in t:
        select(i)
        print(i)

# print(pro)
