import sqlite3
import pandas as pd

DB_PATH = 'AMS.db'

def table_append(df, table):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(table, con=conn, if_exists='append', index=False)
    conn.close()

def get_latest_date(table, column='', value=''):
    conn = sqlite3.connect(DB_PATH)

    query = "SELECT MAX(Date) AS Max_Date FROM {} ".format(table)
    if column=='' or value=='':
        condition = ''  
    else:
        condition = " WHERE {} = '{}'".format(column, value)

    df_max_date = pd.read_sql(query+condition, con=conn)
    conn.close()

    max_date = '2019-12-31' if df_max_date.iat[0,0] == None else  df_max_date.iat[0,0]

    return max_date

def get_holding(acct='', dt=''):

    table = 'Holding_Table_Test'

    if acct=='':
        acctCondition = ''
    elif str(acct).find(',') >= 0:
        acctCondition = " AND AccountID in {} ".format(acct)
    else:
        acctCondition = " AND AccountID = '{}' ".format(acct)

    dt = get_latest_date(table) if dt=='' else dt

    query = "SELECT * FROM {} WHERE Date ='{}'".format(table, dt) + acctCondition

    conn = sqlite3.connect(DB_PATH)
    dfHold = pd.read_sql(query, conn)
    conn.close()

    return dfHold

def get_trans(acct='', dtStart='', dtEnd=''):
    if dtStart =='':
        dtStart = '2019-12-31'

    query = """SELECT * FROM Order_Table 
        INNER JOIN Account_Table 
        ON Order_Table.AccountID = Account_Table.AccountID
        WHERE Date >='{}'""".format(dtStart)

    conn = sqlite3.connect(DB_PATH)
    df_trans = pd.read_sql(query, con = conn)

    return df_trans

def get_symbol_for_close_price():
    dfHold = get_holding()
    dtStart = get_latest_date("Holding_Table_Test")
    dfTrans = get_trans(dtStart=dtStart)
    listHold = list(dfHold['SymbolCode'])
    listTrans = list(dfTrans['SymbolCode'])
    listHold.extend(listTrans)
    listSymbol = list(set(listHold))  #去重
    for cur in ['CNY','HKD','USD']:
        if cur in listSymbol:
            listSymbol.remove(cur)

    return listSymbol