#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, nested_scopes

from logbook import FileHandler
from logbook import Logger

handler = FileHandler('logs/app.log')
log = Logger('scraper')
handler.push_application()
