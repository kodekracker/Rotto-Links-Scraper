#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
from gui import settings
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
from rq import Queue, get_current_job
from rq.job import Job
from redis import Redis
from worker import redis_conn
from scraper import Crawler


class RottoView(MethodView):
    def get(self):
        return render_template('main.html')

q = Queue('high', connection=redis_conn)

app = Flask(__name__)
app.config.from_object(settings)


app.add_url_rule('/', view_func=RottoView.as_view('rotto_view'),
    methods=['GET',])

# task to do by worker
def crawl(payload):
    cr = Crawler(payload['url'],payload['keywords'])
    cr.start()
    results = cr.get_results()
    return results

def is_contain(payload,*args):
    for a in args:
        if not a in payload:
            return False
    return True


# api's decorator
@app.route('/api/v1.0/crawl/', methods=['OPTIONS','POST'])
def add_job():
    response = {}
    try:
        if request.method == 'OPTIONS':
            return make_response(jsonify({"Allow":"POST"}), 200)

        if not request.json or not is_contain(request.json,'url','keywords','email'):
            abort(400)
        #add job in queue
        job = q.enqueue(crawl, request.json)
        job_key = job.key.replace("rq:job:", "")
        response['job_key'] = job_key
        response['job_url'] = url_for('get_results', job_key = job_key,_external=True)
        response['message'] = 'job added'
        return make_response(jsonify(response),200)
    except Exception as e:
        response['error'] = str(e)
        return make_response(jsonify(response), 202)


@app.route('/api/v1.0/crawl/<string:job_key>',methods=['GET'])
def get_results(job_key):
    response = {}
    res_code = None;
    try:
        job = Job.fetch(job_key, connection=redis_conn)
        job_key = job.key.replace("rq:job:", "")
        if(not job.is_finished):
            response['status'] = 'pending'
        else:
            response['status'] = 'completed'
            response['result'] = job.result
        res_code = 200
    except Exception as e:
        response['error'] = 'No Job Found'
        res_code = 202
    return  make_response(jsonify(response),res_code)

# app error handler
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
