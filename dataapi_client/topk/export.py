import requests
import json
from pprint import pprint
import sqlite3
from typing import Sequence, Union
import datetime
from datetime import datetime
#from concurrent import futures
#from threading import Thread
#from multiprocessing import Process


API_KEY = '88aed21fec2d4438996d3b62dcf3807c'
ENDPOINT_BASE = 'http://hydra:8000/api/v1/'
ENDPOINT_AUTH = ENDPOINT_BASE + 'topk/authenticate?api={}'
ENDPOINT_EXPORT = ENDPOINT_BASE + 'topk/import/'


def export_topk(api_key: str,
                date: Union[str, datetime.date],
                symbols: Sequence[str],
                blocking: bool = True,
                verbose: bool = True):
    """
    Export top-k prediction to the data server.

    Args:
        api_key:        API key for authentication.
        date:           Date of prediction.
        symbols:        List of predicted symbols.
        blocking:       Wait for IB symbol lookup before returning if true.
        verbose:        Generate verbose output.

    Returns:


    """

    if not blocking:
        raise NotImplementedError('dataapi-client: non-blocking requests not implemented yet.')

    session = requests.Session()
    if verbose:
        print('dataapi-client: session created')
    try:
        auth_result = session.get(ENDPOINT_AUTH.format(API_KEY))
        if verbose:
            print('dataapi-client: authenticated')
    except Exception as e:
        raise ConnectionError('dataapi-client: failed to connect to server: {e}')

    if isinstance(date, str):
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except:
            raise ValueError(f'{date} is not in %Y-%m-%d format')

    else:
        date = datetime.strftime('%Y-%m-%d')

    json_data = {'api': API_KEY,
                 'date': date,
                 'symbols': symbols}

    data = {'csrfmiddlewaretoken': session.cookies['csrftoken'],
            'json_data': json.dumps(json_data)}

    if verbose:
        print('dataapi-client: exporting top-k symbols')
    response = session.post(ENDPOINT_EXPORT, data=data)
    response_json = json.loads(response.content)

    if verbose:
        print('dataapi-client: response:')
        pprint(response_json)

    return response_json


import csv

with open('2020-09-21.csv') as f:
    syms = tuple(s[0] for s in csv.reader(f))

res = export_topk(API_KEY, '2020-09-21', syms, blocking=True)

print('done')
