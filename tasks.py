from celery import Celery
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
today = datetime.today()
from db_link import Post
from time import sleep

app = Celery()
RUBRICS = ['economy', 'society', 'atomtec', 'teplo', 'space', 'science', 'religion', 'ecology_news', 'mediawars']

@app.task()
def parse_archive():
    date = today.strftime('%Y%m%d')
    url = 'https://ria.ru/archive/{}/'.format(date)
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    for each_div in soup.findAll("div", {"class": "b-list__item"}):
        for item in each_div.find_all('a', href=True):
            url = 'https://ria.ru{}'.format(item['href'])
            url = url.replace('https://ria.ruhttps://','https://')
            title = item.text
            img = item.img['src']
            post = Post(
                title=title,
                url=url,
                img=img
            )
            if len(Post.objects(title=title)) == 0:
                print('save')
                post.save()       # This will perform an insert


@app.task()
def check_metrics():
    for post in Post.objects():
        if post.published > (datetime.today() - timedelta(days=1)):
            sleep(2)
            post.url = post.url.replace('https://ria.ruhttps://','https://')
            if post.url.split('/')[3] not in RUBRICS:
                continue
            r = requests.get(post.url)
            html_doc = r.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            arr_stat = []
            for each_div in soup.findAll("div", {"class": "b-article__info-statistic"}):
                for item in each_div.find_all('span', {'class' : 'b-statistic__number'}):
                    arr_stat.append(item.text)
            arr_metrics = ['comments', 'views', 'likes', 'dislikes']
            dict_metrics = {}
            for i,j in zip(arr_metrics,arr_stat):
                dict_metrics[i] = j
            post.update(set__metrics__=dict_metrics)
            print('Metrics ok')

app.conf.beat_schedule = {
    'planner': {
        'task': 'tasks.parse_archive',
        'schedule': 60.0,
    },
     'planner1': {
         'task': 'tasks.check_metrics',
         'schedule': 1800.0,
     },
}
