# -*- coding: utf-8 -*-

import sys 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import getData

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

        hlayout.setContentsMargins(0,10,0,0)
        #gridInput.setVerticalSpacing(0)

        widgetInput = QWidget()
        widgetInput.setLayout(gridInput)
        #widgetInput.setStyleSheet("background:blue")
        layout.addWidget(widgetInput)
        layout.addWidget(tableView)

        strTable = "Symbol_Table"
        model = QStandardItemModel()
        getData.load_table(tableView, model, strTable)
        self.addActionColumn(tableView, model, strTable)
    
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

    def updateSymbol(self,table):
        btn = self.sender()
        print('update symbol ' + str(btn.property('code')))
        print(table)

    def deleteSymbol(self,table):
        btn = self.sender()
        print('delete symbol ' + str(btn.property('code')))
        print(table)

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