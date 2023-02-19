import pandas as pd
from stc import get_ror_stc, supertrendcloud
import utils
import mplfinance as mpl
import matplotlib.pyplot as plt
import utils


hp = pd.read_excel('stc_hp1.xlsx', index_col=0)
print(hp)
hp.sort_values(by=['cagr', 'mdd', 'win_rate'], ascending=[False, False, True], inplace=True)
# hp.sort_values(by=['mdd', 'cagr', 'win_rate'], ascending=[False, False, True], inplace=True)

tickers = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'BNB/USDT', 'LTC/USDT', 'TRX/USDT', 'DASH/USDT']
i = 6
# df = pd.read_excel('BINANCE_BTC_4h.xlsx', index_col = 0)
# timeframes = ['1m', '15m', '30m', '1h', '4h', '6h']
# for timeframe in timeframes:
#     print(f'Timeframe : {timeframe}')
for ticker in tickers:
    p1 = hp.iloc[i, 0]
    p2 = hp.iloc[i, 1]
    m1 = hp.iloc[i, 2]
    m2 = hp.iloc[i, 3]
    df = utils.get_ohlcv('binance', ticker, 3, timeframe='4h', target_time='2023-01-16 16:00:00')
    print(f"--------------------ticker : {ticker}")
    df = supertrendcloud(df, p1, p2, m1, m2)
    ror_list, buy_history, sell_history, win_rate = get_ror_stc(df, p1, p2, m1, m2)
    mdd, dd = utils.mdd(ror_list)
    period = utils.tdelta2year(df.index)
    cagr = utils.cagr(ror_list, period)
    win_rate = utils.win_rate(ror_list)
    print(f"--------------------period : {period:.3f} year")
    print(f"--------------------MDD : {mdd:.3f}%")
    print(f"--------------------CAGR : {cagr:.3f}%")
    print(f"--------------------win_rate : {win_rate:.3f}%")
    print(f"--------------------Overall Trade : {len(ror_list)} 번\n")


n = 20

# period = utils.tdelta2year(df.index)
# print(period)
# for i in range(n):
#     stc = supertrendcloud(df, hp.iloc[i, 0], hp.iloc[i, 1], hp.iloc[i, 2], hp.iloc[i, 3])

#     ror_list, buy_history, sell_history, win_rate = get_ror_stc(df, 
#                                                                 hp.iloc[i, 0], 
#                                                                 hp.iloc[i, 1], 
#                                                                 hp.iloc[i, 2], 
#                                                                 hp.iloc[i, 3])
    
#     adps = {"trend1" : mpl.make_addplot(df[f'trend_{hp.iloc[i, 0]}_{hp.iloc[i, 2]}']),
#             "trend2" : mpl.make_addplot(df[f'trend_{hp.iloc[i, 1]}_{hp.iloc[i, 3]}']),
#             "buy" : mpl.make_addplot(buy_history['open'], type='scatter'),
#             "sell" : mpl.make_addplot(sell_history['open'], type='scatter')
#             }
#     fig, axes = mpl.plot(df, type='candle', 
#                         addplot=list(adps.values()), 
#                         figsize=(18, 9),
#                         returnfig=True)

#     axes[0].legend([None]*(len(adps)+2))
#     handles = axes[0].get_legend().legendHandles
#     axes[0].legend(handles=handles[2:], labels=list(adps.keys()))
#     fig.savefig(f'./chart/best_hp{i}.png')

# p1 = hp.iloc[i, 0]
# p2 = hp.iloc[i, 1]
# m1 = hp.iloc[i, 2]
# m2 = hp.iloc[i, 3]
# df = supertrendcloud(df, p1, p2, m1, m2)

# ror_list, buy_history, sell_history, win_rate = get_ror_stc(df, 
#                                                             p1,
#                                                             p2,
#                                                             m1, 
#                                                             m2)


# adps = {"trend1" : mpl.make_addplot(df[f'trend_{p1}_{m1}']),
#         "trend2" : mpl.make_addplot(df[f'trend_{p2}_{m2}']),
#         "buy" : mpl.make_addplot(buy_history['close'], type='scatter'),
#         "sell" : mpl.make_addplot(sell_history['close'], type='scatter')
#         }
# fig, axes = mpl.plot(df, type='candle', 
#                     addplot=list(adps.values()), 
#                     figsize=(18, 9),
#                     returnfig=False)

# axes[0].legend([None]*(len(adps)+2))
# handles = axes[0].get_legend().legendHandles
# axes[0].legend(handles=handles[2:], labels=list(adps.keys()))
# fig.savefig(f'./chart/best_hp{i}.png')

