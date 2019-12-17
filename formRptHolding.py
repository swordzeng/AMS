# -*- coding: utf-8 -*-

import sys 
import sqlite3
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import portfolio
import getData
 

class Ui_ReportHolding(object):
    def initUI(self, Ui_ReportHolding):

        self.acctList = ('CITIC','CMS','HUATAI','FUTU')

        self.Date = QDateEdit(QDate.currentDate())
        self.Date.setCalendarPopup(True)
        self.Date.setMaximumDate(QDate.currentDate())
        self.Acct = QComboBox()
        self.Acct.addItems(self.acctList)

        labelDate = QLabel('Report Date')
        labelAcct = QLabel('Account')

        btnReport = QPushButton("RUN REPORT")
        btnReport.clicked.connect(self.loadReport)

        self.tableHold = QTableView()

        hLayout = QHBoxLayout()
        hLayout.addWidget(labelDate)
        hLayout.addWidget(self.Date)
        hLayout.addWidget(labelAcct)
        hLayout.addWidget(self.Acct)
        hLayout.addStretch()
        hLayout.addWidget(btnReport)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hLayout)
        mainLayout.addWidget(self.tableHold)
        self.setLayout(mainLayout)


    def loadReport(self):
        db = sqlite3.connect('AMS.db')
        model = QStandardItemModel()

        dfHold = portfolio.get_hold(self.Date.date().toString('yyyy-MM-dd'), self.acctList)
        getData.load_table(self.tableHold, model, dfHold)

