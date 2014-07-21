#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, nested_scopes

import sys
import nltk
import logging
from bs4 import BeautifulSoup
from urlparse import urljoin
from os.path import splitext, basename

import requests
import grequests
from requests.exceptions import Timeout
from requests.exceptions import RequestException


# Set logging object
logger = logging.getLogger('scraper_logger')


def make_request(url, timeout=5.0, num_of_retry=3, allow_redirects=True):
    """
        Return response object of url if content-type:text/html
    """
    while num_of_retry > 0:
        try:
            res = requests.get(
                url, timeout=timeout, allow_redirects=allow_redirects)
            logger.debug('Made Request %s :: %d ', url, res.status_code)
            if res.status_code == requests.codes.ok:
                return res
            else:
                res.raise_for_status()
            # num of retries completed
            raise RequestException
        except Timeout:
            num_of_retry -= 1
            logger.debug(
                'Retrying :: (Url= %s, Retries Left=%d)', url, num_of_retry)
            continue
        except RequestException as e:
            logger.exception('Error in make_request')


def make_grequest(urls, content=False, size=5):
    """
        Return the dict of (url,status_code, content_type Or content) of each list of url
        in urls
    """
    try:
        reqs = set()
        ret = dict()
        if content:
            reqs = (grequests.get(url) for url in urls)
        else:
            reqs = (grequests.head(url) for url in urls)

        res = grequests.map(reqs, stream=False, size=size)
        for url, r in zip(urls, res):
            logger.debug('Made Request %s :: %d ', url, r.status_code)
            if content:
                ret[url] = {
                    'status_code': r.status_code,
                    'content': r.text
                }
            else:
                ret[url] = {
                    'status_code': r.status_code
                }
        if ret:
            return ret

        raise Exception
    except Exception as e:
        logger.exception('Error in make_grequest')


def is_status_ok(status_code):
    """
        Return true if status code is ok otherwise flase
    """
    if status_code == requests.codes.ok:
        return True
    else:
        return False


def get_plain_text(html):
    """
        Return the plain text in utf-8 encoding from a html
    """
    raw_text = nltk.clean_html(html)
    text = u' '.join(raw_text.split()).encode('utf-8').lower()
    return text


def get_external_links(host_url, html):
    """
        Return the external links
    """
    external_links = []
    soup = BeautifulSoup(html)
    links = soup.find_all('a', href=True)
    # Remove '#' tag links
    links[:] = [l for l in links if not l['href'].startswith('#')]
    for l in links:
        url = get_absolute_url(host_url, l['href'])
        if not url.startswith(host_url):
            external_links.append(url)
    external_links = list(set(external_links))
    return external_links


def get_internal_links(host_url, html):
    """
        Return the internal links
    """
    internal_links = []
    soup = BeautifulSoup(html)
    links = soup.find_all('a', href=True)
    # Remove '#' tag links
    links[:] = [l for l in links if not l['href'].startswith('#')]
    for l in links:
        url = get_absolute_url(host_url, l['href'])
        if url.startswith(host_url):
            internal_links.append(url)
    internal_links = list(set(internal_links))
    return internal_links


def get_absolute_url(base_url, relative_url):
    """
        Return the absolute url from relative url
    """
    # relative url checking and handling
    if relative_url.startswith('.'):
        page, ext = splitext(basename(base_url))
        if ext or base_url.endswith('/'):
            base_url = base_url[:]
        else:
            base_url = base_url[:] + '/'
    absolute_url = urljoin(base_url, relative_url)
    return absolute_url


def clean(str):
    """
        Clean the string by removing leading and trailing whitespaces
        and make it lower case
    """
    return str.strip().lower()
