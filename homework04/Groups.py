import pandas as pd
import requests
import textwrap

from gensim import corpora, models
from gensim.utils import simple_preprocess

from time import sleep
# from stopwords import stop_words

import config


def get_wall(
        owner_id: str = '',
        domain: str = '',
        offset: int = 0,
        count: int = 100,
        filt: str = 'owner',
        extended: int = 0,
        fields: str = '',
        v: str = '5.103',
        n_queries: int = 25) -> pd.DataFrame:
    code = 'return ['
    for i in range(n_queries):
        query = {
            'owner_id': owner_id,
            'domain': domain,
            'offset': (offset + i) * count,
            'count': count,
            'filt': filt,
            'extended': extended,
            'fields': fields,
            'v': v
        }
        code += f'API.wall.get({str(query)})'
        if i < n_queries - 1:
            code += ', '
        else:
            code += '];'

    response = requests.post(
        url="https://api.vk.com/method/execute",
        data={
            "code": code,
            "access_token": config.VK_CONFIG['access_token'],
            "v": v
        }
    )
    return response


def post(
    domain: str='',
    num_topics: int=5,
    num_words: int=8,
    passes: int=5,
    max_requests: int=4):
    offset = 0
    texts = []
    end = False
    n = 0
    while True:
        queries = get_wall(domain=domain, offset=offset).json()['response']
        for q in queries:
            posts = q['items']
            if len(posts):
                for p in posts:
                    texts.append(p['text'])
                    n += 1
            else:
                end = True
                break
        if end:
            break
        offset += 2500
        # print(offset)
        sleep(0.35)
        if offset >= max_requests * 2500:
            break
    print(f'Parsed {n} posts')
    

