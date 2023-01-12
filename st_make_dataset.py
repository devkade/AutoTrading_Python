import ccxt
import pandas as pd
import pandas_ta as ta
from get_key import get_key
import stc


api_key, api_secret = get_key("binance")

ticker = "BTC/USDT"
binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit':True
})

btc_ohlcv = binance.fetch_ohlcv(ticker, '4h', limit=2000)

df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
df.set_index('datetime', inplace=True)
percent = int(len(df) * 0.05)
print(percent)
print(df)

pd.set_option('display.max_rows', 200)

period1 = 10
multi1 = 3
period2 = 10
multi2 = 6

df = stc.supertrendcloud(df, period1, period2, multi1, multi2)

df.to_excel('stc.xlsx')
