from mongoengine import *
connect('mongoengine_ria', host='localhost', port=27017)

import datetime

class Post(Document):
    title = StringField(required=True, max_length=10000)
    url = StringField(required=True)
    img = StringField(required=True, max_length=1000)
    published = DateTimeField(default=datetime.datetime.now)
    metrics = DictField()
