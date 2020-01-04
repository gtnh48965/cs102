# coding=utf-8
import config
import gensim
import pyLDAvis.gensim
import re
import requests

from stop_words import get_stop_words
from string import punctuation


def get_wall(
        owner_id: str = '',
        domain: str = '',
        offset: int = 0,
        count: int = 10,
        filter: str = 'owner',
        extended: int = 0,
        fields: str = '',
        v: str = '5.103'):
    code = ("return API.wall.get({" +
            f"'owner_id': '{owner_id}'," +
            f"'domain': '{domain}'," +
            f"'offset': {offset}," +
            f"'count': {count}," +
            f"'filter': '{filter}'," +
            f"'extended': {extended}," +
            f"'fields': '{fields}'," +
            f"'v': {v}," +
            "});")

    response = requests.post(
        url="https://api.vk.com/method/execute",
        data={
            "code": code,
            "access_token": config.VK_CONFIG['access_token'],
            "v": v
        }
    )

    resp = []
    for i in range(count):
            resp.append(response.json()['response']['items'][i]['text'])
    return resp


def stopwords(text):
    text = [[j for j in text[k] if j not in stop_words] for k in range(len(text))]
    return text


def symbols(text):
    upd = []
    new_text = []
    for j in text:
        for word in j:
            word = ''.join(ch for ch in word if ch not in punctuation and ch != 'В«' and ch != 'В»')
            emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"u"\U0001F1E0-\U0001F1FF""]+", flags=re.UNICODE)
            if not word.isalpha():
                continue
            if len(word) > 4:
                continue
            upd.append(emoji_pattern.sub(r'', word))
        new_text.append(upd)
        upd = []
    return new_text


if __name__=='__main__':
    stop_words = get_stop_words('russian')
    wall = []
    for i in range(2):
        for group in ['itmoru']:
            wall.extend(get_wall(domain=group, count=100, offset=100 * i))

    texts = [[text.lower() for text in lst.split()] for lst in wall]
    texts = stopwords(texts)
    texts = symbols(texts)


    dictionary = gensim.corpora.Dictionary(texts)
    full_text = []
    for i in range(len(texts)):
        full_text.extend(texts[i])
    corpus = [dictionary.doc2bow(full_text)]

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=dictionary,
                                                num_topics=10,
                                                alpha='auto',
                                               per_word_topics=False)

    vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
    pyLDAvis.save_html(vis, 'LDA.html')
    pyLDAvis.show(data=vis, open_browser=True)
