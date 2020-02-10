from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
import tushare as ts
import pandas as pd
import db_service
import traceback
import time

ALPHA_VANTAGE_KEY = 'PHOPU7GYO084YDMT'
ts.set_token('afc4e40c16f034b23840195764b992b74cbd76c7964eb150afe496d6')

def get_close_price(symbol,startDate='',endDate=''):
    # alpha vantage每分钟只能提取五只股票数据，国内股票用tushare替代
    if symbol.split('.')[1].strip().upper() in ['SS','SZ']:
        start_date = '2019-12-01' if startDate == '' else startDate
        end_date = time.strftime("%Y-%m-%d") if endDate == '' else endDate
        start_date = start_date.replace('-', '')
        end_date = end_date.replace('-', '')
        symbolCode = symbol.replace(".SS", ".SH")
        data = ts.pro_bar(ts_code=symbolCode, start_date=start_date, end_date=end_date)
        close = data.loc[:, ('trade_date','ts_code','close')]
        close.rename(columns={'trade_date':'Date','ts_code':'SymbolCode','close':'Close'},inplace=True)
        close['Date'] = close.apply(lambda x: x['Date'][0:4]+'-'+x['Date'][4:6]+'-'+x['Date'][6:], axis=1)
        close['SymbolCode'] = symbol
    else:
        ts = TimeSeries(key=ALPHA_VANTAGE_KEY, output_format='pandas', indexing_type='date')
        data, meta_data = ts.get_daily(symbol)
        data.reset_index(inplace=True)
        close = data.loc[:, ('date','4. close')]
        close.rename(columns={'date':'Date','4. close':'Close'},inplace=True)
        close.insert(1,'SymbolCode',symbol)
        pd.to_datetime(close['Date'], unit='s').dt.strftime('%Y-%m-%d')     #将Timestamp转换为字符串
    
    return close

def get_realtime_price(symbol):
    if type(symbol) is str:
        price = get_realtime_price_single(symbol)
        return price
    else:
        price = pd.DataFrame(columns=('SymbolCode','Close','DayRatio'))
        for code in symbol:
            price_single = get_realtime_price_single(code)
            price = price.append(price_single, ignore_index=True)

        return price

def get_realtime_price_single(symbol):
    ts = TimeSeries(key=ALPHA_VANTAGE_KEY, output_format='pandas', indexing_type='date')
    data, meta_data = ts.get_quote_endpoint(symbol)
    price = data.reset_index(drop=True)
    price = price[['01. symbol','05. price','10. change percent']]
    price.rename(columns={'01. symbol':'SymbolCode', '05. price':'Close', '10. change percent':'DayRatio'}, inplace = True)
    price.iat[0,2] = float(price.iat[0,2].split('%')[0].strip())/100

    return price

def get_latest_exchange_rate(cur):
    cc = ForeignExchange(key=ALPHA_VANTAGE_KEY)
    # There is no metadata in this call
    data, _ = cc.get_currency_exchange_rate(from_currency=cur,to_currency='CNY')
    exRate = float(data['5. Exchange Rate'])

    return exRate

def get_exchange_rate(cur):
    cc = ForeignExchange(key=ALPHA_VANTAGE_KEY, output_format='pandas', indexing_type='date')
    # There is no metadata in this call
    data, _ = cc.get_currency_exchange_daily(from_symbol=cur,to_symbol='CNY')
    data.reset_index(inplace=True)
    exRate = data.loc[:, ('date','4. close')]
    exRate.rename(columns={'date':'Date','4. close':'Close'},inplace=True)
    exRate.insert(1,'SymbolCode',cur)
    pd.to_datetime(exRate['Date'], unit='s').dt.strftime('%Y-%m-%d')
    
    return exRate

def save_close_price(symbol):
    for code in symbol:
        try:
            maxDate = db_service.get_latest_date('Close_Price','SymbolCode',code)
            dfClose = get_close_price(code)
            dfClose = dfClose.loc[dfClose["Date"] > maxDate]
            db_service.table_append(dfClose,'Close_Price')
        except Exception as e:
            #print('Error: Close price of Symbol: {} failed!'.format(code))
            #print(repr(e))
            traceback.print_exc()
        else:
            print('Close price of Symbol : {} successful!'.format(code))

def save_exchange_rate(symbol=['HKD','USD']):
    for code in symbol:
        try:
            maxDate = db_service.get_latest_date('Close_Price','SymbolCode',code)
            dfClose = get_exchange_rate(code)
            dfClose = dfClose.loc[dfClose["Date"] > maxDate]
            db_service.table_append(dfClose,'Close_Price')
        except Exception as e:
            traceback.print_exc()
        else:
            print('Close price of Symbol : {} successful!'.format(code))

