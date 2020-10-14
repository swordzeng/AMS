import sqlite3
import requests
import pandas as pd
import re
import json
import urllib.request
# import pdb


def cal_daily_hold(dt, acct):
    pass
    # 复制前一日持仓
    # 计算当日买入
    # 计算当日卖出
    # 合并
    # 计算剩余指标


def get_hold(dt, account, region='ALL'):
    db = sqlite3.connect('AMS.db')

    query = "SELECT SymbolCode, SymbolName, Exchange, AssetClass,Sector,CurSettle AS Cur,Region FROM Symbol_Table"
    df_symbol = pd.read_sql(query, con=db)

    if account.find(',') >= 0:
        acctCondition = " in {} ".format(account)
    else:
        acctCondition = " = '{}' ".format(account)

    query = """
            SELECT *
            FROM Order_Table
            WHERE AccountID {} and Date <= '{}' """.format(acctCondition, dt)

    df_trans = pd.read_sql(query, con=db)
    df_trans = pd.merge(df_trans, df_symbol, on='SymbolCode', how='left')

    if region != 'ALL':
        if region == 'CHINA':
            df_trans = df_trans[df_trans['AccountID'].isin(['CITIC', 'CMS', 'HUATAI'])]
        if region == 'HKSAR':
            df_trans = df_trans[df_trans['AccountID'].isin(['FUTU', 'SNOWBALL'])]

    # 取股票持仓数量
    df_stock = df_trans[~df_trans['AssetClass'].isin(['CASH'])]
    df_stock_sum = df_stock[['SymbolCode', 'Qty']]
    df_stock_sum = df_stock_sum.groupby(['SymbolCode']).sum()

    # 计算股票持仓成本金额
    df_stock_sum['CostAmt'] = 0.0
    df_trans_buy = df_stock[df_stock['Qty'] >= 0]
    for code in df_stock_sum.index.tolist():
        Qty = df_stock_sum.loc[code, 'Qty']
        if Qty > 0:
            cost_amt = get_cost(code, Qty, df_trans_buy)
            df_stock_sum.loc[code, 'CostAmt'] = cost_amt

    # 取现金持仓数量
    df_cur = df_trans[['CurSettle', 'SettleAmt']]
    df_cur_sum = df_cur.groupby(['CurSettle']).sum()
    df_cur_sum.rename(columns={'SettleAmt': 'Qty'}, inplace=True)
    df_cur_sum.index.name = 'SymbolCode'
    df_cur_sum['CostAmt'] = df_cur_sum['Qty']

    # pdb.set_trace()
    # 合并股票持仓和现金持仓
    df_hold = df_stock_sum.append(df_cur_sum)
    df_hold = df_hold[~df_hold['Qty'].isin([0])]    # 去除报告日持仓为0的标的
    df_hold = pd.merge(df_hold, df_symbol, on='SymbolCode', how='left')     # 补充名称和行业

    df_hold['Date'] = dt

    df_hold = get_realtime_price_sina(df_hold)
    df_hold = cal_factor(df_hold)

    hkd_rate = get_exchange_rate('HKD')
    df_hold['ExRate'] = df_hold.apply(lambda x: hkd_rate if x['Cur'] == 'HKD' else 1, axis=1)
    df_hold['MV_CNY'] = df_hold['MV'] * df_hold['ExRate']

    df_hold = df_hold[['SymbolCode', 'SymbolName', 'Sector', 'Cur', 'Qty', 'CostPrice', 'Price', 'DayRatio', 'MV', 'PL', 'Ratio', 'MV_CNY']]
    return df_hold


def get_cost(code, qt, df):
    df_code = df[df['SymbolCode'].isin([code])]
    df_code = df_code.sort_values('Date', ascending=False)

    # 从当前持仓日往前取买入即分红送股数据获取成本金额
    # 直至当前持仓数量扣除完整为止
    amt_cost = 0
    for i in df_code.index.tolist():
        if qt <= 0:
            break
        else:
            qt_trans = df_code.loc[i, 'Qty']
            amt_trans = df_code.loc[i, 'SettleAmt']
            amt_cost = amt_cost + (amt_trans * (qt/qt_trans if qt_trans > qt else 1)) * -1
            qt = qt - qt_trans

    return amt_cost


def get_realtime_price_sina(df):
    df['Price'] = 0.0
    df['DayRatio'] = 0.0

    for index, row in df.iterrows():
        if row['AssetClass'] == 'CASH':
            df.loc[index, 'Price'] = 1.0
        elif row['AssetClass'] == 'EQUITY':
            Exchange = df.loc[index, 'Exchange']
            if Exchange == 'HKEX':
                Exchange = 'HK'
            elif Exchange == 'SSE':
                Exchange = 'SH'
            elif Exchange == 'SZSE':
                Exchange = 'SZ'
            code = Exchange.lower() + str(df.loc[index, 'SymbolCode'].split('.')[0]).zfill(5)
            url = 'http://hq.sinajs.cn/?format=text&list={}'.format(code)
            price_text = requests.get(url).text
            price_list = price_text.split(',')

            if Exchange == 'HKEX':
                price = price_list[2]
                preClose = price_list[3]
            else:
                price = price_list[3]
                preClose = price_list[2]
            price = float(price)
            preClose = float(preClose)
            df.loc[index, 'Price'] = price
            if preClose != 0:
                df.loc[index, 'DayRatio'] = round((price-preClose) / preClose, 4)

    return df


def cal_factor(df):
    # 计算指标
    df['CostPrice'] = df.apply(lambda x: round(x['CostAmt']/x['Qty'], 3), axis=1)
    df['MV'] = df.apply(lambda x: round(float(x['Qty'])*float(x['Price']), 2), axis=1)
    df['PL'] = df.apply(lambda x: round(x['MV']-x['CostAmt'], 2), axis=1)
    # 解决 -0 问题
    df['PL'] = df.apply(lambda x: x['PL'] if x['PL'] != 0 else abs(x['PL']), axis=1)

    df['Ratio'] = round(df.apply(lambda x: ((x['MV']-x['CostAmt'])/x['CostAmt']) if x['CostAmt'] != 0 else 0, axis=1), 4)
    # 解决 -0 问题
    df['Ratio'] = df.apply(lambda x: x['Ratio'] if x['Ratio'] != 0 else abs(x['Ratio']), axis=1)

    return df


def get_exchange_rate(cur):
    url = "http://webforex.hermes.hexun.com/forex/quotelist?code=FOREX{}CNY&column=Code,Price".format(cur)
    req = urllib.request.Request(url)
    f = urllib.request.urlopen(req)
    html = f.read().decode("utf-8")
    s = re.findall("{.*}", str(html))[0]
    sjson = json.loads(s)
    rate = sjson["Data"][0][0][1]/10000

    return rate
