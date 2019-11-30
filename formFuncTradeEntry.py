# -*- coding: utf-8 -*-

import sys 
import sqlite3
import pandas.io.sql as sql
import pandas as pd
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
        db = sqlite3.connect('AMS.db')
        query = "select * from Holding_Table"
        df = pd.read_sql(query, con = db)
        model = PandasModel(df)
        self.tableHold.setModel(model)
        self.tableHold.verticalHeader().setHidden(True)
        self.tableHold.setSortingEnabled(True)
        self.tableHold.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableHold.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:lightblue;color: black;padding-left: 4px;border: 1px solid #6c6c6c;font: bold;}")
