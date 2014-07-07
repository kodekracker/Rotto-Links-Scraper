#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import requests
import nltk
from bs4 import BeautifulSoup
from urlparse import urljoin
from os.path import splitext, basename


def get_plain_text(html):
    """Return the plain text from a html"""
    raw_text = nltk.clean_html(html)
    text = u' '.join(raw_text.split()).encode('utf-8').lower()
    return text


def get_html(url):
    """Return the html of a url page"""
    try:
        headers = {'User-agent': 'Rotto-Scaper'}
        r = requests.get(url,headers=headers)
        return r.text
    except


def get_links(html):
    """Return the set of links from a html text"""
    soup = BeautifulSoup(html)
    links = soup.find_all('a', href=True)
    # Remove 'has' tag links
    links[:] = [l for l in links if not l['href'].startswith('#')]
    return links


def get_status_code(url):
    """Return the status code of a given Url"""
    r = requests.head(url)
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
    index = relative_url.find('?')
    if index > 0 :
        relative_url = relative_url[:index]
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
