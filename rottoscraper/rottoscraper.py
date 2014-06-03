#! /usr/bin/python


import Queue
import requests
import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
from os.path import splitext, basename

temp_links = []

def print_links(links):
	"""Print all the links of a set"""
	cnt = 1
	for l in links:
		print str(cnt)+') '+l
		cnt += 1

def get_object(url):
	"""Return the requests object of a Url"""
	headers = {'User-agent': 'Mozilla/5.0'}
	r = requests.get(url,headers=headers)
	return r

def get_links(url):
	"""Return the set of links from a particular Url"""
	r = get_object(url)
	soup = BeautifulSoup(r.text)
	links = soup.find_all('a', href=True)
	return links

def get_status_code(url):
	"""Return the status code of a given Url"""
	r = get_object(url)
	return r.status_code

def process_queue(host_url,seed_url,q,bravo_links,rotto_links,visited_links):
	"""Adds the Url in a seed Url to Queue """
	links = get_links(seed_url)
	for l in links:
		url = l['href']
		# relative url checking and handling
		if url.startswith('.'):
			page, ext = splitext(basename(seed_url))
			if ext or seed_url.endswith('/'):
				base_url = seed_url
			else:
				base_url = seed_url + '/'
		else:
			base_url = seed_url
		temp_links.append(url)
		url = urljoin(base_url, url)
		if url not in visited_links and url.startswith(host_url):
			print 'Checking Url Status: ', url
			print 'Status:: ',get_status_code(url)
			if ( get_status_code(url) == requests.codes.ok):
				bravo_links.append(url)
				q.put(url)
			else:
				rotto_links.append(url)
			visited_links.append(url)
		else:
			if url in visited_links:
				print 'Already Visited :', url
			else:
				print 'External Link : ', url
		print '\n'

def crawler(host_url,seed_url,q,bravo_links,rotto_links,visited_links):
	"""Crawls the seed Url"""
	process_queue(host_url,seed_url,q,bravo_links,rotto_links,visited_links)
	if not q.empty():
		seed_url = q.get()
		print "Dequeuing ::", seed_url
		crawler(host_url,seed_url,q,bravo_links,rotto_links,visited_links)
	return

def start_crawler(seed_url):
	"""Return the set of rotto links from a seed Url"""
	bravo_links = []	# a set of all fine/unbroken links
	rotto_links = []	# a set of all broken links 
	visited_links = []	# a set of visited links
	host_url = seed_url # base url 

	q = Queue.Queue()
	crawler(host_url,seed_url,q,bravo_links,rotto_links,visited_links)

	print '\n'
	print 'Total Bravo Links : ', len(bravo_links)
	print 'Total Rotto Links : ', len(rotto_links)
	print '\n'
	print 'List of Bravo Links : '
	print_links(bravo_links)
	print '\n'
	print 'List of Rotto Links : '
	print_links(rotto_links)
	print '\n'
	print 'List of all Links : '
	print_links(visited_links)
	print '\n'
	'''print 'List of all href : '
	print_links(temp_links)
	print '\n'''

def main():
	"""Main function of the crawler"""
	seed_url = raw_input("Enter the seed url: ")
	print 'Crawler Starts..........\n'
	start_crawler(seed_url)
	print 'Crawler Stops........... \n'

if __name__ == "__main__":
	main()