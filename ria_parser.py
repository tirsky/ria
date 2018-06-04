import sys
import requests
from bs4 import BeautifulSoup
import datetime
today = datetime.date.today()

def get_ria_archive():
    date = today.strftime('%Y%m%d')
    url = 'https://ria.ru/archive/{}/'.format(date)
    print(url)
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    for each_div in soup.findAll("div", {"class": "b-list__item"}):
        for item in each_div.find_all('a', href=True):
            url = 'https://ria.ru{}'.format(item['href'])
            get_stat(item.text, url, item.img['src'])
            
def get_stat(title,url,img):
    print('stat', url)
    url = url.replace('https://ria.ruhttps://','https://')
    stop_urls = ['realty', 'tourism']
    for u in stop_urls:
        if u in url:
            return
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    print(title, url,img)
    for each_div in soup.findAll("div", {"class": "b-article__info-statistic"}):
        for item in each_div.find_all('span', {'class' : 'b-statistic__number'}):
            print(item.text)


get_ria_archive()
