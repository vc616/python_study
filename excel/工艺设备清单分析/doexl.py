from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
import xlrd
from xlutils.copy import copy
import re
import numpy as np


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.fileName1 = ""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(413, 270)
        self.lineEdit = QtWidgets.QLineEdit(MainWindow)
        self.lineEdit.setGeometry(QtCore.QRect(30, 30, 291, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.checkBox = QtWidgets.QCheckBox(MainWindow)
        self.checkBox.setGeometry(QtCore.QRect(-140, 230, 71, 16))
        self.checkBox.setObjectName("checkBox")
        self.open = QtWidgets.QPushButton(MainWindow)
        self.open.setGeometry(QtCore.QRect(330, 30, 75, 23))
        self.open.setObjectName("open")
        self.open.clicked.connect(self.openfile)
        self.open_2 = QtWidgets.QPushButton(MainWindow)
        self.open_2.setGeometry(QtCore.QRect(150, 200, 75, 23))
        self.open_2.setObjectName("open_2")
        self.open_2.clicked.connect(self.excel_ds)
        self.textBrowser = QtWidgets.QTextBrowser(MainWindow)
        self.textBrowser.setEnabled(False)
        self.textBrowser.setGeometry(QtCore.QRect(40, 80, 351, 91))
        self.textBrowser.setAcceptDrops(False)
        self.textBrowser.setToolTip("")
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setFrameShadow(QtWidgets.QFrame.Raised)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.checkBox, self.lineEdit)
        # MainWindow.setTabOrder(self.checkBox, self.lineEdit)
        # self.open.clicked.connect(self.openfile)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "工艺清单数据处理"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.open.setText(_translate("MainWindow", "打开"))
        self.open_2.setText(_translate("MainWindow", "确定"))
        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">说明：1、请确保标题行中有“规格”、“数量”关键字。</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">      2、请确设备清单位于表格第一个sheet。</p>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

    def openfile(self):
        # openfile_name = QFileDialog.getOpenFileName(self,'选择文件','','Excel files(*.xlsx , *.xls)')
        self.fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./",
                                                               "Excel Files (*.xlsx , *.xls)")  # 设置文件扩展名过滤,注意用双分号间隔
        print("打开文件名：", self.fileName1)
        self.lineEdit.setText(self.fileName1)

    def excel_ds(self):
        tablename = self.fileName1
        if tablename.endswith(".xlsx"):
            newtable = tablename.replace(".xlsx", "(电气).xls")
        if tablename.endswith(".xls"):
            newtable = tablename.replace(".xls", "(电气).xls")
        print("新文件名：", newtable)
        book = xlrd.open_workbook(tablename)  # 打开一个excel,根据excel文件格式写后缀
        sheet = book.sheet_by_index(0)  # 根据顺序获取sheet,0表示第一个sheet

        old_content = copy(book)
        ws = old_content.get_sheet(0)
        # print("测试01")
        gjc = ["数量", "序号", "名称", "规格", "材质", "备注", "品牌", "单位"]
        tj = []
        nrows = sheet.nrows
        print("总行数：", nrows)
        for i in range(nrows):
            # print(i)
            tj.append(0)
            h = sheet.row_values(i)
            for j in h:
                for k in gjc:
                    match = re.search(k, str(j))
                    if match != None:
                        tj[i] = tj[i] + 1
        # print(tj)
        bth = tj.index(max(tj))
        print("标题行：", bth)
        if tj[bth] > 3:
            y = sheet.row_values(bth)
            f_guige = 1000
            f_num = 1000
            for i in range(len(y)):
                if "规格" in str(y[i]):
                    print(y[i], "第", i, "列")
                    f_guige = i
                if "数量" == str(y[i]):
                    print(y[i], "第", i, "列")
                    f_num = i

            # i = len(y)
            # print("总行数：", i)
            f_kw = i + 1
            ws.write(bth, f_kw, "设备功率")
            f_skw = i + 2
            ws.write(bth, f_skw, "总功率")
            f_bp = i + 3
            ws.write(bth, f_bp, "变频数量")
            f_zq = i + 4
            ws.write(bth, f_zq, "直启数量")
            f_11 = i + 5
            ws.write(bth, f_11, "<11kW")
            f_22 = i + 6
            ws.write(bth, f_22, "11-22kW")
            f_75 = i + 7
            ws.write(bth, f_75, "22-75kW")
            f_other = i + 8
            ws.write(bth, f_other, ">75kW")
            sum_kw = 0.0
            sum_zq = 0
            sum_bp = 0
            sum_11 = 0
            sum_22 = 0
            sum_75 = 0
            sum_other = 0
            # print("测试点01")
            if f_guige == 1000 or f_num == 1000:
                print("在标题行中未找到规格或数量列")
            else:
                for i in range(nrows):  # 获取excel中有多少行
                    # for i in range(1, 11, 1):
                    # print(i)
                    if i > bth:

                        r1 = sheet.cell(i, f_guige).value
                        # print(i, r1)
                        t = sheet.cell(i, f_num).value
                        r2 = str(r1)
                        r = r2.replace(" ", "")
                        r = r.replace(" ", "")
                        #print(r)
                        #print(np.fromstring(r1, dtype=np.uint8))
                        s1 = re.search("\d*\.?\d*[kK][wW]", r)
                        print(i, r, s1)
                        if s1:
                            s2 = s1.group()
                            # print("S2:", s2)
                            s3 = float(s2[:len(s2) - 2])
                            ws.write(i, f_kw, s3)
                            ws.write(i, f_skw, t * s3)
                            sum_kw = sum_kw + t * s3
                            k1 = re.search("变频", r)
                            if k1:
                                ws.write(i, f_bp, t)
                                sum_bp = sum_bp + t
                            else:
                                ws.write(i, f_zq, t)
                                sum_zq = sum_zq + t

                                if s3 <= 11:
                                    ws.write(i, f_11, t)
                                    sum_11 = sum_11 + t
                                elif s3 <= 22 and s3 > 11:
                                    ws.write(i, f_22, t)
                                    sum_22 = sum_22 + t
                                elif s3 <= 75 and s3 > 22:
                                    ws.write(i, f_75, t)
                                    sum_75 = sum_75 + t
                                elif s3 > 75:
                                    ws.write(i, f_other, t)
                                    sum_other = sum_other + t
                        else:
                            #print("pass")
                            pass
                ws.write(i + 1, f_skw, sum_kw)
                ws.write(i + 1, f_bp, sum_bp)
                ws.write(i + 1, f_zq, sum_zq)
                ws.write(i + 1, f_11, sum_11)
                ws.write(i + 1, f_22, sum_22)
                ws.write(i + 1, f_75, sum_75)
                ws.write(i + 1, f_other, sum_other)
                #print("测试点02")
                try:
                    old_content.save(newtable)
                    print("新文件保存成功")
                except:
                    print("文件保存失败")
        else:
            print("未找到标题行")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
