import sqlite3
import pandas as pd
import datetime

DB_PATH = 'AMS.db'

def table_append(df, table):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(table, con=conn, if_exists='append', index=False)
    conn.close()

def table_delete(table, column, value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = "delete from {} where {} = '{}'".format(table, column, value)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def update_latest_date(table, setColumn, setValue, conColumn, conValue):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    sql = "update {} set {} = '{}' where {}='{}'".format(table, setColumn, setValue, conColumn, conValue)
    cursor.execute(sql)
    conn.commit()
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

    table = 'Holding_Table'

    if acct=='':
        acctCondition = ''
    elif type(acct) is str:
        acctCondition = " AND AccountID = '{}' ".format(acct)
    else:
        acctCondition = " AND AccountID in {} ".format(str(tuple(acct)))

    if dt == '':
        dt = get_latest_date(table)

    dt = dt if type(dt) is str else dt.strftime('%Y-%m-%d')

    query = "SELECT * FROM {} WHERE Date ='{}'".format(table, dt) + acctCondition

    conn = sqlite3.connect(DB_PATH)
    dfHold = pd.read_sql(query, conn)
    conn.close()

    return dfHold

def get_trans(acct='', dtStart='', dtEnd=''):
    if dtStart =='':
        dtStart = '2019-12-31'

    if dtEnd =='':
        dtEnd = datetime.datetime.now().strftime('%Y-%m-%d')

    query = """SELECT Order_Table.* FROM Order_Table 
        INNER JOIN Account_Table 
        ON Order_Table.AccountID = Account_Table.AccountID
        WHERE Date >'{}' and Date <='{}' """.format(dtStart, dtEnd)

    conn = sqlite3.connect(DB_PATH)
    df_trans = pd.read_sql(query, con = conn)

    return df_trans

def get_history_price(symbol='',dtStart='',dtEnd='', type='equity'):

    dtStart = '2019-12-31' if dtStart == '' else dtStart
    dtEnd = datetime.datetime.strptime(date, '%Y-%m-%d') if dtEnd =='' else dtEnd

    '''
    if type(dtStart) is str:
        dtStart = dtStart 
    else:
        dtStart = dtStart.strftime('%Y-%m-%d')

    dateEnd = dtEnd if type(dtEnd) is str else dtEnd.strftime('%Y-%m-%d')
    '''
    
    if symbol=='':
        symbolCondition = ''
    elif type(symbol) is str:
        symbolCondition = " AND SymbolCode = '{}' ".format(symbol)
    else:
        symbolCondition = " AND SymbolCode in {} ".format(str(tuple(symbol)))

    table =  'Close_Price' if type == 'equity' else 'Exchange_Rate'

    query = """SELECT * FROM {}
        WHERE Date >'{}' and Date <='{}' """.format(table, dtStart, dtEnd) + symbolCondition

    conn = sqlite3.connect(DB_PATH)
    closePrice = pd.read_sql(query, con = conn)

    return closePrice

def get_symbol_for_close_price(dtStart=''):
    dfHold = get_holding()
    if dtStart=='':
        dtStart = get_latest_date("Holding_Table")
    dfTrans = get_trans(dtStart=dtStart)
    listHold = list(dfHold['SymbolCode'])
    listTrans = list(dfTrans['SymbolCode'])
    listHold.extend(listTrans)
    listSymbol = list(set(listHold))  #去重
    for cur in ['CNY','HKD','USD']:
        if cur in listSymbol:
            listSymbol.remove(cur)

    return listSymbol