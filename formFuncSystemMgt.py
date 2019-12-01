# -*- coding: utf-8 -*-

import sys 
import sqlite3
import pandas.io.sql as sql
import pandas as pd
from DataFrameModel import PandasModel
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_funcSystemMgt(object):
    def initUI(self, Ui_funcSystemMgt):

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        tabWidget = QTabWidget()
        mainLayout.addWidget(tabWidget)

        self.tabSymbol = QWidget()
        self.tabAcct = QWidget()

        tabWidget.addTab(self.tabSymbol, "Symbol Management")
        tabWidget.addTab(self.tabAcct, " Account Management")

        self.tabSymbolUI()
        self.tabAcctUI()

    def tabSymbolUI(self):
        layout = QVBoxLayout()
        self.tabSymbol.setLayout(layout)

        labelSymbolCode = QLabel('Symbol Code')
        editSymbolCode = QLineEdit()
        labelSymbolName = QLabel('Symbol Name')
        editSymbolName = QLineEdit()
        labelUnderly = QLabel('Underlying')
        editUnderly = QComboBox()
        editUnderly.addItems(['','MHI'])
        labelAsset = QLabel('Asset Class')
        editAsset = QComboBox()
        editAsset.addItems(['Stock','Future','ETF'])
        labelExchange = QLabel('Exchange')
        editExchange = QComboBox()
        editExchange.addItems(['SSE','SZ','HKEx','HKFE'])
        labelCur = QLabel('Currency')
        editCur = QComboBox()
        editCur.addItems(['CNY','HKD','USD'])
        labelMultiplier = QLabel('Multiplier')
        editMultiplier = QLineEdit()
        labelCommission = QLabel('Commission')
        editCommission = QLineEdit()

        #layoutInput = QHBoxLayout()
        gridInput = QGridLayout()
        gridInput.addWidget(labelSymbolCode,0,0)
        gridInput.addWidget(editSymbolCode,0,1)
        gridInput.addWidget(labelSymbolName,1,0)
        gridInput.addWidget(editSymbolName,1,1)
        gridInput.addWidget(labelUnderly,0,2)
        gridInput.addWidget(editUnderly,0,3)
        gridInput.addWidget(labelAsset,1,2)
        gridInput.addWidget(editAsset,1,3)
        gridInput.addWidget(labelExchange,0,4)
        gridInput.addWidget(editExchange,0,5)
        gridInput.addWidget(labelCur,1,4)
        gridInput.addWidget(editCur,1,5)
        gridInput.addWidget(labelMultiplier,0,6)
        gridInput.addWidget(editMultiplier,0,7)
        gridInput.addWidget(labelCommission,1,6)
        gridInput.addWidget(editCommission,1,7)
        gridInput.setColumnStretch(0,1)
        gridInput.setColumnStretch(1,1)
        gridInput.setColumnStretch(2,1)
        gridInput.setColumnStretch(3,1)
        gridInput.setColumnStretch(4,1)
        gridInput.setColumnStretch(5,1)
        gridInput.setColumnStretch(6,1)
        gridInput.setColumnStretch(7,1)


        btnAdd = QPushButton('Insert')
        btnUpdate = QPushButton('Update')
        btnDelete = QPushButton('Detele')
        btnAdd.clicked.connect(self.insertSymbol)
        btnUpdate.clicked.connect(self.updateSymbol)
        btnDelete.clicked.connect(self.deleteSymbol)
        hlayout = QHBoxLayout()
        hlayout.addStretch(5)
        hlayout.addWidget(btnAdd)
        hlayout.addWidget(btnUpdate)
        hlayout.addWidget(btnDelete)
        gridInput.addLayout(hlayout,2,0,1,8)

        tableView = QTableView()

        layout.addLayout(gridInput)
        layout.addWidget(tableView)

        strTable = "Symbol_Table"

        self.load_data(tableView,strTable)
    
    def tabAcctUI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("男"))
        sex.addWidget(QRadioButton("女"))
        layout.addRow(QLabel("性别"), sex)
        layout.addRow("生日", QLineEdit())
        self.tabAcct.setLayout(layout)

    def insertSymbol(self):
        print('insert symbol')

    def updateSymbol(self):
        print('update symbol')

    def deleteSymbol(self):
        btn = self.sender()
        print('delete symbol ' + str(btn.property('row')))

    def load_data(self,tableWidget,tableName):
        db = sqlite3.connect('AMS.db')
        query = "select * from " + tableName
        df = pd.read_sql(query, con = db)
        model = QStandardItemModel(df.shape[0],df.shape[1]+1) #多一列做操作按钮
        headName = list(df)
        headName.append('Action')
        model.setHorizontalHeaderLabels(headName)
        for row in range(df.shape[0]):
            for column in range(df.shape[1]):
                item = QStandardItem()
                itemValue = df.iloc[row,column]
                item.setData(QVariant(itemValue), Qt.DisplayRole)
                model.setItem(row, column, item)

        tableWidget.setModel(model)

        for row in range(df.shape[0]):
            btnDelete = QPushButton('Delete')
            btnDelete.clicked.connect(self.deleteSymbol)
            btnDelete.setProperty("row", df.iloc[row,0])
            #btnDelete.setProperty("column", column)
            tableWidget.setIndexWidget(model.index(row,df.shape[1]), btnDelete)

        #隐藏行号
        tableWidget.verticalHeader().setHidden(True)
        tableWidget.setSortingEnabled(True)
        #水平方向标签拓展剩下的窗口部分，填满表格
        tableWidget.horizontalHeader().setStretchLastSection(True)
        #水平方向，表格大小拓展到适当的尺寸      
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:lightblue;color: black;padding-left: 4px;border: 1px solid #6c6c6c;font: bold;}")
        

