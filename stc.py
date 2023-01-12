import pprint
import mplfinance as mpl
import pandas as pd
import pandas_ta as ta
import ccxt
import get_key

api_key, api_secret = get_key.get_key('binance')
binance = ccxt.binance(config={
    'apiKey':api_key,
    'secret':api_secret,
    'enableRateLimit':True,  # 지정가 주문만 사용
    'options': {
        'defaultType': 'future'
    }
})

ticker = 'BTC/USDT'
btc = binance.fetch_ohlcv(ticker, '4h', since=None, limit=1000)

df = pd.DataFrame(btc, columns=['time', 'open', 'high', 'low', 'close', 'volumn'])
df['time'] = pd.to_datetime(df['time'], unit='ms')
df.set_index('time', inplace=True)


# percent = int(len(df) * 0.1)
# print(percent)
# df = df.iloc[:percent]
# df = df[pd.DatetimeIndex(df.index).year==2019]

# 2개의 supertrend를 사용해 그 사이의 구름대를 형성
# up_trend => 직전 봉이 직전 up_trend보다 큰 경우 유지. 아니면 갱신
# down_trend => 직전 봉이 직전 down_trend보다 작은 경우 유지. 아니면 갱신
# trend => 시장가가 직전 down_trend보다 클 때 1, up_trend보다 작을 때 -1 아니면 직전 trend가 nan일 때 1로 변환
# st_line = trend == 1 ? up_trend : down_trend

period1 = 10
multi1 = 3
period2 = 60
multi2 = 6

pd.set_option('display.max_rows', 300)
def supertrendcloud(df, period1, period2, multi1, multi2):
    
    st1 = ta.supertrend(df['high'], df['low'], df['close'], length=period1, multiplier=multi1)
    st2 = ta.supertrend(df['high'], df['low'], df['close'], length=period2, multiplier=multi2)


    trend1 = [0]*len(st1) # pd.Series(, name='trend1')
    for i in range(len(st1)):
        if st1[f'SUPERTd_{period1}_{multi1}.0'].iloc[i] > 0:
            trend1[i] = st1[f'SUPERTl_{period1}_{multi1}.0'].iloc[i]
        else:
            trend1[i] = st1[f'SUPERTs_{period1}_{multi1}.0'].iloc[i]


    trend2 = [0]*len(st2) # pd.Series(, name='trend2')
    for i in range(len(st2)):
        if st2[f'SUPERTd_{period2}_{multi2}.0'].iloc[i] > 0:
            trend2[i] = st2[f'SUPERTl_{period2}_{multi2}.0'].iloc[i]
        else:
            trend2[i] = st2[f'SUPERTs_{period2}_{multi2}.0'].iloc[i]

    # STC = pd.concat([trend1, trend2], axis=1)
    # STC.set_index(df.index)
    # df = pd.concat([df, STC], axis=1)
    df[f'trend_{period1}_{multi1}'] = trend1
    df[f'trend_{period2}_{multi2}'] = trend2
    
    # df['trend1'] = trend1
    # df['trend2'] = trend2

    return df



# adps = [mpl.make_addplot(st1[[f'SUPERT_{period1}_{multi1}.0',
#                               f'SUPERTl_{period1}_{multi1}.0',
#                               f'SUPERTs_{period1}_{multi1}.0']])]
#        mpl.make_addplot(st2[f'SUPERT_{period2}_{multi2}.0'])]


# adps = [
# mpl.make_addplot(stc[['trend1', 'trend2']])
# ]
# mpl.plot(df, type='candle', addplot=adps, figscale = 1.5)