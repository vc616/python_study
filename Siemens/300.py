import pymysql
import time
import threading
import os
from HslCommunication import SiemensS7Net
from HslCommunication import SiemensPLCS
import csv
import re
import pprint


debug = 12
sn_list = []
ip_list = []
sq_Record = []
sq_Norecord = []
sq_fl = []
sq_bl = []
temp = []
con = {}
# nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

mysql_host = "localhost"
mysql_host = "192.168.0.81"
mysql_user = "root"
mysql_password = "51660180"
mysql_db = "dt"
mysql_port = 3306

def readfile():
    device = []
    ip = []
    port = []
    name = []
    ard = []
    typ = []
    plc = []
    record = []
    device_and_name = []
    a = []
    b = []
    for root, dirs, files in os.walk(os.getcwd()):
        a = files[:]
    # print(a)
    for i in a:
        w = i.lower()
        if w.endswith(".csv") == True:
            if len(w.split(",")) == 5:
                b.append(w)
    if len(b) >0:
        print("有效配置文件列表：", b)

    for i in b:
        hang = 0
        deviceinf = i.split(",")
        if len(deviceinf) == 5:
            with open(i, "r", encoding="gb2312") as f:
                reader = csv.reader(f)
                for row in reader:
                    hang = hang + 1
                    if hang > 1:
                        # print(row)
                        s = "错误行："
                        for ii in range(len(row)):
                            if row[ii] == "":
                                for k in row:
                                    s = s + k + "   "
                                print(s + "请检查此行信息是否完整！")
                        if s == "错误行：":
                            device.append(deviceinf[0].lower())
                            plc.append(deviceinf[1])
                            ip.append(deviceinf[2])
                            port.append(deviceinf[3])
                            name.append(row[0].upper())
                            ard.append(row[1].upper())
                            typ.append(row[2].upper())
                            record.append(row[3].upper())

            f.close()
    # print(hang)
    tf = {}
    errnum = {}
    for i in range(len(typ)):
        s = ard[i]
        if typ[i] == "REAL" or typ[i] == "INT" or typ[i] == "DINT":
            if s.startswith("DB"):
                n = re.findall(r"\d+", s, )  # 搜索DB22.33.7中的22、33组成数组["22","33","7"]
                if (len(n) == 2) & (int(n[0]) < 65535) & (int(n[1]) < 9999):
                    pass
                else:
                    errnum[i] = n
            elif s.startswith("M") or s.startswith("I"):
                n = re.findall(r"\d+", s, )
                if (len(n) == 1) & (int(n[0]) < 65535):
                    pass
                else:
                    errnum[i] = n
            else:
                errnum[i] = n
        if typ[i] == "BOOL":
            if s.startswith("DB"):
                n = re.findall(r"\d+", s, )
                if (len(n) == 3) & (int(n[0]) < 65535) & (int(n[1]) < 9999) & (int(n[2]) < 8):
                    pass
                else:
                    errnum[i] = n
            if s.startswith("M") or s.startswith("I"):
                n = re.findall(r"\d+", s, )
                if (len(n) == 2) & (int(n[0]) < 65535) & (int(n[1]) < 8):
                    pass
                else:
                    errnum[i] = n

    for i in range(len(device)):  # 查询 重复行
        device_and_name.append(device[i] + name[i])
    for j in range(len(device_and_name)):
        e = device_and_name[j]
        if e not in tf:
            tf[e] = ""
        else:
            errnum[j] = device[j] + "," + name[j]
    if errnum == {}:
        return {"device": device, "ip": ip, "port": port, "name": name, "ard": ard, "typ": typ, "plc": plc,
                "record": record}
    else:
        print("存在错误行：", errnum)
        return False

