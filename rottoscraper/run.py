#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import sys
import logging
import logging.config

from scraper.task import start_dispatcher

def setup_logging(default_path='logging-conf.json',default_level=logging.INFO,env_key='LOG_CFG'):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f.read())
        print config
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

if __name__ == '__main__':
    # set package path in system environmnet path
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
    sys.path.append(path)

    # setup logging configuration
    setup_logging()

    if(len(sys.argv)!=2):
        app.run()
    else:
        if(sys.argv[1]=='app'):
            app.run()
        elif(sys.argv[1]=='scraper'):
            url = 'http://akshayon.net'
            keywords = ['akshay','sunny','python','pelican','redis','twitter']
            # start_dispatcher(url, keywords)
