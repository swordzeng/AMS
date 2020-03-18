# -*- coding: utf-8 -*-

# import sys
import sqlite3
import pandas as pd
from PyQt5 import QtCore, QtWidgets, QtGui
import getData
import DataFrameModel as dfm


class Ui_funcSystemMgt(object):
    def initUI(self, Ui_funcSystemMgt):

        self.db = sqlite3.connect('AMS.db')
        self.tableView = QtWidgets.QTableView()

        mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(mainLayout)

        tabWidget = QtWidgets.QTabWidget()
        mainLayout.addWidget(tabWidget)

        self.tabSymbol = QtWidgets.QWidget()
        self.tabAcct = QtWidgets.QWidget()

        tabWidget.addTab(self.tabSymbol, "Symbol Management")
        tabWidget.addTab(self.tabAcct, " Account Management")

        self.tabSymbolUI()
        self.tabAcctUI()

    def tabSymbolUI(self):
        layout = QtWidgets.QVBoxLayout()
        self.tabSymbol.setLayout(layout)

        labelSymbolCode = QtWidgets.QLabel('Symbol Code')
        labelSymbolName = QtWidgets.QLabel('Symbol Name')
        labelUnderly = QtWidgets.QLabel('Underlying')
        labelAsset = QtWidgets.QLabel('Asset Class')
        labelMarket = QtWidgets.QLabel('Exchange')
        labelCur = QtWidgets.QLabel('Currency')
        labelMultiplier = QtWidgets.QLabel('Multiplier')
        labelCommission = QtWidgets.QLabel('Commission')
        labelSector = QtWidgets.QLabel('Sector')
        labelRegion = QtWidgets.QLabel('Region')

        self.editSymbolCode = QtWidgets.QLineEdit()
        self.editSymbolName = QtWidgets.QLineEdit()
        self.editUnderly = QtWidgets.QComboBox()
        self.editAsset = QtWidgets.QComboBox()
        self.editMarket = QtWidgets.QComboBox()
        self.editCur = QtWidgets.QComboBox()
        self.editMultiplier = QtWidgets.QLineEdit('1')
        self.editCommission = QtWidgets.QLineEdit('0')
        self.editSector = QtWidgets.QComboBox()
        self.editRegion = QtWidgets.QComboBox()

        self.editUnderly.addItems(['', 'MHI', 'MCH'])
        self.editAsset.addItems(['EQUITY', 'BOND', 'DERIVATIVES', 'CASH'])
        self.editMarket.addItems(['', 'SSE', 'SZSE', 'HKEX'])
        self.editCur.addItems(['CNY', 'HKD', 'USD'])
        self.editRegion.addItems(['', 'CN', 'HK'])

        self.editSector.setEditable(True)
        codeList = getData.get_list('Symbol_Table', 'Sector')
        codeList.insert(0, '')
        codeList = [str(i) for i in codeList]
        self.editSector.addItems(codeList)

        # layoutInput = QHBoxLayout()
        gridInput = QtWidgets.QGridLayout()
        gridInput.addWidget(labelSymbolCode, 0, 0)
        gridInput.addWidget(self.editSymbolCode, 0, 1)
        gridInput.addWidget(labelSymbolName, 1, 0)
        gridInput.addWidget(self.editSymbolName, 1, 1)
        gridInput.addWidget(labelUnderly, 0, 2)
        gridInput.addWidget(self.editUnderly, 0, 3)
        gridInput.addWidget(labelAsset, 1, 2)
        gridInput.addWidget(self.editAsset, 1, 3)
        gridInput.addWidget(labelMarket, 0, 4)
        gridInput.addWidget(self.editMarket, 0, 5)
        gridInput.addWidget(labelCur, 1, 4)
        gridInput.addWidget(self.editCur, 1, 5)
        gridInput.addWidget(labelMultiplier, 0, 6)
        gridInput.addWidget(self.editMultiplier, 0, 7)
        gridInput.addWidget(labelCommission, 1, 6)
        gridInput.addWidget(self.editCommission, 1, 7)
        gridInput.addWidget(labelSector, 0, 8)
        gridInput.addWidget(self.editSector, 0, 9)
        gridInput.addWidget(labelRegion, 1, 8)
        gridInput.addWidget(self.editRegion, 1, 9)

        btnClear = QtWidgets.QPushButton('Clear')
        btnClear.clicked.connect(self.clearSymbol)
        gridInput.addWidget(btnClear, 0, 10)

        btnAdd = QtWidgets.QPushButton('Insert')
        btnAdd.clicked.connect(self.insertSymbol)
        gridInput.addWidget(btnAdd, 1, 10)

        gridInput.setColumnStretch(0, 2)
        gridInput.setColumnStretch(1, 3)
        gridInput.setColumnStretch(2, 2)
        gridInput.setColumnStretch(3, 3)
        gridInput.setColumnStretch(4, 2)
        gridInput.setColumnStretch(5, 3)
        gridInput.setColumnStretch(6, 2)
        gridInput.setColumnStretch(7, 3)
        gridInput.setColumnStretch(8, 2)
        gridInput.setColumnStretch(9, 3)
        gridInput.setColumnStretch(10, 3)

        gridInput.setVerticalSpacing(3)

        widgetInput = QtWidgets.QWidget()
        widgetInput.setLayout(gridInput)
        widgetInput.setStyleSheet('''
            QWidget{border: 1px solid gray;}
            QComboBox{border: 1px solid gray;}
            QLineEdit{border: 1px solid gray;}
            QPushButton{border: 1px solid gray;}
            QLabel{border: none;}
            ''')
        layout.addWidget(widgetInput)
        layout.addWidget(self.tableView)

        self.fill_data()

    def fill_data(self):
        strTable = "Symbol_Table"
        query = "SELECT * FROM Symbol_Table ORDER BY AssetClass, Region, Exchange, SymbolCode"
        model = QtGui.QStandardItemModel()
        df = pd.read_sql(query, con=self.db)
        dfm.load_table(self.tableView, model, df)
        self.addActionColumn(self.tableView, model, strTable)
        self.tableView.sortByColumn(2, QtCore.Qt.DescendingOrder)

    def tabAcctUI(self):
        layout = QtWidgets.QFormLayout()
        sex = QtWidgets.QHBoxLayout()
        sex.addWidget(QtWidgets.QRadioButton("男"))
        sex.addWidget(QtWidgets.QRadioButton("女"))
        layout.addRow(QtWidgets.QLabel("性别"), sex)
        layout.addRow("生日", QtWidgets.QLineEdit())
        self.tabAcct.setLayout(layout)

    def insertSymbol(self):
        if self.editSymbolCode.text().strip() != '':
            query = "SELECT * FROM Symbol_Table WHERE SymbolCode = '" + self.editSymbolCode.text().strip() + "'"
            df = pd.read_sql(query, con=self.db)

            if df.empty:
                dictSymbol = {}
                dictSymbol['SymbolCode'] = self.editSymbolCode.text().strip()
                dictSymbol['SymbolName'] = self.editSymbolName.text().strip()
                dictSymbol['Exchange'] = self.editMarket.currentText()
                dictSymbol['Underlying'] = self.editUnderly.currentText()
                dictSymbol['AssetClass'] = self.editAsset.currentText()
                dictSymbol['CurTrade'] = self.editCur.currentText()
                dictSymbol['CurSettle'] = self.editCur.currentText()
                dictSymbol['Multiplier'] = self.editMultiplier.text().strip()
                dictSymbol['Commission'] = self.editCommission.text().strip()
                dictSymbol['Sector'] = self.editSector.currentText().strip()
                dictSymbol['Region'] = self.editRegion.currentText().strip()
                getData.insert_record('Symbol_Table', dictSymbol)
                self.fill_data()
                QtWidgets.QMessageBox.information(self, 'info', 'Symbol created!', QtWidgets.QMessageBox.Close)
            else:
                QtWidgets.QMessageBox.warning(self, 'warning', 'Symbol already exists!', QtWidgets.QMessageBox.Close)

    def copySymbol(self, table):
        code = self.sender()
        symbolCode = str(code.property('code'))
        symbol = getData.MySymbol(symbolCode)

        self.editSymbolCode.setText(symbol.Code)
        self.editSymbolName.setText(symbol.Name)
        self.editMarket.setCurrentText(symbol.Exchange)
        self.editUnderly.setCurrentText(symbol.Underly)
        self.editAsset.setCurrentText(symbol.AssetClass)
        self.editCur.setCurrentText(symbol.CurTrade)
        self.editMultiplier.setText(str(symbol.Multiplier))
        self.editCommission.setText(str(symbol.Commission))
        self.editSector.setCurrentText(symbol.Sector)
        self.editRegion.setCurrentText(symbol.Region)

    def clearSymbol(self, table):
        self.editSymbolCode.setText('')
        self.editSymbolName.setText('')
        self.editMarket.setCurrentText('')
        self.editUnderly.setCurrentText('')
        self.editAsset.setCurrentText('')
        self.editCur.setCurrentText('')
        self.editMultiplier.setText('')
        self.editCommission.setText('')
        self.editSector.setCurrentText('')
        self.editRegion.setCurrentText('')

    def deleteSymbol(self, table):
        btn = self.sender()
        symbol = str(btn.property('code'))
        reply = QtWidgets.QMessageBox.question(self, 'Delete', 'Sure to delete symbol :' + symbol + '?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            query = "DELETE FROM " + table + " WHERE SymbolCode = '" + symbol + "'"
            print(query)
            cursor = self.db.cursor()
            cursor.execute(query)
            self.db.commit()
            cursor.close()

        self.fill_data()

    def addActionColumn(self, tableView, model, tableName):
        columnPos = model.columnCount() - 1
        tableView.setColumnHidden(columnPos, False)

        rowCount = model.rowCount()
        for row in range(rowCount):
            symbolCode = model.itemData(model.index(row, 0))[0]  # 返回dict类型

            hlayout = QtWidgets.QHBoxLayout()
            groupAction = QtWidgets.QGroupBox()

            iconDelete = QtGui.QIcon()
            iconDelete.addFile('logo/delete1.png')
            btnDelete = QtWidgets.QPushButton('')
            btnDelete.setIcon(iconDelete)
            btnDelete.clicked.connect(lambda: self.deleteSymbol(tableName))
            btnDelete.setProperty("code", symbolCode)

            iconCopy = QtGui.QIcon()
            iconCopy.addFile('logo/edit1.png')
            btnCopy = QtWidgets.QPushButton('')
            btnCopy.setIcon(iconCopy)
            btnCopy.clicked.connect(lambda: self.copySymbol(tableName))
            btnCopy.setProperty("code", symbolCode)

            hlayout.addWidget(btnDelete)
            hlayout.addWidget(btnCopy)
            hlayout.setContentsMargins(0, 0, 0, 0)
            btnDelete.setFixedWidth(40)
            btnCopy.setFixedWidth(40)
            btnDelete.setFixedHeight(30)
            btnCopy.setFixedHeight(30)
            groupAction.setLayout(hlayout)

            tableView.setIndexWidget(model.index(row, columnPos), groupAction)
