import pandas as pd
import mplfinance as mpl
import ccxt
from get_key import get_key
from stc import supertrendcloud
import numpy as np
import matplotlib.pyplot as plt
import utils
from stc import supertrendcloud, get_ror_stc


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

# df.to_excel('BINANCE_BTC_4h_1.xlsx', index=True)

########################################################################
# df = pd.read_excel('BINANCE_BTC_4h_1.xlsx', index_col=0)
df = utils.get_ohlcv('binance', 'BTC/USDT', 4, target_time='2019-12-31 00:00:00')

period1 = 3
multi1 =1
period2 = 3
multi2 = 2

# supertrendcloud 데이터 준비
df = supertrendcloud(df, period1, period2, multi1, multi2)
########################################################################



########################################################################
ror_list, buy_history, sell_history, win_rate = get_ror_stc(df, period1, period2, multi1, multi2)
period = utils.tdelta2year(df.index)
mdd, dd = utils.mdd(ror_list)
cagr = utils.cagr(ror_list, period)
print(f"--------------------period : {period:.3f} year")
print(f"--------------------MDD : {mdd:.3f}%")
print(f"--------------------CAGR : {cagr:.3f}%")
print(f"--------------------Overall Trade : {len(ror_list)} 번")
########################################################################


# ahpr = utils.Ahpr(ror_list, period)
# print(f"--------------------Annualized HPR : {ahpr:.3f}%")

## candle, trend, 포지션 진입, 청산 시각화 추가
adps = {"trend1" : mpl.make_addplot(df[f'trend_{period1}_{multi1}']),
        "trend2" : mpl.make_addplot(df[f'trend_{period2}_{multi2}']),
        "buy" : mpl.make_addplot(buy_history['close'], type='scatter'),
        "sell" : mpl.make_addplot(sell_history['close'], type='scatter')
        }
fig, axes = mpl.plot(df, type='candle', 
                     addplot=list(adps.values()), 
                     figsize=(18, 9),
                     returnfig=False)

axes[0].legend([None]*(len(adps)+2))
handles = axes[0].get_legend().legendHandles
axes[0].legend(handles=handles[2:], labels=list(adps.keys()))
fig.savefig('chart.png')