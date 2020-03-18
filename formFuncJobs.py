# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
import pandas as pd
import sqlite3
import datetime


class Ui_Jobs(object):
    def initUI(self, Ui_Jobs):
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.initHoldingCal()
        self.mainLayout.addStretch()

        self.check_status()

    def Cal_Holding(self):
        if self.HoldingStatus.text() == '':
            self.check_status()
        else:
            self.HoldingStatus.setText('')

    def max_holding(self):
        db = sqlite3.connect('AMS.db')
        query = "select max(Date) as 'Date' from Holding_Table"
        df = pd.read_sql(query, con=db)
        dayMax = datetime.datetime.strptime(df.loc[0, 'Date'], "%Y-%m-%d").date()

        return dayMax

    def check_status(self):
        dayMax = self.max_holding()
        strStatus = 'Max Holding Date: ' + datetime.datetime.strftime(dayMax, '%Y-%m-%d')
        self.HoldingStatus.setText(strStatus)

        timeDelta = (QtCore.QDate.currentDate().toPyDate() - dayMax).days
        if timeDelta > 1:
            self.HoldingStatus.setStyleSheet("color:red;")
        else:
            self.HoldingStatus.setStyleSheet("color:black;")

    def initHoldingCal(self):
        groupHolding = QtWidgets.QGroupBox()
        groupHoldingLayout = QtWidgets.QVBoxLayout()
        groupHolding.setLayout(groupHoldingLayout)

        layoutHoldingTitle = QtWidgets.QHBoxLayout()
        labelHoldingTitle = QtWidgets.QLabel('Holding Calculation')
        labelHoldingTitle.setFont(QtGui.QFont("Timers", 14, QtGui.QFont.Bold))
        labelHoldingTitle.setStyleSheet("border: 1px solid gray; background-color: white")
        labelHoldingTitle.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        layoutHoldingTitle.addWidget(labelHoldingTitle)

        dayMax = self.max_holding()
        dayStart = dayMax + datetime.timedelta(days=1)

        labelStart = QtWidgets.QLabel("Date Start")
        labelEnd = QtWidgets.QLabel("Date End")
        self.DateStart = QtWidgets.QDateEdit(dayStart)
        self.DateEnd = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.DateStart.setCalendarPopup(True)
        self.DateEnd.setCalendarPopup(True)
        self.DateStart.setMaximumDate(QtCore.QDate.currentDate())
        self.DateEnd.setMaximumDate(QtCore.QDate.currentDate())
        self.HoldingStatus = QtWidgets.QLabel('')
        self.btnCalHold = QtWidgets.QPushButton('Cal Holding')
        self.btnCalHold.clicked.connect(self.Cal_Holding)

        layoutHolding = QtWidgets.QHBoxLayout()
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

        self.mainLayout.addWidget(groupHolding)
