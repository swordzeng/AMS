# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from first import Ui_First
from second import Ui_Second
 
class Ui_MainWindow(QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

        self.setWindowTitle('AMS')
        self.resize(1200,600)

        self.first = First()
        self.second = Second()

        funcSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        btnReport = QtWidgets.QPushButton('REPORT')
        btnReport.setFixedSize(150,30)
        funcSplitter.addWidget(btnReport)
        btnFunc = QtWidgets.QPushButton('FUNCTION')
        btnFunc.setFixedSize(150,30)
        funcSplitter.addWidget(btnFunc)
        #用frame占位，保持菜单按钮位置固定不变
        frame = QtWidgets.QFrame()
        funcSplitter.addWidget(frame)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(20)
        self.splitter.addWidget(funcSplitter)
        self.splitter.addWidget(self.first)
        self.splitter.setSizes([0, 1]) 

        layout = QtWidgets.QVBoxLayout(self) 
        layout.addWidget(self.splitter) 
        self.handleLayout(self.splitter)

        btnReport.clicked.connect(lambda :self.changeUI('REPORT'))
        btnFunc.clicked.connect(lambda :self.changeUI('FUNCTION'))

    def handleLayout(self, splitter):
        handle = splitter.handle(1) 
        layout = QtWidgets.QVBoxLayout() 
        layout.setContentsMargins(0, 0, 0, 0) 
        button = QtWidgets.QToolButton(handle) 
        button.setArrowType(QtCore.Qt.LeftArrow) 
        button.setFixedSize(20,40)
        button.clicked.connect(lambda: self.handleSplitterButton(True)) 
        layout.addWidget(button) 
        handle.setLayout(layout) 

    def handleSplitterButton(self, left=True): 
        if not all(self.splitter.sizes()): 
            self.splitter.setSizes([1, 1]) 
        elif left: 
            self.splitter.setSizes([0, 1]) 

    def changeUI(self,name):
        if name == "REPORT":
            self.splitter.widget(1).setParent(None)
            self.splitter.insertWidget(1, self.first)
            self.handleLayout(self.splitter)
 
        if name == "FUNCTION":
            self.splitter.widget(1).setParent(None)
            self.splitter.insertWidget(1, self.second)
            self.handleLayout(self.splitter)
        
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
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())