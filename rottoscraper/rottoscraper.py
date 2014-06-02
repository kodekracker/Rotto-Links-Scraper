
from bs4 import BeautifulSoup
import urllib2
import requests
from urlparse import urljoin


def print_links(lnk):
		for l in lnk:
			print l

if __name__ == "__main__":
	# Base Url :: Target site
	base_url = "http://www.saurabh-kumar.com"
	r = requests.get(base_url)
	soup = BeautifulSoup(r.text)

	# Extract all links
	links = soup.find_all('a')

	#Structure to store all Relevant Links
	list_ok = []
	list_notok = []
	visited_link = []


	print len(links)
	header = {'User-agent': 'Mozilla/5.0'}
	# Iterating all links in Page
	for lk in links:
		if lk.has_attr('href'):
			link = lk['href']
			url = urljoin(base_url,link)
			#print 'url = ',url
			if url not in visited_link and url.startswith(base_url):
				print 'Visiting Url = ', url
				r = requests.get(url,headers=header)
				if (r.status_code == requests.codes.ok):
					list_ok.append(url)
				else:
					list_notok.append(url)

				visited_link.append(url)
			else:
				if url in visited_link:
					print 'Already Visited.', url
				else:
					print 'External Link', url
		else:
			pass

	# Display result
	print "Ok link::"
	print_links(list_ok)

	print "Roto link::"
	print_links(list_notok)