# -*- coding: utf-8 -*-

import sys 
import sqlite3
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import getData

class Ui_funcTradeAnalysis(object):
    def initUI(self, Ui_funcTradeAnalysis):

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        self.widgetEdit = QWidget()
        mainLayout.addWidget(self.widgetEdit)

        self.tableTrade = QTableView()
        self.tableOrderPL = QTableView()
        self.tableDayPL = QTableView()
        self.tableMonthPL = QTableView()
        hLayout = QHBoxLayout()
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.tableDayPL,2)
        vLayout.addWidget(self.tableMonthPL,1)
        hLayout.addWidget(self.tableTrade,5)
        hLayout.addWidget(self.tableOrderPL,2)
        hLayout.addLayout(vLayout,2)
        mainLayout.addLayout(hLayout)

        self.Symbol = MySymbol('')

        self.initEdit()
        self.fill_data()

    def fill_data(self):
        db = sqlite3.connect('AMS.db')
        model = QStandardItemModel()
        query = """
            SELECT Time,SymbolCode AS Symbol,OrderID,TradeID,OpenClose AS OC,OrderType AS BS,Price,Qty,Commission AS Comm
            FROM Order_Table
            WHERE AccountID = 'IB' and Date = '"""
        query = query + self.Date.date().toString('yyyy-MM-dd') + "'"
        df = pd.read_sql(query, con = db)
        getData.load_table(self.tableTrade, model, df)
        #self.addActionColumn(self.tableView, model, strTable)

        query = "SELECT * FROM Order_Table"
        dfAll = pd.read_sql(query, con=db)
        dfAll['DateTime'] = pd.to_datetime(dfAll['Date'])
        dfAll['Year'] = dfAll['DateTime'].dt.year
        dfAll['Month'] = dfAll['DateTime'].dt.month
        dfAll['Day'] = dfAll['DateTime'].dt.day
        dfMonth = dfAll[(dfAll['Year']==self.Date.date().year()) & (dfAll['Month']==self.Date.date().month())]
        dfOrderPL = dfMonth.groupby(['Date','OrderID'])[['SettleAmt']].sum()
        dfDayPL = dfMonth.groupby(['Date'])[['SettleAmt']].sum()
        dfMonthPL = dfAll.groupby(['Year','Month'])[['SettleAmt']].sum()

        modelOrderPL = QStandardItemModel()
        modelDayPL = QStandardItemModel()
        modelMonthPL  = QStandardItemModel()

        dfOrderPL.reset_index(inplace =True)
        dfOrderPL.sort_values(by=['Date', 'OrderID'], ascending=False, inplace=True)
        dfDayPL.reset_index(inplace =True)
        dfDayPL.sort_values(by='Date', ascending=False, inplace=True)
        dfMonthPL.reset_index(inplace =True)
        dfMonthPL.sort_values(by=['Year', 'Month'], ascending=False, inplace=True)
        getData.load_table(self.tableOrderPL, modelOrderPL, dfOrderPL)
        getData.load_table(self.tableDayPL, modelDayPL, dfDayPL)
        getData.load_table(self.tableMonthPL, modelMonthPL, dfMonthPL)

        self.tableTrade.sortByColumn(0,0)

    def initEdit(self):
        layout = QVBoxLayout()
        self.widgetEdit.setLayout(layout)

        labelDate = QLabel("Date")
        labelTime = QLabel("Time")
        labelSymbolCode = QLabel("Symbol Code")
        labelOrderID = QLabel("Order ID")
        labelTradeID = QLabel("Trade ID")
        labelBuySell = QLabel("Buy/Sell")
        labelPrice = QLabel("Price")
        labelCur = QLabel("Currency")
        labelQty = QLabel("Quantity")
        labelTradeAmt = QLabel("Trade Amt")
        labelCommission = QLabel("Commission")
        labelSettleAmt = QLabel("Settle Amt")

        self.Date = QDateEdit(QDate.currentDate())
        self.Time = QTimeEdit(QTime.currentTime())
        self.SymbolCode = QComboBox()
        self.OrderID = QComboBox()
        self.TradeID = QComboBox()
        self.BuySell = QComboBox()
        self.Price = QLineEdit('0')
        self.Cur = QComboBox()
        self.Qty = QLineEdit('0')
        self.TradeAmt = QLineEdit('0')
        self.Commission = QLineEdit('0')
        self.SettleAmt = QLineEdit('0')

        cal = QCalendarWidget()
        self.Date.setCalendarPopup(True)
        self.Date.setCalendarWidget(cal)
        self.Date.setMaximumDate(QDate.currentDate())
        self.Date.setDate(cal.selectedDate())
        self.Time.setDisplayFormat('HH:mm:ss')
        codeList = getData.get_list('Symbol_Table','SymbolCode')
        codeList.insert(0,'')
        codeList = [str(i) for i in codeList]
        self.SymbolCode.addItems(codeList)
        self.OrderID.addItems(list(map(str,range(1,10))))
        self.TradeID.addItems(list(map(str,range(1,10))))
        self.Cur.addItems(['HKD','CNY','USD'])
        self.BuySell.addItems(['Open-Buy','Open-Sell','Close-Buy','Close-Sell'])

        self.TradeAmt.setReadOnly(True)
        self.SettleAmt.setReadOnly(True)
        
        self.SymbolCode.setStyleSheet("background-color:white")
        self.OrderID.setStyleSheet("background-color:white")
        self.TradeID.setStyleSheet("background-color:white")
        self.BuySell.setStyleSheet("background-color:white")
        self.Cur.setStyleSheet("background-color:white")
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
        gridEdit.addWidget(labelPrice,0,6)
        gridEdit.addWidget(self.Price,0,7)
        gridEdit.addWidget(labelQty,0,8)
        gridEdit.addWidget(self.Qty,0,9)
        gridEdit.addWidget(labelTradeAmt,0,10)
        gridEdit.addWidget(self.TradeAmt,0,11)
        gridEdit.addWidget(labelTime,1,0)
        gridEdit.addWidget(self.Time,1,1)
        gridEdit.addWidget(labelBuySell,1,2)
        gridEdit.addWidget(self.BuySell,1,3)
        gridEdit.addWidget(labelTradeID,1,4)
        gridEdit.addWidget(self.TradeID,1,5)
        gridEdit.addWidget(labelCur,1,6)
        gridEdit.addWidget(self.Cur,1,7)
        gridEdit.addWidget(labelCommission,1,8)
        gridEdit.addWidget(self.Commission,1,9)
        gridEdit.addWidget(labelSettleAmt,1,10)
        gridEdit.addWidget(self.SettleAmt,1,11)

        btnInsert = QPushButton('INSERT')
        btnInsert.clicked.connect(self.insertTrade)
        gridEdit.addWidget(btnInsert,3,10,1,2)

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
        #gridEdit.setHorizontalSpacing(15)

        layout.addLayout(gridEdit)

    def insertTrade(self):
        dictData = {}
        dictData['AccountID'] = 'IB'
        dictData['Date'] = self.Date.date().toString('yyyy-MM-dd')
        dictData['Time']= self.Time.time().toString('HH:mm:ss')
        dictData['SymbolCode'] = self.SymbolCode.currentText()
        dictData['SymbolName'] = self.Symbol.Name
        dictData['OrderID'] = int(self.OrderID.currentText())
        dictData['TradeID'] = int(self.TradeID.currentText())
        listBuySell = self.BuySell.currentText().split('-')
        dictData['OrderType'] = listBuySell[1]
        dictData['OpenClose'] =  listBuySell[0]
        dictData['CurTrade'] = self.Cur.currentText()
        dictData['CurSettle'] = self.Cur.currentText()
        dictData['Price'] = float(self.Price.text())
        dictData['Qty'] = float(self.Qty.text())
        dictData['Commission'] = float(self.Commission.text())
        dictData['TradeAmt']    = float(self.TradeAmt.text())
        dictData['SettleAmt'] = float(self.SettleAmt.text())

        getData.insert_record('Order_Table', dictData)
        self.fill_data()

    def codeChanged(self):
        self.Symbol = MySymbol(self.SymbolCode.currentText())
        self.Commission.setText(str(self.Symbol.Commission))
        self.Cur.setCurrentText(self.Symbol.curSettle)

    def amtCal(self):
        price = 0 if self.Price.text().strip()=='' else float(self.Price.text().strip())
        qty = 0 if self.Qty.text().strip()=='' else float(self.Qty.text().strip())
        comm = 0 if self.Commission.text().strip()=='' else float(self.Commission.text().strip())
        
        amtTrade = price * qty * self.Symbol.Multiplier

        strBuySell = self.BuySell.currentText().split('-')[1]
        if strBuySell == 'Buy':
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
            self.Market = df.iloc[0]['Market']
            self.Underly = df.iloc[0]['Underlying']
            self.AssetClass = df.iloc[0]['AssetClass']
            self.CurTrade = df.iloc[0]['CurTrade']
            self.curSettle = df.iloc[0]['CurSettle']
            self.Multiplier = df.iloc[0]['Multiplier']
            self.Commission = df.iloc[0]['Commission']
        else:
            self.Code = ''
            self.Name = ''
            self.Market = ''
            self.Underly = ''
            self.AssetClass = ''
            self.CurTrade = ''
            self.curSettle = ''
            self.Multiplier = ''
            self.Commission = 0            
