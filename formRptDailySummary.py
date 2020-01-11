# -*- coding: utf-8 -*-
 
from PyQt5 import QtCore, QtGui, QtWidgets
from DataFrameModel import PandasModel
import pandas as pd
import sqlite3
 

class Ui_DailySummary(object):
    def initUI(self, Ui_DailySummary):

        #初始化报告参数
        self.rptDate = ''
        self.rptAcct = ''

        #初始化页面布局组件
        mainLayout = QtWidgets.QVBoxLayout(self)
        paraLayout = QtWidgets.QHBoxLayout()
        rptLayout = QtWidgets.QHBoxLayout()

        ########################################################
        #设置参数内容与格局
        #添加日期参数
        labelDate = QtWidgets.QLabel('Date')
        cal = QtWidgets.QCalendarWidget()
        dtEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        dtEdit.setCalendarPopup(True)
        dtEdit.setCalendarWidget(cal)
        dtEdit.setMaximumDate(QtCore.QDate.currentDate())
        dtEdit.setDate(cal.selectedDate())

        #添加账号参数
        labelAcct = QtWidgets.QLabel('Account')
        comboAcct = QtWidgets.QComboBox()
        comboAcct.setEditable(True)
        comboAcct.lineEdit().setAlignment(QtCore.Qt.AlignLeft)

        #提取报告按钮
        btnReport = QtWidgets.QPushButton("RUN REPORT")

        #设置参数布局内容
        paraLayout.addWidget(labelDate)
        paraLayout.addWidget(dtEdit)
        paraLayout.addWidget(labelAcct)
        paraLayout.addWidget(comboAcct)
        paraLayout.addStretch(10)
        paraLayout.addWidget(btnReport)
        paraLayout.addStretch(1)

        ########################################################
        #报告内容
        self.tblHold = QtWidgets.QTableView()
        rptLayout.addWidget(self.tblHold)

        ########################################################
        #设置页面主格局
        paraWidgets = QtWidgets.QWidget()
        paraWidgets.setLayout(paraLayout)
        mainLayout.addWidget(paraWidgets)
        #mainLayout.addLayout(paraLayout)
        mainLayout.addLayout(rptLayout)

        #设置默认参数
        comboAcct.addItems(['Citic', 'CMB', 'ALL'])

        #设置参数操作事件
        dtEdit.dateChanged.connect(self.saveDate)
        comboAcct.currentTextChanged.connect(self.saveAcct)
        btnReport.clicked.connect(self.loadReport)

        #页面视觉调整
        #comboAcct.setStyleSheet("background-color:white;")
        paraWidgets.setStyleSheet('''
            QDateEdit{background-color:white}
            QComboBox{background-color:white}
            QPushButton{background-color:white;font:bold}
            ''')
        paraLayout.setContentsMargins(0, 5, 0, 5)
        rptLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        #提取默认参数值
        self.rptDate = dtEdit.date().toString('yyyy-MM-dd')
        self.rptAcct = comboAcct.currentText()

        #btnFunc.setIcon(QtGui.QIcon("mesh.png"))
        btnReport.setStyleSheet("background-image:url(./logo/current.png);background-color:#87ba50")

    def loadReport(self):
        db = sqlite3.connect('AMS.db')
        query = "select * from Holding_Table where Date = '{}'".format(self.rptDate)
        print(query)
        df = pd.read_sql(query, con = db)
        model = PandasModel(df)
        self.tblHold.setModel(model)
        self.tblHold.setSortingEnabled(True)
        self.tblHold.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:lightblue;color: black;padding-left: 4px;border: 1px solid #6c6c6c;font: bold;}")

    def saveAcct(self, str):
        self.rptAcct = str

    def saveDate(self, date):
        self.rptDate = date.toString('yyyy-MM-dd')
        