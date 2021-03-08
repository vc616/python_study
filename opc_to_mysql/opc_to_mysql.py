# 自动遍历kepserver中已经组态的链接和变量，并自动在mysql中创建相关表格和字段
import logging
import sys
import threading
import time

import pymysql
from opcua import Client

sys.path.insert(0, "..")

mysql_host = "192.168.0.81"
mysql_user = "root"
mysql_password = "********"
mysql_db = "dt"
mysql_port = 3306
kepserver_host = "192.168.0.81"
kepserver_port = "49320"
#

dic = {}
con = {}


class sqex():
    def __init__(self, host=mysql_host, user=mysql_user, password=mysql_password, port=mysql_port, dbn=mysql_db):

        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.dbn = dbn

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

        if ty == 'Boolean':
            ty = "varchar(20)"
        if ty == "Int32":
            ty = 'Int'
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


class SubHandler(object):
    """
    Client to subscription. It will receive events from server
    """

    def datachange_notification(self, node, val, data):
        global dic
        liststr = []
        liststr = node.nodeid.Identifier.split(".")
        dic[liststr[1]][liststr[2]] = val
        # print(type(val))

    def event_notification(self, event):
        print("Python: New event", event)


class readkepserver():
    def __init__(self, host=kepserver_host, port=kepserver_port):
        self.pro = []
        self.name = []
        self.type = []
        self.pro_g = []
        self.name_g = []
        self.type_g = []
        self.sublist = []
        self.host = host
        self.port = port

    def ergodic(self):
        if __name__ == "__main__":
            logging.basicConfig(level=logging.WARN)
            client = Client("opc.tcp://" + self.host + ":" + self.port)
            try:
                client.connect()
                for i in client.get_node("ns=2;s=S7-300").get_children():  # 获取项目节点列表
                    r = i.get_browse_name().Name
                    if r != '_Statistics' and r != '_System':  # 筛选后将有效的项目列表存入pro列表
                        self.pro.append(r)
                print("------从kepserver中读取的项目名列表------------------------")
                print(self.pro)
                print("-----------------------------------------------------------")

                for k in range(len(self.pro)):  # 按项目列表开始遍历
                    self.name.append([])
                    self.type.append([])
                    t = client.get_node("ns=2;s=S7-300." + self.pro[k]).get_children()  # 获取项目下所有变量节点
                    for i in t:
                        tag8 = i.get_browse_name().Name
                        if tag8 != '_System' and tag8 != '_Statistics' and tag8 != '_InternalTags':  # 筛选有效变量
                            self.name[k].append(tag8)
                            tag9 = i.get_data_type_as_variant_type().name
                            self.type[k].append(tag9)
                self.pro_g = self.pro[:]  # 变量_a 用于订阅，原变量做删减后用于修改数据库表格
                self.name_g = self.name[:]  # 变量_a 用于订阅，原变量做删减后用于修改数据库表格
                self.type_g = self.type[:]  # 变量_a 用于订阅，原变量做删减后用于修改数据库表格

                for i in range(len(self.name)):
                    print(self.pro_g[i])
                    print(self.name_g[i])
                    print(self.type_g[i])
                global dic
                global dict
                dic = {}
                dict = {}
                for i in range(len(self.pro_g)):
                    dic[self.pro_g[i]] = {}
                    dict[self.pro_g[i]] = {}
                    for j in range(len(self.name_g[i])):
                        dic[self.pro_g[i]][self.name_g[i][j]] = "n"
                        dict[self.pro_g[i]][self.name_g[i][j]] = self.type_g[i][j]
                client.disconnect()
            except:
                pass

            # print(pro[i])
            # print("变量名数量：",len(name[i]),"变量名列表：", name[i])
            # print("变量类型数量：",len(type[i]), "变量类型列表：",type[i])
            # for j in range(len(self.name[i])):
            # if self.type[i][j] == 'Float':
            # s.C_columns(self.pro[i], self.name[i][j], self.type[i][j])


class Subscribe_tag():
    def __init__(self, host=kepserver_host, port=kepserver_port):
        self.taglist = []
        self.host = host
        self.port = port

    def subscribe(self):
        global dic
        if __name__ == "__main__":
            logging.basicConfig(level=logging.WARN)
            client = Client("opc.tcp://" + self.host + ":" + self.port)
            try:
                client.connect()
                for i, j in dic.items():
                    for k, l in j.items():
                        ss = client.get_node("ns=2;s=S7-300." + i + "." + k)
                        self.taglist.append(ss)
                print("订阅变量总数为：", len(self.taglist))
            except:
                pass
            handler = SubHandler()
            sub = client.create_subscription(5000, handler)
            handle1 = sub.subscribe_data_change(self.taglist)


