import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from formRptDailySummary import Ui_DailySummary
from formRptTest import Ui_ReportTest
from formFuncTradeEntry import Ui_funcTradeEntry
from formFuncSystemMgt import Ui_funcSystemMgt
from formSecond import Ui_Second

class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):

        QWidget.__init__(self, parent=None)
        self.setWindowTitle('Asset Management System')
        self.resize(1200,700)

        #定义页面名称常量
        self.UI_REPORT_SUMMARY = 'REPORT SUMMARY'
        self.UI_REPORT_HOLDING = 'REPORT HOLDING ANALYSIS'
        self.UI_FUNC_TRADE_ENTRY = 'FUNCTION TRANDE ENTRY'
        self.UI_FUNC_TRADE_ANALYSIS = 'FUNCTION TRADE ANALYSIS'
        self.UI_FUNC_SYSTEM_MGT = "FUNCTION SYSMTEM MANAGEMENT"

        #初始化页面
        self.formReportSummary = initRptDailySummary()
        self.formReportHolding = initRptTest()
        self.formFuncTradeEntry = initFuncTradeEntry()
        self.formFuncSystemMgt = initFuncSysMgt()
        self.formFuncTradeAnalysis = initSecond()

        #MainWindow已经有默认layout，不能直接set layout，不然会报警告
        mainWidget = QWidget()
        mainLayout = QVBoxLayout()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        #创建页面容器并加载默认页面
        self.mainSplitter = QSplitter(Qt.Horizontal) 
        self.mainSplitter.addWidget(self.formFuncTradeEntry)
        mainLayout.addWidget(self.mainSplitter)

        #############################################################
        ### 设置菜单栏

        menuBar = self.addToolBar('')
        menuBar.setMovable(False)

        pixLogo = QPixmap('logo/logo.png')
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
        menuReport.addAction("概览", lambda:self.changeUI(self.UI_REPORT_SUMMARY))
        menuReport.addAction("持仓分析",lambda:self.changeUI(self.UI_REPORT_HOLDING))
        btnReport.setMenu(menuReport)

        btnFunc = QPushButton("交易管理")
        menuFunc = QMenu()
        menuFunc.addAction("交易录入",lambda:self.changeUI(self.UI_FUNC_TRADE_ENTRY))
        menuFunc.addAction("交易分析",lambda:self.changeUI(self.UI_FUNC_TRADE_ANALYSIS))
        menuFunc.addAction("系统管理",lambda:self.changeUI(self.UI_FUNC_SYSTEM_MGT))
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
            form = self.formReportSummary
        if name == self.UI_REPORT_HOLDING:
            form = self.formReportHolding
        if name == self.UI_FUNC_TRADE_ENTRY:
            form = self.formFuncTradeEntry
        if name == self.UI_FUNC_TRADE_ANALYSIS:
            form = self.formFuncTradeAnalysis
        if name == self.UI_FUNC_SYSTEM_MGT:
            form = self.formFuncSystemMgt

        self.mainSplitter.widget(0).setParent(None)
        self.mainSplitter.insertWidget(0, form)

class initRptDailySummary(QWidget, Ui_DailySummary):
    def __init__(self):
        super(initRptDailySummary,self).__init__()
        #子窗口初始化时实现子窗口布局
        self.initUI(self)

class initRptTest(QWidget, Ui_ReportTest):
    def __init__(self):
        super(initRptTest,self).__init__()
        self.initUI(self)
  
class initFuncTradeEntry(QWidget, Ui_funcTradeEntry):
    def __init__(self):
        super(initFuncTradeEntry,self).__init__()
        self.initUI(self)

class initFuncSysMgt(QWidget, Ui_funcSystemMgt):
    def __init__(self):
        super(initFuncSysMgt,self).__init__()
        self.initUI(self)

class initSecond(QWidget, Ui_Second):
    def __init__(self):
        super(initSecond,self).__init__()
        self.initUI(self)

if __name__ == '__main__':
    #字体大小自适应分辨率
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())