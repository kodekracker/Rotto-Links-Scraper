#! /usr/bin/env python
# -*- coding: utf-8 -*-

# 'Rotto' refer to rotten|broken links

import requests
import urllib2
import nltk
import time
import threading
from Queue import Queue
from bs4 import BeautifulSoup
from urlparse import urljoin
from os.path import splitext, basename
from aho import AhoCorasick
from robotparser import RobotFileParser

class Rotto:
	'Nothing'
	def __init__(self):
		base_url = None
		rotto_links = []
		keywords_match = []

class Crawler:
	'Find the rotto links in a given seed url'
	def __init__(self,host_url=None,keywords=[]):
		self.host_url = host_url
		self.keywords = keywords
		self.visited_links = set()	# a set of visited links
		self.res = [] # a list of rotto result
		self.rp = None

	def add_seed_url(self, seed_url):
		"""Add seed url """
		self.seed_url = seed_url


	def add_keywords(self, keywords):
		"""Add keywords """
		self.keywords = keywords


	def set_robot_rule(self):
		"""Set the robots.txt rules"""
		self.rp = RobotFileParser()
		url  = get_absolute_url(self.host_url,'/robots.txt')
		self.rp.set_url(url)
		self.rp.read()


	def match_keyword(self, base_url, html, rotto_links):
		"""Match Keyword in a html"""
		text = get_plain_text(html)
		aho = AhoCorasick()
		for key in self.keywords:
			aho.add_keyword(key)
		aho.make_keyword_tree()
		matched_keys = aho.search_keywords(text)
		matched_keys = list(set(matched_keys))
		# Add Rotto Links to Rotto Object
		r = Rotto()
		r.base_url = base_url
		r.rotto_links = rotto_links
		r.keywords = matched_keys

		self.res.append(r)


	def fill_queue(self, seed_url, queue):
		"""Adds the Url in a seed Url to Queue """
		base_url = seed_url
		html = get_html(seed_url)
		links = get_links(html)
		rotto_links = [] # a set of all broken links in a particular page
		for l in links:
			url = get_absolute_url(base_url, l['href'])
			if self.rp.can_fetch("*", url):
				if url.startswith(self.host_url):
					if url not in self.visited_links:
						status_code = get_status_code(url)
						if ( is_link_ok(status_code) ):
							lock.acquire()
							queue.put(url)
							lock.release()
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

		if rotto_links:
			self.match_keyword(base_url, html, rotto_links)


	def crawl_url(self, queue):
		"""Crawls the seed Url"""
		while True:
			seed_url = queue.get()
			print "%s Dequed :: %s at %s" % (threading.currentThread().getName(), seed_url, time.ctime())
			self.fill_queue(seed_url, queue)
			queue.task_done()


	def print_results(self):
		print 'Total Visited Links :- %d' % len(self.visited_links)
		cnt1 = 1
		for l in self.visited_links:
			print '\t%d) %s'% (cnt1, l)
			cnt1 += 1
		print
		if self.res:
			print '<-----------  Result Founded  ------------>'
			print
			cnt1 = 1
			for r in self.res:
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


def get_plain_text(html):
	"""Return the plain text from a html"""
	raw_text = nltk.clean_html(html)
	text = u' '.join(raw_text.split()).encode('utf-8').lower()
	return text


def get_html(url):
	"""Return the html of a url page"""
	headers = {'User-agent': 'Rotto-Scaper'}
	r = requests.get(url,headers=headers)
	return r.text


def get_links(html):
	"""Return the set of links from a html text"""
	soup = BeautifulSoup(html)
	links = soup.find_all('a', href=True)
	links[:] = [l for l in links if not l['href'].startswith('#')]
	return links


def get_status_code(url):
	"""Return the status code of a given Url"""
	r = requests.get(url)
	return r.status_code

def is_link_ok(status_code):
	"""Return the status of link"""
	if status_code >= 400:
		return False
	else:
		return True


def get_absolute_url(base_url,relative_url):
	"""Return the absolute url from relative url"""
	# relative url checking and handling
	absolute_url = ""
	if relative_url.startswith('.'):
		page, ext = splitext(basename(base_url))
		if ext or base_url.endswith('/'):
			base_url = base_url[:]
		else:
			base_url = base_url[:] + '/'
	absolute_url = urljoin(base_url, relative_url)
	return absolute_url


def clean(str):
	return str.strip().lower()


lock = threading.Lock()
def main():
	"""Main function of the crawler"""
	seed_url = raw_input("Enter the seed url: ")
	line = raw_input("Enter the keywords(Use ',' to seperate words): ")
	keywords = line.split(',')
	keywords = map(clean, keywords)
	print '\nCrawler Starts..........'
	cr = Crawler(seed_url, keywords)
	cr.set_robot_rule()
	num_of_threads = 1
	queue = Queue()
	queue.put(seed_url)
	for i in range(num_of_threads):
		thread_Name = 'Thread-%d' % (i)
		t = threading.Thread(name=thread_Name, target=cr.crawl_url, args=(queue,))
		t.setDaemon(True)
		t.start()
	queue.join()
	print '\nProcessing Completed.'
	print
	cr.print_results()
	print '\nCrawler Stops........... '


if __name__ == "__main__":
	start_time = time.time()
	main()
	print "\nElapsed Time: %s sec. " % (time.time() - start_time)
