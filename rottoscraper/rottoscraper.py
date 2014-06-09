#! /usr/bin/python


import requests
import urllib2
import nltk
from Queue import Queue
from bs4 import BeautifulSoup
from urlparse import urljoin
from os.path import splitext, basename
from aho import AhoCorasick

def print_links(links):
	"""Print all the links of a set"""
	cnt = 1
	for l in links:
		print str(cnt)+') '+l
		cnt += 1
'''
import nltk   
from urllib2 import urlopen

url = "http://kodekracker.github.io"
html = urlopen(url).read()    
raw = nltk.clean_html(html)  
print ' '.join(raw.split())

'''

def get_text(url,html):
	raw_content = nltk.clean_html(html)
	content = ' '.join(raw_content.split())
	with open("data.txt","a") as file_data:
		file_data.write(content)
		file_data.write("\n........")


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
	r = requests.head(url)
	return r.status_code

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

def process_queue(host_url,seed_url,q,bravo_links,rotto_links,visited_links):
	"""Adds the Url in a seed Url to Queue """
	base_url = seed_url
	html = get_html(seed_url)
	links = get_links(html)
	for l in links:
		url = get_absolute_url(base_url, l['href'])
		if url.startswith(host_url):
			if url not in visited_links:
				print 'Checking Url Status: ', url
				status_code = get_status_code(url)
				print 'Status:: ', status_code
				if ( status_code == requests.codes.ok):
					bravo_links.append(url)
					q.put(url)
				else:
					rotto_links.append(url)
					# code for text retrieval from baseurl and searching key
					get_text(base_url,html)
				visited_links.append(url)
			else:
				print 'Already Visited :', url
		else:
			print 'External Link : ', url
		print

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

	q = Queue()
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

def main():
	"""Main function of the crawler"""
	seed_url = raw_input("Enter the seed url: ")
	print 'Crawler Starts..........\n'
	start_crawler(seed_url)
	print 'Crawler Stops........... \n'

if __name__ == "__main__":
	main()
