import numpy as np
import pandas as pd


pq = 'ANALY_MWT2_UCORE'
with pd.HDFStore(pq + '.h5') as hdf:
    print("keys:", hdf.keys())
    data = hdf.select('data')

print(data.head(10))

toRemove = ['um', 'user']
tIndices = [[], [], [], [], [], []]  # only scope and first five tokens remembered.
fileIDs = {}


def cleanTokens(scope, toks):
    result = [scope]
    for t in toks:
        t = t.strip('_')
        if t.isdigit():
            continue
        if len(t) < 3:
            continue
        if t in toRemove:
            continue
        result.append(t)
    return result


def indexTokens(toks):
    result = [0, 0, 0, 0, 0, 0]
    c = 0
    for t in toks:
        if t not in tIndices:
            tIndices.append(t)
        result[c] = tIndices.index(t)
        c += 1
    return result


AT = []
fIDcounter = 0
i = 0
# for i in range(10):
# for i in range(data.shape[0]):
# dser = data.iloc[i, :]
for _index, dser in data.iterrows():
    # print(i, dser)
    sc = dser.scope
    ds = dser.dataset.replace(':', '.').split('.')
    fn = dser.filename.replace(':', '.').split('.')
    ts = dser.timeStart
    fs = dser.filesize // 1024
    if dser.filename not in fileIDs:
        fileIDs[dser.filename] = fIDcounter
        fIDcounter += 1
    fID = fileIDs[dser.filename]

    # print(sc)
    # print(ds)
    # print(fn)

    # print("---------------------------")
    if sc in ds:
        ds.remove(sc)
    # if sc in fn:
    #     fn.remove(sc)
    # for t in ds:
        # if t in fn:
        # fn.remove(t)
    # tokens = set(ds)
    # tokens |= set(fn)
    # for t in tokens:
        # if t in AT.keys():
        # AT[t] += 1
        # else:
        # AT[t] = 1
    tokens = cleanTokens(sc, ds)
    # print(sc)
    # print(ds)
    # print(fn)
    # print(tokens)
    tIs = indexTokens(tokens[0:6])
    # print(tIs)
    tIs.extend([ts, fs, fID])
    AT.append(tIs)
    # print("===========================")
    if i % 10000 == 0:
        print('done:', i)
    i += 1

# print(AT)
all_tokens = pd.DataFrame(AT)
all_tokens.columns = ['1', '2', '3', '4', '5', '6', 'time', 'kB', 'fID']
all_tokens.sort_values(by='time', axis='index', inplace=True, ascending=True)
all_tokens.set_index('time', inplace=True)
print(all_tokens.head(15))

all_tokens.to_hdf(pq + '_processed.h5', key='data', mode='w', complevel=1)
