#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

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
from flask.ext.cors import cross_origin
from werkzeug.contrib.fixers import ProxyFix

import config
from db import Database

class AppView(MethodView):
    def get(self):
        return render_template('main.html')

app = Flask(__name__)
app.config.from_object(config)
# required for gunicorn
app.wsgi_app = ProxyFix(app.wsgi_app)

app.add_url_rule('/', view_func=AppView.as_view('app_view'), methods=['GET',])

def is_contain(payload,*args):
    for a in args:
        if not a in payload:
            return False
    return True


# api's decorator
@app.route('/api/v1.0/crawl/', methods=['OPTIONS','POST'])
@cross_origin(headers=['Content-Type']) # Send Access-Control-Allow-Headers
def add_website():
    response = {}
    try:
        if request.method == 'OPTIONS':
            return make_response(jsonify({"Allow":"POST"}), 200)

        if not request.json or not is_contain(request.json,'url','keywords','email_id'):
            abort(400)

        #add website in database for processing
        website = Database.add_request(request.json)
        response = website
        return make_response(jsonify(response),200)
    except Exception as e:
        response['error']= 'Internal Error, Please Try Again.'
        return make_response(jsonify(response), 202)


@app.route('/api/v1.0/crawl/<string:website_id>',methods=['GET'])
def get_results(website_id):
    response = {}
    try:
        res_code = None;
        if not Database.website_exists(id=website_id):
            response['error'] = 'No Such Job Found'
            res_code = 202
        else:
            website = Database.fetch_website(id=website_id)
            response = website
            res_code = 200
        return  make_response(jsonify(response),res_code)
    except Exception as e:
        response['error']= 'Internal Error, Please Try Again.'
        return make_response(jsonify(response), 202)

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
