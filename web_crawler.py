#!/usr/bin/env python
""" WebCrawler: fetch images from various search engines and download them"""

from __future__ import print_function
from math import ceil
import sys
import os
import json
import images_downloader

__author__ = "Amine BENDAHMANE (@AmineHorseman)"
__email__ = "bendahmane.amine@gmail.com"
__license__ = "GPL"
__date__ = "May 2nd, 2016"


class WebCrawler(object):
    """ Fetch images from various search engines and download them"""
    search_engines = ['google', 'flickr']
    api_keys = []
    images_links = {}
    keywords = ''

    def __init__(self, api_keys):
        for engine, _ in api_keys.items():
            if engine not in self.search_engines:
                error_msg = "Search engine " + engine + \
                            " not supported. Please use only the following engines: "
                error_msg += ', '.join(self.search_engines)
                self.error(error_msg)
        self.api_keys = api_keys

    @staticmethod
    def error(msg):
        """Display an error message and exit"""
        print("Error: ", msg)
        exit()


    def collect_links_from_web(self, keywords, number_links_per_engine,
                               remove_duplicated_links=False):
        """ Crawl search engines to collect images links matching a list of keywords.
            Each keyword is processed seperately."""
        # validate params:
        number_links = int(number_links_per_engine)
        if number_links <= 0:
            print("Warning: number_links_per_engine must be positive, \
                    value changed to default (100 links)")
            number_links = 100
        if not keywords:
            self.error("Error: No keyword")
        elif isinstance(keywords, basestring):
            keywords = [keywords]
        self.keywords = [keywords]

        # call methods for fetching image links in the selected search engines:
        print("Start fetching...")
        for keyword in keywords:
            print("\nFetching for '", keyword, "' images...")
            extracted_links = []
            for engine, keys in self.api_keys.items():
                try:
                    method = getattr(self, 'fetch_from_' + engine)
                except AttributeError:
                    self.error('funciton fetch_from_' + engine + '() not defined')
                temporary_links = method(keyword, keys[0], keys[1], number_links)
                extracted_links += temporary_links
                print("\r >> ", len(temporary_links), " links extracted", end="\n")

            # remove duplicated links:
            if remove_duplicated_links:
                links_count = len(extracted_links)
                extracted_links = list(set(extracted_links))
                print(" >> ", links_count - len(extracted_links),
                      " duplicated links removed, ", len(extracted_links), " kept")

            # store the links into the global list:
            self.images_links[keyword] = extracted_links

    def fetch_from_google(self, keyword, api_key, engine_id, number_links=50):
        """Fetch images from google using API Key"""
        items_per_page = 10 # max 10 for google api
        if number_links < 10:
            items_per_page = number_links
        pages_nbr = int(ceil(number_links / items_per_page))
        from googleapiclient.discovery import build  # no need to import the package if the user didn't choose google in the list ??!
        links = []

        # get first page and store:
        print("Crawling Google Search Engine...")
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
            links.append(image['link'])

        # get next pages:
        for i in range(1, pages_nbr):
            sys.stdout.flush()
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
                links.append(image['link'])
        print("\r >> ", len(links), " links extracted...", end="")

        # store and reduce the number of images if too much:
        return links

    def fetch_from_flickr(self, keyword, api_key, api_secret, number_links=50):
        """ Fetch images from Flikr """
        from flickrapi import FlickrAPI # we import flikcr API only if needed

        # calculate number of pages:
        if number_links < 200:
            items_per_page = number_links
        else:
            items_per_page = 200   # max 200 for flikr
        pages_nbr = int(ceil(number_links / items_per_page))
        links = []

        # get links from the first page:
        print("Carwling Flickr Search...")
        flickr = FlickrAPI(api_key, api_secret)
        response = flickr.photos_search(api_key=api_key,
                                        text=keyword,
                                        per_page=items_per_page,
                                        media='photos',
                                        sort='relevance')
        images = [im for im in list(response.iter()) if im.tag == 'photo']
        for photo in images:
            photo_url = "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg". format(
                photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))
            links.append(photo_url)
        print(" >> ", len(links), " links extracted...", end="")

        # get next pages:
        for i in range(1, pages_nbr):
            response = flickr.photos_search(api_key=api_key,
                                            text=keyword,
                                            per_page=items_per_page,
                                            media='photos',
                                            page = i + 1,  
                                            sort='relevance')
            images = [im for im in list(response.iter()) if im.tag == 'photo']
            for photo in images:
                link = "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg". format(
                    photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))
                links.append(link)
            print("\r >> ", len(links), " links extracted...", end="")

        # store and reduce the number of images if too much:
        return links

    def save_urls_to_json(self, filename):
        """ Save links to disk """
        folder, _ = os.path.split(filename)
        if filename and not os.path.exists(folder):
            os.makedirs(folder)
        with open(filename, 'w') as links_file:
            json.dump(self.images_links, links_file)
        print("\nLinks saved to '", filename, "'")

    def save_urls(self, filename):
        """ Save links to disk """
        folder, _ = os.path.split(filename)
        if filename and not os.path.exists(folder):
            os.makedirs(folder)
        with open(filename, 'w') as links_file:
            for keyword in self.images_links:
                for link in self.images_links[keyword]:
                    links_file.write(link)
        print("\nLinks saved to '", filename, "'")

    def load_urls(self, filename):
        """ Load links from a file"""
        if not os.path.isfile(filename):
            self.error("Failed to load URLs, file '" + filename + "' does not exist")
        with open(filename) as links_file:
            self.images_links['images'] = []
            for link in links_file:
                self.images_links['images'].append(link)
        print("\nLinks loaded from ", filename)

    def load_urls_from_json(self, filename):
        """ Load links from a json file"""
        if not os.path.isfile(filename):
            self.error("Failed to load URLs, file '" + filename + "' does not exist")
        with open(filename) as links_file:
            self.images_links = json.load(links_file)
        print("\nLinks loaded from ", filename)

    def download_images(self, target_folder='./data'):
        """ Download images and store them in the specified folder """
        print(" ")
        downloader = images_downloader.ImagesDownloader()
        if not target_folder:
            target_folder = './data'
        downloader.download(self.images_links, target_folder)
