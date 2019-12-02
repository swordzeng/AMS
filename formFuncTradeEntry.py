# -*- coding: utf-8 -*-

import sys 
import sqlite3
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_funcTradeEntry(object):
    def initUI(self, Ui_funcTradeEntry):

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        self.widgetEdit = QWidget()
        self.tableView = QTableView()
        mainLayout.addWidget(self.widgetEdit)
        mainLayout.addWidget(self.tableView)

        self.initEdit()

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
        labelTradeAmt = QLabel("Trade Amt")
        labelCommission = QLabel("Commission")
        labelSettleAmt = QLabel("Settle Amt")

        self.Date = QDateEdit(QDate.currentDate())
        self.Time = QTimeEdit(QTime.currentTime())
        self.SymbolCode = QLineEdit()
        self.SymbolName = QLineEdit()
        self.OrderID = QComboBox()
        self.TradeID = QComboBox()
        self.BuySell = QComboBox()
        self.OpenClose = QComboBox()
        self.Price = QLineEdit()
        self.TradeAmt = QLineEdit()
        self.Commission = QLineEdit()
        self.SettleAmt = QLineEdit()

        cal = QCalendarWidget()
        self.Date.setCalendarPopup(True)
        self.Date.setCalendarWidget(cal)
        self.Date.setMaximumDate(QDate.currentDate())
        self.Date.setDate(cal.selectedDate())
        self.OrderID.addItems(list(map(str,range(1,10))))
        self.TradeID.addItems(list(map(str,range(1,10))))
        self.BuySell.addItems(['Buy','Sell'])
        self.OpenClose.addItems(['Open','Close'])

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
        gridEdit.addWidget(labelCommission,0,10)
        gridEdit.addWidget(self.Commission,0,11)
        gridEdit.addWidget(labelTime,1,0)
        gridEdit.addWidget(self.Time,1,1)
        gridEdit.addWidget(labelSymbolName,1,2)
        gridEdit.addWidget(self.SymbolName,1,3)
        gridEdit.addWidget(labelTradeID,1,4)
        gridEdit.addWidget(self.TradeID,1,5)
        gridEdit.addWidget(labelOpenClose,1,6)
        gridEdit.addWidget(self.OpenClose,1,7)
        gridEdit.addWidget(labelTradeAmt,1,8)
        gridEdit.addWidget(self.TradeAmt,1,9)
        gridEdit.addWidget(labelSettleAmt,1,10)
        gridEdit.addWidget(self.SettleAmt,1,11)

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

        layout.addLayout(gridEdit)

        hlayout = QHBoxLayout()
        btnInsert = QPushButton('INSERT')
        btnInsert.clicked.connect(self.insertTrade)
        hlayout.addStretch(8)
        hlayout.addWidget(btnInsert)

        layout.addLayout(hlayout)

    def insertTrade(self):
        print('insert trade function')
