#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys

from logger import log
from rottoscraper.db import create_db
from rottoscraper.gui import app
from rottoscraper.scraper import dispatch_website
from rottoscraper.scraper.insert import insert_user

if __name__ == '__main__':
    # set package path in system environmnet path
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./rottoscraper"))
    sys.path.append(path)

    # Create a logs direcory if not exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    if(sys.argv[1]=='app'):
        app.run()
    elif(sys.argv[1]=='scraper'):
        url = 'http://akshayon.net/'
        keywords = ['akshay','sunny','python','pelican','redis','twitter']
        dispatch_website(url, keywords)
    elif(sys.argv[1]=='db' and sys.argv[2]=='create'):
        create_db()
        print 'Successfully created database.'
    else:
        print 'No arguments matched'
