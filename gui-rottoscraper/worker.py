#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rq import Worker, Queue, Connection
from redis import Redis
from settings import REDIS_HOST, REDIS_PORT, QUEUES_LISTEN

# Tell RQ what Redis Connection to Use
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, QUEUES_LISTEN))
        worker.work()
