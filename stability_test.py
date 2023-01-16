from Stochastic_rsi import stocastic_plus_rsi, fnRSI, get_stochastic
from stc import supertrendcloud
from stc_backtesting import get_ror_stc
import pandas as pd
import utils
import numpy as np
import matplotlib.pyplot as plt

period1 = 7
multi1 = 3
period2 = 7
multi2 = 6

df = pd.read_excel(f"BINANCE_BTC_4h.xlsx", index_col=0)    # KRW-BTC_4hours.xlsx

period = utils.tdelta2year(df.index)

stocastic = get_stochastic(df,14,3,3)
rsi = fnRSI(df['close'],14)
fast_k = stocastic['fast_k']
cum_ror, ror_list, sto_win_rate = stocastic_plus_rsi(df,rsi,fast_k)
sto_mdd, sto_dd = utils.mdd(ror_list)
sto_cagr = utils.cagr(ror_list, period)
sto_win_rate = utils.win_rate(sto_win_rate)

df_stc = supertrendcloud(df, period1, period2, multi1, multi2)

ror_list, buy_history, sell_history, stc_win_rate = get_ror_stc(df_stc, period1, period2, multi1, multi2)
stc_mdd, stc_dd = utils.mdd(ror_list)
stc_cagr = utils.cagr(ror_list, period)
stc_win_rate = utils.win_rate(stc_win_rate)
print(f"--------------------Stochastic+RSI - period : {period:.3f} year")
print(f"--------------------Stochastic+RSI - MDD : {sto_mdd:.3f}%")
print(f"--------------------Stochastic+RSI - CAGR : {sto_cagr:.3f}%")
print(f"--------------------Stochastic+RSI - Win Rate : {sto_win_rate:.3f}%")
print("\n")
print(f"--------------------SuperTrendCloud - period : {period:.3f} year")
print(f"--------------------SuperTrendCloud - MDD : {stc_mdd:.3f}%")
print(f"--------------------SuperTrendCloud - CAGR : {stc_cagr:.3f}%")
print(f"--------------------SuperTrendCloud - Win Rate : {stc_win_rate:.3f}%")