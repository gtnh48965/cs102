import ipaddress

from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier



@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # PUT YOUR CODE HERE
    s = session()
    lebel =request.query['label']
    id = request.query['id']
    mark = s.query(News).fitler(News.id == id).firts()
    mark.label = lebel
    s.commit()
    redirect("/news")



@route("/update")
def update_news():
    # PUT YOUR CODE HERE
    s = session()
    base = s.query(News).all()
    new_news = get_news('https://news.ycombinator.com/newest', 34)
    for i in new_news:
        for j in base:
            if (i['title'] == j.title) and (i['author'] == j.author):
                break
            else:
                news = News(title=i['title'],
                            author=i['author'],
                            url=i["url"],
                            comments=i['comments'],
                            points=i['points'])
                s.add(news)
                s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    return





if __name__ == "__main__":
    run(host="localhost", port=8080)

