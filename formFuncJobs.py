# -*- coding: utf-8 -*-
 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pandas as pd
import sqlite3

class Ui_Jobs(object):
    def initUI(self, Ui_Jobs):
        self.initEdit()

    def Cal_Holding(self):
        if self.HoldingStatus.text() == '':
            self.HoldingStatus.setText('Everything is up to date .......................')
        else:
            self.HoldingStatus.setText('')

    def check_status(self):
        db = sqlite3.connect('AMS.db')
        query = "select max(Date) as 'Date' from Holding_Table"
        df = pd.read_sql(query, con = db)
        print(df.loc[0,'Date'])

    def initEdit(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        groupHolding = QGroupBox()
        groupHoldingLayout = QVBoxLayout()
        groupHolding.setLayout(groupHoldingLayout)

        layoutHoldingTitle = QHBoxLayout()
        labelHoldingTitle = QLabel('Holding Calculation')
        labelHoldingTitle.setFont(QFont("Timers", 14, QFont.Bold))
        labelHoldingTitle.setStyleSheet("border: 1px solid gray; background-color: white")
        labelHoldingTitle.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        layoutHoldingTitle.addWidget(labelHoldingTitle)

        labelStart = QLabel("Date Start")
        labelEnd = QLabel("Date End")
        self.DateStart = QDateEdit()
        self.DateEnd = QDateEdit(QDate.currentDate())
        self.HoldingStatus = QLabel('')
        self.btnCalHold = QPushButton('Cal Holding')
        self.btnCalHold.clicked.connect(self.Cal_Holding)

        layoutHolding = QHBoxLayout()
        layoutHolding.addWidget(labelStart)
        layoutHolding.addWidget(self.DateStart)
        layoutHolding.addWidget(labelEnd)
        layoutHolding.addWidget(self.DateEnd)
        layoutHolding.addStretch()
        layoutHolding.addWidget(self.HoldingStatus)
        layoutHolding.addWidget(self.btnCalHold)

        groupHoldingLayout.addLayout(layoutHoldingTitle)
        groupHoldingLayout.addLayout(layoutHolding)
        
        groupHolding.setStyleSheet('''
            QGroupBox{border: 1px solid gray;}
            QDateEdit{border: 1px solid gray;}
            QLabel{border: none;}
            ''') 

        groupHoldingLayout.setSpacing(8)
        groupHoldingLayout.setContentsMargins(0, 0, 0, 0)
        layoutHoldingTitle.setContentsMargins(10, 10, 10, 0)
        layoutHolding.setContentsMargins(10, 0, 10, 10)

        mainLayout.addWidget(groupHolding)
        mainLayout.addStretch()

        self.check_status()
        


