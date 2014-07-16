#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
from scraper.task import start_dispatcher

if __name__ == '__main__':
    start_time = time.time()
    # set package path in system environmnet path
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
    sys.path.append(path)
    if(len(sys.argv)!=2):
        app.run()
    else:
        if(sys.argv[1]=='app'):
            app.run()
        elif(sys.argv[1]=='scraper'):
            url = 'http://akshayon.net'
            keywords = ['akshay','sunny','python','pelican','redis','twitter']
            start_dispatcher(url, keywords)
            print "\nElapsed Time: %s sec. " % (time.time() - start_time)
