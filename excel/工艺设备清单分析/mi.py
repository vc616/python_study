import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import mainUi


class MainCode(QMainWindow, mainUi.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        mainUi.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #self.btn_save.clicked.connect(self.open)
        self.open.clicked.connect(self.on_open)


    def on_open(self):
        #download_path = QtWidgets.QFileDialog.getExistingDirectory(self,"浏览","C:")
        download_path = Qtwidgets.QFileDialog.getOpenFileName(self,'选择文件','','Excel files(*.xlsx , *.xls)')
        self.lineEdit.setText(download_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = MainCode()
    md.show()
    sys.exit(app.exec_())
