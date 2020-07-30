# from Rucio traces extract all the paths accessed by MWT2 jobs not running via VP.
# store all the data in a parque file (pyarrow engine)

from time import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import pandas as pd
from secret import es_auth

pq = 'MWT2'
# pq = 'ALL'

es = Elasticsearch(hosts=['http://atlas-kibana.mwt2.org:9200'], http_auth=es_auth)
print(es.ping())

dt = 30 * 86400
query = {
    "size": 0,
    "_source": ["scope", "dataset", "filename", "timeStart", "filesize"],
    "query": {
        "bool": {
            "must": [
                {"term": {"eventType": "get_sm_a"}},
                {"term": {"pq": pq}},
                {"range": {"timeStart": {"gt": int(time() - dt), "format": "epoch_second"}}},
                {"exists": {"field": "filesize"}}
            ]
        }
    }
}
print("Query:\n",query)
data = []
count = 0

es_response = scan(es, index='*rucio-traces-2020*',  query=query)
# es_response = scan(es, index='rucio_traces',  query=query, request_timeout=60)
for item in es_response:
    sou = item['_source']
    doc = [
        sou['scope'],
        sou['dataset'],
        sou['filename'],
        sou['timeStart'],
        sou['filesize']
    ]
#     print(doc)
    data.append(doc)

    if count and not count % 1000:
        print(count)
    count += 1

print(count)

all_accesses = pd.DataFrame(data).sort_values(4)
all_accesses.columns = ['scope', 'dataset', 'filename', 'timeStart', 'filesize']
# all_accesses.set_index('filename', drop=True, inplace=True)
all_accesses.to_parquet(pq + '.pa', engine='pyarrow')
