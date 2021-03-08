# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUi.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
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
        self.open_2 = QtWidgets.QPushButton(MainWindow)
        self.open_2.setGeometry(QtCore.QRect(150, 200, 75, 23))
        self.open_2.setObjectName("open_2")
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "工艺清单数据处理"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.open.setText(_translate("MainWindow", "打开"))
        self.open_2.setText(_translate("MainWindow", "确定"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">说明：</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1、请确保表格首行中有“规格”、“数量”、“备注”关键字。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2、确保“备注”列为表格在最后一列，新增加的数据列将位于此列后面。</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
