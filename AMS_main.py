# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from first import Ui_First
from second import Ui_Second
 
class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        
        self.first = First()
        self.second = Second()

        frameMenu = QtWidgets.QFrame()
        vbox = QtWidgets.QVBoxLayout(frameMenu)
        btnReport = QtWidgets.QPushButton('REPORT')
        btnReport.setObjectName('REPORT')
        vbox.addWidget(btnReport)
        btnFunc = QtWidgets.QPushButton('FUNCTION')
        btnFunc.setObjectName('FUNCTION')
        vbox.addWidget(btnFunc)
        vbox.addStretch(1)

        self.splitter.addWidget(frameMenu)
        self.splitter.addWidget(self.first)
 
        btnReport.clicked.connect(lambda :self.change(self.btnReport.objectName()))
        btnFunc.clicked.connect(lambda :self.change(self.btnFunc.objectName()))

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.splitter)
        self.setLayout(hbox)

    def change(self,name):
        if name == "REPORT":
            self.splitter.widget(1).setParent(None)
            self.splitter.insertWidget(1, self.first)
 
        if name == "FUNCTION":
            self.splitter.widget(1).setParent(None)
            self.splitter.insertWidget(1, self.second)
 
class First(QWidget, Ui_First):
    def __init__(self):
        super(First,self).__init__()
        # 子窗口初始化时实现子窗口布局
        self.initUI(self)
 
        # 设置子窗体最小尺寸
        self.setMinimumWidth(30)
        self.setMinimumHeight(30)
 
class Second(QWidget, Ui_Second):
    def __init__(self):
        super(Second,self).__init__()
        self.setupUi(self)
        self.setMinimumWidth(30)
        self.setMinimumHeight(30)
 
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())