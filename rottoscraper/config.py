#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
# configuration

DEBUG = True
SECRET_KEY='\xb1\x85s\xe7\xa9\xcc\xe9C\xabq+\xcb/Nf\xea\x18C>\xfe:\xf8QY',
USERNAME = 'admin'
PASSWORD = 'admin'

DATABASE_URI = 'sqlite:///' + os.getenv('DATABASE_PATH', None) + 'rottoscraper.db'

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# You can also specify the Redis DB to use
REDIS_DB = 0
# REDIS_PASSWORD = 'very secret'

# Queues to listen on
QUEUES_LISTEN = ['high', 'normal', 'low']

# Mail Details
FROM = 'Rotto Links Scaper<noreply@rottoscraper.com>'

# SMTP Cerendentials
SMTP_USER = os.getenv('SMTP_USER', None)
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', None)

# Logs DIR Path
LOGS_DIR = os.getenv('LOGS_DIR', 'logs/')
