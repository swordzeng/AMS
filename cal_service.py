from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
import pandas as pd
import db_service
import traceback
import time
import datetime
import pdb

ALPHA_VANTAGE_KEY = 'PHOPU7GYO084YDMT'
TUSHARE_KEY ='afc4e40c16f034b23840195764b992b74cbd76c7964eb150afe496d6'

def get_close_price(symbol,startDate='',endDate=''):
    '''
    # alpha vantage每分钟只能提取五只股票数据，国内股票用tushare替代
    if symbol.split('.')[1].strip().upper() in ['SS','SZ']:
        start_date = '2019-12-31' if startDate == '' else startDate
        end_date = time.strftime("%Y-%m-%d") if endDate == '' else endDate
        start_date = start_date.replace('-', '')
        end_date = end_date.replace('-', '')
        symbolCode = symbol.replace(".SS", ".SH")
        #local variable 'ts' referenced before assignment
        tushare.set_token(TUSHARE_KEY)
        data = tushare.pro_bar(ts_code=symbolCode, start_date=start_date, end_date=end_date)
        close = data.loc[:, ('trade_date','ts_code','close')]
        close.rename(columns={'trade_date':'Date','ts_code':'SymbolCode','close':'Close'},inplace=True)
        close['Date'] = close.apply(lambda x: x['Date'][0:4]+'-'+x['Date'][4:6]+'-'+x['Date'][6:], axis=1)
        close['SymbolCode'] = symbol
    else:
    '''
    ts = TimeSeries(key=ALPHA_VANTAGE_KEY, output_format='pandas', indexing_type='date')
    data, meta_data = ts.get_daily(symbol)
    data.reset_index(inplace=True)
    close = data.loc[:, ('date','4. close')]
    close.rename(columns={'date':'Date','4. close':'Close'},inplace=True)
    close.insert(1,'SymbolCode',symbol)
    close['Date'] = close.apply(lambda x: x['Date'].strftime('%Y-%m-%d'),axis=1)
    
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
    exRate['Date'] = exRate.apply(lambda x: x['Date'].strftime('%Y-%m-%d'),axis=1)
    
    return exRate

def save_close_price(symbol='', dtStart=''):
    if symbol=='':
        symbolList = db_service.get_symbol_for_close_price(dtStart)
    elif type(symbol) is str:
        symbolList = []
        symbolList.append(symbol)
    else:
        symbolList = symbol

    # alpha vantage 每分钟只能提取五个代码数据，满五个停一分钟再继续
    count = 0

    print(symbolList)
    for code in symbolList:
        print(code + ' & ' + str(count))
        try:
            if count >= 5:
                print('sleep 60 seconds')
                time.sleep(60)  #休眠60秒
                count = 1    
            else:
                count = count + 1

            maxDate = db_service.get_latest_date('Close_Price','SymbolCode',code)
            maxDate = '2019-12-30' if maxDate == '2019-12-31' else maxDate
            now = datetime.datetime.now()
            nowDate = now.strftime('%Y-%m-%d')
            nowTime = now.strftime('%H:%M:%S')
            #maxDate2 = datetime.datetime.strptime(maxDate, '%Y-%m-%d')
            #date = get_weekday(datetime.datetime.now().strftime('%Y-%m-%d'),'pre')
            #if date > maxDate2:
            dfClose = get_close_price(code)
            dfClose = dfClose.loc[dfClose["Date"] > maxDate]
            if nowTime < '16:30:00':
                dfClose = dfClose.loc[dfClose["Date"] < nowDate]
                nowDate = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

            db_service.table_append(dfClose,'Close_Price')

        except Exception as e:
            print('Error: Close price of Symbol: {} failed!'.format(code))
            print(repr(e))
            #traceback.print_exc()
        else:
            print('Close price of Symbol : {}, date: {} successful!'.format(code, nowDate))

def save_exchange_rate(symbol=['HKD','USD']):
    for code in symbol:
        try:
            maxDate = db_service.get_latest_date('Exchange_Rate','SymbolCode',code)
            maxDate = '2019-12-30' if maxDate == '2019-12-31' else maxDate
            now = datetime.datetime.now()
            nowDate = now.strftime('%Y-%m-%d')
            nowTime = now.strftime('%H:%M:%S')

            dfClose = get_exchange_rate(code)
            dfClose = dfClose.loc[dfClose["Date"] > maxDate]
            if nowTime < '16:30:00':
                dfClose = dfClose.loc[dfClose["Date"] < nowDate]
                nowDate = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

            db_service.table_append(dfClose,'Exchange_Rate')
        except Exception as e:
            traceback.print_exc()
        else:
            print('Close price of Symbol : {}, date: {} successful!'.format(code, nowDate))

