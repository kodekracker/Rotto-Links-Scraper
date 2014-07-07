#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import time
from rottoscraper import Crawler


def main():
    """Main function of the crawler"""
    start_time = time.time()
    seed_url = raw_input("Enter the seed url: ")
    line = raw_input("Enter the keywords(Use ',' to seperate words): ")
    keywords = line.split(',')
    print '\nCrawler Starts..........'
    cr = Crawler(seed_url, keywords)
    cr.start()
    print '\nProcessing Completed.'
    print
    cr.print_results()
    print '\nCrawler Stops........... '
    print "\nElapsed Time: %s sec. " % (time.time() - start_time)


if __name__ == "__main__":
    main()
