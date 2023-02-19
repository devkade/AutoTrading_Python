import pprint
import mplfinance as mpl
import pandas as pd
import pandas_ta as ta
import ccxt
import get_key
import numpy as np

# txt 파일에서 api key 받아오기
# api_key, api_secret = get_key.get_key('binance')
# binance = ccxt.binance(config={
#     'apiKey':api_key,
#     'secret':api_secret,
#     'enableRateLimit':True,  # 지정가 주문만 사용
#     'options': {
#         'defaultType': 'future'
#     }
# })

# # ticker 설정, DataFrame 설정
# ticker = 'BTC/USDT'
# btc = binance.fetch_ohlcv(ticker, '4h', since=None, limit=1000)

# df = pd.DataFrame(btc, columns=['time', 'close', 'high', 'low', 'close', 'volumn'])
# df['time'] = pd.to_datetime(df['time'], unit='ms')
# df.set_index('time', inplace=True)


# 2개의 supertrend를 사용해 그 사이의 구름대를 형성
# up_trend => 직전 봉이 직전 up_trend보다 큰 경우 유지. 아니면 갱신
# down_trend => 직전 봉이 직전 down_trend보다 작은 경우 유지. 아니면 갱신
# trend => 시장가가 직전 down_trend보다 클 때 1, up_trend보다 작을 때 -1 아니면 직전 trend가 nan일 때 1로 변환
# st_line = trend == 1 ? up_trend : down_trend

# supertrendcloud 함수 정의
# pandas_ta 라이브러리 사용
# supertrend 함수 사용 시 supertrend, direction, 봉 위 trend, 봉 아래 trend return
# 그 중 supertrend만 사용하면 되지만 반환된 supertrend로는 mplfinance 그래프에 잘못 그려지는 에러 발생해 
# df에 column을 추가해 mplfinance그래프에 그려질 수 있도록 설정
def supertrendcloud(df, period1, period2, multi1, multi2):
    
    # supertrend
    st1 = ta.supertrend(df['high'], df['low'], df['close'], length=period1, multiplier=multi1)
    st2 = ta.supertrend(df['high'], df['low'], df['close'], length=period2, multiplier=multi2)

    # df에 저장
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

def get_ror_stc(df, period1, period2, multi1, multi2):
    
    # buy long   : st1, st2 trend < close
    # sell long  : st2 < close < st1
    # buy short  : st1, st2 trend > close
    # sell short : st1 < close < st2

    # long, short 매수 매도 조건 설정
    cond_buy_long = ((df[f'trend_{period1}_{multi1}'] <= df['close']) & 
                    (df[f'trend_{period2}_{multi2}'] <= df['close']))
    cond_buy_short = ((df[f'trend_{period1}_{multi1}'] >= df['close']) & 
                    (df[f'trend_{period2}_{multi2}'] >= df['close']))
    cond_sell_long = ((df[f'trend_{period1}_{multi1}'] >= df['close']) & 
                    (df[f'trend_{period2}_{multi2}'] <= df['close'])) 
    cond_sell_short = ((df[f'trend_{period1}_{multi1}'] <= df['close']) & 
                    (df[f'trend_{period2}_{multi2}'] >= df['close']))

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
        
        # print(f'------------------------ buy_date : {buy_date}')

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
        # print(f'------------------------ sell_date : {sell_date}, dir : {dir}')
        
        # 수익률 계산
        # try:
        if dir == 'l':
            profit = df.loc[sell_date, 'close'] / df.loc[buy_date, 'close'] - 0.005
            acc_ror *= profit
            if profit > 1:
                win_rate.append(1)
            else:
                win_rate.append(0)
        elif dir == 's':
            profit = df.loc[buy_date, 'close'] / df.loc[sell_date, 'close'] - 0.005
            acc_ror *= profit
            if profit >= 1:
                win_rate.append(1)
            else:
                win_rate.append(0)
        acc_ror_list.append(acc_ror)
        # except ValueError:
        #     pass
        # print(acc_ror, "\n")


    # 시각화
    ## 포지션 진입, 청산 시각화
    buy_history = pd.DataFrame([np.nan]*len(df), columns=['close'], index=df.index)
    for b in buy:
        buy_history.loc[b, 'close'] = df.loc[b, 'close']

    sell_history = pd.DataFrame([np.nan]*len(df), columns=['close'], index=df.index)
    for s in sell:
        sell_history.loc[s, 'close'] = df.loc[s, 'close']
    
    return acc_ror_list, buy_history, sell_history, win_rate

# 그래프 그리기
# adps = [mpl.make_addplot(st1[[f'SUPERT_{period1}_{multi1}.0',
#                               f'SUPERTl_{period1}_{multi1}.0',
#                               f'SUPERTs_{period1}_{multi1}.0']])]
#        mpl.make_addplot(st2[f'SUPERT_{period2}_{multi2}.0'])]


# adps = [
# mpl.make_addplot(stc[['trend1', 'trend2']])
# ]
# mpl.plot(df, type='candle', addplot=adps, figscale = 1.5)