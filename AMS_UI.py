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
        menuReport = QMenu()
        menuReport.setFixedWidth(120)
        menuReport.addAction("概览")
        menuReport.addAction("持仓分析")
        btnReport.setMenu(menuReport)
        toolBar.addWidget(btnReport)

        btnFunc = QPushButton("交易管理")
        menuFunc = QMenu()
        menuFunc.setFixedWidth(120)
        menuFunc.setStyleSheet("text-align:center")
        menuFunc.addAction("交易录入")
        menuFunc.addAction("交易查看")
        btnFunc.setMenu(menuFunc)
        toolBar.addWidget(btnFunc)

        btnSpace = QPushButton("")
        btnSpace.setFixedWidth(20)
        toolBar.addWidget(btnSpace)

        #添加border:none才能将背景色应用到整个tool bar
        toolBar.setStyleSheet("background-color:black; border:none")
        self.setStyleSheet('''
            QPushButton{color:white;height:40;width:120;font-family:SimHei;font-size:16px;}
            QPushButton::menu-indicator{image:none}
            ''')

        btnFunc.setStyleSheet('''
            QMenu {border-radius:5px;font-family:SimHei;font-size:16px;}
            QMenu::item {height:40px; width:120px;padding-left:30px;border: 1px solid none;}
            QMenu::item:selected {background-color:rgb(0,120,215);padding-left:25px;border: 1px solid rgb(65,173,255);}
            ''')


if __name__ == '__main__':
    #字体大小自适应分辨率
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())