# -*- coding: utf-8 -*-

import sys 
import sqlite3
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import portfolio
import getData
from DataFrameModel import PandasModel,FloatDelegate

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

        dfHold = portfolio.get_hold(self.Date.date().toString('yyyy-MM-dd'), self.acctList)
        dfHold['Action'] = ''
        
        count = dfHold.shape[1] - 1
        model = PandasModel(dfHold)
        self.tableHold.setModel(model)
        self.tableHold.setItemDelegate(FloatDelegate(3, self.tableHold))

        self.tableHold.setSortingEnabled(True)
        self.tableHold.verticalHeader().setHidden(True)
        #水平方向，表格大小拓展到适当的尺寸      
        self.tableHold.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableHold.resizeColumnsToContents()
        self.tableHold.setAlternatingRowColors(True)
        self.tableHold.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:lightblue;color: black;padding-left: 4px;border: 1px solid #6c6c6c;font: bold;}")
        
        self.addActionColumn(self.tableHold, model, 'XXX')

    def addActionColumn(self, tableView, model, tableName):
        columnPos = model.columnCount() - 1
        tableView.setColumnHidden(columnPos, False)

        rowCount = model.rowCount()
        for row in range(rowCount):
            iconDelete = QIcon()
            iconDelete.addFile('logo/delete1.png')
            btnDelete = QPushButton('')
            btnDelete.setIcon(iconDelete)
            btnDelete.clicked.connect(lambda:self.deleteSymbol(model))
            SymbolCode = model.itemData(model.index(row,0))[0]  #返回dict类型
            btnDelete.setProperty("row", row)    
            tableView.setIndexWidget(model.index(row,columnPos), btnDelete) 

    def deleteSymbol(self,table):
        btn = self.sender()
        code = table.data(table.index(btn.property('row'),0)).value()
        print(code)
