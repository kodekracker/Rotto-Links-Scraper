#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys

from db import Database
from gui import app
from scraper import dispatcher

if __name__ == '__main__':
    if(sys.argv[1]=='app'):
        app.run()
    elif(sys.argv[1]=='dispatcher'):
        dispatcher()
    elif(sys.argv[1]=='db' and sys.argv[2]=='create'):
        Database.create()
        print 'Successfully created database.'
    else:
        print 'No arguments matched'
