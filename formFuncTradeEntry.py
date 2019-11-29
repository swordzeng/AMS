# -*- coding: utf-8 -*-

import sys 
import sqlite3
import pandas.io.sql as sql
from pandas import Series,DataFrame
from DataFrameModel import PandasModel
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_funcTradeEntry(object):
    def initUI(self, Ui_funcTradeEntry):
        mainLayout = QtWidgets.QVBoxLayout()
        
        btnLoadData = QtWidgets.QPushButton("Load Data")
        btnLoadData.clicked.connect(self.load_data)

        self.tableHold = QtWidgets.QTableView() 

        mainLayout.addWidget(btnLoadData)
        mainLayout.addWidget(self.tableHold)
        self.setLayout(mainLayout)

    def load_data(self):
        print('load data')
        con = sqlite3.connect('AMS.db')
        query = "select * from Holding_Table"
        cur = con.execute(query)
        rows = cur.fetchall()
        df = DataFrame(rows)
        model = PandasModel(df)
        self.tableHold.setModel(model)
        self.tableHold.setSortingEnabled(True)
        self.tableHold.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:lightblue;color: black;padding-left: 4px;border: 1px solid #6c6c6c;font: bold;}")
 