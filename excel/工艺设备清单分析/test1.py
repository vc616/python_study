from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
import xlrd
from xlutils.copy import copy
import re


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow,self).__init__()
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
        self.textBrowser.setGeometry(QtCore.QRect(40, 80, 311, 91))
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
        #MainWindow.setTabOrder(self.checkBox, self.lineEdit)
        #self.open.clicked.connect(self.openfile)
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
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">说明：</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1、请确保表格首行中有“规格”、“数量”、“备注”关键字。</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2、确保“备注”列为表格在最后一列，新增加的数据列将位于此列后面。</p>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

    def openfile(self):
        #openfile_name = QFileDialog.getOpenFileName(self,'选择文件','','Excel files(*.xlsx , *.xls)')
        self.fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./",
                                                          "Excel Files (*.xlsx , *.xls)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(self.fileName1)
        self.lineEdit.setText(self.fileName1)

    def excel_ds(self):
        tablename = self.fileName1
        newtable = tablename.replace(".xlsx", "_电气.xls")
        book = xlrd.open_workbook(tablename)  # 打开一个excel,根据excel文件格式写后缀
        sheet = book.sheet_by_index(0)  # 根据顺序获取sheet,0表示第一个sheet

        old_content = copy(book)
        ws = old_content.get_sheet(0)

        y = sheet.row_values(0)

        for i in range(len(y)):
            if "规格" in y[i]:
                print(y[i], "第", i, "列")
                f_guige = i

            if "数量" == y[i]:
                print(y[i], "第", i, "列")
                f_num = i

            if "备注" in y[i]:
                print(y[i], "第", i, "列")
                f_kw = i + 2
                ws.write(0, f_kw, "设备功率")
                f_skw = i + 3
                ws.write(0, f_skw, "总功率")
                f_bp = i + 4
                ws.write(0, f_bp, "变频数量")
                f_zq = i + 5
                ws.write(0, f_zq, "直启数量")
                f_11 = i + 6
                ws.write(0, f_11, "<11kW")
                f_22 = i + 7
                ws.write(0, f_22, "11-22kW")
                f_75 = i + 8
                ws.write(0, f_75, "22-75kW")
                f_other = i + 9
                ws.write(0, f_other, ">75kW")
        sum_kw = 0.0
        sum_zq = 0
        sum_bp = 0
        sum_11 = 0
        sum_22 = 0
        sum_75 = 0
        sum_other = 0
        for i in range(sheet.nrows):  # 获取excel中有多少行
            r = sheet.cell(i, f_guige).value
            t = sheet.cell(i, f_num).value
            # print(r)
            s1 = re.search("\d*\.?\d*[kK][wW]", r)
            if s1:
                s2 = s1.group()
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

                    if s3<=11:
                        ws.write(i, f_11, t)
                        sum_11 = sum_11 + t
                    elif s3<=22 and s3 > 11:
                        ws.write(i, f_22, t)
                        sum_22 = sum_22 + t
                    elif s3<=75 and s3 > 22:
                        ws.write(i, f_75, t)
                        sum_75 = sum_75 + t
                    elif s3 > 75 :
                        ws.write(i, f_other, t)
                        sum_other = sum_other + t
            else:
                pass
        ws.write(i + 1, f_skw, sum_kw)
        ws.write(i + 1, f_bp, sum_bp)
        ws.write(i + 1, f_zq, sum_zq)
        ws.write(i + 1, f_11, sum_11)
        ws.write(i + 1, f_22, sum_22)
        ws.write(i + 1, f_75, sum_75)
        ws.write(i + 1, f_other, sum_other)



        old_content.save(newtable)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

