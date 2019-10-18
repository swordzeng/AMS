# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from rptDailySummary import Ui_DailySummary
from rptReportTest import Ui_ReportTest
from second import Ui_Second
import sys
 
class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=None)
        
        #initialize format of main form
        self.setWindowTitle('AMS')
        self.resize(900,600)
        self.setStyleSheet("background-color:grey")

        self.formDailySummary = initDailySummary()
        self.formReportTest = initReportTest()
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

        #menu buttons
        menuBox = QtWidgets.QToolBox()

        groupReport = QtWidgets.QGroupBox()
        groupLayoutRpt = QtWidgets.QVBoxLayout(groupReport)
        groupLayoutRpt.setAlignment(QtCore.Qt.AlignCenter)
        btnReportDailySummary = QtWidgets.QPushButton('REPORT SUMMARY')
        btnReportTest = QtWidgets.QPushButton('REPORT TEST')
        btnReportTest.setFixedHeight(40)
        groupLayoutRpt.addWidget(btnReportDailySummary)
        groupLayoutRpt.addWidget(btnReportTest)
        groupLayoutRpt.setSpacing(0)

        groupFunc = QtWidgets.QGroupBox()
        groupLayoutFunc = QtWidgets.QVBoxLayout(groupFunc)
        groupLayoutFunc.setAlignment(QtCore.Qt.AlignCenter)
        btnFunc = QtWidgets.QPushButton('FUNCTION II')
        groupLayoutFunc.addWidget(btnFunc)
        
        menuBox.addItem(groupReport,"REPORT")
        menuBox.addItem(groupFunc,"FUNCTION")

        menuSplitter.addWidget(lblLogo)
        #menuSplitter.addWidget(btnReportDailySummary)
        #menuSplitter.addWidget(btnFunc)
        menuSplitter.addWidget(menuBox)
        #用frame占位，保持菜单按钮位置固定不变
        frame = QtWidgets.QFrame()
        menuSplitter.addWidget(frame)

        #set menu & button size
        lblLogo.setScaledContents(True)
        lblLogo.setFixedSize(180,80)
        #btnReportDailySummary.setFixedHeight(40)
        #btnReportTest.setFixedHeight(40)
        #btnFunc.setFixedHeight(40)

        #make splitter handle invisible
        #不写这段代码macOS在handle处会有一条线，不清楚原因
        #有了这个代码这条线消失，也不清楚原因
        #menuSplitter.handle(1).setFixedHeight(1)
        #menuSplitter.handle(2).setFixedHeight(1)
        #menuSplitter.handle(3).setFixedHeight(1)
        #分割线默认鼠标为拆分条，修改为无指针
        #menuSplitter.handle(1).setCursor(QtCore.Qt.BlankCursor)
        #menuSplitter.handle(2).setCursor(QtCore.Qt.BlankCursor)
        #menuSplitter.handle(3).setCursor(QtCore.Qt.BlankCursor)
        
        #set menu button separate line format
        #lblLogo.setStyleSheet("border-bottom-style:solid;border-bottom-width:1;border-bottom-color:white")
        #btnReportDailySummary.setStyleSheet("border-bottom-style:solid;border-bottom-width:1;border-bottom-color:white")
        #btnFunc.setStyleSheet("border-bottom-style:solid;border-bottom-width:1;border-bottom-color:white")

        menuSplitter.setStyleSheet('''
            QPushButton{border-style:solid;border-width:2;border-color:red;color:white;background-color:none}
            QLabel{border:none;background-color:grey}
            QToolBoxButton{min-height:50;border-style:solid;border-width:2;border-color:red;}
            QToolBox::tab{border-style:solid;border-width:2;border-color:red;background-color:#87ba50}
            QToolBox::tab:selected{border:none;background-color:#87ba50;background-image:url(current.png)}
            QGroupBox{border-style:solid;border-width:2;border-color:red;background-color:blue}
            QFrame{border:solid;background-color:black}
            ''')

        #connect button function
        btnReportDailySummary.clicked.connect(lambda :self.changeUI('REPORT SUMMARY'))
        btnReportTest.clicked.connect(lambda :self.changeUI('REPORT TEST'))
        btnFunc.clicked.connect(lambda :self.changeUI('FUNCTION II'))

        #initialize main splitter
        self.mainSplitter.addWidget(menuSplitter)
        self.mainSplitter.addWidget(self.formDailySummary)
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
        handle.setCursor(QtCore.Qt.PointingHandCursor)

    def handleSplitterButton(self, left=True): 
        if not all(self.mainSplitter.sizes()): 
            self.mainSplitter.setSizes([1, 1]) 
        elif left: 
            self.mainSplitter.setSizes([0, 1]) 

    def changeUI(self,name):
        if name == "REPORT SUMMARY":
            self.mainSplitter.widget(1).setParent(None)
            self.mainSplitter.insertWidget(1, self.formDailySummary)
            self.handleLayout(self.mainSplitter)

        if name == "REPORT TEST":
            self.mainSplitter.widget(1).setParent(None)
            self.mainSplitter.insertWidget(1, self.formReportTest)
            self.handleLayout(self.mainSplitter)

        if name == "FUNCTION II":
            self.mainSplitter.widget(1).setParent(None)
            self.mainSplitter.insertWidget(1, self.second)
            self.handleLayout(self.mainSplitter)
        
class initDailySummary(QWidget, Ui_DailySummary):
    def __init__(self):
        super(initDailySummary,self).__init__()
        #子窗口初始化时实现子窗口布局
        self.initUI(self)

class initReportTest(QWidget, Ui_ReportTest):
    def __init__(self):
        super(initReportTest,self).__init__()
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