#! /usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import local

def app():
    local('python rottoscraper/run.py app')

def dispatcher():
    local('python rottoscraper/run.py dispatcher')

def worker():
    local('python rottoscraper/worker.py')
