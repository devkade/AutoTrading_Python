import pandas as pd
import mplfinance as mpl
import ccxt
from get_key import get_key
from stc import supertrendcloud
import datetime
import numpy as np
import time
import matplotlib.pyplot as plt
import utils


# api_key, api_secret = get_key("binance")

# ticker = "BTC/USDT"
# binance = ccxt.binance(config={
#     'apiKey': api_key,
#     'secret': api_secret,
#     'enableRateLimit':True
# })
# # df 준비
# since = binance.parse8601('2022-01-01 00:00:00')
# btc_ohlcv = binance.fetch_ohlcv(ticker, '4h', since=since, limit=1000)

# df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
# df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
# df.set_index('datetime', inplace=True)
# print(df)

########################################################################
# df = pd.read_excel('BINANCE_BTC_4h.xlsx', index_col=0)

# period1 = 7
# multi1 = 3
# period2 = 7
# multi2 = 6

# supertrendcloud 데이터 준비
# df = supertrendcloud(df, period1, period2, multi1, multi2)
########################################################################


def get_ror_stc(df, period1, period2, multi1, multi2):

    # buy long   : st1, st2 trend < open
    # sell long  : st2 < open < st1
    # buy short  : st1, st2 trend > open
    # sell short : st1 < open < st2

    # long, short 매수 매도 조건 설정
    cond_buy_long = ((df[f'trend_{period1}_{multi1}'] <= df['open']) & 
                    (df[f'trend_{period2}_{multi2}'] <= df['open']))
    cond_buy_short = ((df[f'trend_{period1}_{multi1}'] >= df['open']) & 
                    (df[f'trend_{period2}_{multi2}'] >= df['open']))
    cond_sell_long = ((df[f'trend_{period1}_{multi1}'] >= df['open']) & 
                    (df[f'trend_{period2}_{multi2}'] <= df['open'])) 
    cond_sell_short = ((df[f'trend_{period1}_{multi1}'] <= df['open']) & 
                    (df[f'trend_{period2}_{multi2}'] >= df['open']))

    # 포지션 진입 시기 list
    buy = []
    # 포지션 청산 시기 list
    sell = []
    # 누적 수익률 list
    acc_ror_list = []
    acc_ror = 1
    # 승률 list
    win_rate = []
    sell_date = None

    # long, short을 위한 direction 설정
    df.loc[cond_buy_long, 'dir'] = 'l'
    df.loc[cond_buy_short, 'dir'] = 's'

    buy_time = df.index[cond_buy_long | cond_buy_short]
    dirs = df.loc[cond_buy_long | cond_buy_short, 'dir']


    # 수익률 계산
    for buy_date, dir in zip(buy_time, dirs):
        # buy_date = df.index[buy_long][10]
        if sell_date!=None and (buy_date <= sell_date):
            continue
        buy.append([buy_date])
        
        print(f'------------------------ buy_date : {buy_date}')

        # long, short일 때 청산 조건 설정
        if dir == 'l':
            sell_candidate = df.index[cond_sell_long]
            inverse_candidate = df.index[cond_buy_short]
        elif dir == 's':
            sell_candidate = df.index[cond_sell_short]
            inverse_candidate = df.index[cond_buy_long]
        else:
            continue
        
        if len(sell_candidate[buy_date < sell_candidate]) == 0:
            sell_date = df.index[-1]
        else:
            sell_date = sell_candidate[buy_date < sell_candidate][0]
            if len(inverse_candidate[buy_date < inverse_candidate]) != 0:
                inverse_date = inverse_candidate[buy_date < inverse_candidate][0]
                if inverse_date < sell_date:
                    sell_date = inverse_date
        sell.append([sell_date])
        print(f'------------------------ sell_date : {sell_date}, dir : {dir}')
        
        # 수익률 계산
        if dir == 'l':
            profit = df.loc[sell_date, 'open'] / df.loc[buy_date, 'open'] - 0.005
            acc_ror *= profit
            if profit >= 1:
                win_rate.append(1)
            else:
                win_rate.append(0)
        elif dir == 's':
            profit = df.loc[buy_date, 'open'] / df.loc[sell_date, 'open'] - 0.005
            acc_ror *= profit
            if profit >= 1:
                win_rate.append(1)
            else:
                win_rate.append(0)
        acc_ror_list.append(acc_ror)
        print(acc_ror, "\n")


    # 시각화
    ## 포지션 진입, 청산 시각화
    buy_history = pd.DataFrame([np.nan]*len(df), columns=['open'], index=df.index)
    for b in buy:
        buy_history.loc[b, 'open'] = df.loc[b, 'open']

    sell_history = pd.DataFrame([np.nan]*len(df), columns=['open'], index=df.index)
    for s in sell:
        sell_history.loc[s, 'open'] = df.loc[s, 'open']
    
    return acc_ror_list, buy_history, sell_history, win_rate

########################################################################
# ror_list, buy_history, sell_history, win_rate = get_ror_stc(df, period1, period2, multi1, multi2)
# period = utils.tdelta2year(df.index)
# mdd, dd = utils.mdd(ror_list)
# cagr = utils.cagr(ror_list, period)
# print(f"--------------------period : {period:.3f} year")
# print(f"--------------------MDD : {mdd:.3f}%")
# print(f"--------------------CAGR : {cagr:.3f}%")
########################################################################


# ahpr = utils.Ahpr(ror_list, period)
# print(f"--------------------Annualized HPR : {ahpr:.3f}%")

## candle, trend, 포지션 진입, 청산 시각화 추가
# adps = {"trend1" : mpl.make_addplot(df[f'trend_{period1}_{multi1}']),
#         "trend2" : mpl.make_addplot(df[f'trend_{period2}_{multi2}']),
#         "buy" : mpl.make_addplot(buy_history['open'], type='scatter'),
#         "sell" : mpl.make_addplot(sell_history['open'], type='scatter')}
# fig, axes = mpl.plot(df, type='candle', 
#                      addplot=list(adps.values()), 
#                      figsize=(18, 9),
#                      returnfig=False)

# axes[0].legend([None]*(len(adps)+2))
# handles = axes[0].get_legend().legendHandles
# axes[0].legend(handles=handles[2:], labels=list(adps.keys()))
# fig.savefig('chart.png')