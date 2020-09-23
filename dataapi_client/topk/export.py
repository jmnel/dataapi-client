import requests
import json
from pprint import pprint
import sqlite3
from typing import Sequence, Union, Optional
import datetime
from datetime import datetime

from ..api import ApiConfig

ENDPOINT_BASE = 'https://data.jmnel.com/api/v1/'
ENDPOINT_AUTH = ENDPOINT_BASE + 'topk/authenticate?api={}'
ENDPOINT_EXPORT = ENDPOINT_BASE + 'topk/import/'


def export_topk(date: Union[str, datetime.date],
                symbols: Sequence[str],
                api_key: Optional[str] = None,
                blocking: bool = True,
                verbose: bool = False):
    """
    Export top-k prediction to the data server.

    Args:
        date:           Date of prediction.
        symbols:        List of predicted symbols.
        api_key:        API key for authentication.
        blocking:       Wait for IB symbol lookup before returning if true.
        verbose:        Generate verbose output.

    Returns:


    """

    if api_key is None or api_key == '':
        if ApiConfig.api_key is None or ApiConfig.api_key == '':
            raise ValueError('dataapi-client: API key not provided')
        else:
            api_key = ApiConfig.api_key

    if not blocking:
        raise NotImplementedError('dataapi-client: non-blocking requests not implemented yet.')

    session = requests.Session()
    if verbose:
        print('dataapi-client: session created')
    try:
        auth_result = session.get(ENDPOINT_AUTH.format(api_key))
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

    json_data = {'api': api_key,
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
