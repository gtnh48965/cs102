import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    global comentss
    title = []
    coments = []
    url = []
    point = []
    autor = []
    comentss = []
    line = parser.find_all('a', {'storylink'})
    poi = parser.find_all('span', {"score"})
    au = parser.find_all('a', {'hnuser'})
    com = parser.find_all('td', {"subtext"})

    for hit in line:
        title.append(hit.text)
    for a in line:
        url.append(a['href'])
    poin = []
    for i in poi:
        point.append(i.text)

    for pd in point:
        remove = pd.replace(" points", "")
        poin.append(remove)


    for js in au:
        autor.append(js.text)

    s = []
    for ss in com:
        for ls in ss:
            s.append(ls)
    m=len(s)
    for lp in range(15, m, 17):
        coments.append(s[lp])

    list2 = []

    for item in coments:
        if item != ' ':
            list2.append(item)

    for lol in list2:
        comentss.append(lol.text)

    cam = []

    for j in comentss:
        if j !='discuss':
            remove = j.replace("\xa0comments","")
            cam.append(remove)
        else:
            remove = j
            cam.append(remove)

    m =len (cam)

    zs = []
    for i in range(m):
        zs.append({'author': (autor[i]),
                   'comments': (cam[i]),
                   'points': (poin[i]),
                   'title': (title[i]),
                   'url': (url[i])})
    parser = zs

    return parser


def extract_next_page(parser):
    """ Extract next page URL """
    # PUT YOUR CODE HERE

    return parser.find('a', {'morelink'})['href']




def get_news(url="https://news.ycombinator.com/newest", n_pages=35):
    """ Collect news from a given web page """
    news = []

    while n_pages:

        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)

        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1

    return news

