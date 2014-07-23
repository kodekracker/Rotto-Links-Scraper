#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, nested_scopes

import os
import json
import sys
import logging
import logging.handlers

from logger import log
from rottoscraper.gui import app
from rottoscraper.scraper.task import start_dispatcher


if __name__ == '__main__':
    # set package path in system environmnet path
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "/rottoscraper"))
    sys.path.append(path)

    # Create a logs direcory if not exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    if(len(sys.argv)!=2):
        app.run()
    else:
        if(sys.argv[1]=='app'):
            app.run()
        elif(sys.argv[1]=='scraper'):
            url = 'http://akshayon.net'
            keywords = ['akshay','sunny','python','pelican','redis','twitter']
            start_dispatcher(url, keywords)
        else:
            print 'You entered wrong arguments'
