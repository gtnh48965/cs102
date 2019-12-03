import requests
import cas


def get_page(group: str, week: str = '') -> str:
    if week:
        week = str(week) + '/'
    url = f'{cas.domain}/{group}/{week}raspisanie_zanyatiy_{group}.html'
    response = requests.get(url)
    web_page = response.text
    return web_page
