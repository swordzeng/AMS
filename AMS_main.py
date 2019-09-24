# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from first import Ui_First
from second import Ui_Second
 
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        
        # initialize format of main form
        self.setWindowTitle('AMS')
        self.setFixedSize(900,600)
        self.setStyleSheet("background-color:lightblue")
        #self.resize(1200,600)

        self.first = First()
        self.second = Second()
        self.mainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # main form layout
        mainWidget = QtWidgets.QWidget()
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainWidget.setLayout(mainLayout)
        mainLayout.addWidget(self.mainSplitter)
        self.setCentralWidget(mainWidget)

        # initialize menu widgets
        menuSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        menuSplitter.setHandleWidth(0)
        pixLogo = QtGui.QPixmap('logo.png')
        lblLogo = QtWidgets.QLabel()
        lblLogo.setScaledContents(True)
        lblLogo.setFixedSize(150,60)
        lblLogo.setPixmap(pixLogo)
        menuSplitter.addWidget(lblLogo)
        btnReport = QtWidgets.QPushButton('REPORT')
        btnReport.setFixedSize(150,30)
        menuSplitter.addWidget(btnReport)
        btnFunc = QtWidgets.QPushButton('FUNCTION')
        btnFunc.setFixedSize(150,30)
        menuSplitter.addWidget(btnFunc)
        #用frame占位，保持菜单按钮位置固定不变
        frame = QtWidgets.QFrame()
        menuSplitter.addWidget(frame)

        # initialize main splitter
        self.mainSplitter.addWidget(menuSplitter)
        self.mainSplitter.addWidget(self.first)
        #菜单默认关闭
        self.mainSplitter.setSizes([1, 1]) 

        # format handle of main splitter
        self.mainSplitter.setHandleWidth(20)
        self.handleLayout(self.mainSplitter)
        
        #self.mainSplitter.setStyleSheet('''
        #    QWidget{border-style:solid;border-width:2;border-color:red}
        #    ''')
        
        menuSplitter.setStyleSheet('''
            QPushButton{border:none;color:white;background-color:black}
            QLabel{border:none;background-color:black}
            QFrame{border:none;background-color:black}
            ''')

        # connect button function
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