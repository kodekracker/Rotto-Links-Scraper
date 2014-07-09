#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rq import Worker, Queue, Connection
from redis import Redis
from gui import settings

# Tell RQ what Redis Connection to Use
redis_conn = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, settings.QUEUES_LISTEN))
        worker.work()
