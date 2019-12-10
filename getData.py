import sqlite3
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time

def get_list(tableName, columnName):
    db = sqlite3.connect('AMS.db')
    query = "select distinct {} from {} order by {}".format(columnName, tableName, columnName)
    df = pd.read_sql(query, con = db)
    listValue = list(df[columnName])

    return listValue

def insert_record(tableName, dictData):
    columnName = ','.join(dictData.keys())
    listData = dictData.values()
    #给str类型加上单引号，然后将List转为字符串，转的过程中需要将数字转为字符串
    columnData = list(map(lambda x: "'%s'"%x if type(x).__name__=='str' else x, listData))
    columnData = ','.join('%s' %id for id in columnData)

    db = db = sqlite3.connect('AMS.db')
    cur = db.cursor()
    query = "INSERT INTO {} ({}) VALUES ({})".format(tableName, columnName, columnData)
    cur.execute(query)
    db.commit()

def load_table(tableView, model, df):
    #db = sqlite3.connect('AMS.db')
    #query = "select * from " + tableName + condition
    #df = pd.read_sql(query, con = db)
    rowCount = df.shape[0]
    columnCount = df.shape[1]
    model.setRowCount = rowCount
    model.setColumnCount = columnCount + 1  #添加一列作为操作列，默认不显示
    headName = list(df)
    headName.append('Action')
    model.setHorizontalHeaderLabels(headName)
    for row in range(rowCount):
        for column in range(columnCount):
            item = QStandardItem()
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            itemValue = df.iloc[row,column]
            if type(itemValue).__name__ == 'int64':
                itemValue = int(itemValue)
            if type(itemValue).__name__ == 'float64':
                itemValue = float(itemValue)
                if itemValue < 0:
                    item.setForeground(QBrush(QColor(255, 0, 0)))
            item.setData(itemValue, Qt.DisplayRole)
            model.setItem(row, column, item)

    tableView.setModel(model)

    tableView.setColumnHidden(columnCount, True)    #默认隐藏action列
    tableView.verticalHeader().setHidden(True)      #隐藏行号
    tableView.setSortingEnabled(True)
    #水平方向标签拓展剩下的窗口部分，填满表格
    #tableWidget.horizontalHeader().setStretchLastSection(True)
    #水平方向，表格大小拓展到适当的尺寸      
    tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    tableView.resizeColumnsToContents()
    tableView.horizontalHeader().setStyleSheet("QHeaderView::section {background-color:lightblue;color: black;padding-left: 4px;border: 1px solid #6c6c6c;font: bold;}")
    