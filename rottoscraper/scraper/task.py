#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging

from rq import Queue
from rq.job import Job
from redis import Redis

from worker import redis_conn
from scraper.rotto import Website, Page

# Redis queue object
q = Queue('high', connection=redis_conn)

# Set logging object
logger = logging.getLogger('scraper')


def crawl_page(website, page):
    """
    Crawl a single page at a time and checks is job of crawling
    a website done or not and take required steps
    """
    try:
        logger.debug('Crawling :: ', page.url)

        # get page content
        logger.info('Getting Page Content :: %s', page.url)
        page.get_content()

        # get keywords matched
        keys = page.get_keywords_matched(website.aho)
        logger.info('Matched Keywords :: %s', keys)

        # get external links
        page.get_external_links()
        logger.info('Found External Links :: %d', len(page.external_links))

        # get internal links
        page.get_internal_links(website)
        logger.info('Found Internal Links :: %d', len(page.internal_links))

        # get status code of all links
        logger.info('Getting Status of all Links')
        page.get_status_codes_of_links(website)

        logger.info('Enqueueing New Jobs ')
        # enqueue the un-broken internal links
        for p in page.crawl_pages:
            logger.info('Enqueued :: %s', p.url)
            website.no_of_pages_queued += 1
            q.enqueue(crawl_page, website, p)

        logger.info('Adding Result to website')
        # add rotto links to result
        if page.rotto_links:
            logger.info('Broken Links Found :: %s', page.rotto_links)
            website.add_to_result(
                page.url, page.rotto_links, page.matched_keywords)

        logger.debug('Crawled :: %s', page.url)

        # increment the pages crawled by 1
        website.no_of_pages_crawled += 1

        logger.info('Website %s :: Pages Queued -> %d', website.url,website.no_of_pages_queued)
        logger.info('Website %s :: Pages Crawled -> %d', website.url,website.no_of_pages_crawled)
        # checks if website crawled completely or not
        if website.is_website_crawled_completely():
            logger.debug('Website %s crawled Completely', website.url)
            # save results to database
            logger.debug('Saving results to database')
            # send the email to user
            logger.debug('Sending email to user')

    except Exception as e:
        logger.exception('Error in crawling :: %s ', page.url)
    return website


def start_dispatcher(url, keywords):
    """
    Dispatcher to start crawling of a website
    """
    try:
        logger.debug('Dispatcher Start :: %s', url)
        website = Website(url, keywords)
        website.preInit()
        page = Page(website.url, website.url)
        website.no_of_pages_queued += 1
        job = q.enqueue(crawl_page, website, page)
        logger.debug('Job Added in Queue :: %s', url)
    except Exception as e:
        logger.exception('Error occurred in dispatcher')
