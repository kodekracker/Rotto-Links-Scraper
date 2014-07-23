#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, nested_scopes

import time

from rq import Queue
from rq.job import Job
from redis import StrictRedis

from logger import log
from worker import redis_conn
from rottoscraper.scraper.rotto import Website, Page

# Redis queue object
q = Queue('high', connection=redis_conn)


def crawl_page(website, page):
    """
    Crawl a single page at a time and checks is job of crawling
    a website done or not and take required steps
    """
    try:
        # Create redis object
        r = StrictRedis(host='localhost', port=6379, db=0)

        log.debug('Crawling :: %s', page.url)

        # get page content
        log.info('Getting Page Content :: %s' % (page.url))
        page.get_content()

        # get keywords matched
        keys = page.get_keywords_matched(website.aho)
        log.info('Matched Keywords :: %s' % (keys))

        # get external links
        # page.get_external_links()
        log.info('Found External Links :: %d' % (len(page.external_links)))

        # get internal links
        page.get_internal_links(website)
        log.info('Found Internal Links :: %d' % (len(page.internal_links)))

        # get status code of all links
        log.info('Getting Status of all Links')
        page.get_status_codes_of_links(website)

        log.info('Enqueueing New Jobs ')
        # enqueue the un-broken internal links
        for p in page.crawl_pages:
            log.info('Enqueued :: %s' % (p.url))
            r.incr(website.url+':pages_queued')
            q.enqueue(crawl_page, website, p)


        log.info('Adding Result to website')
        # add rotto links to result
        if page.rotto_links:
            # log.info('Broken Links Found :: %s', page.rotto_links)
            website.add_to_result(page.url, page.rotto_links, page.matched_keywords)

        log.debug('Crawled :: %s' % (page.url))

        # increment website crawled page counter
        r.incr(website.url+':pages_crawled')

        log.info('Pages Queued:: %s' % (r.get(website.url+':pages_queued')))
        log.info('Pages Crawled:: %s' % (r.get(website.url+':pages_crawled')))


        # checks if website crawled completely or not
        if r.get(website.url+':pages_queued')==r.get(website.url+':pages_crawled'):
            log.info('Website %s crawled Completely' % (website.url))
            # save results to database
            log.info('Saving results to database')
            # send the email to user
            log.info('Sending email to user')

    except Exception as e:
        log.exception('Error in crawling :: %s ' % (page.url))
    return website


def start_dispatcher(url, keywords):
    """
    Dispatcher to start crawling of a website
    """
    try:
        log.debug('Dispatcher Start :: %s'%(url))

        # Create redis object
        r = StrictRedis(host='localhost', port=6379, db=0)

        # create and set website and page object for a job
        website = Website(url, keywords)
        website.preInit()
        page = Page(website.url, website.url)

        # set website completion variables in redis db
        r.set(website.url+':pages_queued', 1)
        r.set(website.url+':pages_crawled', 0)

        # Enqueue job in redis-queue
        job = q.enqueue(crawl_page, website, page)

        log.debug('Job Added in Queue :: %s' %(url))
    except Exception as e:
        log.exception('Error occurred in dispatcher')
