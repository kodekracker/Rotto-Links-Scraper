#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mako.template import Template

from worker import qH
from worker import qL
from worker import rDB
from scraper import Page
from scraper import Website
from db import Database
from logger import log

SMTP_USER = os.getenv('sendgriduser', None)
SMTP_PASSWORD = os.getenv('sendgridpass', None)

FROM = 'Rotto Scaper<rottoscaper@scaper.in>'
TO = []

def dispatcher():
    """
    Takes a un-crawled job(website) from database and dispatch it
    to process
    """
    try:
        log.debug('Dispatcher Start')
        while True:
            websites = Database.fetches(limit=5)
            for website in websites:
                dispatch_website(website.id, website.url, website.keywords)
            # sleep for 15 minutes
            log.debug('Dispatcher sleeps for 15 minutes')
            time.sleep(60*15)

    except Exception:
        log.exception('Error in dispatcher')


def dispatch_website(id, url, keywords):
    """
    Dispatcher to start crawling of a website
    """
    try:
        Database.set_website_status(id=id, status='queued')

        # create and set website and page object for a job
        website = Website(id=id, url=url, keywords=keywords)
        website.preInit()
        page = Page(website.url, website.url)

        # set website completion variables in redis db
        rDB.set(website.id+':pages_queued', 1)
        rDB.set(website.id+':pages_crawled', 0)

        # Enqueue job in redis-queue
        job = qH.enqueue(crawl_page, website, page)

        log.debug('Website Added in Queue :: {0}'.format(url))
    except Exception as e:
        log.exception('Error occurred in dispatch website')


def crawl_page(website, page):
    """
    Crawl a single page at a time and checks is job of crawling
    a website done or not and take required steps
    """
    try:
        # set website status to started if it's a first page of website
        if rDB.get(website.id+':pages_queued')==1:
            Database.set_website_status(id=website.id, status='started')

        log.debug('Crawling :: %s' % page.url)

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
            rDB.incr(website.id+':pages_queued')
            qH.enqueue(crawl_page, website, p)


        log.info('Adding Result to website')
        # add rotto links to result
        if page.rotto_links:
            log.info('Broken Links Found :: %s' % page.rotto_links)
            website.add_to_result(page)

        log.debug('Crawled :: %s' % (page.url))

        # increment website crawled page counter
        rDB.incr(website.url+':pages_crawled')

        log.info('Pages Queued:: %s' % (rDB.get(website.id+':pages_queued')))
        log.info('Pages Crawled:: %s' % (rDB.get(website.id+':pages_crawled')))


        # checks if website crawled completely or not
        if rDB.get(website.id+':pages_queued')==rDB.get(website.id+':pages_crawled'):
            log.info('Website %s crawled Completely' % (website.url))
            # save results to database
            qH.enqueue(save_result_to_database, website)
            log.info('Saving results to database')
            # send the email to user
            log.info('Sending email to user')

    except Exception as e:
        log.exception('Error in crawling :: %s ' % (page.url))
    return website


def save_result_to_database(website):
    """
    Saves result to database
    """
    try:
        Database.set_website_status(id=website.id, status='finished', result=website.result_to_json())
        log.info('Result Save successfully :: {0}'.format(website.url))
    except Exception as e:
        log.exception('Error in saving result in database')

def result_mail(website):
    try:
        # Create message container - the correct MIME type is
        # multipart/alternative.
        msg = MIMEMultipart('alternative')

        # Add user Mail ID to TO list
        website = Database.fetch_website(id=website.id)
        TO.append(website['user']['email_id'])

        msg['Subject'] = 'Crawler Result'
        msg['From'] = FROM
        msg['To'] = ','.join(TO)

        # Create the body of the message (an HTML version).
        mytemplate = Template(filename='rottoscaper/scraper/resultmail.html')
        # Pass result ID to template
        html = mytemplate.render(website=data)

        # Record the MIME types of text/html.
        part = MIMEText(html, 'html')

        # Attach part into message container.
        msg.attach(part)

        # Set SMTP server login ceredentials and send mail
        server = smtplib.SMTP('smtp.sendgrid.net')
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
        logger.info('Successfully sent the mail')
        print "Successfully sent the mail"
    except Exception as e:
        logger.exception("Failed to send intro mail")
        print "Failed to send intro mail"

