# -*- coding: utf-8 -*-

import sys 
import sqlite3
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import portfolio
import DataFrameModel as dfm

class Ui_ReportHolding(object):
    def initUI(self, Ui_ReportHolding):

        self.acctList = ('CITIC','CMS','HUATAI','FUTU')
        self.initForm()

    def initForm(self):

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        self.Date = QDateEdit(QDate.currentDate())
        self.Date.setCalendarPopup(True)
        self.Date.setMaximumDate(QDate.currentDate())
        self.Acct = QComboBox()
        self.Acct.addItem('ALL')
        self.Acct.addItems(self.acctList)
        labelDate = QLabel('Report Date')
        labelAcct = QLabel('Account')
        btnReport = QPushButton("RUN REPORT")
        btnReport.clicked.connect(self.loadReport)
        hLayout = QHBoxLayout()
        hLayout.addWidget(labelDate)
        hLayout.addWidget(self.Date)
        hLayout.addWidget(labelAcct)
        hLayout.addWidget(self.Acct)
        hLayout.addStretch()
        hLayout.addWidget(btnReport)
        mainLayout.addLayout(hLayout)

        self.MV_CNY = QLabel()
        self.PL_CNY = QLabel()
        self.MV_HKD = QLabel()
        self.PL_HKD = QLabel()
        label_MV_CNY = QLabel('人民币市值')
        label_PL_CNY = QLabel('人民币盈利')
        label_MV_HKD = QLabel('港币市值')
        label_PL_HKD = QLabel('港币盈利')
        gridEdit = QGridLayout()
        gridEdit.addWidget(label_MV_CNY,0,0)
        gridEdit.addWidget(self.MV_CNY,1,0)
        gridEdit.addWidget(label_PL_CNY,0,1)
        gridEdit.addWidget(self.PL_CNY,1,1)
        gridEdit.addWidget(label_MV_HKD,0,2)
        gridEdit.addWidget(self.MV_HKD,1,2)
        gridEdit.addWidget(label_PL_HKD,0,3)
        gridEdit.addWidget(self.PL_HKD,1,3)
        gridEdit.setRowStretch(0,1)
        gridEdit.setRowStretch(1,2)        
        groupBox = QGroupBox('')
        groupBox.setLayout(gridEdit)
        mainLayout.addWidget(groupBox)

        self.tableHold = QTableView()
        mainLayout.addWidget(self.tableHold)

        mainLayout.setStretchFactor(hLayout,1)
        mainLayout.setStretchFactor(groupBox,2)
        mainLayout.setStretchFactor(self.tableHold,10)

        label_MV_CNY.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        label_PL_CNY.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        label_MV_HKD.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        label_PL_HKD.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.MV_CNY.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.PL_CNY.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.MV_HKD.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.PL_HKD.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.MV_CNY.setFont(QFont("Timers", 20, QFont.Bold))
        self.PL_CNY.setFont(QFont("Timers", 20, QFont.Bold))
        self.MV_HKD.setFont(QFont("Timers", 20, QFont.Bold))
        self.PL_HKD.setFont(QFont("Timers", 20, QFont.Bold))   
        
    def loadReport(self):

        acct = self.Acct.currentText()
        if acct == 'ALL':
            strAcct = str(self.acctList)
        else:
            strAcct = acct

        dfHold = portfolio.get_hold(self.Date.date().toString('yyyy-MM-dd'), strAcct)
        dfHold = dfHold.sort_values('SymbolCode',ascending=True)

        model = dfm.PandasModel(dfHold)
        self.tableHold.setModel(model)
        dfm.FormatView(self.tableHold)
        self.tableHold.sortByColumn(0,Qt.AscendingOrder)

        self.load_sum_factor(dfHold)

    def load_sum_factor(self, dfHold):
        df = dfHold[['Cur','MV','PL']]
        df_sum = df.groupby(['Cur']).sum()

        if 'HKD' not in list(df_sum.index):
            df_sum.loc['HKD'] = [0,0]

        if 'CNY' not in list(df_sum.index):
            df_sum.loc['CNY'] = [0,0]

        self.MV_CNY.setText(format(df_sum.loc['CNY','MV'],'0,.2f'))
        self.PL_CNY.setText(format(df_sum.loc['CNY','PL'],'0,.2f'))
        self.MV_HKD.setText(format(df_sum.loc['HKD','MV'],'0,.2f'))
        self.PL_HKD.setText(format(df_sum.loc['HKD','PL'],'0,.2f'))

        if df_sum.loc['HKD','PL']<0:
            self.PL_HKD.setStyleSheet("color:red;")
        else:
            self.PL_HKD.setStyleSheet("color:black;")

        if df_sum.loc['CNY','PL']<0:
            self.PL_CNY.setStyleSheet("color:red;")
        else:
            self.PL_CNY.setStyleSheet("color:black;")

    def deleteSymbol(self,model):
        btn = self.sender()
        code = model.data(model.index(btn.property('row'),0)).value()
        print(code)
