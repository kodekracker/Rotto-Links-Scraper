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


app = Flask(__name__)
app.config.from_object(settings)

@app.route('/')
def show_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
