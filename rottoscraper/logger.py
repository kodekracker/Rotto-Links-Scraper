#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, nested_scopes

import os

import logbook
from logbook import FileHandler
from logbook import Logger

from config import LOGS_DIR

log = Logger('scraper')

# Create a logs direcory if not exist
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
log_file_name = 'rottoscraper.log'
file_handler = FileHandler(LOGS_DIR + log_file_name, level=logbook.DEBUG)
file_handler.push_application()
