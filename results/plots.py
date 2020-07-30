
import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np
TB = 1024 * 1024 * 1024

# name = 'InfiniteCache_LRU'
# name = '20TB_LRU'
name = '100TB_LRU'


df = pd.read_parquet(name + '.pa')
print("data loaded:", df.shape[0])

print(df)
df['ch_files'] = df['cache hit'].cumsum()
df['CHR files'] = df['ch_files'] / df.index

df['tmp'] = df['cache hit'] * df['kB']
df['ch_data'] = df['tmp'].cumsum()
df['data delivered'] = df['kB'].cumsum()
del df['tmp']
df['CHR data'] = df['ch_data'] / df['data delivered']
df["cache size"] = df["cache size"] / TB
print(df)
f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'hspace': 0.15})

ax22 = ax2.twinx()
f.suptitle(name)
ax1.plot(df["CHR files"])
ax1.plot(df["CHR data"])
ax2.plot(df["reward"].cumsum())
# ax22.plot(df["cache size"])
# ax22.set_ylabel('cache fill [TB]', color='b')
ax22.plot(df["reward"].rolling(5000).mean())
ax22.set_ylabel('rolling reward', color='b')
ax1.legend()
ax2.legend()
ax1.grid(True)
ax2.grid(True)
# plt.tight_layout()
plt.savefig('plots/' + name + '.png')
