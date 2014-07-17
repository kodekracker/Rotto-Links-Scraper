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
    try:
        print '--> Crawling :: ', page.url
        # get page content
        page.get_content()
        print '--> Page Content :: '

        # get keywords matched
        keys = page.get_keywords_matched(website.aho)
        print '--> Matched Keywords :: ', keys

        # get external links
        page.get_external_links()
        print '--> Found External Links :: ', len(page.external_links)

        # get internal links
        page.get_internal_links()
        print '--> Found Internal Links :: ', len(page.internal_links)

        # get status code of all links
        print '--> Getting Status of all Links '
        page.get_status_codes_of_links(website)

        print '--> Enqueueing New Jobs '
        # enqueue the un-broken internal links
        for p in page.crawl_pages:
            print '\t Enqueued :: ',p.url
            q.enqueue(crawl_page, website, p)

        print '--> Adding Result '
        # add rotto links to result
        if page.rotto_links:
            print '\t Broken Links Found :: ', page.rotto_links
            website.add_to_result(page.url, page.rotto_links, page.matched_keywords)

        print '--> Crawled :: ', page.url
    except Exception as e:
        print '--> Error in crawl %s :: %s '% (page.url, str(e))
    return website

def start_dispatcher(url, keywords):
    try:
        print 'Dispatcher Start'
        website = Website(url, keywords)
        website.preInit()
        page = Page(website.host_url, website.host_url)
        job = q.enqueue(crawl_page, website, page)

        while not job.is_finished:
            if job.is_failed:
                print 'Job Failed'
                break
            pass
        wb = job.result
        print type(wb)
        print 'Job Compeleted'
    except Exception as e:
        print '--> Error occurred in dispatcher :: ', e
