reset should return first access (first state)
add visualization on cache hit rate.
add actor cleaning step: 
* move from hwm/lwm cleanup to cleanup for each file and have hwm:98%
* ask actor for decission to remove or not. List files in order of LRU. Signal to not learn is given by listing file size as negative value. 

# input generation
values:
1. filesize 
2. scope index
3. dataset index
4. filename index
5. 10 tokens
    * remove scope tokens from dataset and filename tokens
    * remove dataset tokens from filename tokens


WHY IS INSPECTOR SO F... SLOW?