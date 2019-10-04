# -*- coding: utf-8 -*-
 
# Form implementation generated from reading ui file 'first.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
 
from PyQt5 import QtCore, QtGui, QtWidgets
from DataFrameModel import PandasModel
import pandas as pd
 
 
class Ui_First(object):
    def initUI(self, Ui_First):
        #self.setStyleSheet("border-style:solid;border-width:2;border-color:red;")

        self.rptDate = ''
        self.rptAcct = ''

        vLayout = QtWidgets.QVBoxLayout(self)
        hLayout = QtWidgets.QHBoxLayout()
        hLayout2 = QtWidgets.QHBoxLayout()

        lblDate = QtWidgets.QLabel(self)
        lblDate.setText('Date')
        hLayout.addWidget(lblDate)

        cal = QtWidgets.QCalendarWidget(self)
        dtEdit = QtWidgets.QDateEdit(QtCore.QDate.currentDate(), self)
        dtEdit.setCalendarPopup(True)
        dtEdit.setCalendarWidget(cal)
        dtEdit.setMaximumDate(QtCore.QDate.currentDate())
        dtEdit.setDate(cal.selectedDate())
        dtEdit.dateChanged.connect(self.saveDate)
        dtEdit.setFixedWidth(120)
        hLayout.addWidget(dtEdit)

        lblAcct = QtWidgets.QLabel(self)
        lblAcct.setText('Account')
        hLayout.addWidget(lblAcct)

        comboAcct = QtWidgets.QComboBox()
        comboAcct.setEditable(True)
        comboAcct.lineEdit().setAlignment(QtCore.Qt.AlignLeft)
        #comboAcct.lineEdit().setStyleSheet("text-align:center; vertical-align: middle;")
        comboAcct.addItems(['Citic', 'CMB', 'ALL'])
        comboAcct.currentTextChanged.connect(self.saveAcct)
        comboAcct.setFixedWidth(80)
        #comboAcct.setStyleSheet("text-align:center; vertical-align: middle;")
        comboAcct.setStyleSheet("background-color:white;")
        hLayout.addWidget(comboAcct)

        hLayout.addStretch(10)

        btnReport = QtWidgets.QPushButton("RUN REPORT", self)
        btnReport.clicked.connect(self.loadReport)
        hLayout.addWidget(btnReport)

        hLayout.addStretch(1)

        widget = QtWidgets.QWidget()
        widget.setLayout(hLayout)
        widget.setFixedHeight(50)

        vLayout.addWidget(widget)

        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout2.setContentsMargins(0, 0, 0, 0)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(0)

        self.tblHold = QtWidgets.QTableView(self)
        hLayout2.addWidget(self.tblHold)

        vLayout.addLayout(hLayout2)

        self.rptDate = dtEdit.date().toString('yyyyMMdd')
        self.rptAcct = comboAcct.currentText()

    def loadReport(self):
        df = pd.read_excel('A_Shares.xlsx',sheet_name='Trans')
        model = PandasModel(df)
        self.tblHold.setModel(model)
        self.tblHold.setSortingEnabled(True)
        self.tblHold.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:lightblue;color: black;padding-left: 4px;border: 1px solid #6c6c6c;font: bold;}")

    def saveAcct(self, str):
        self.rptAcct = str

    def saveDate(self, date):
        self.rptDate = date.toString('yyyyMMdd')