from Stochastic_rsi import stocastic_plus_rsi, fnRSI, get_stochastic
from stc import supertrendcloud, get_ror_stc
import pandas as pd
import utils
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_excel(f"BINANCE_BTC_4h.xlsx", index_col=0)    # KRW-BTC_4hours.xlsx
period = utils.tdelta2year(df.index)

# Stochastic + rsi

# n_days = 14
# slowk_days = 3
# slowd_days = 3


# stocastic = get_stochastic(df,n_days,slowk_days,slowd_days)
# rsi = fnRSI(df['close'],14)
# fast_k = stocastic['fast_k']
# cum_ror, ror_list, sto_win_rate = stocastic_plus_rsi(df,rsi,fast_k)
# sto_mdd, sto_dd = utils.mdd(ror_list)
# sto_cagr = utils.cagr(ror_list, period)
# sto_win_rate = utils.win_rate(sto_win_rate)

stc_hp = pd.read_excel('stc_hp1.xlsx', index_col=0)

# supertrendcloud 

periods = [3, 5, 7, 10, 12, 15, 30]
multis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

period1 = 7
multi1 = 3
period2 = 7
multi2 = 6

P1 = []
P2 = []
M1 = []
M2 = []
mdd = []
cagr = []
win_rate = []
overall_trade = []
max_cagr = 0
max_index = 0
index = 0

for p1 in periods:
    if p1 > 5:
        continue
    for p2 in periods:
        if p2 < 15:
            continue
        for m1 in multis:
            for m2 in multis:
                if m1 >= m2:
                    continue
                print(f'p1:{p1}, p2:{p2}, m1:{m1}, m2:{m2}')
                df_stc = supertrendcloud(df, p1, p2, m1, m2)
                try:
                    ror_list, buy_history, sell_history, stc_win_rate = get_ror_stc(df_stc, p1, p2, m1, m2)
                    stc_mdd, stc_dd = utils.mdd(ror_list)
                    stc_cagr = utils.cagr(ror_list, period)
                    stc_win_rate = utils.win_rate(stc_win_rate)
                    
                    P1.append(p1)
                    P2.append(p2)
                    M1.append(m1)
                    M2.append(m2)
                    mdd.append(stc_mdd)
                    cagr.append(stc_cagr)
                    win_rate.append(stc_win_rate)
                    overall_trade.append(len(ror_list))
                    
                    if max_cagr < stc_cagr:
                        max_cagr = stc_cagr
                        max_index = index
                    
                    index += 1
                except ValueError:
                    pass

data = {'p1': P1,
        'p2': P2,
        'm1': M1,
        'm2': M2,
        'mdd':mdd,
        'cagr': cagr,
        'win_rate': win_rate,
        'overall_trade' : overall_trade}
hp_df = pd.DataFrame(data)
print(max_index)
hp_df = pd.concat([stc_hp, hp_df], axis=0)
hp_df.to_excel('stc_hp1.xlsx')

# df_stc = supertrendcloud(df, 3, 7, 2, 4)

# ror_list, buy_history, sell_history, stc_win_rate = get_ror_stc(df_stc, 3, 7, 2, 4)
# stc_mdd, stc_dd = utils.mdd(ror_list)
# stc_cagr = utils.cagr(ror_list, period)
# stc_win_rate = utils.win_rate(stc_win_rate)
                
                
# print(f"--------------------Stochastic+RSI - period : {period:.3f} year")
# print(f"--------------------Stochastic+RSI - MDD : {sto_mdd:.3f}%")
# print(f"--------------------Stochastic+RSI - CAGR : {sto_cagr:.3f}%")
# print(f"--------------------Stochastic+RSI - Win Rate : {sto_win_rate:.3f}%")
# print("\n")
# print(f"--------------------SuperTrendCloud - period : {period:.3f} year")
# print(f"--------------------SuperTrendCloud - MDD : {stc_mdd:.3f}%")
# print(f"--------------------SuperTrendCloud - CAGR : {stc_cagr:.3f}%")
# print(f"--------------------SuperTrendCloud - Win Rate : {stc_win_rate:.3f}%")