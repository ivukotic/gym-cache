
import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np
TB = 1024 * 1024 * 1024
df = None
names = ['20TB_LRU', '100TB_LRU', 'InfiniteCache_LRU']


f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'hspace': 0.15})
f.suptitle(' '.join(names))

for name in names:

    with pd.HDFStore(name + '.h5') as hdf:
        print("keys:", hdf.keys())
        df = hdf.select(name)
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

    # ax22 = ax2.twinx()
    ax1.plot(df["CHR files"], label=name)
    ax2.plot(df["CHR data"], label=name)

    # ax2.plot(df["reward"].cumsum())
    # ax22.plot(df["cache size"])
    # ax22.set_ylabel('cache fill [TB]', color='b')
    # ax22.plot(df["reward"].rolling(500).sum())
    # ax22.set_ylabel('rolling reward', color='b')

ax1.legend()
ax2.legend()
ax1.set_ylabel('cache hit rate [files]')
ax2.set_ylabel('cache hit rate [data]')
ax2.set_xlabel('files accessed')
ax1.grid(True)
ax2.grid(True)
# plt.tight_layout()
plt.savefig('plots/combinations/combination.png')
