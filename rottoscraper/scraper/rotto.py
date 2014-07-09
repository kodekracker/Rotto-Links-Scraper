#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 'Rotto' refer to rotten|broken links

from __future__ import absolute_import

import time
import threading
import scraper.webutil as webutil
from Queue import Queue
from scraper.aho import AhoCorasick
from robotparser import RobotFileParser

lock = threading.Lock()

class Crawler:
	"""
		Find the rotto links in a given seed url
	"""
	def __init__(self,host_url=None,keywords=[]):
		self.host_url = host_url
		self.keywords = keywords
		self.visited_links = set()	# a set of visited links
		self.result = [] # a list of rotto result
		self.rp = None
		self.queue = Queue()
		self.aho = AhoCorasick()

	def preInit(self):
		"""
			Pre Init instructions for a crawler
		"""
		# trim all keywords
		self.keywords = map(webutil.clean, self.keywords)

		# put seed url in queue
		self.queue.put(self.host_url)

		# make a keyword tree
		for key in self.keywords:
			self.aho.add_keyword(key)
		self.aho.make_keyword_tree()

		# set robot.txt file rules
		self.set_robot_rule();

	def add_seed_url(self, seed_url):
		"""Add seed url """
		self.seed_url = seed_url


	def add_keywords(self, keywords):
		"""Add keywords """
		self.keywords = keywords


	def set_robot_rule(self):
		"""Set the robots.txt rules"""
		self.rp = RobotFileParser()
		url  = webutil.get_absolute_url(self.host_url,'/robots.txt')
		self.rp.set_url(url)
		self.rp.read()

	def add_to_result(self, base_url, rotto_links, keywords):
		"""
			Add the rotto links to results
		"""
		res = {}
		res['base_url'] = base_url
		res['rotto_links'] = rotto_links
		res['keywords'] = keywords
		self.result.append(res)

	def match_keyword(self, base_url, html, rotto_links):
		"""Match Keyword in a html"""
		text = webutil.get_plain_text(html)
		matched_keys = self.aho.search_keywords(text)
		matched_keys = list(set(matched_keys))
		# Add Rotto Links to Rotto Object
		self.add_to_result(base_url,rotto_links,matched_keys)

	def fill_queue(self, seed_url):
		"""Adds the Url in a seed Url to Queue """
		base_url = seed_url
		html = webutil.get_html(seed_url)
		links = webutil.get_links(html)
		rotto_links = [] # a set of all broken links in a particular page
		for l in links:
			url = webutil.get_absolute_url(base_url, l['href'])
			lock.acquire()
			# Start of Critical Section
			if self.rp.can_fetch("*", url):
				if url.startswith(self.host_url):
					if url not in self.visited_links:
						status_code = webutil.get_status_code(url)
						if ( webutil.is_link_ok(status_code) ):
							#print 'Putting :: %s' % (url)
							self.queue.put(url)
						else:
							rotto_links.append(url)
						self.visited_links.add(url)
					else:
						pass
						#print	'Already Visited :', url
				else:
					pass
					#	External Link :  url
			else:
				pass
				#	Not allowed to scrape
			# End of Critical Section
			lock.release()

		if rotto_links:
			self.match_keyword(base_url, html, rotto_links)


	def crawl_url(self):
		"""Crawls the seed Url"""
		while True:
			seed_url = self.queue.get()
			self.visited_links.add(seed_url)
			print "%s Dequed :: %-100s \t%s" % (threading.currentThread().getName(), seed_url, time.ctime())
			self.fill_queue(seed_url)
			self.queue.task_done()

	def start(self,num_of_threads=5,interval=3):
		"""
			Start the crawler
		"""
		# execute preInit
		self.preInit()

		for i in range(num_of_threads):
			thread_Name = 'Thread-%d' % (i)
			t = threading.Thread(name=thread_Name, target=self.crawl_url, args=())
			t.setDaemon(True)
			t.start()
		self.queue.join()

	def get_results(self):
		"""
			Return the results
		"""
		return self.result;

	def print_results(self):
		"""
			Print the results
		"""
		print 'Total Visited Links :- %d' % len(self.visited_links)
		cnt1 = 1
		for l in self.visited_links:
			print '\t%d) %s'% (cnt1, l)
			cnt1 += 1
		print
		if self.result:
			print '<-----------  Result Founded  ------------>'
			print
			cnt1 = 1
			for r in self.result:
				print cnt1, ') Base Url:- ', r.base_url
				cnt2 = 1
				if r.rotto_links:
					print '    List of Rotto links:- '
					for rl in r.rotto_links:
						print '   ',cnt1,'.',cnt2,') ',rl
						cnt2 += 1
				print '    Keyword Matched:- ',
				if r.keywords:
					for k in r.keywords:
						if k:
							print k,', ',
				else:
					print 'No Keyword match'
				print
				print
				cnt1 += 1
			print
			print '<------------ End of Result  ------------>'
		else:
			print 'No result found.....'
