import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):

        QWidget.__init__(self, parent=None)
        self.setWindowTitle('Asset Management System')
        self.resize(900,600)

        #MainWindow已经有默认layout，不能直接set layout，不然会报警告
        mainWidget = QWidget()
        mainLayout = QVBoxLayout()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        toolBar = self.addToolBar('')
        toolBar.setMovable(False)

        pixLogo = QPixmap('logo.png')
        lblLogo = QLabel()
        lblLogo.setPixmap(pixLogo)
        lblLogo.setScaledContents(True)
        lblLogo.setFixedSize(120,50)
        toolBar.addWidget(lblLogo)

        #菜单按钮居右
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolBar.addWidget(spacer)

        btnReport = QPushButton("报告生成")
        btnReport.setFixedWidth(120)
        menuReport = QMenu()
        menuReport.addAction("aaa")
        menuReport.addAction("bbb")
        btnReport.setMenu(menuReport)
        toolBar.addWidget(btnReport)

        btnFunc = QPushButton("交易管理")
        btnFunc.setFixedWidth(120)
        menuFunc = QMenu()
        menuFunc.setFixedWidth(120)
        menuFunc.setStyleSheet("text-align:center")
        menuFunc.addAction("aaa")
        menuFunc.addAction("bbb")
        btnFunc.setMenu(menuFunc)
        toolBar.addWidget(btnFunc)

        btnSpace = QPushButton("")
        btnSpace.setFixedWidth(60)
        toolBar.addWidget(btnSpace)

        #添加border:none才能将背景色应用到整个tool bar
        toolBar.setStyleSheet("background-color:black; border:none")
        btnReport.setStyleSheet("color:white")
        btnFunc.setStyleSheet("color:white")

if __name__ == '__main__':
    #字体大小自适应分辨率
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())