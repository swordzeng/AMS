import sqlite3
import requests
import pandas as pd

def get_hold(dt, account):
    db = sqlite3.connect('AMS.db')

    query = "SELECT SymbolCode, SymbolName, Market, AssetClass,Sector,CurSettle AS Cur FROM Symbol_Table"
    df_symbol = pd.read_sql(query, con=db)

    if account.find(',') >=0:
        acctCondition = " in {} ".format(account)
    else:
        acctCondition = " = '{}' ".format(account)

    query = """
            SELECT *
            FROM Order_Table
            WHERE AccountID {} and Date <= '{}' """.format(acctCondition,dt)

    df_trans = pd.read_sql(query, con = db)
    df_trans = pd.merge(df_trans, df_symbol, on='SymbolCode', how='left')

    #取股票持仓数量
    df_stock = df_trans[~df_trans['AssetClass'].isin(['CASH'])]
    df_stock_sum = df_stock[['SymbolCode','Qty']]
    df_stock_sum = df_stock_sum.groupby(['SymbolCode']).sum()

    #计算股票持仓成本金额
    df_stock_sum['CostAmt'] = 0.0
    df_trans_buy = df_stock[df_stock['Qty']>=0]
    for code in df_stock_sum.index.tolist():
        Qty = df_stock_sum.loc[code,'Qty']
        if Qty > 0:
            cost_amt = get_cost(code, Qty, df_trans_buy)
            df_stock_sum.loc[code, 'CostAmt'] = cost_amt

    #取现金持仓数量
    df_cur = df_trans[['CurSettle', 'SettleAmt']]
    df_cur_sum = df_cur.groupby(['CurSettle']).sum()
    df_cur_sum.rename(columns={'SettleAmt':'Qty'}, inplace=True)
    df_cur_sum.index.name = 'SymbolCode'
    df_cur_sum['CostAmt'] = df_cur_sum['Qty']

    #合并股票持仓和现金持仓
    df_hold = df_stock_sum.append(df_cur_sum)
    df_hold = df_hold[~df_hold['Qty'].isin([0])]    #去除报告日持仓为0的标的
    df_hold = pd.merge(df_hold, df_symbol, on='SymbolCode', how='left') #补充名称和行业
    
    df_hold['Date'] = dt

    df_hold = get_realtime_price(df_hold)
    df_hold = cal_factor(df_hold)

    df_hold = df_hold[['SymbolCode','SymbolName','Cur','Qty','CostPrice','Price','MV','PL','Ratio']]
    return df_hold

def get_cost(code, qt, df):
    df_code = df[df['SymbolCode'].isin([code])]
    df_code = df_code.sort_values('Date', ascending=False)
    
    #从当前持仓日往前取买入即分红送股数据获取成本金额
    #直至当前持仓数量扣除完整为止
    amt_cost = 0
    for i in df_code.index.tolist():
        if qt <= 0:
            break
        else:
            qt_trans = df_code.loc[i,'Qty']
            amt_trans =  df_code.loc[i,'SettleAmt']
            amt_cost = amt_cost + (amt_trans * (qt/qt_trans if qt_trans>qt else 1)) * -1
            qt = qt - qt_trans
    
    return amt_cost

def get_realtime_price(df):
    df['Price'] = 0.0

    for index, row in df.iterrows():
        if row['AssetClass'] == 'CASH':
            df.loc[index, 'Price'] = 1.0
        elif row['AssetClass'] == 'EQUITY':
            market = df.loc[index,'Market']
            code = market.lower() + df.loc[index,'SymbolCode'].split('.')[0]
            url = 'http://hq.sinajs.cn/?format=text&list={}'.format(code)
            price_text = requests.get(url).text
            price_list = price_text.split(',')
            if market =='HK':
                price = price_list[5]
            else:
                price = price_list[3]
            df.loc[index, 'Price'] = float(price)

    return df

def cal_factor(df):
    #计算指标
    df['CostPrice'] = df.apply(lambda x: round(x['CostAmt']/x['Qty'],3),axis=1)
    df['MV'] = df.apply(lambda x: round(float(x['Qty'])*float(x['Price']),2),axis=1)
    df['PL'] = df.apply(lambda x: round(x['MV']-x['CostAmt'],2),axis=1)
    #解决 -0 问题
    df['PL'] = df.apply(lambda x: x['PL'] if x['PL'] != 0 else abs(x['PL']),axis=1)
    
    df['Ratio'] = round(df.apply(lambda x:((x['MV']-x['CostAmt'])/x['CostAmt']) if x['CostAmt']!=0 else 0, axis=1), 4)
    #解决 -0 问题
    df['Ratio'] = df.apply(lambda x: x['Ratio'] if x['Ratio'] != 0 else abs(x['Ratio']),axis=1)

    return df

