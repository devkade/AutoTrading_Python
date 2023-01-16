import pandas as pd
import pyupbit
import ccxt
import time
import datetime
import numpy as np

tickers = {"upbit": "KRW-BTC",
           "binance": "BTC/USDT"}

def get_ohlcv(exchange='upbit', ticker = 'KRW-BTC', n=1, target_time=None): #코인의 정보를 불러옴, 500*n개의 정보
    dfs = [ ]
    if exchange=='upbit':
        df = pyupbit.get_ohlcv(ticker, interval="minute240", to=target_time)
        dfs.append(df)
        for i in range(n):
            df = pyupbit.get_ohlcv(ticker, interval="minute240", to = df.index[0]) #to: 출력할 max date time을 지정
            dfs.append(df)
            time.sleep(0.2) #한 번에 너무 많은 데이터를 요청하면 웹서버에서 차단할 수 있음
    
    elif exchange=='binance':
        binance = ccxt.binance()
        if target_time is None:
            last = datetime.datetime.fromtimestamp(binance.milliseconds()/1000)
        else:
            last = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        days = datetime.timedelta(days=np.ceil((1000*n)/6))
        back = datetime.datetime.strftime(last-days, '%Y-%m-%d %H:%M:%S')
        since = binance.parse8601(back)
        df = binance.fetch_ohlcv(ticker, '4h', since=since, limit=1000)
        df = pd.DataFrame(df, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)
        dfs.append(df)
        for i in range(n-1):
            since = binance.parse8601(datetime.datetime.strftime(df.index[-1], '%Y-%m-%d %H:%M:%S'))
            df = binance.fetch_ohlcv(ticker, '4h', since=since, limit=1000)
            df = pd.DataFrame(df, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
            df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
            df.set_index('datetime', inplace=True)
            dfs.append(df)
            time.sleep(0.2)

    df = pd.concat(dfs) #list안에 있는 데이터프레임을 하나로 합쳐줌
    df = df.sort_index()
    return df

def get_mdd(ror: list, window=20):
    ror = pd.Series(ror)
    maximum = ror.rolling(len(ror), min_periods=1).max()
    dd = (ror - maximum) / maximum
    mdd = dd.min()

    return mdd*100, dd

def hpr(ror: list):
    final_ror = ror[-1]
    return (final_ror - 1) / 1

def Ahpr(ror: list, period: float):
    return ((1+hpr(ror))**(1/period)-1)*100

def tdelta2year(index: pd.DatetimeIndex):
    return (index[-1]-index[0]).days/365.2425

# 연평균 복리수익률
def cagr(ror: list, period: float):
    return ((ror[-1]/1)**(1/period)-1)*100

def win_rate(win_rate: list):
    num_trade = len(win_rate)
    win_trade = win_rate.count(1)
    return win_trade / num_trade * 100

# df = get_ohlcv('binance', tickers['binance'], 4)
# print(get_period(df.index))
# df.to_excel('BINANCE_BTC_4h.xlsx', index=True)