# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from first import Ui_First
from second import Ui_Second
import sys
 
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        
        #initialize format of main form
        self.setWindowTitle('AMS')
        #self.setFixedSize(900,600)
        self.resize(900,600)
        self.setStyleSheet("background-color:lightblue")

        self.first = First()
        self.second = Second()
        self.mainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        #main form layout
        mainWidget = QtWidgets.QWidget()
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainWidget.setLayout(mainLayout)
        mainLayout.addWidget(self.mainSplitter)
        self.setCentralWidget(mainWidget)

        #initialize menu widgets
        menuSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        menuSplitter.setHandleWidth(0)
        pixLogo = QtGui.QPixmap('logo.png')
        lblLogo = QtWidgets.QLabel()
        lblLogo.setPixmap(pixLogo)
        btnReport = QtWidgets.QPushButton('REPORT')
        btnFunc = QtWidgets.QPushButton('FUNCTION')

        menuSplitter.addWidget(lblLogo)
        menuSplitter.addWidget(btnReport)
        menuSplitter.addWidget(btnFunc)
        #用frame占位，保持菜单按钮位置固定不变
        frame = QtWidgets.QFrame()
        menuSplitter.addWidget(frame)

        #set menu & button size
        lblLogo.setScaledContents(True)
        lblLogo.setFixedSize(180,80)
        btnReport.setFixedHeight(40)
        btnFunc.setFixedHeight(40)

        #make splitter handle invisible
        menuSplitter.handle(1).setFixedHeight(1)
        menuSplitter.handle(2).setFixedHeight(1)
        menuSplitter.handle(3).setFixedHeight(1)

        #set menu button separate line format
        lblLogo.setStyleSheet("border-bottom-style:solid;border-bottom-width:1;border-bottom-color:white")
        btnReport.setStyleSheet("border-bottom-style:solid;border-bottom-width:1;border-bottom-color:white")
        btnFunc.setStyleSheet("border-bottom-style:solid;border-bottom-width:1;border-bottom-color:white")

        menuSplitter.setStyleSheet('''
            QPushButton{border:none;color:white;background-color:black}
            QLabel{border:none;background-color:black}
            QFrame{border:none;background-color:black}
            ''')

        #connect button function
        btnReport.clicked.connect(lambda :self.changeUI('REPORT'))
        btnFunc.clicked.connect(lambda :self.changeUI('FUNCTION'))

        #initialize main splitter
        self.mainSplitter.addWidget(menuSplitter)
        self.mainSplitter.addWidget(self.first)
        #菜单默认展开
        self.mainSplitter.setSizes([1, 1]) 

        #format handle of main splitter
        self.mainSplitter.setHandleWidth(20)
        self.handleLayout(self.mainSplitter)
        
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
        if not all(self.mainSplitter.sizes()): 
            self.mainSplitter.setSizes([1, 1]) 
        elif left: 
            self.mainSplitter.setSizes([0, 1]) 

    def changeUI(self,name):
        if name == "REPORT":
            self.mainSplitter.widget(1).setParent(None)
            self.mainSplitter.insertWidget(1, self.first)
            self.handleLayout(self.mainSplitter)
 
        if name == "FUNCTION":
            self.mainSplitter.widget(1).setParent(None)
            self.mainSplitter.insertWidget(1, self.second)
            self.handleLayout(self.mainSplitter)
        
class First(QWidget, Ui_First):
    def __init__(self):
        super(First,self).__init__()
        #子窗口初始化时实现子窗口布局
        self.initUI(self)
 
class Second(QWidget, Ui_Second):
    def __init__(self):
        super(Second,self).__init__()
        self.initUI(self)
 
if __name__ == '__main__':
    #字体大小自适应分辨率
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())