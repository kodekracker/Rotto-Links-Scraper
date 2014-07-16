#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from rq import Queue
from rq.job import Job
from redis import Redis
from worker import redis_conn
from scraper.rotto import Website, Page

q = Queue('high', connection=redis_conn)

def crawl_page(website, page):

    print 'Crawling :: ', page.url
    # get page content
    page.get_content()

    # get keywords matched
    page.get_keywords_matched(website.aho)

    # get external links
    page.get_external_links()

    # get internal links
    page.get_internal_links()

    # get status code of all links
    page.get_status_codes_of_links()

    # enqueue the un-broken internal links
    for p in page.crawl_pages:
        q.enqueue(crawl_page, website, p)

    # add rotto links to result
    if page.rotto_links:
        website.add_to_result(page.url, page.rotto_links, page.matched_keywords)


def start_dispatcher(url, keywords):
    try:
        print 'Dispatcher Start'
        website = Website(url, keywords)
        website.preInit()
        page = Page(website.host_url, website.host_url)
        job = q.enqueue(crawl_page, website, page)
        print 'Your job is in processing state'
    except Exception as e:
        print 'Error occurred in dispatcher :: ', e
