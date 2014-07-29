#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, nested_scopes

import os

import logbook
from logbook import FileHandler
from logbook import Logger

log = Logger('scraper')

# Create a logs direcory if not exist
if not os.path.exists('logs'):
    os.makedirs('logs')
file_handler = FileHandler('logs/app.log', level=logbook.DEBUG)
file_handler.push_application()
