
from statistics import median
from typing import Optional
import requests
from api import get_friends
import datetime
# from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE
    res= get_friends(user_id, 'bdate')
    namber = res['count']
    namber = int(namber) - 1
    resp=[]
    new = datetime.datetime.today()
    year = new.year
    year = year % 2000
    for i in range(0, namber):
        if res['items'][i].get('bdate') != None:
            if len(res['items'][i].get('bdate')) > 5:
                resp.append(res['items'][i].get('bdate'))

    nan = len(resp)
    for j in range(0, nan):
        s = resp[j]
        resp[j] = s[-4:]
    oll = []

    result = [int(item) for item in resp]

    for k in range(0, nan):
        if result[k] >= 2000:
            s = abs(result[k] % 2000 - year)
            oll.append(s)
        else:
            s = abs(result[k] - 2000) + year
            oll.append(s)


    if len(oll):
        return median(oll)
    else:
        return None


age_predict(394254792)