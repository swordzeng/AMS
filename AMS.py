import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from formRptDailySummary import Ui_DailySummary
from formRptHolding import Ui_ReportHolding
from formFuncTradeAnalysis import Ui_funcTradeAnalysis
from formFuncSystemMgt import Ui_funcSystemMgt
from formFuncTradeEntry import Ui_funcTradeEntry
from formFuncJobs import Ui_Jobs
import cal_service as cal
import db_service as db
import threading
import datetime
import time


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent=None)
        self.setWindowTitle('Asset Management System')
        self.resize(1200, 700)

        # 定义页面名称常量
        self.UI_REPORT_SUMMARY = 'REPORT SUMMARY'
        self.UI_REPORT_HOLDING = 'REPORT HOLDING ANALYSIS'
        self.UI_FUNC_TRADE_ENTRY = 'FUNCTION TRANDE ENTRY'
        self.UI_FUNC_TRADE_ANALYSIS = 'FUNCTION TRADE ANALYSIS'
        self.UI_FUNC_SYSTEM_MGT = "FUNCTION SYSMTEM MANAGEMENT"
        self.UI_FUNC_JOBS = "FUNCTION JOBS"

        # 初始化页面
        self.formReportHolding = initRptHolding()
        # self.formReportSummary = initRptDailySummary()
        # self.formFuncTradeEntry = initFuncTradeEntry()
        # self.formFuncSystemMgt = initFuncSysMgt()
        # self.formFuncTradeAnalysis = initFuncTradeAnalysis()
        # self.formFuncJobs = initFuncJobs()

        # MainWindow已经有默认layout，不能直接set layout，不然会报警告
        mainWidget = QtWidgets.QWidget()
        mainLayout = QtWidgets.QVBoxLayout()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        # 创建页面容器并加载默认页面
        self.mainSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.mainSplitter.addWidget(self.formReportHolding)
        mainLayout.addWidget(self.mainSplitter)

        # ############################################################
        # ## 设置菜单栏

        menuBar = self.addToolBar('')
        menuBar.setMovable(False)

        pixLogo = QtGui.QPixmap('logo/logo.png')
        lblLogo = QtWidgets.QLabel()
        lblLogo.setPixmap(pixLogo)
        lblLogo.setScaledContents(True)
        lblLogo.setFixedSize(120, 50)
        menuBar.addWidget(lblLogo)

        # 菜单按钮居右
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        menuBar.addWidget(spacer)

        btnReport = QtWidgets.QPushButton("报告报告")
        menuReport = QtWidgets.QMenu()
        menuReport.addAction("概览", lambda: self.changeUI(self.UI_REPORT_SUMMARY))
        menuReport.addAction("持仓分析", lambda: self.changeUI(self.UI_REPORT_HOLDING))
        menuReport.addAction("期货分析", lambda: self.changeUI(self.UI_FUNC_TRADE_ANALYSIS))
        btnReport.setMenu(menuReport)

        btnFunc = QtWidgets.QPushButton("系统管理")
        menuFunc = QtWidgets.QMenu()
        menuFunc.addAction("交易管理", lambda: self.changeUI(self.UI_FUNC_TRADE_ENTRY))
        menuFunc.addAction("系统管理", lambda: self.changeUI(self.UI_FUNC_SYSTEM_MGT))
        menuFunc.addAction("作业管理", lambda: self.changeUI(self.UI_FUNC_JOBS))
        btnFunc.setMenu(menuFunc)

        btnSpace = QtWidgets.QPushButton("")
        btnSpace.setFixedWidth(20)

        groupMenu = QtWidgets.QGroupBox()
        layoutMenu = QtWidgets.QHBoxLayout()
        layoutMenu.addWidget(btnReport)
        layoutMenu.addWidget(btnFunc)
        layoutMenu.addWidget(btnSpace)
        groupMenu.setLayout(layoutMenu)

        menuBar.addWidget(groupMenu)

        # 添加border:none才能将背景色应用到整个tool bar
        menuBar.setStyleSheet("background-color:black; border:none")
        groupMenu.setStyleSheet('''
            QPushButton{color:white;height:40;width:120;font-family:SimHei;font-size:16px;}
            QPushButton::menu-indicator{image:none}
            ''')

        # ## 设置菜单栏
        #############################################################

    def funcDemo(self):
        print('test')

    def changeUI(self, name):
        if name == self.UI_REPORT_SUMMARY:
            formReportSummary = initRptDailySummary()
            form = formReportSummary
        if name == self.UI_REPORT_HOLDING:
            formReportHolding = initRptHolding()
            form = formReportHolding
        if name == self.UI_FUNC_TRADE_ENTRY:
            formFuncTradeEntry = initFuncTradeEntry()
            form = formFuncTradeEntry
        if name == self.UI_FUNC_TRADE_ANALYSIS:
            formFuncTradeAnalysis = initFuncTradeAnalysis()
            form = formFuncTradeAnalysis
        if name == self.UI_FUNC_SYSTEM_MGT:
            formFuncSystemMgt = initFuncSysMgt()
            form = formFuncSystemMgt
        if name == self.UI_FUNC_JOBS:
            formFuncJobs = initFuncJobs()
            form = formFuncJobs

        self.mainSplitter.widget(0).setParent(None)
        self.mainSplitter.insertWidget(0, form)


class initRptDailySummary(QtWidgets.QWidget, Ui_DailySummary):
    def __init__(self):
        super(initRptDailySummary, self).__init__()
        # 子窗口初始化时实现子窗口布局
        self.initUI(self)


class initFuncJobs(QtWidgets.QWidget, Ui_Jobs):
    def __init__(self):
        super(initFuncJobs, self).__init__()
        # 子窗口初始化时实现子窗口布局
        self.initUI(self)


class initRptHolding(QtWidgets.QWidget, Ui_ReportHolding):
    def __init__(self):
        super(initRptHolding, self).__init__()
        self.initUI(self)


class initFuncTradeAnalysis(QtWidgets.QWidget, Ui_funcTradeAnalysis):
    def __init__(self):
        super(initFuncTradeAnalysis, self).__init__()
        self.initUI(self)


class initFuncSysMgt(QtWidgets.QWidget, Ui_funcSystemMgt):
    def __init__(self):
        super(initFuncSysMgt, self).__init__()
        self.initUI(self)


class initFuncTradeEntry(QtWidgets.QWidget, Ui_funcTradeEntry):
    def __init__(self):
        super(initFuncTradeEntry, self).__init__()
        self.initUI(self)


def initJobs(self):
    t_last_str = db.get_latest_date('Job_Info', 'JobName', 'save_close_price')
    t_last = datetime.datetime.strptime(t_last_str, '%Y-%m-%d %H:%M:%S')
    t_now = datetime.datetime.now()
    t_now_str = t_now.strftime('%Y-%m-%d %H:%M:%S')
    t_checkpoint_str = (t_now+datetime.timedelta(days=-1)).strftime('%Y-%m-%d') + ' 16:30:00'
    t_checkpoint = datetime.datetime.strptime(t_checkpoint_str, '%Y-%m-%d %H:%M:%S')

    if t_last < t_checkpoint:
        cal.save_close_price()
        time.sleep(60)
        cal.save_exchange_rate()
        db.update_latest_date('Job_Info', 'Date', t_now_str, 'JobName', 'save_close_price')
    else:
        print('close price is update to date')

    cal.cal_holding()
    db.update_latest_date('Job_Info', 'Date', t_now_str, 'JobName', 'cal_holding')
    print('holding data is update to date')
    print('Init jobs finished')


if __name__ == '__main__':
    # 字体大小自适应分辨率
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()

    t1 = threading.Thread(target=initJobs, args=("t1",))
    t1.start()

    sys.exit(app.exec_())
