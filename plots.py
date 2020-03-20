
import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np

fn = 'monitoring.h5'
df = None
with pd.HDFStore(fn) as hdf:
    print("keys in file:", fn, ':', hdf.keys())
    df = hdf.select('monitoring')
    print("data loaded:", df.shape[0])

print(df)
df['ch_files'] = df['cache hit'].cumsum()
df['CHR files'] = df['ch_files'] / df.index

df['tmp'] = df['cache hit'] * df['kB']
df['ch_data'] = df['tmp'].cumsum()
df['data delivered'] = df['kB'].cumsum()
del df['tmp']
df['CHR data'] = df['ch_data'] / df['data delivered']
print(df)
f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'hspace': 0.15})

# f.suptitle('Cache hit rates')
ax1.plot(df["CHR files"])
ax1.plot(df["CHR data"])
ax2.plot(df["reward"].cumsum())
# ax2.plot(df["inst chr files"])
# ax2.plot(df["inst chr data"])
ax1.legend()
ax2.legend()
ax1.grid(True)
ax2.grid(True)
# plt.tight_layout()
plt.savefig("CHR_env_.png")
