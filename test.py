import csv

import dataapi_client

API_KEY = '88aed21fec2d4438996d3b62dcf3807c'

dataapi_client.ApiConfig.api_key = API_KEY

with open('2020-09-21.csv') as f:
    syms = tuple(s[0] for s in csv.reader(f))


res = dataapi_client.topk.export(date='2020-09-21', symbols=syms, blocking=True, verbose=False)

# print('done')
