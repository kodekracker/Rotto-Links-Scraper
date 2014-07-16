#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 'Rotto' refer to rotten|broken links

from __future__ import absolute_import, nested_scopes

import time
import reppy
import scraper.utils as utils
from scraper.aho import AhoCorasick
from reppy.cache import RobotsCache

class Link(object):
    """
    Represent a Link

    :param url: Url of Link
    :param status_code: Status Code of a Link
    """
    def __init__(self, url=None,status_code=None):
        self.url = url
        self.status_code = status_code

    def set_status_code(self,status_code):
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
    def __init__(self, host_url= None, url=None, status_code=None, content=None):
        """
            Initialize class attributes
        """
        Link.__init__(self, url, status_code);
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
            try:
                res = utils.make_request(self.url)
                self.status_code = res.status_code
                self.content = res.text
            except Exception:
                pass
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
        links = utils.get_external_links(self.host_url, self.content)
        for url in links:
            self.external_links.append(Link(url))
        return self.external_links

    def get_internal_links(self):
        """
            Returns a list of internal links in a page
        """
        if not self.content:
            self.get_content()
        links = utils.get_internal_links(self.host_url, self.content)
        for url in links:
            self.internal_links.append(Link(url))
        return self.internal_links

    def get_status_codes_of_links(self):
        """
            Returns status_code of all links
        """
        # process external links
        urls = (u.url for u in self.external_links)

        # get the dict of (url,status_code) of each external links
        res = utils.make_grequest(urls)

        # set status code of each external links
        for link in self.external_links:
            link.set_status_code(res[link.url].get('status_code', None))

        # process internal links
        urls = (u.url for u in self.internal_links)

        # get the dict of (url,status_code,content) of each internal links
        res = utils.make_grequest(urls, content=True)

        for link in self.internal_links:
            link.set_status_code(res[link.url].get('status_code', None))

            if is_status_ok(link.get_status_code()):
                page = Page(self.host_url, link.url)
                page.content = res[link.url].get('content', None)
                crawl_pages.append(page)
            else:
            	print 'Broken Url Found:: ', link.url
                self.rotto_links.append(link.url)


class Website:
	"""
	Website to be crawled

	:param host_url: Host url to be crawl
	:param keywords: List of Keywords to be search
	:param visited_links: List of all Visited Links
	:param robots: Object of RobotsCache
	:param aho: Object of AhoCorasick
	:param result: List of broken pages
	"""
	def __init__(self,host_url=None,keywords=[]):
		self.host_url = host_url
		self.keywords = keywords
		self.visited_links = set()	# a set of visited links
		self.robots = RobotsCache()
		self.rp = None
		self.aho = AhoCorasick()
		self.result = []
		self.response = {}

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
		self._set_robot_rule();

	def _set_robot_rule(self):
		"""Set the robots.txt rules"""
		url  = utils.get_absolute_url(self.host_url,'/robots.txt')
		self.rp = self.robots.fetch(url)

	def add_to_result(self, base_url, rotto_links, keywords):
		"""
			Add the rotto links to results
		"""
		res = {}
		res['base_url'] = base_url
		res['rotto_links'] = rotto_links
		res['keywords'] = keywords
		self.result.append(res)

	def get_results(self):
		"""
			Return the results
		"""
		self.response['url'] = self.host_url
		self.response['keywords'] = self.keywords
		self.response['total_visited_links'] = len(self.visited_links)
		self.response['result'] = self.result
		return self.response;