def todict(p):
    # 将从文件中读取到的所有变量信息存储到字典中，结构如下：
    # {'shangrao':
    #   {'inf':
    #       {'ip': '192.168.0.100', 'port': '102'},
    #   'content':
    #       {'NI13021': {'value': 0, 'typ': 'REAL', 'ard': 'DB113.0'},
    #       'NI18021': {'value': 0, 'typ': 'REAL', 'ard': 'DB113.4'}
    #       .
    #       .
    #       }
    #   },
    # 'wanan':
    #   {'inf':
    #       {'ip': '192.168.0.100', 'port': '103'},
    #   'content':
    #       {'PI27021': {'value': 0, 'typ': 'REAL', 'ard': 'DB113.16'},
    #       'PI28021': {'value': 0, 'typ': 'REAL', 'ard': 'DB113.20'}
    #       .
    #       .
    #       }
    #   }
    # }
    device = p["device"]
    ip = p["ip"]
    port = p["port"]
    name = p["name"]
    ard = p["ard"]
    typ = p["typ"]
    plc = p["plc"]
    rec = p["record"]
    tag = {}
    p_list = []

    for i in device:
        if i not in p_list:
            p_list.append(i)

    for k in p_list:
        t = {}
        inf = {}
        for i in range(len(device)):
            if k == device[i]:
                inf["inf"] = {"ip": ip[i], "port": port[i], "plc": plc[i], "t": "", "Read_qua": "", "Rec_qua": ""}
                t[name[i]] = {"value": 0, "typ": typ[i], "ard": ard[i], "qua": 0, "rec": rec[i], "block": ""}
                tag[device[i]] = {"inf": inf["inf"], "content": t}
    return tag

def block(dict):
    for device, g in dict.items():
        f = {}
        for k, v in dict[device]["content"].items():
            # print(v)
            v_ard = v["ard"].upper()
            v_typ = v["typ"].upper()
            m = re.match(r"([a-z]*)(\d*)", v_ard, re.I).group()  # 搜索DB22、M3等数据区域名称
            m = m.upper()
            # print(m)
            if "M" in m:
                m = "M"
            if "I" in m:
                m = "I"
            na = re.findall(r"\d+", v_ard, )  # 搜索DB22.33.7中的22、33组成数组["22","33","7"]
            # print(na)
            if "DB" in v_ard:
                n = int(na[1])  # 搜索DB22.DBW33中的33
                if m not in f.keys():
                    f[m] = {"A": n, "B": n}
            if "M" in v_ard:
                n = int(na[0])  # 搜索M22 中的22
                if m not in f.keys():
                    f["M"] = {"A": n, "B": n}
            if "I" in v_ard:
                n = int(na[0])  # 搜索I22 中的22
                if m not in f.keys():
                    f["I"] = {"A": n, "B": n}

            if v_typ == "REAL":
                if n + 3 > f[m]["B"]:
                    f[m]["B"] = n + 3
            if v_typ == "INT":
                if n + 1 > f[m]["B"]:
                    f[m]["B"] = n + 1
            if v_typ == "BOOL":
                if n > f[m]["B"]:
                    f[m]["B"] = n
            if n < f[m]["A"]:
                f[m]["A"] = n
            dict[device]["content"][k]["block"] = m
        dict[device]["block"] = f
    return dict

