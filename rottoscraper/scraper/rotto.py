#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time

import reppy
from reppy.cache import RobotsCache

from . import utils
from .aho import AhoCorasick

class Link(object):

    """
    Represent a Link

    :param url: Url of Link
    :param status_code: Status Code of a Link
    """

    def __init__(self, url=None, status_code=None):
        self.url = url
        self.status_code = status_code

    def set_status_code(self, status_code):
        self.status_code = status_code

    def get_status_code(self):
        return self.status_code

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def __str__(self):
        return "%s has status code %d" % (self.url, self.status_code)


class Page(Link):

    """
    Represent a Page

    :param host_url: Host Url of a Page
    :param content: HTML Content of a Page
    :param matched_keywords: Matched Keywords in a Page
    :param external_links: List of External Link Objects in a Page
    :param internal_links: List of Internal Link Objects in a Page
    :param rotto_links: List of Broken Urls in a Page
    """

    def __init__(self, host_url=None, url=None, status_code=None, content=None):
        """
        Initialize class attributes
        """
        Link.__init__(self, url, status_code)
        self.host_url = host_url
        self.content = None
        self.matched_keywords = []
        self.external_links = []
        self.internal_links = []
        self.crawl_pages = []
        self.rotto_links = []

    def get_content(self):
        """
        Returns the html content of a page
        """
        if not self.content:
            res = utils.make_request(self.url)
            self.status_code = res.status_code
            self.content = res.text
        return self.content

    def get_keywords_matched(self, aho):
        """
        Returns keywords matched in page
        """
        if not self.content:
            self.get_content()

        if not self.matched_keywords:
            text = utils.get_plain_text(self.content)
            self.matched_keywords = aho.search_keywords(text)
            self.matched_keywords = list(set(self.matched_keywords))
        return self.matched_keywords

    def get_external_links(self):
        """
        Returns a list of external links in a page
        """
        if not self.content:
            self.get_content()
        urls = utils.get_external_links(self.host_url, self.url, self.content)

        # exclude all non-html files url's
        urls = self.exclude_parser(urls)

        for url in urls:
            self.external_links.append(Link(url))
        return self.external_links

    def get_internal_links(self, website):
        """
        Returns a list of internal links in a page
        """
        if not self.content:
            self.get_content()
        urls = utils.get_internal_links(self.host_url, self.url, self.content)

        # exclude all url's not satisfied robots.txt rules
        urls = [ url for url in urls if website.rules.allowed(url, '*')]

        # exclude all non-html files url's
        urls = self.exclude_parser(urls)

        for url in urls:
            self.internal_links.append(Link(url))
        return self.internal_links

    def exclude_parser(self, urls):
        """
        Parser to exclude all non-html urls
        """
        reg_ex = '.*(jpg|jpeg|pdf|svg|png|gif|woff|mp4|ogg|avi|mp3|webp|tiff|css|js)$'

        def crawlable(url):
            if bool(re.match(reg_ex, url)):
                return False
            return True
        return [url for url in urls if crawlable(url)]

    def get_status_codes_of_links(self, website):
        """
        Returns status_code of all links
        """
        # add this page in visited links
        website.visited_links[self.url] = {'status_code': self.status_code}

        urls = []
        # process external links
        for link in self.external_links:
            if link.url not in website.visited_links:
                urls.append(link.url)

        if urls:
            # get the dict of (url,status_code) of each external links
            res = utils.make_grequest(urls)

            # set status code of each external links
            for link in self.external_links:
                if link.url in res:
                    status_code = res[link.url].get('status_code', None)
                    website.visited_links[link.url] = {'status_code': status_code}
                    link.set_status_code(status_code)
                else:
                    status_code = website.visited_links[link.url].get('status_code', None)
                    link.set_status_code(status_code)

        urls = []
        # process internal links
        for link in self.internal_links:
            if link.url not in website.visited_links:
                urls.append(link.url)

        if urls:
            # get the dict of (url,status_code,content) of each internal links
            res = utils.make_grequest(urls, content=True)

            rt = []
            # set status code of each external links
            for link in self.internal_links:

                if link.url in res:
                    status_code = res[link.url].get('status_code', None)
                    website.visited_links[link.url] = {'status_code': status_code}
                    link.set_status_code(status_code)

                    # check status is ok or not
                    if utils.is_status_ok(status_code):
                        page = Page(self.host_url, link.url)
                        page.content = res[link.url].get('content', None)
                        self.crawl_pages.append(page)
                    else:
                        print '\t Broken Url Found:: ', link.url
                        rt.append(link.url)
                else:
                    status_code = website.visited_links[link.url].get('status_code', None)
                    link.set_status_code(status_code)

            self.rotto_links = list(set(rt))

class Website(object):

    """
    Website to be crawled

    :param host_url: Host url to be crawl
    :param keywords: List of Keywords to be search
    :param visited_links: List of all Visited Links
    :param robots: Object of RobotsCache
    :param aho: Object of AhoCorasick
    :param result: List of broken pages
    """

    def __init__(self, id=None, url=None, keywords=[]):
        self.id = id
        self.url = url
        self.keywords = keywords
        self.visited_links = dict()
        self.rules = None
        self.aho = AhoCorasick()
        self.result = []

    def preInit(self):
        """
        Pre Init instructions for a crawler
        """
        # trim all keywords
        self.keywords = map(utils.clean, self.keywords)

        # make a keyword tree
        for key in self.keywords:
            self.aho.add_keyword(key)
        self.aho.make_keyword_tree()

        # set robot.txt file rules
        self._set_robot_rule()

    def _set_robot_rule(self):
        """
        Set the robots.txt rules
        """
        self.rules = RobotsCache().fetch(self.url)

    def add_to_result(self, page):
        """
        Add the rotto links to results
        """
        self.result.append(page)

    def result_to_json(self):
        res = []
        for page in self.result:
            res.append({
                    'url' : page.url,
                    'keywords' : page.matched_keywords,
                    'rotto_links' : page.rotto_links
                })

        return res
