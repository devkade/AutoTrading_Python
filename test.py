import pandas as pd

df = pd.DataFrame([[1, 2, 3],[0.1, 0.2, 0.3]], columns=['a', 'b', 'c'])

f = df['a']
s = df['b']
t = df['c']

p = [f-s, f-t, t-s]
print(p)
ab = pd.concat(p, axis=1)
print(ab)