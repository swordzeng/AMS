# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from first import Ui_First
from second import Ui_Second
 
class Ui_MainWindow(QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        
        self.setWindowTitle('AMS')
        self.resize(800,600)

        self.first = First()
        self.second = Second()

        vSplit = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        btnReport = QtWidgets.QPushButton('REPORT')
        btnReport.setObjectName('REPORT')
        btnReport.setFixedSize(150,40)
        vSplit.addWidget(btnReport)
        btnFunc = QtWidgets.QPushButton('FUNCTION')
        btnFunc.setObjectName('FUNCTION')
        btnFunc.setFixedSize(150,40)
        vSplit.addWidget(btnFunc)
        #用frame占位，保持菜单按钮位置固定不变
        frame = QtWidgets.QFrame()
        vSplit.addWidget(frame)
        
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(vSplit)
        self.splitter.addWidget(self.first)

        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.splitter)
        self.setLayout(hbox)

        btnReport.clicked.connect(lambda :self.change(btnReport.objectName()))
        btnFunc.clicked.connect(lambda :self.change(btnFunc.objectName()))

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
        self.initUI(self)
        self.setMinimumWidth(30)
        self.setMinimumHeight(30)
 
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    ui.show()
    sys.exit(app.exec_())