def cal_holding(startDate='', endDate='' ):

    lastDate = db_service.get_latest_date('Holding_Table')
    lastDate = datetime.datetime.strptime(lastDate, '%Y-%m-%d').date()
    firstDate = get_weekday(lastDate)   # 在原最大持仓日往后一工作日作为计算起点

    if startDate == '':
        startDate = firstDate

    if type(startDate) is str:
        startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d').date()

    # 开始日期是周末，开始日期向后取工作日
    if startDate.weekday() == 5:    
        startDate = startDate + datetime.timedelta(days=2)
    elif startDate.weekday() == 6:
         startDate = startDate + datetime.timedelta(days=1)
    else:
        startDate = startDate

    # 输入开始日期大于上一持仓日期，自动补足
    if startDate > firstDate:    
        startDate = firstDate

    # 当前日期不计算持仓，历史持仓只到T-1日
    if endDate == '':
        endDate = datetime.datetime.now().date() + datetime.timedelta(days=-1)

    if type(endDate) is str:
        endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d').date()

    # 结束日期是周末，结束日期往前取工作日
    if endDate.weekday() == 5:      
        endDate = endDate + datetime.timedelta(days=-1)
    elif endDate.weekday() == 6:
         endDate = endDate + datetime.timedelta(days=-2)
    else:
        endDate = endDate

    holdDate = startDate
    while holdDate <= endDate:
        print('################# cal holding @' + holdDate.strftime('%Y-%m-%d'))
        
        preHoldDate = get_weekday(date=holdDate, prepost='pre')
        preHold = db_service.get_holding(dt=preHoldDate)
        trans = db_service.get_trans(dtStart=preHoldDate.strftime('%Y-%m-%d'), dtEnd=holdDate.strftime('%Y-%m-%d'))
        trans.rename(columns={'CurTrade':'Cur'}, inplace=True)

        hold = preHold.loc[:, ('AccountID','SymbolCode','SymbolName','Cur','Qty','Cost','Close','ExRate')]
        hold.rename(columns={'Qty':'QtyPre', 'Cost':'CostPre','Close':'ClosePre','ExRate':'ExRatePre'}, inplace=True)
        hold.insert(0,'Date',holdDate.strftime('%Y-%m-%d'))

        transBuy = trans.loc[(trans['OrderType'] == 'Buy') | (trans['OrderType'] == 'Bonus')]
        if transBuy.empty is False:
            price = transBuy[['AccountID','SymbolCode','Price']].groupby(by=['AccountID','SymbolCode'], as_index=False).max()

            transBuy = transBuy.loc[:, ('AccountID','SymbolCode','SymbolName','Cur','Qty','SettleAmt')]
            transBuy.rename(columns={'Qty':'QtyBuy','SettleAmt':'SettleAmtBuy'}, inplace=True)
            transBuy = transBuy.groupby(['AccountID','SymbolCode','SymbolName','Cur']).sum()
            transBuy.insert(0,'Date',holdDate.strftime('%Y-%m-%d'))
            transBuy['SettleAmtBuy'] = abs(transBuy['SettleAmtBuy'])
            transBuy['CostBuy'] = transBuy['SettleAmtBuy']/transBuy['QtyBuy']
            #transBuy.drop(columns=['SettleAmt'],inplace=True)
            transBuy.reset_index(inplace =True)

            hold = pd.merge(hold,transBuy,on=['Date','AccountID','SymbolCode','SymbolName','Cur'],how='outer')
            hold = pd.merge(hold,price,on=['AccountID','SymbolCode'],how='left')

            hold.fillna(0, inplace=True)
        else:
            hold['QtyBuy'] = 0
            hold['CostBuy'] = 0  
            hold['Price'] = 0
            hold['SettleAmtBuy'] = 0

        transSell = trans.loc[trans['OrderType'] == 'Sell']
        if transSell.empty is False:
            transSell = transSell.loc[:, ('AccountID','SymbolCode','SymbolName','Cur','Qty','SettleAmt')]
            transSell.rename(columns={'Qty':'QtySell','SettleAmt':'SettleAmtSell'}, inplace=True)
            transSell['QtySell'] = transSell.apply(lambda x: abs(x['QtySell']), axis=1 )
            transSell = transSell.groupby(['AccountID','SymbolCode','SymbolName','Cur']).sum()
            transSell.insert(0,'Date',holdDate.strftime('%Y-%m-%d'))
            transSell['SettleAmtSell'] = abs(transSell['SettleAmtSell'])
            transSell['PriceSell'] = transSell['SettleAmtSell']/transSell['QtySell']
            #transSell.drop(columns=['SettleAmt'],inplace=True)
            transSell.reset_index(inplace =True)
            hold = pd.merge(hold,transSell,on=['Date','AccountID','SymbolCode','SymbolName','Cur'],how='outer')
            hold.fillna(0, inplace=True)
        else:
            hold['QtySell'] = 0
            hold['PriceSell'] = 0   
            hold['SettleAmtSell'] = 0    

        transInterest = trans.loc[trans['OrderType'] == 'Interest']
        if transInterest.empty is False:
            transInterest = transInterest.loc[:, ('AccountID','SymbolCode','SymbolName','Cur','SettleAmt')]
            transInterest.rename(columns={'SettleAmt':'DailyInterest'}, inplace=True)
            transInterest = transInterest.groupby(['AccountID','SymbolCode','SymbolName','Cur']).sum()
            transInterest.insert(0,'Date',holdDate.strftime('%Y-%m-%d'))
            transInterest.reset_index(inplace =True)
            hold = pd.merge(hold,transInterest,on=['Date','AccountID','SymbolCode','SymbolName','Cur'],how='outer')
            hold.fillna(0, inplace=True)
        else:
            hold['DailyInterest'] = 0  

        transMoneyOut = trans.loc[trans['OrderType'] == 'Withdraw']    
        transMoneyOut = transMoneyOut.loc[:, ('AccountID','SymbolCode','SymbolName','Cur','SettleAmt')] 
        transMoneyOut.rename(columns={'SettleAmt':'MoneyOut'}, inplace=True) 
        #transMoneyOut['MoneyOut'] = transMoneyOut.apply(lambda x: abs(x['MoneyOut']), axis=1 )
        transMoneyOut = transMoneyOut.groupby(['AccountID','SymbolCode','SymbolName','Cur']).sum()  

        transMoneyIn = trans.loc[trans['OrderType'] == 'Deposit']    
        transMoneyIn = transMoneyIn.loc[:, ('AccountID','SymbolCode','SymbolName','Cur','SettleAmt')] 
        transMoneyIn.rename(columns={'SettleAmt':'MoneyIn'}, inplace=True)  
        transMoneyIn = transMoneyIn.groupby(['AccountID','SymbolCode','SymbolName','Cur']).sum()  

        #pdb.set_trace()

        if transMoneyOut.empty is True and transMoneyIn.empty is True:
            hold['MoneyIn'] = 0  
            hold['MoneyOut'] = 0  
        else:
            money = pd.merge(transMoneyIn,transMoneyOut,on=['AccountID','SymbolCode','SymbolName','Cur'],how='outer')
            money.fillna(0,inplace=True)
            money.reset_index(inplace=True)
            money.insert(0,'Date',holdDate.strftime('%Y-%m-%d'))
            hold = pd.merge(hold,money, on=['Date','AccountID','SymbolCode','SymbolName','Cur'],how='outer')
            hold.fillna(0, inplace=True)

        closePrice = db_service.get_history_price(dtStart=preHoldDate, dtEnd=holdDate)
        hold = pd.merge(hold,closePrice,on=['Date','SymbolCode'],how='left')
        
        exchangeRate = db_service.get_history_price(dtStart=preHoldDate, dtEnd=holdDate, type='exchange')
        exchangeRate.rename(columns={'Close':'ExRate'}, inplace=True)
        hold = pd.merge(hold,exchangeRate,on=['Date','SymbolCode'],how='left')
        hold['ExRate'] = hold['ExRate'].fillna(hold['ExRatePre'])
        hold['ExRate'] = hold.apply(lambda x: 1.0 if x['ExRate']==0 else x['ExRate'], axis=1 )

        #四舍五入过后计算的收益会有小数精度问题
        #hold['CostBuy'] = hold.apply(lambda x: round(x['CostBuy'],3), axis=1)
        #hold['PriceSell'] = hold.apply(lambda x: round(x['PriceSell'],3), axis=1)

        moneySettle = hold.loc[:, ('AccountID','Cur','SettleAmtBuy','SettleAmtSell')]
        moneySettle['SettleAmt'] = moneySettle.apply(lambda x: x['SettleAmtSell']-x['SettleAmtBuy'], axis=1)
        moneySettle.drop(columns=['SettleAmtBuy','SettleAmtSell'],inplace=True)
        moneySettle = moneySettle.groupby(['AccountID','Cur']).sum()
        moneySettle.reset_index(inplace =True)
        moneySettle.rename(columns={'Cur':'SymbolCode'}, inplace=True)
        hold = pd.merge(hold,moneySettle, on=['AccountID','SymbolCode'],how='left')

        hold['Qty'] = hold.apply(lambda x: x['QtyPre']+x['MoneyIn']+x['MoneyOut']+x['DailyInterest']+x['SettleAmt'] \
            if x['SymbolCode'] in ['HKD','CNY','USD'] else x['QtyPre']+x['QtyBuy']-x['QtySell'],axis=1)
        hold['Cost'] = hold.apply(lambda x: 0 if x['QtyPre']+x['QtyBuy']==0 \
            else (x['QtyPre']*x['CostPre'] + x['QtyBuy']*x['CostBuy']-x['DailyInterest'])/(x['QtyPre']+x['QtyBuy']),axis=1)
        hold['Cost'] = hold.apply(lambda x: 1.0 if x['SymbolCode'] in ['HKD','CNY','USD'] else x['Cost'], axis=1 )

        hold['Qty'] = hold.apply(lambda x: round(x['Qty'],3), axis=1)
        #hold['Cost'] = hold.apply(lambda x: round(x['Cost'],3), axis=1)
        
        #如果取到的收盘价为空，则取前日收盘价替代，前日收盘价仍为空，则用成本价替代
        hold['Close'] = hold['Close'].fillna(hold['ClosePre'])
        #hold['Close'] = hold.apply(lambda x: x['CostPre'] if x['Close']==0 else x['Close'], axis=1 )
        hold['Close'] = hold.apply(lambda x: x['Price'] if x['Close']==0 else x['Close'], axis=1 )

        hold['MV'] = hold.apply(lambda x: x['Qty'] * x['Close'], axis=1 )
        hold['HoldingFloat'] = hold.apply(lambda x: x['Qty'] * (x['Close']-x['Cost']), axis=1 )
        hold['DailyRealized'] = hold.apply(lambda x: x['QtySell']*(x['PriceSell']-x['ClosePre']) if x['QtySell']<=x['QtyPre'] \
            else (x['QtySell']-x['QtyPre'])*(x['PriceSell']-x['CostBuy'])+x['QtyPre']*(x['PriceSell']-x['ClosePre']), axis=1 )
        hold['DailyFloat'] = hold.apply(lambda x: (x['QtyPre']-x['QtySell'])*(x['Close']-x['ClosePre']) + x['QtyBuy']*(x['Close']-x['CostBuy']) \
            if x['QtySell']<=x['QtyPre'] else (x['QtyBuy']+x['QtyPre']-x['QtySell'])*(x['Close']-x['CostBuy']), axis=1 )

        hold['MV'] = hold.apply(lambda x: round(x['MV'],2), axis=1)
        hold['HoldingFloat'] = hold.apply(lambda x: round(x['HoldingFloat'],2), axis=1)
        hold['DailyRealized'] = hold.apply(lambda x: round(x['DailyRealized'],2), axis=1)
        hold['DailyFloat'] = hold.apply(lambda x: round(x['DailyFloat'],2), axis=1)

        holdCur = hold[hold['SymbolCode'].isin(['CNY','HKD','USD'])]
        holdSymbol = hold[~hold['SymbolCode'].isin(['CNY','HKD','USD'])]
        holdSymbol = holdSymbol[~(holdSymbol['QtyBuy'].isin([0]) & holdSymbol['QtySell'].isin([0]) & holdSymbol['Qty'].isin([0]))]
        hold = pd.concat([holdCur,holdSymbol],ignore_index=True)
        
        #pdb.set_trace()

        hold.drop(columns=['QtyPre','CostPre','ClosePre','ExRatePre','Price','SettleAmtBuy','SettleAmtSell','SettleAmt'],inplace=True)

        db_service.table_delete('Holding_Table', 'Date', holdDate.strftime('%Y-%m-%d'))
        db_service.table_append(hold,'Holding_Table')

        holdDate = get_weekday(holdDate)

def get_weekday(date='',prepost='post'):
    if type(date) is str:
        if date == '':
            date = datetime.datetime.now().strftime('%Y-%m-%d')

        dt = datetime.datetime.strptime(date, '%Y-%m-%d')
    else:
        dt = date

    week = dt.weekday()

    if prepost == 'pre':
        if week == 0:    # Monday
            lastDay = dt + datetime.timedelta(days=-3)
        elif week == 6:  # Sunday
            lastDay = dt + datetime.timedelta(days=-2)
        else:
            lastDay = dt + datetime.timedelta(days=-1)

    if prepost == 'post':
        if week == 4:    # Friday
            lastDay = dt + datetime.timedelta(days=3)
        elif week == 5:  # Saturday
            lastDay = dt + datetime.timedelta(days=2)
        else:
            lastDay = dt + datetime.timedelta(days=1)

    #strLastDay = lastDay.strftime('%Y-%m-%d')

    return lastDay


