# -*- coding: utf-8 -*-

import sys 
import sqlite3
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import getData

class Ui_funcTradeEntry(object):
    def initUI(self, Ui_funcTradeEntry):

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        self.widgetEdit = QWidget()
        self.tableView = QTableView()
        mainLayout.addWidget(self.widgetEdit)
        mainLayout.addWidget(self.tableView)

        self.initEdit()

        strTable = "Order_Table"
        model = QStandardItemModel()
        getData.load_table(self.tableView, model, strTable)
        self.addActionColumn(self.tableView, model, strTable)

        self.Symbol = MySymbol('')

    def initEdit(self):
        layout = QVBoxLayout()
        self.widgetEdit.setLayout(layout)

        labelDate = QLabel("Date")
        labelTime = QLabel("Time")
        labelSymbolCode = QLabel("Symbol Code")
        labelSymbolName = QLabel("Symbol Name")
        labelOrderID = QLabel("Order ID")
        labelTradeID = QLabel("Trade ID")
        labelBuySell = QLabel("Buy/Sell")
        labelOpenClose = QLabel("Open/Close")
        labelPrice = QLabel("Price")
        labelCur = QLabel("Currency")
        labelQty = QLabel("Quantity")
        labelTradeAmt = QLabel("Trade Amt")
        labelCommission = QLabel("Commission")
        labelSettleAmt = QLabel("Settle Amt")

        self.Date = QDateEdit(QDate.currentDate())
        self.Time = QTimeEdit(QTime.currentTime())
        self.SymbolCode = QComboBox()
        self.SymbolName = QLineEdit()
        self.OrderID = QComboBox()
        self.TradeID = QComboBox()
        self.BuySell = QComboBox()
        self.OpenClose = QComboBox()
        self.Price = QLineEdit()
        self.Cur = QComboBox()
        self.Qty = QLineEdit()
        self.TradeAmt = QLineEdit()
        self.Commission = QLineEdit()
        self.SettleAmt = QLineEdit()

        cal = QCalendarWidget()
        self.Date.setCalendarPopup(True)
        self.Date.setCalendarWidget(cal)
        self.Date.setMaximumDate(QDate.currentDate())
        self.Date.setDate(cal.selectedDate())
        codeList = getData.get_list('Symbol_Table','SymbolCode')
        codeList.insert(0,'')
        self.SymbolCode.addItems(codeList)
        self.SymbolName.setStyleSheet("background-color:rgb(225,225,225)")
        self.OrderID.addItems(list(map(str,range(1,10))))
        self.TradeID.addItems(list(map(str,range(1,10))))
        self.Cur.addItems(['HKD','CNY','USD'])
        self.BuySell.addItems(['Buy','Sell'])
        self.OpenClose.addItems(['Open','Close'])
        
        self.SymbolName.setReadOnly(True)
        self.TradeAmt.setReadOnly(True)
        self.SettleAmt.setReadOnly(True)
        
        self.SymbolCode.setStyleSheet("background-color:white")
        self.OrderID.setStyleSheet("background-color:white")
        self.TradeID.setStyleSheet("background-color:white")
        self.BuySell.setStyleSheet("background-color:white")
        self.OpenClose.setStyleSheet("background-color:white")
        self.Cur.setStyleSheet("background-color:white")
        self.SymbolName.setStyleSheet("background-color:rgb(225,225,225)")
        self.TradeAmt.setStyleSheet("background-color:rgb(225,225,225)")
        self.SettleAmt.setStyleSheet("background-color:rgb(225,225,225)")

        self.SymbolCode.currentIndexChanged.connect(self.codeChanged)
        self.BuySell.currentIndexChanged.connect(self.amtCal)
        self.Price.editingFinished.connect(self.amtCal)
        self.Qty.editingFinished.connect(self.amtCal)
        self.Commission.editingFinished.connect(self.amtCal)

        pDoubleValidator = QDoubleValidator(self)
        self.Price.setValidator(pDoubleValidator)
        self.Qty.setValidator(pDoubleValidator)
        self.Commission.setValidator(pDoubleValidator)

        gridEdit = QGridLayout()
        gridEdit.addWidget(labelDate,0,0)
        gridEdit.addWidget(self.Date,0,1)
        gridEdit.addWidget(labelSymbolCode,0,2)
        gridEdit.addWidget(self.SymbolCode,0,3)
        gridEdit.addWidget(labelOrderID,0,4)
        gridEdit.addWidget(self.OrderID,0,5)
        gridEdit.addWidget(labelBuySell,0,6)
        gridEdit.addWidget(self.BuySell,0,7)
        gridEdit.addWidget(labelPrice,0,8)
        gridEdit.addWidget(self.Price,0,9)
        gridEdit.addWidget(labelTradeAmt,0,10)
        gridEdit.addWidget(self.TradeAmt,0,11)
        gridEdit.addWidget(labelTime,1,0)
        gridEdit.addWidget(self.Time,1,1)
        gridEdit.addWidget(labelSymbolName,1,2)
        gridEdit.addWidget(self.SymbolName,1,3)
        gridEdit.addWidget(labelTradeID,1,4)
        gridEdit.addWidget(self.TradeID,1,5)
        gridEdit.addWidget(labelOpenClose,1,6)
        gridEdit.addWidget(self.OpenClose,1,7)
        gridEdit.addWidget(labelQty,1,8)
        gridEdit.addWidget(self.Qty,1,9)
        gridEdit.addWidget(labelSettleAmt,1,10)
        gridEdit.addWidget(self.SettleAmt,1,11)
        gridEdit.addWidget(labelCur,3,6)
        gridEdit.addWidget(self.Cur,3,7)
        gridEdit.addWidget(labelCommission,3,8)
        gridEdit.addWidget(self.Commission,3,9)

        gridEdit.setColumnStretch(0,1)
        gridEdit.setColumnStretch(1,2)
        gridEdit.setColumnStretch(2,1)
        gridEdit.setColumnStretch(3,2)
        gridEdit.setColumnStretch(4,1)
        gridEdit.setColumnStretch(5,2)
        gridEdit.setColumnStretch(6,1)
        gridEdit.setColumnStretch(7,2)
        gridEdit.setColumnStretch(8,1)
        gridEdit.setColumnStretch(9,2)
        gridEdit.setColumnStretch(10,1)
        gridEdit.setColumnStretch(11,2)
        gridEdit.setHorizontalSpacing(15)

        btnInsert = QPushButton('INSERT')
        btnInsert.clicked.connect(self.insertTrade)
        gridEdit.addWidget(btnInsert,3,11)

        layout.addLayout(gridEdit)

    def insertTrade(self):
        print('insert trade function')

    def codeChanged(self):
        self.Symbol = MySymbol(self.SymbolCode.currentText())
        self.SymbolName.setText(self.Symbol.Name)
        self.Commission.setText(str(self.Symbol.Commission))
        self.Cur.setCurrentText(self.Symbol.curSettle)

    def amtCal(self):
        price = 0 if self.Price.text().strip()=='' else float(self.Price.text().strip())
        qty = 0 if self.Qty.text().strip()=='' else float(self.Qty.text().strip())
        comm = 0 if self.Commission.text().strip()=='' else float(self.Commission.text().strip())
        
        amtTrade = price * qty * self.Symbol.Multiplier

        if self.BuySell.currentText() == 'Buy':
            amtSettle = -1 * (amtTrade + qty * comm)
        else:
            amtSettle = amtTrade - qty * comm

        self.TradeAmt.setText(str(amtTrade))
        self.SettleAmt.setText(str(amtSettle)) 

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
                transID = model.itemData(model.index(row,0))[0]  #返回dict类型
                btnDelete.setProperty("ID", transID)    
                tableView.setIndexWidget(model.index(row,columnPos), btnDelete)           

class MySymbol:
    def __init__(self, symbolCode):
        db = sqlite3.connect('AMS.db')
        query = "select * from Symbol_Table where SymbolCode='{}'".format(symbolCode)
        df = pd.read_sql(query, con = db)

        if not df.empty:
            self.Code = df.iloc[0]['SymbolCode']
            self.Name = df.iloc[0]['SymbolName']
            self.Exchange = df.iloc[0]['Exchange']
            self.Underly = df.iloc[0]['Underlying']
            self.AssetClass = df.iloc[0]['AssetClass']
            self.CurTrade = df.iloc[0]['CurTrade']
            self.curSettle = df.iloc[0]['CurSettle']
            self.Multiplier = df.iloc[0]['Multiplier']
            self.Commission = df.iloc[0]['Commission']
        else:
            self.Code = ''
            self.Name = ''
            self.Exchange = ''
            self.Underly = ''
            self.AssetClass = ''
            self.CurTrade = ''
            self.curSettle = ''
            self.Multiplier = ''
            self.Commission = 0            

