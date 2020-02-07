# -*- coding: utf-8 -*-

import sys 
import sqlite3
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import DataFrameModel as dfm
import getData
import datetime

class Ui_funcTradeEntry(object):
    def initUI(self, Ui_funcTradeEntry):

        self.acctList = ('CITIC','CMS','HUATAI','FUTU')

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.widgetEdit = QWidget()
        self.mainLayout.addWidget(self.widgetEdit)

        self.groupBox = QGroupBox()
        self.mainLayout.addWidget(self.groupBox)

        self.Symbol = getData.MySymbol('')

        self.initEdit()
        self.fill_data()

    def fill_data(self):
        dateStart = self.StartDate.date().toString('yyyy-MM-dd')
        dateEnd = self.EndDate.date().toString('yyyy-MM-dd')
        if self.AccountID.currentText() == 'ALL':
            strAcct = str(self.acctList)
        else:
            strAcct = "('" +  self.AccountID.currentText() + "')"

        db = sqlite3.connect('AMS.db')
        query = """
            SELECT ID,AccountID,Date,SymbolCode,SymbolName,OrderType,Price,CurSettle AS Cur,Qty,Commission AS Comm,TradeAmt,SettleAmt
            FROM Order_Table
            WHERE AccountID in {} and Date >= '{}' and Date <= '{}' """.format(strAcct,dateStart,dateEnd)
        df = pd.read_sql(query, con = db)
        df['Action'] = ''
        #df.sort_values(by=['Date'], ascending=False, inplace=True)

        model = dfm.PandasModel(df)
        self.tableTrade.setModel(model)
        dfm.FormatView(self.tableTrade)
        dfm.addActionColumn(self.tableTrade, model, 'Order_Table', self.deleteSymbol)
        self.tableTrade.sortByColumn(0,Qt.DescendingOrder)
        #self.tableTrade.hideColumn(0)

    def get_symbol_list(self):
        self.SymbolCode.clear()

        codeList = getData.get_list('Symbol_Table','SymbolCode')
        codeList.insert(0,'')
        listSymbol = []
        i = 0
        for code in codeList:
            codeSymbol = getData.MySymbol(code)
            listSymbol.insert(i, codeSymbol.Code.ljust(10,' ') + ' | ' + codeSymbol.Name)
            i = i + 1
        self.SymbolCode.addItems(listSymbol)

    def initEdit(self):
        layout = QVBoxLayout()
        self.widgetEdit.setLayout(layout)

        labelAcct = QLabel("Account ID")
        labelDate = QLabel("Trade Date")
        labelSymbolCode = QLabel("Symbol Code")
        labelOrderType = QLabel("Order Type")
        labelPrice = QLabel("Price")
        labelCur = QLabel("Currency")
        labelQty = QLabel("Quantity")
        labelTradeAmt = QLabel("Trade Amt")
        labelCommission = QLabel("Commission")
        labelSettleAmt = QLabel("Settle Amt")

        self.Acct = QComboBox()
        self.Date = QDateEdit(QDate.currentDate())
        self.SymbolCode = QComboBox()
        self.OrderType = QComboBox()
        self.Price = QLineEdit('0')
        self.Cur = QComboBox()
        self.Qty = QLineEdit('0')
        self.TradeAmt = QLineEdit('0')
        self.Commission = QLineEdit('0')
        self.SettleAmt = QLineEdit('0')

        self.Acct.addItems(self.acctList)
        self.Date.setCalendarPopup(True)
        self.Date.setMaximumDate(QDate.currentDate())
        self.get_symbol_list()
        self.Cur.addItems(['HKD','CNY','USD'])
        self.OrderType.addItems(['Buy','Sell','Deposit','Withdraw','Bonus','Interest'])

        self.Acct.setStyleSheet("background-color:white")
        self.SymbolCode.setStyleSheet("background-color:white")
        self.OrderType.setStyleSheet("background-color:white")
        self.Cur.setStyleSheet("background-color:white")

        self.SymbolCode.currentIndexChanged.connect(self.codeChanged)
        self.OrderType.currentIndexChanged.connect(self.amtCal)
        self.Price.editingFinished.connect(self.amtCal)
        self.Qty.editingFinished.connect(self.amtCal)
        self.Commission.editingFinished.connect(self.amtCal)

        pDoubleValidator = QDoubleValidator(self)
        self.Price.setValidator(pDoubleValidator)
        self.Qty.setValidator(pDoubleValidator)
        self.Commission.setValidator(pDoubleValidator)

        gridEdit = QGridLayout()
        gridEdit.addWidget(labelAcct,0,0)
        gridEdit.addWidget(self.Acct,0,1)
        gridEdit.addWidget(labelSymbolCode,0,2)
        gridEdit.addWidget(self.SymbolCode,0,3)
        gridEdit.addWidget(labelOrderType,0,4)
        gridEdit.addWidget(self.OrderType,0,5)
        gridEdit.addWidget(labelPrice,0,6)
        gridEdit.addWidget(self.Price,0,7)
        gridEdit.addWidget(labelTradeAmt,0,8)
        gridEdit.addWidget(self.TradeAmt,0,9)

        gridEdit.addWidget(labelDate,1,0)
        gridEdit.addWidget(self.Date,1,1)
        gridEdit.addWidget(labelCur,1,2)
        gridEdit.addWidget(self.Cur,1,3)
        gridEdit.addWidget(labelQty,1,4)
        gridEdit.addWidget(self.Qty,1,5)
        gridEdit.addWidget(labelCommission,1,6)
        gridEdit.addWidget(self.Commission,1,7)
        gridEdit.addWidget(labelSettleAmt,1,8)
        gridEdit.addWidget(self.SettleAmt,1,9)

        btnInsert = QPushButton('INSERT')
        btnInsert.clicked.connect(self.insertTrade)
        gridEdit.addWidget(btnInsert,1,10)

        btnRefreshSymbol = QPushButton('Refresh Symbol')
        btnRefreshSymbol.clicked.connect(self.get_symbol_list)
        gridEdit.addWidget(btnRefreshSymbol,0,10)

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
        gridEdit.setColumnStretch(10,2)
        #gridEdit.setHorizontalSpacing(15)

        layout.addLayout(gridEdit)

        hLayout = QHBoxLayout()
        vLayout = QVBoxLayout()

        labelStartDate = QLabel("Start Date")
        labelEndDate = QLabel("End Date")
        labelAccount = QLabel("Account ID")
        self.StartDate = QDateEdit(QDate(2018,12,31))
        self.EndDate = QDateEdit(QDate.currentDate())
        self.AccountID = QComboBox()

        self.StartDate.setCalendarPopup(True)
        self.StartDate.setMaximumDate(QDate.currentDate())
        self.EndDate.setCalendarPopup(True)
        self.EndDate.setMaximumDate(QDate.currentDate())
        self.AccountID.addItems(self.acctList)
        self.AccountID.insertItem(0,'ALL')
        self.AccountID.setCurrentIndex(0)
        self.AccountID.setStyleSheet("background-color:white")

        self.StartDate.dateChanged.connect(self.fill_data)
        self.EndDate.dateChanged.connect(self.fill_data)
        self.AccountID.currentIndexChanged.connect(self.fill_data)

        hLayout.addWidget(labelStartDate)
        hLayout.addWidget(self.StartDate)
        hLayout.addWidget(labelEndDate)
        hLayout.addWidget(self.EndDate)
        hLayout.addWidget(labelAccount)
        hLayout.addWidget(self.AccountID)
        hLayout.addStretch()

        self.tableTrade = QTableView()

        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.tableTrade)

        self.groupBox.setLayout(vLayout)

        self.groupBox.setStyleSheet('''
            QGroupBox{border: 1px solid gray;}
            ''') 
        self.widgetEdit.setStyleSheet('''
            QWidget{border: 1px solid gray;}
            QComboBox{border: 1px solid gray;}
            QLineEdit{border: 1px solid gray;}
            QPushButton{border: 1px solid gray;}
            QLabel{border: none;}
            ''')
        self.mainLayout.setSpacing(6)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        #gridEdit.setContentsMargins(0, 0, 0, 0)
        gridEdit.setSpacing(3)
        hLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(0)
        hLayout.setSpacing(6)

    def insertTrade(self):
        dictData = {}
        dictData['AccountID'] = self.Acct.currentText()
        dictData['InputTime'] = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
        dictData['Date'] = self.Date.date().toString('yyyy-MM-dd')
        dictData['Time']= '00:00:00'
        dictData['SymbolCode'] = self.SymbolCode.currentText().split('|')[0].strip()
        dictData['SymbolName'] = self.SymbolCode.currentText().split('|')[1].strip()
        dictData['OrderID'] = 0
        dictData['TradeID'] = 0
        dictData['OrderType'] = self.OrderType.currentText()
        dictData['OpenClose'] =  ''
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
        self.Symbol = getData.MySymbol(self.SymbolCode.currentText().split('|')[0].strip())
        self.Cur.setCurrentText(self.Symbol.curSettle)

    def amtCal(self):
        price = 0 if self.Price.text().strip()=='' else float(self.Price.text().strip())
        qty = 0 if self.Qty.text().strip()=='' else float(self.Qty.text().strip())
        comm = 0 if self.Commission.text().strip()=='' else float(self.Commission.text().strip())
        
        amtTrade = abs(price * qty)

        strOrderType = self.OrderType.currentText()
        if strOrderType == 'Buy':
            amtSettle = -1 * (amtTrade + comm)
        elif strOrderType == 'Sell':
            amtSettle = amtTrade - comm
        elif  strOrderType == 'Deposit':
            amtSettle = amtTrade
        elif strOrderType == 'Withdraw':
            amtSettle = amtTrade * -1
        elif strOrderType == 'Interest':
            amtSettle = amtTrade
        elif  strOrderType == 'Bonus':
            amtSettle = amtTrade
        else:
            amtSettle = 0

        self.TradeAmt.setText(str(amtTrade))
        self.SettleAmt.setText(str(amtSettle)) 

    def deleteSymbol(self, model):
        btn = self.sender()
        db = sqlite3.connect('AMS.db')
        transID = model.data(model.index(btn.property('row'),0)).value()
        print(transID)
        query = "DELETE FROM Order_Table WHERE ID = " + str(transID)
        print(query)
        cursor = db.cursor()
        cursor.execute(query)
        db.commit()
        cursor.close()

        self.fill_data()


     

