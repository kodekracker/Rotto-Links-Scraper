#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, nested_scopes

import logbook
from logbook import FileHandler
from logbook import Logger

log = Logger('scraper')

file_handler = FileHandler('logs/app.log', level=logbook.DEBUG)
file_handler.push_application()
