import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    # PUT YOUR CODE HERE
    res = requests.Sessions()

    retry = Retry(max_retries, max_retries, max_retries, backoff_factor=backoff_factor)
    adapter = HTTPAdapter(max_retries=retry)
    res.mount('http://', adapter)
    res.mount('https://', adapter)
    try:
        response =requests.get(url, params, timeout=timeout)
        response.raise_for_status()  # выдает исключение при ошибке 500
    except Exception as e:
        print(e)

    else:
        return response

def get_friends(user_id, fields=''):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE
    domain = config.VK_CONFIG['domain']
    access_token = config.VK_CONFIG['access_token']
    v = '5.103'

    query = f'{domain}/friends.get?user_id={user_id}&fields={fields}&access_token={access_token}&v={v}'
    response = requests.get(query)
    return response.json()['response']['items']



def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE
