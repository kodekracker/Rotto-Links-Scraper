
from bs4 import BeautifulSoup
import urllib2
import requests
from urlparse import urljoin

# Base Url :: Target site
base_url = "http://www.facebook.com"  
soup = BeautifulSoup(requests.get(base_url).text)

# Extract all links
links = soup('a')

#Structure to store all Relevant Links
list_ok = []
list_notok = []
visited_link = []


print len(links)
header = {'User-agent': 'Mozilla/5.0'}
# Iterating all links in Page
for lk in links:
	url = urljoin(base_url,lk['href'])
	if url not in visited_link:
		print 'Visiting Url = ', url
		r = requests.get(url,headers=header)
		if (r.status_code == requests.codes.ok):
			list_ok.append(url)
		else:
			list_notok.append(url)
		visited_link.append(url)
	else:
		print 'Already Visited.', url

# Display result
print "Ok link::"
for xok in list_ok:
	print xok

print "Roto(Broken) link::"
for rot in list_notok:
	print rot