def read_PLC(dev):
    global dict
    plc = dict[dev]["inf"]["plc"]
    ip = dict[dev]["inf"]["ip"]
    port = dict[dev]["inf"]["port"]
    p = 0
    if plc == "300":
        p = SiemensPLCS.S300
    if plc == "400":
        p = SiemensPLCS.S400
    if plc == "1200":
        p = SiemensPLCS.S1200
    if plc == "1500":
        p = SiemensPLCS.S1500
    if plc.lower() == "200smart":
        p = SiemensPLCS.S200Smart

    siemens = SiemensS7Net(p, ip)
    siemens.port = int(port)

    if siemens.ConnectServer().IsSuccess == True:
        read = {}
        for db, AB in dict[dev]["block"].items():
            # print(db)
            # print(AB)
            if (db == "M") or (db == "I"):
                read[db] = (siemens.Read(db + str(AB["A"]), int(AB["B"] - AB["A"] + 1)))
                # print(db)
            else:
                read[db] = (siemens.Read(db + "." + str(AB["A"]), int(AB["B"] - AB["A"] + 1)))
            # print(db)
        s = 0
        for i, k in read.items():
            if k.IsSuccess != True:
                s = 1
        if s == 0:
            for name, k in dict[dev]["content"].items():
                # print(name)
                # print(k)
                typ = k["typ"]
                ard = k["ard"]
                block = k["block"]
                # print(typ)
                # print(block)
                na = re.findall(r"\d+", ard, )  # 搜索DB22.33.7中的22、33组成数组["22","33","7"]
                if "M" in ard:
                    s = int(na[0]) - int(dict[dev]["block"]["M"]["A"])
                if "DB" in ard:
                    s = int(na[1]) - int(dict[dev]["block"][block]["A"])
                if typ == "REAL":
                    # print(s)
                    dict[dev]["content"][name]["value"] = siemens.byteTransform.TransSingle(read[block].Content, s)
                if typ == "INT":
                    # print(s)
                    dict[dev]["content"][name]["value"] = siemens.byteTransform.TransInt16(read[block].Content, s)
                if typ == "DINT":
                    # print(s)
                    dict[dev]["content"][name]["value"] = siemens.byteTransform.TransInt32(read[block].Content, s)
                if typ == "BOOL":
                    # pass
                    if "M" in ard:
                        s1 = int(na[0]) - int(dict[dev]["block"]["M"]["A"])
                        s2 = int(na[1])
                        # print(s1, s2)
                        dict[dev]["content"][name]["value"] = \
                            siemens.byteTransform.TransBoolArray(read[block].Content, s1, 1)[s2]
                    if "I" in ard:
                        s1 = int(na[0]) - int(dict[dev]["block"]["I"]["A"])
                        s2 = int(na[1])
                        # print(s1, s2)
                        dict[dev]["content"][name]["value"] = \
                            siemens.byteTransform.TransBoolArray(read[block].Content, s1, 1)[s2]
                    if "DB" in ard:
                        s1 = int(na[1]) - int(dict[dev]["block"][block]["A"])
                        s2 = int(na[2])
                        # print(s1, s2)
                        dict[dev]["content"][name]["value"] = \
                            siemens.byteTransform.TransBoolArray(read[block].Content, s1, 1)[s2]
                dict[dev]["content"][name]["qua"] = 1
            dict[dev]["inf"]["t"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            dict[dev]["inf"]["Read_qua"] = 1
            dict[dev]["inf"]["Rec_qua"] = 1
        else:
            for name, k in dict[dev]["content"].items():
                dict[dev]["content"][name]["value"] = "null"
                dict[dev]["content"][name]["qua"] = 0
    else:
        for name, k in dict[dev]["content"].items():
            dict[dev]["content"][name]["value"] = "null"
            dict[dev]["content"][name]["qua"] = 0
        dict[dev]["inf"]["Read_qua"] = 0
        dict[dev]["inf"]["Rec_qua"] = 0
    # print(dev, dict[dev])

####################################################################################

class sqex():
    def __init__(self, host=mysql_host, user=mysql_user, password=mysql_password, port=mysql_port, dbn=mysql_db):

        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.dbn = dbn

    def readcf(self):  # 读取服务器配置
        readconfig_debug = 0
        global con
        sq = "SELECT ID, ReadCycle, RecordCycle FROM config"
        host = mysql_host
        user = mysql_user
        password = mysql_password
        dbn = mysql_db
        port = mysql_port
        try:
            if readconfig_debug == 1:
                print(sq)
            db = pymysql.connect(host, user, password, dbn, port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.commit()
            result = cursor.fetchall()
            for x in result:
                con[x[0]] = {}
                con[x[0]]["ReadCycle"] = x[1]
                con[x[0]]["RecordCycle"] = x[2]
            # print(con)
            db.close()
            return True
        except:
            if readconfig_debug == 1:
                print("获取服务器配置失败！X")
            return False

    def F_table(self, table):  # 在数据库dbn中查找名为table 的表格是否存在，返回True 或者 False

        sq = "SELECT	Count( * ) FROM	`TABLES` WHERE	`TABLES`.TABLE_NAME = '" + table + "' 	AND `TABLES`.TABLE_SCHEMA = '" + self.dbn + "'"
        try:
            db = pymysql.connect(self.host, self.user, self.password, "information_schema", self.port)
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

    def F_columns(self, table, columns):  # #在数据库 dbn 中名为 table 的表格中查找字段 columns 是否存在，返回True 或者 False

        sq = """SELECT Count(*) FROM information_schema.columns WHERE table_name = '""" + table + "' AND column_name = '" + columns + "' AND TABLE_SCHEMA = '" + self.dbn + "'"
        try:
            db = pymysql.connect(self.host, self.user, self.password, "information_schema", self.port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.commit()
            result = cursor.fetchone()
            db.close()
        except:
            pass
            # db.close()
        # print(result)
        try:
            if result[0] == 1:
                return True
            else:
                return False
        except:
            print("数据库连接失败，请检查参数，查找字段")
            return False

    def C_table_r(self, name):  # 创建表格，时创建部分额外字段

        sq = """CREATE TABLE `""" + name + """`  (  `TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, 
         `subtime` double DEFAULT NULL,`Flow_in` float(255, 0) DEFAULT NULL,  `Flow_out17` float(255, 0)
          DEFAULT NULL,`Flow_out28` varchar(255) CHARACTER SET latin1 COLLATE latin1_danish_ci 
          DEFAULT NULL,PRIMARY KEY (`TIME`) USING BTREE) ENGINE = InnoDB CHARACTER SET = latin1 
          COLLATE = latin1_danish_ci ROW_FORMAT = Compact;"""
        sq = """CREATE TABLE `""" + name + """`  (  `TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                 `subtime` double DEFAULT NULL,PRIMARY KEY (`TIME`) USING BTREE) ENGINE = InnoDB CHARACTER SET = latin1 
                  COLLATE = latin1_danish_ci ROW_FORMAT = Compact;"""

        try:
            db = pymysql.connect(self.host, self.user, self.password, self.dbn, self.port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.close()
            print("创建数据表", name, "成功！")
        except:
            print("创建数据表", name, "失败！")

    def C_table(self, name):  # 创建表格，时创建部分额外字段

        sq = """CREATE TABLE `""" + name + """`  (
              `ID` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
              `TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (`ID`) USING BTREE
            ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Compact;"""
        sq2 = """INSERT INTO `""" + name + """`(`ID`) VALUES ('""" + name + """')"""
        # print(sq2)

        try:
            db = pymysql.connect(self.host, self.user, self.password, self.dbn, self.port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.close()
            print("创建数据表", name, "成功！")
        except:
            print("创建数据表", name, "失败！")
        time.sleep(1)
        try:
            db = pymysql.connect(self.host, self.user, self.password, self.dbn, self.port)
            cursor = db.cursor()
            cursor.execute(sq2)
            db.commit()
            db.close()
            print("初始化", name, "成功！")
        except:
            print("初始化", name, "失败！")

    def C_columns(self, table, columns, ty):

        if ty == 'BOOL':
            ty = "varchar(20)"
        if ty == "DINT":
            ty = 'Int'
        if ty == "REAL":
            ty = "FLOAT"
        sq = "ALTER TABLE `" + table + "` ADD `" + columns + "` " + ty
        try:
            db = pymysql.connect(self.host, self.user, self.password, self.dbn, self.port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.close()
            print("在数据表", table, "中创建字段", columns, "成功！")
        except:
            print("在数据表", table, "中创建字段", columns, "失败！")

    def F_columns_all(self, table):
        r = []
        # sq = """SELECT Count(*) FROM information_schema.columns WHERE table_name = '""" + table + "' AND column_name = '" \
        # + columns + "' AND TABLE_SCHEMA = '" + self.dbn + "'"
        sq = "SELECT `COLUMNS`.COLUMN_NAME FROM `COLUMNS` WHERE `COLUMNS`.TABLE_NAME = '" + table + "' AND `COLUMNS`.TABLE_SCHEMA = '" + self.dbn + "'"
        try:
            db = pymysql.connect(self.host, self.user, self.password, "information_schema", self.port)
            cursor = db.cursor()
            cursor.execute(sq)
            db.commit()
            result = cursor.fetchall()
            db.close()
            for row in result:
                r.append(row[0])
            print(table, "数据获取成功，F_columns_all")
            return r
        except:
            print(table, "数据获取失败，F_columns_all")
            return r

    def sync(self):
        for i, j in dict.items():
            ia = i + "_r"
            if self.F_table(i) == False:
                print(self.C_table(i))
            if self.F_table(ia) == False:
                print(self.C_table_r(ia))
            name1 = self.F_columns_all(i)
            # print("name",name)
            name = []
            for r in name1:
                name.append(r.upper())
            # print(name)
            name_r = []
            name_r1 = self.F_columns_all(ia)
            for r in name_r1:
                name_r.append(r.upper())
            # print(name_r)
            for k, l in j["content"].items():
                # print(k)
                if l["rec"] == "Y":
                    if k not in name_r:
                        self.C_columns(ia, k, l["typ"])
                # else:                                #  2021年2月2日修改，包括下面两行，
                if k not in name:
                    self.C_columns(i, k, l["typ"])

    def insert_sql(self, pro_name):
        global dict
        dic = dict[pro_name]
        # print(dic)
        global trend_y
        # while 1:
        host = mysql_host
        user = mysql_user
        password = mysql_password
        port = mysql_port
        dabase = mysql_db
        s = []
        v = []
        # nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for key, value in dic["content"].items():
            ty = value["typ"]
            if value["rec"] == "Y":
                if ty == "REAL":
                    s.append(key)
                    v.append(str(round(value["value"], 1)))
                elif ty == "BOOL":
                    s.append(key)
                    v.append("'" + str(value["value"]) + "'")
                elif ty == "INT32":
                    s.append(key)
                    v.append(str(value))
        # print(s,v)
        if len(s) > 0:
            # s.append("subtime")
            # v.append(str(subtime))
            insert_str_key = "(`" + ("`, `".join(s)) + "`)"
            insert_str_value = "(" + (", ".join(v)) + ")"
            insert_sql = "INSERT INTO `" + dabase + "`.`" + pro_name + "_r`" + insert_str_key + " VALUES " + insert_str_value
            # print(pro_name, insert_sql)
            try:
                db = pymysql.connect(host, user, password, dabase, port)
                cursor = db.cursor()
                cursor.execute(insert_sql)
                db.commit()
                db.close()
                print(pro_name, "归档数据上传成功！√")
                dict[pro_name]["inf"]["Rec_qua"] = 0
            except:
                print(pro_name, "归档数据上传失败  X")


    def update_sql(self, pro_name):
        global dict
        dic = dict[pro_name]
        host = mysql_host
        user = mysql_user
        dabase = mysql_db
        password = mysql_password
        port = mysql_port
        s = []
        # print("update_sql" ,dic)
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        s.append(("`TIME` = '" + nowtime + "'"))
        for key, value in dic["content"].items():
            ty = value["typ"]
            # if value["rec"] != "Y":
            if ty == "REAL":
                s.append("`" + key + "`" + "=" + str(round(value["value"], 1)))
            if ty == "INT":
                s.append("`" + key + "`" + "=" + str(value["value"]))
            if ty == "BOOL":
                s.append("`" + key + "`" + "='" + str(value["value"]) + "'")
        if len(s) > 0:
            update_key_value = ", ".join(s)
            update_str = "UPDATE `" + dabase + "`.`" + pro_name + "` SET " + update_key_value + " WHERE ID = '" + pro_name + "'"
            print(pro_name, update_str)
            try:
                db = pymysql.connect(host, user, password, dabase, port)
                cursor = db.cursor()
                cursor.execute(update_str)
                db.commit()
                db.close()
                print(pro_name, "实时数据上传成功！√")
                dict[pro_name]["inf"]["Read_qua"] = 0
            except:
                print(pro_name, "实时数据上传失败  X")

def read_PLC_cycle(pro_name):
    global con
    d = threading.Thread(target=read_PLC, name="wew", args=(pro_name,))
    d.start()
    d.join()
    # e = threading.Thread(target=s.update_sql, name="wew", args=(pro_name,))
    # e.start()
    # # e.join()
    t0 = int(time.time())
    while 1:
        t1 = int(time.time())
        try:
            t = con[pro_name]["ReadCycle"]
        except:
            t = 30
        if t < 10:
            t = 10
        if t1 - t0 >= t:
            t0 = t1
            d1 = threading.Thread(target=read_PLC, name="wew", args=(pro_name,))
            d1.start()
            # d1.join()
            if dict[pro_name]["inf"]["Read_qua"] == 1:
                e1 = threading.Thread(target=s.update_sql, name="wew", args=(pro_name,))
                e1.start()
                e1.join()
            else:
                print(pro_name, "数据读取失败！read_PLC_cycle")
            # print(pro_name,"定时进程启动,t =",t)
        time.sleep(0.1)

def insert_sql_cycle(pro_name):
    global con
    w = 0
    while dict[pro_name]["inf"]["Rec_qua"] != 1:
        pass
        time.sleep(1)
        w = w + 1
        if w > 30:
            print(pro_name,"数据读取失败！insert_sql_cycle",)
            w = 0
    d = threading.Thread(target=s.insert_sql, name="wew", args=(pro_name,))
    d.start()
    # d.join()
    t0 = int(time.time())
    while 1:
        t1 = int(time.time())
        try:
            t = con[pro_name]["RecordCycle"]
        except:
            t = 60
        if t < 30:
            t = 30
        if t1 - t0 >= t:
            t0 = t1
            if dict[pro_name]["inf"]["Rec_qua"] == 1:
                d = threading.Thread(target=s.insert_sql, name="wew", args=(pro_name,))
                d.start()
                # d.join()
            else:
                print(pro_name, "数据读取失败！insert_sql_cycle")
            # print(pro_name, "插入数据进程启动,t = ", t)
        time.sleep(0.1)

def readconfig_cycle():
    t = 60
    global con
    f = threading.Thread(target=s.readcf, name="wew", args=())
    f.start()
    f.join()
    t0 = int(time.time())
    p = 0
    while 1:
        time.sleep(0.9)
        if (con != {}) & (p == 0):
            pprint.pprint(con)
            p =1
        t1 = int(time.time())
        if t1 - t0 >= t:
            t0 = t1
            f = threading.Thread(target=s.readcf, name="wew", args=())
            f.start()

if __name__ == "__main__":
    p = readfile()
    if debug == 1:
        print("file ok ")
        print(p)
    dict1 = {}
    if p != False:
        print("配置文件读取完毕。")
        dict1 = todict(p)
        # print(dict1)
        if debug == 1:
            print("inf+content")
            print(dict1)
    dict = {}
    if dict1 != {}:
        dict = block(dict1)
        if debug == 1:
            print("inf+content+block:")
    pprint.pprint(dict)
    print("数据字典已生成。")
    s = sqex()
    # s.readcf()
    s.sync()
    print("配置文件与数据库同步完毕。")
    if dict != {}:
        print("开始读取并上传数据。")
        # print("shuchu",dict)
        rc = threading.Thread(target=readconfig_cycle, name="wew", args=())
        rc.start()
        # rc.join()

        for i, k in dict.items():
            d = threading.Thread(target=read_PLC_cycle, name="wew", args=(i,))
            d.start()
            d1 = threading.Thread(target=insert_sql_cycle, name="wew", args=(i,))
            d1.start()
    else:
        while 1:
            print("配置文件读取失败，请检查配置文件是否存在！")
            time.sleep(3600)
