#!/usr/bin/env python
""" WebCrawler: fetch images from various search engines and download them"""

__author__ = "Amine BENDAHMANE (@AmineHorseman)"
__email__ = "bendahmane.amine@gmail.com"
__license__ = "GPL"
__date__ = "May 2nd, 2016"
__status__ = "developpemnt"

import sys

class WebCrawler(object):
    """ Fetch images from various search engines and download them"""
    search_engines = ['google']
    api_keys = []
    images_links = []
    unique_images_links = []

    def __init__(self, keys):
        for item in keys:
            if item[0] in self.search_engines:
                self.api_keys.append(item)
            else:
                error_msg = "Search engine " + item[0] + " not supported. Please use only the following engines: "
                for item in self.search_engines:
                    error_msg += item + ", "
                self.error(error_msg)

    @staticmethod
    def error(msg):
        """Display an error message and exit"""
        print "Error: " + msg
        exit()


    def fetch_links(self, keyword, number_links_per_engine, remove_duplicated_links=False):
        """ TODO """
        # validate params:
        number_links = int(number_links_per_engine)
        if number_links <= 0:
            print " Warning: number_links_per_engine must be positive, \
                    value changed to default (100 links)"
            number_links = 100

        # call methods for fetching image links in the selected search engines:
        print "Fetching..."
        for item in self.api_keys:
            try:
                method = getattr(self, 'fetch_from_' + item[0])
            except AttributeError:
                self.error(method + ' not defined')
            method(keyword, item[1], item[2], number_links)
        links_count = len(self.images_links)
        sys.stdout.write("\r >> %d links extracted\n" % links_count)
        
        # remove duplicated links:
        if remove_duplicated_links:
            print "Removing duplicated links..."
            self.unique_images_links = set(self.images_links)
        removed_links_count = links_count - len(self.unique_images_links)
        print " >> " + str(len(self.unique_images_links)) + " links remained (" + str(
            removed_links_count) + " links removed)"

    def fetch_from_google(self, keyword, api_key, engine_id, number_links=100):
        """Fetch images from google using API Key"""
        items_per_page = 10 # max: 10
        pages_nbr = number_links / items_per_page
        from googleapiclient.discovery import build  # no need to import the package if the user didn't choose google in the list ??!

        # get first page and store:
        print "Fetching images from google search..."
        service = build("customsearch", "v1", developerKey=api_key)
        response = service.cse().list(q=keyword,
                                      cx=engine_id,
                                      searchType='image',
                                      num=items_per_page,
                                      fileType='jpg&img;png&img;bmp&img;gif&img',
                                      fields='items/link, queries',
                                     ).execute()
        items = response['items']
        for image in items:
            self.images_links.append(image['link'])

        # get next pages:
        for i in range(1, pages_nbr):
            sys.stdout.write("\r(%d links...)" % i*items_per_page)
            response = service.cse().list(q=keyword,
                                          cx=engine_id,
                                          searchType='image',
                                          num=items_per_page,
                                          fileType='jpg&img;png&img;bmp&img;gif&img',
                                          fields='items/link, queries',
                                          start=response['queries']['nextPage'][0]['startIndex'],
                                         ).execute()
            items = response['items']
            for image in items:
                self.images_links.append(image['link'])


    def save_urls(self, filename):
        """ Save links to disk """
        f = open(filename, 'w')
        for link in self.unique_images_links:
            f.write(link + "\n")
        print "Links saved to " + filename

    def download_images(self, folder):
        """ TODO """