def readcf(t):  # 读取服务器配置
    readconfig_debug = 0
    global con
    sq = "SELECT ID, RecordTime, TTI FROM config"
    host = mysql_host
    user = mysql_user
    password = mysql_password
    dbn = mysql_db
    port = mysql_port
    while 1:
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
                con[x[0]]["RT"] = x[1]
                con[x[0]]["TTI"] = x[2]
            print(con)
            db.close()
        except:
            if readconfig_debug == 1:
                print("获取服务器配置失败！X")
        time.sleep(t)


def insert_sql(pro_name):
    global dic
    global trend_y
    ticks0 = time.perf_counter()
    while 1:
        host = mysql_host
        user = mysql_user
        password = mysql_password
        port = mysql_port
        dabase = mysql_db
        s = []
        v = []
        # nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        for key, value in dic[pro_name].items():
            ty = type(value)
            if ty == float:
                s.append(key)
                v.append(str(round(value, 1)))
            elif "System" in key and ty == bool:
                s.append(key)
                v.append("'" + str(value) + "'")
            elif ty == "Int32":
                s.append(key)
                v.append(str(value))

        ticks1 = time.perf_counter()
        subtime = ticks1 - ticks0
        ticks0 = ticks1
        print(ticks1)
        if len(s) > 0:
            s.append("subtime")
            v.append(str(subtime))
            insert_str_key = "(`" + ("`, `".join(s)) + "`)"
            insert_str_value = "(" + (", ".join(v)) + ")"
            insert_sql = "INSERT INTO `" + dabase + "`.`" + pro_name + "_r`" + insert_str_key + " VALUES " + insert_str_value
            print(pro_name, insert_sql)
            try:
                db = pymysql.connect(host, user, password, dabase, port)
                cursor = db.cursor()
                cursor.execute(insert_sql)
                db.commit()
                db.close()
                print(pro_name, "归档数据上传成功！√", i)
            except:
                print(pro_name, "归档数据上传失败  X")
        else:
            print(pro_name, "没有获取到可归档数据 X ")
        try:
            t = con[pro_name][0]
            if t < 5:
                t = 5
            else:
                pass
        except:
            t = 60
        time.sleep(t)


def update_sql(pro_name):
    global dic
    global con
    while 1:
        host = mysql_host
        user = mysql_user
        dabase = mysql_db
        password = mysql_password
        port = mysql_port
        s = []
        # nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for key, value in dic[pro_name].items():
            ty = type(value)
            if ty == float:
                s.append("`" + key + "`" + "=" + str(round(value, 1)))
            if ty == int:
                s.append("`" + key + "`" + "=" + str(value))
            if ty == bool:
                s.append("`" + key + "`" + "='" + str(value) + "'")
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
            except:
                print(pro_name, "实时数据上传失败  X")
        else:
            print(pro_name, "没有获取到实时数据 X ")
        try:
            t = con[pro_name][1]
            if t < 3:
                t = 3
            else:
                pass
        except:
            t = 60
        time.sleep(t)


def sync():
    s = sqex()
    for i, j in dic.items():
        ia = i + "_r"
        if s.F_table(i) == False:
            print(s.C_table(i))
        if s.F_table(ia) == False:
            print(s.C_table_r(ia))
        name = s.F_columns_all(i)
        # print(name)
        name_r = s.F_columns_all(ia)
        # print(name_r)
        for k, l in j.items():
            # print(k)
            if len(name) > 0:  # 对比读取的变量名跟数据表中的差别，筛选新增的变量
                if k not in name:
                    # print(i,"—",k,"—",dict[i][k])
                    s.C_columns(i, k, dict[i][k])
            if len(name_r) > 0:
                if k not in name_r:
                    # print(ia,"—",k,"—",dict[i][k])
                    if ("System" in k) or (dict[i][k] == "Float") or (dict[i][k] == "Int32"):  # 筛选需要归档的变量
                        s.C_columns(ia, k, dict[i][k])


d = readkepserver()
d.ergodic()  # 读取所有服务器中的变量，存入dic和dict两个字典
# dic = {'guangchangA': {'COD4': 'n', 'cod7': 'n', 'code900': 'n', 'E_Stop': 'n',
# dict = {'guangchangA': {'COD4': 'Int32', 'cod7': 'Boolean', 'code900': 'Boolean', 'E_Stop': 'Boolean'

# 开始同步数据库
sync()
# 数据库同步结束

# 开始订阅变量
e = Subscribe_tag()
e.subscribe()

# 开始读取数据更新时间参数线程
rec = threading.Thread(target=readcf, name="re1", args=(60,))  # 开启读取服务器配置线程
rec.start()
time.sleep(10)

# 开始数据库写入线程
for i, j in dic.items():
    d = threading.Thread(target=insert_sql, name="wew", args=(i,))
    e = threading.Thread(target=update_sql, name="wew", args=(i,))
    d.start()
    time.sleep(1)
    e.start()
    time.sleep(1)
