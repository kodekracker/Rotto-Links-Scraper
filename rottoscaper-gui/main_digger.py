# -*- coding: utf-8 -*-
"""
    digger
    ~~~~~~
"""

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack

# configuration
DATABASE = ''
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('DAEMONFLASK_SETTINGS', silent=True)


@app.route('/')
def show_page():
    return render_template('search.html')


if __name__ == '__main__':
    app.run()