import sqlite3
import pandas as pd

def get_hold(dt, account):
    db = sqlite3.connect('AMS.db')

    query = "SELECT SymbolCode, SymbolName, AssetClass,Sector FROM Symbol_Table"
    df_symbol = pd.read_sql(query, con=db)

    query = """
            SELECT *
            FROM Order_Table
            WHERE AccountID in {} and Date <= '{}' """.format(str(account),dt)
    df_trans = pd.read_sql(query, con = db)
    df_trans = pd.merge(df_trans, df_symbol, on='SymbolCode', how='left')

    df_stock = df_trans[~df_trans['AssetClass'].isin(['CASH'])]
    df_stock = df_stock[['SymbolCode','Qty']]
    df_stock_sum = df_stock.groupby(['SymbolCode']).sum()

    df_cur = df_trans[['CurSettle', 'SettleAmt']]
    df_cur_sum = df_cur.groupby(['CurSettle']).sum()
    df_cur_sum.rename(columns={'SettleAmt':'Qty'}, inplace=True)
    df_cur_sum.index.name = 'SymbolCode'

    df_hold = df_stock_sum.append(df_cur_sum)
    df_hold = df_hold[~df_hold['Qty'].isin([0])]    #去除报告日持仓为0的标的
    df_hold = pd.merge(df_hold, df_symbol, on='SymbolCode', how='left') #补充名称和行业
    df_hold.reset_index(inplace=True)
    
    return df_hold
