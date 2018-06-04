from flask import Flask, jsonify, send_from_directory
from db_link import Post
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)

METRICS = ['likes', 'views', 'dislikes', 'comments']
RUBRICS = ['economy', 'society', 'atomtec', 'teplo', 'space', 'science', 'religion', 'ecology_news', 'mediawars']

def abort_if_metric_doesnt_exist(metric):
    if metric not in METRICS:
        abort(404, message="This metric {} doesn't exist".format(metric))

class Ria(Resource):
    def get(self, metric):
        abort_if_metric_doesnt_exist(metric)
        arr = []
        for i in Post.objects():
            if i.published > datetime.today() - timedelta(days=1):
                if len(i.metrics) > 0:
                    d = {}
                    if i.url.split('/')[3] not in RUBRICS:
                        continue
                    for k,v in i.metrics.items():
                        d[k] = int(v)
                    d['url'] = i.url
                    d['title'] = i.title
                    d['rubric'] = i.url.split('/')[3]
                    d['published'] = i.published.strftime("%d %b в %H:%M")
                    arr.append(d)
        #s = sorted(arr, key=lambda k: int(k[metric]), reverse=True)
        return jsonify({'data': arr})

    def delete(self):
        pass

    def put(self):
        pass

@app.route('/ria_top')
def root():
    return app.send_static_file('index.html')

api.add_resource(Ria, '/ria_top/<metric>')
