import sqlite3
import pandas as pd

def get_trans(dt, account):
    db = sqlite3.connect('AMS.db')
    query = """
            SELECT *
            FROM Order_Table
            WHERE AccountID in {} and Date <= '{}' """.format(str(account),dt)
    df_trans = pd.read_sql(query, con = db)
    
    return df_trans


def get_holding(date, df_trans):
    #取股票持仓
    df_trans_stock = df_trans[~df_trans['Symbol_Code'].isin(tuple_cur)]
    df_group_stock = df_trans_stock.loc[:, ['Symbol_Code', 'Symbol_Name', 'Cur', 'Quantity']]
    df_group_stock = df_group_stock.groupby(['Symbol_Code', 'Symbol_Name', 'Cur']).sum()
    df_group_stock = df_group_stock.reset_index()
    df_group_stock.drop(index=(df_group_stock.loc[(df_group_stock['Quantity']==0)].index), inplace=True)
    df_group_stock['Date'] = date
    
    #取持仓股票成本
    df_trans_buy = df_trans_stock[df_trans_stock['Quantity']>=0]
    df_group_stock['Cost_Amt'] = float(0)
    for i in df_group_stock.index.tolist():
        code = df_group_stock.loc[i,'Symbol_Code']
        hold_quantity = df_group_stock.loc[i,'Quantity']
        if hold_quantity > 0:
            cost_amt = get_cost(code, hold_quantity, df_trans_buy)
            df_group_stock.at[i, 'Cost_Amt'] = cost_amt

    #取现金持仓
    df_trans_cur = df_trans
    df_group_cur = df_trans_cur.loc[:, ['Cur', 'Settle_Amt']]
    df_group_cur = df_group_cur.groupby(['Cur']).sum()
    df_group_cur = df_group_cur.reset_index()
    df_group_cur['Date'] = date
    df_group_cur['Symbol_Code'] = df_group_cur['Cur']
    df_group_cur['Symbol_Name'] = df_group_cur['Cur']
    df_group_cur.rename(columns={'Settle_Amt':'Quantity'}, inplace=True)
    df_group_cur['Cost_Amt'] = df_group_cur['Quantity']
    
    #合并资金及股票持仓
    df_hold = df_group_stock.append(df_group_cur, ignore_index=True)
    df_hold = df_hold.round(4)
    df_hold.sort_values(by = ['Cur', 'Symbol_Code'],axis = 0,ascending = True, inplace=True)
    
    #获取行业信息
    df_sector = pd.DataFrame(pd.read_csv('data/Sector.csv',header=0))
    df_hold = pd.merge(df_hold, df_sector, how='left')
    df_hold = df_hold[['Date','Symbol_Code', 'Symbol_Name', 'Sector', 'Cur', 'Quantity', 'Cost_Amt']]
    
    return df_hold