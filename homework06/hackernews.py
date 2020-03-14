import ipaddress

from bottle import (
    route, run, template, request, redirect
)
from sqlalchemy.orm import load_only
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
from scraputils import get_news
new= get_news(url="https://news.ycombinator.com/newest", n_pages=1)

@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # PUT YOUR CODE HERE

    s = session()
    label = request.query.label
    nam_id = request.query.id
    news = s.query(News).filter(News.id == nam_id).one()
    news.label = label
    s.commit()
    redirect("/news")



@route("/update")
def update_news():
    # PUT YOUR CODE HERE
    s = session()
    new = get_news("https://news.ycombinator.com/newest", 1)
    old = s.query(News).all()
    old_ta = [(news.title, news.author) for news in old]
    for i in new:
        if (i['title'], i['author']) not in old_ta:
                news = News(title= i['title'],
                        author=i['author'],
                        url=i['url'],
                        comments=i['comments'],
                        points=i['points'])
                s.add(news)
        s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    s=session()

    classif = NaiveBayesClassifier()
    train_news = s.query(News).filter(News.label is not None).options(load_only("title", "label")).all()

    x_train = [row.title for row in train_news]
    y_train = [row.label for row in train_news]

    classif.fit(x_train, y_train)
    test_news = s.query(News).filter(News.label is None).all()

    x = [row.title for row in test_news]
    labels = classif.predict(x)

    good = [test_news[i] for i in range(len(test_news)) if labels[i] == 'good']

    maybe = [test_news[i] for i in range(len(test_news)) if labels[i] == 'maybe']

    never = [test_news[i] for i in range(len(test_news)) if labels[i] == 'never']

    return template('recommendations_template',
                    {'good': good, 'never': never, 'maybe': maybe})







if __name__ == "__main__":
    run(host="localhost", port=8080)

