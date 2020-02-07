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
    df.dropna(axis = 0, inplace=True)   #去掉空值
    df=df[~df[columnName].isin([''])]   #去掉空字符串
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

class MySymbol:
    def __init__(self, symbolcode):
        db = sqlite3.connect('AMS.db')
        query = "select * from Symbol_Table where SymbolCode='{}'".format(symbolcode)
        df = pd.read_sql(query, con = db)

        if not df.empty:
            self.Code = df.iloc[0]['SymbolCode']
            self.Name = df.iloc[0]['SymbolName']
            self.Exchange = df.iloc[0]['Exchange']
            self.Underly = df.iloc[0]['Underlying']
            self.AssetClass = df.iloc[0]['AssetClass']
            self.CurTrade = df.iloc[0]['CurTrade']
            self.curSettle = df.iloc[0]['CurSettle']
            self.Multiplier = df.iloc[0]['Multiplier']
            self.Commission = df.iloc[0]['Commission']
            self.Sector = df.iloc[0]['Sector']
            self.Region = df.iloc[0]['Region']
        else:
            self.Code = ''
            self.Name = ''
            self.Exchange = ''
            self.Underly = ''
            self.AssetClass = ''
            self.CurTrade = ''
            self.curSettle = ''
            self.Multiplier = ''
            self.Commission = 0  
            self.Sector = ''
            self.Region = ''    