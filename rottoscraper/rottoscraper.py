#! /usr/bin/python
# coding: utf-8

import requests
import urllib2
import nltk
from Queue import Queue
from bs4 import BeautifulSoup
from urlparse import urljoin
from os.path import splitext, basename
from aho import AhoCorasick

class Rotto:
	'Nothing'
	def __init__(self):
		base_url = None
		rotto_links = []
		keywords_match = []

class Crawler:
	'Find the rotto links in a given seed url'
	def __init__(self,seed_url=None,keywords=[]):
		self.host_url = seed_url
		self.seed_url = seed_url
		self.keywords = keywords
		self.bravo_links = []	# a set of all fine/unbroken links
		self.visited_links = []	# a set of visited links
		self.q = Queue()
		self.res = [] # a list of rotto result

	def add_seed_url(self, seed_url):
		"""Add seed url """
		self.seed_url = seed_url


	def add_keywords(self, keywords):
		"""Add keywords """
		self.keywords = keywords


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


	def process_queue(self):
		"""Adds the Url in a seed Url to Queue """
		base_url = self.seed_url
		html = get_html(self.seed_url)
		links = get_links(html)
		rotto_links = [] # a set of all broken links in a particular page
		for l in links:
			url = get_absolute_url(base_url, l['href'])
			if url.startswith(self.host_url):
				if url not in self.visited_links:
					#print 'Checking Url Status: ', url
					status_code = get_status_code(url)
					#print 'Status:: ', status_code
					if ( isLinkOk(status_code) ):
						self.bravo_links.append(url)
						self.q.put(url)
					else:
						rotto_links.append(url)
					self.visited_links.append(url)
				else:
					pass
					#print 'Already Visited :', url
			else:
				pass
				#print 'External Link : ', url
			#print

		if rotto_links:
			self.match_keyword(base_url, html, rotto_links)


	def crawl_url(self):
		"""Crawls the seed Url"""
		self.process_queue()
		if not self.q.empty():
			self.seed_url = self.q.get()
			#print "Dequeuing ::", self.seed_url
			self.crawl_url()
		return


	def start_crawler(self):
		"""Return the set of rotto links from a seed Url"""
		print 'Please Wait While the Seed URL is processing.....'
		print '.................................................'
		self.crawl_url()
		print 'Processing Completed.'
		self.print_results()

	def print_results(self):
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
	headers = {'User-agent': 'Mozilla/5.0'}
	r = requests.get(url,headers=headers)
	return r.text


def get_links(html):
	"""Return the set of links from a html text"""
	soup = BeautifulSoup(html)
	links = soup.find_all('a', href=True)
	return links


def get_status_code(url):
	"""Return the status code of a given Url"""
	r = requests.get(url)
	return r.status_code

def isLinkOk(status_code):
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


def main():
	"""Main function of the crawler"""
	seed_url = raw_input("Enter the seed url: ")
	line = raw_input("Enter the keywords(Use ',' to seperate keywords): ")
	keywords = line.split(',')
	keywords = map(clean, keywords)
	print 'Crawler Starts..........'
	cr = Crawler(seed_url, keywords)
	cr.start_crawler()
	print 'Crawler Stops........... '


if __name__ == "__main__":
	main()
