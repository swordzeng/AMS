# -*- coding: utf-8 -*-

import sys 
import sqlite3
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import getData

class Ui_funcSystemMgt(object):
    def initUI(self, Ui_funcSystemMgt):

        self.db = sqlite3.connect('AMS.db')
        self.tableView = QTableView()

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
        labelSymbolName = QLabel('Symbol Name')
        labelUnderly = QLabel('Underlying')
        labelAsset = QLabel('Asset Class')
        labelExchange = QLabel('Exchange')
        labelCur = QLabel('Currency')
        labelMultiplier = QLabel('Multiplier')
        labelCommission = QLabel('Commission')

        self.editSymbolCode = QLineEdit()
        self.editSymbolName = QLineEdit()
        self.editUnderly = QComboBox()
        self.editAsset = QComboBox()
        self.editExchange = QComboBox()
        self.editCur = QComboBox()
        self.editMultiplier = QLineEdit('1')
        self.editCommission = QLineEdit('0')

        self.editUnderly.addItems(['','MHI'])
        self.editAsset.addItems(['Stock','Future','ETF'])
        self.editExchange.addItems(['SSE','SZ','HKEx','HKFE'])
        self.editCur.addItems(['CNY','HKD','USD'])

        #layoutInput = QHBoxLayout()
        gridInput = QGridLayout()
        gridInput.addWidget(labelSymbolCode,0,0)
        gridInput.addWidget(self.editSymbolCode,0,1)
        gridInput.addWidget(labelSymbolName,1,0)
        gridInput.addWidget(self.editSymbolName,1,1)
        gridInput.addWidget(labelUnderly,0,2)
        gridInput.addWidget(self.editUnderly,0,3)
        gridInput.addWidget(labelAsset,1,2)
        gridInput.addWidget(self.editAsset,1,3)
        gridInput.addWidget(labelExchange,0,4)
        gridInput.addWidget(self.editExchange,0,5)
        gridInput.addWidget(labelCur,1,4)
        gridInput.addWidget(self.editCur,1,5)
        gridInput.addWidget(labelMultiplier,0,6)
        gridInput.addWidget(self.editMultiplier,0,7)
        gridInput.addWidget(labelCommission,1,6)
        gridInput.addWidget(self.editCommission,1,7)
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
        btnAdd.clicked.connect(self.insertSymbol)
        btnUpdate.clicked.connect(self.updateSymbol)
        hlayout = QHBoxLayout()
        hlayout.addStretch(5)
        hlayout.addWidget(btnAdd)
        hlayout.addWidget(btnUpdate)
        gridInput.addLayout(hlayout,2,0,1,8)

        hlayout.setContentsMargins(0,10,0,0)
        #gridInput.setVerticalSpacing(0)

        widgetInput = QWidget()
        widgetInput.setLayout(gridInput)
        #widgetInput.setStyleSheet("background:blue")
        layout.addWidget(widgetInput)
        layout.addWidget(self.tableView)

        self.fill_data()

    def fill_data(self):
        strTable = "Symbol_Table"
        query = "SELECT * FROM Symbol_Table"
        model = QStandardItemModel()
        df = pd.read_sql(query, con = self.db)
        getData.load_table(self.tableView, model, df)
        self.addActionColumn(self.tableView, model, strTable)

    def tabAcctUI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("男"))
        sex.addWidget(QRadioButton("女"))
        layout.addRow(QLabel("性别"), sex)
        layout.addRow("生日", QLineEdit())
        self.tabAcct.setLayout(layout)

    def insertSymbol(self):
        if self.editSymbolCode.text().strip() != '':
            query = "SELECT * FROM Symbol_Table WHERE SymbolCode = '" + self.editSymbolCode.text().strip() + "'"
            df = pd.read_sql(query, con = self.db)

            if df.empty:
                dictSymbol = {}
                dictSymbol['SymbolCode'] = self.editSymbolCode.text().strip()
                dictSymbol['SymbolName'] = self.editSymbolName.text().strip()
                dictSymbol['Exchange'] = self.editExchange.currentText()
                dictSymbol['Underlying'] = self.editUnderly.currentText()
                dictSymbol['AssetClass'] = self.editAsset.currentText()
                dictSymbol['CurTrade'] = self.editCur.currentText()
                dictSymbol['CurSettle'] = self.editCur.currentText()
                dictSymbol['Multiplier'] = self.editMultiplier.text().strip()
                dictSymbol['Commission'] = self.editCommission.text().strip()
                getData.insert_record('Symbol_Table', dictSymbol)
                self.fill_data()
            else:
                print('symbol exist')

    def updateSymbol(self,table):
        btn = self.sender()
        print('update symbol ' + str(btn.property('code')))
        print(table)

    def deleteSymbol(self,table):
        btn = self.sender()
        query = "DELETE FROM " + table + " WHERE SymbolCode = '" + str(btn.property('code')) + "'"
        print(query)
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()
        cursor.close()

        self.fill_data()

    def addActionColumn(self, tableView, model, tableName):
        columnPos = model.columnCount() - 1
        tableView.setColumnHidden(columnPos, False)

        rowCount = model.rowCount()
        for row in range(rowCount):
            iconDelete = QIcon()
            iconDelete.addFile('logo/delete1.png')
            btnDelete = QPushButton('')
            btnDelete.setIcon(iconDelete)
            btnDelete.clicked.connect(lambda:self.deleteSymbol(tableName))
            symbolCode = model.itemData(model.index(row,0))[0]  #返回dict类型
            btnDelete.setProperty("code", symbolCode)    
            tableView.setIndexWidget(model.index(row,columnPos), btnDelete)           