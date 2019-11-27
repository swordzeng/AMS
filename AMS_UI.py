import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from rptDailySummary import Ui_DailySummary
from rptReportTest import Ui_ReportTest
from second import Ui_Second

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

        #创建页面容器并加载默认页面
        self.formDailySummary = initDailySummary()
        self.mainSplitter = QSplitter(Qt.Horizontal) 
        self.mainSplitter.addWidget(self.formDailySummary)
        mainLayout.addWidget(self.mainSplitter)

        #定义页面名称常量
        self.UI_REPORT_SUMMARY = 'REPORT SUMMARY'
        self.UI_REPORT_HOLDING = 'REPORT HOLDING ANALYSIS'
        self.UI_FUNC_TRADE_ENTRY = 'FUNCTION TRANDE ENTRY'
        self.UI_FUNC_TRADE_MGT = 'FUNCTION TRADE MANAGEMENT'

        #############################################################
        ### 设置菜单栏

        menuBar = self.addToolBar('')
        menuBar.setMovable(False)

        pixLogo = QPixmap('logo.png')
        lblLogo = QLabel()
        lblLogo.setPixmap(pixLogo)
        lblLogo.setScaledContents(True)
        lblLogo.setFixedSize(120,50)
        menuBar.addWidget(lblLogo)

        #菜单按钮居右
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        menuBar.addWidget(spacer)

        btnReport = QPushButton("报告生成")
        menuReport = QMenu()
        actRptSummary = menuReport.addAction("概览", lambda:self.changeUI(self.UI_REPORT_SUMMARY))
        menuReport.addAction("持仓分析",lambda:self.changeUI(self.UI_REPORT_HOLDING))
        btnReport.setMenu(menuReport)

        btnFunc = QPushButton("交易管理")
        menuFunc = QMenu()
        menuFunc.addAction("交易录入",lambda:self.changeUI(self.UI_FUNC_TRADE_ENTRY))
        menuFunc.addAction("交易查看",lambda:self.changeUI(self.UI_FUNC_TRADE_MGT))
        btnFunc.setMenu(menuFunc)

        btnSpace = QPushButton("")
        btnSpace.setFixedWidth(20)

        groupMenu = QGroupBox()
        layoutMenu = QHBoxLayout()
        layoutMenu.addWidget(btnReport)
        layoutMenu.addWidget(btnFunc)
        layoutMenu.addWidget(btnSpace)
        groupMenu.setLayout(layoutMenu)

        menuBar.addWidget(groupMenu)

        #添加border:none才能将背景色应用到整个tool bar
        menuBar.setStyleSheet("background-color:black; border:none")
        groupMenu.setStyleSheet('''
            QPushButton{color:white;height:40;width:120;font-family:SimHei;font-size:16px;}
            QPushButton::menu-indicator{image:none}
            ''')

        ### 设置菜单栏
        #############################################################

    def funcDemo(self):
        print('test')

    def changeUI(self,name):
        if name == self.UI_REPORT_SUMMARY:
            form = initDailySummary()
        if name == self.UI_REPORT_HOLDING:
            form = initReportTest()
        if name == self.UI_FUNC_TRADE_ENTRY:
            form = Second()
        if name == self.UI_FUNC_TRADE_MGT:
            form = Second()

        self.mainSplitter.widget(0).setParent(None)
        self.mainSplitter.insertWidget(0, form)

class initDailySummary(QWidget, Ui_DailySummary):
    def __init__(self):
        super(initDailySummary,self).__init__()
        #子窗口初始化时实现子窗口布局
        self.initUI(self)

class initReportTest(QWidget, Ui_ReportTest):
    def __init__(self):
        super(initReportTest,self).__init__()
        self.initUI(self)
  
class Second(QWidget, Ui_Second):
    def __init__(self):
        super(Second,self).__init__()
        self.initUI(self)

if __name__ == '__main__':
    #字体大小自适应分辨率
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())