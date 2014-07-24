#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import redis
from rq import Worker, Queue, Connection

from settings import REDIS_HOST
from settings import REDIS_PORT
from settings import REDIS_DB
from settings import QUEUES_LISTEN


# Get redis url
redis_url = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT)

# Get redis connection
redis_conn = redis.from_url(redis_url)

# Get redis queue object for each listing
qH = Queue('high', connection=redis_conn)
qN = Queue('normal', connection=redis_conn)
qL = Queue('low', connection=redis_conn)

# Create redis database object
rDB = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


if __name__ == '__main__':
    # start a worker
    with Connection(redis_conn):
        worker = Worker(map(Queue, QUEUES_LISTEN))
        worker.work()
