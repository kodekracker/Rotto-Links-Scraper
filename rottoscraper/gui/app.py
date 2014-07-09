#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import settings
from flask import Flask
from flask import request
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template
from flask import flash
from flask import make_response
from flask import jsonify
from flask.views import MethodView
from Rotto-Links-Scraper.rottoscraper import Crawler

class RottoView(MethodView):
    def get(self):
        return render_template('main.html')

q = Queue('high', connection=redis_conn)

app = Flask(__name__)
app.config.from_object(settings)


app.add_url_rule('/', view_func=RottoView.as_view('rotto_view'),
    methods=['GET',])


# api's decorator
@app.route('/api/v1.0/', methods=['OPTIONS','POST'])
def add_job():
    try:
        if request.method == 'OPTIONS':
            return make_response(jsonify({"Allow":"POST"}), 200)

        if not request.json or not is_payload_ok(request.json):
            abort(400)
        #add job in queue
        job = q.enqueue(start_crawl, url)
        job_key = job.key.replace("rq:job:", "")
        return make_response(jsonify(response),200)
    except Exception as e:
        response = 'Internal Error,Please Try Again.'
        return make_response(jsonify({'error': response}), 202)

@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()
