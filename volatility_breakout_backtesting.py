import pybithumb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# df = pybithumb.get_ohlcv("BTC")
# df['range']= (df['high']-df['low'])*0.5
# df['target'] = df['open'] + df['range'].shift(1)

def get_ror(k=0.5):
    df = pybithumb.get_ohlcv("BTC")
    df['range'] = (df['high']-df['low'])*k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0032
    df['ror'] =np.where(df['high'] > df['target'],
                        df['close'] / df['target']-fee,
                        1)

    ror = df['ror'].cumprod()[-2]
    return ror, df

def get_hpr(ticker):
    try:
        df = pybithumb.get_ohlcv(ticker)
        df = df.loc['2018']

        df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
        df['range'] = (df['high']-df['low'])*0.8
        df['target'] = df['open'] + df['range'].shift(1)
        df['bull'] = df['open'] > df['ma5']

        fee = 0.0032
        df['ror'] =np.where(df['high'] > df['target'],
                            df['close'] / df['target']-fee,
                            1)

        df['hpr'] = df['ror'].cumprod()
        df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
        return df['hpr'][-2]
    except:
        return 1

df_ror = pd.DataFrame()

for k in np.arange(0.1, 1, 0.1):
    ror, df = get_ror(k)
    df_ror[str(k)] = df['ror']
    

plt.plot(df_ror['0.1'])
#plt.plot(df_ror.loc['0.2'])
plt.show()

# tickers = pybithumb.get_tickers()

# hprs = []
# for ticker in tickers:
#     hpr = get_hpr(ticker)
#     hprs.append((ticker, hpr))

# sorted_hprs = sorted(hprs, key=lambda x:x[1], reverse=True)
# print(sorted_hprs[:5])

# for k in np.arange(0.1, 1.0, 0.1):
#     ror = get_ror(k)
#     print("%.1f %f" % (k, ror))
# df.to_excel("btc.xlsx")
