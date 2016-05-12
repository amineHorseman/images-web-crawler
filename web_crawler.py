#!/usr/bin/env python
""" WebCrawler: fetch images from various search engines and download them"""

from __future__ import print_function
import images_downloader
import sys
import os

__author__ = "Amine BENDAHMANE (@AmineHorseman)"
__email__ = "bendahmane.amine@gmail.com"
__license__ = "GPL"
__date__ = "May 2nd, 2016"
__status__ = "developpemnt"


class WebCrawler(object):
    """ Fetch images from various search engines and download them"""
    search_engines = ['google', 'flickr']
    api_keys = []
    images_links = []
    keyword = ''

    def __init__(self, keys):
        for item in keys:
            if item[0] in self.search_engines:
                self.api_keys.append(item)
            else:
                error_msg = "Search engine " + item[0] + \
                            " not supported. Please use only the following engines: "
                for item in self.search_engines:
                    error_msg += item + ", "
                self.error(error_msg)

    @staticmethod
    def error(msg):
        """Display an error message and exit"""
        print("Error: ", msg)
        exit()


    def collect_links_from_web(self, keyword, number_links_per_engine, remove_duplicated_links=False):
        """ Crawl search engines to collect images links matching a specific keyword """
        # validate params:
        number_links = int(number_links_per_engine)
        if number_links <= 0:
            print("Warning: number_links_per_engine must be positive, \
                    value changed to default (100 links)")
            number_links = 100
        if not keyword:
            self.error("Error: No keyword")
        else: self.keyword = keyword

        # call methods for fetching image links in the selected search engines:
        print("Start fetching...")
        for item in self.api_keys:
            try:
                method = getattr(self, 'fetch_from_' + item[0])
            except AttributeError:
                self.error(item[0] + ' function not defined')
            method(keyword, item[1], item[2], number_links)
            links_count = len(self.images_links)
            print("\r >> ", links_count, " links extracted", end="\n")

        # remove duplicated links:
        if remove_duplicated_links:
            print("Removing duplicated links...")
            unique_images_links = set(self.images_links)
            self.images_links = list(unique_images_links)
            removed_links_count = links_count - len(unique_images_links)
            print(" >> ", removed_links_count, " / ", links_count," links removed")

    def fetch_from_google(self, keyword, api_key, engine_id, number_links=50):
        """Fetch images from google using API Key"""
        items_per_page = 10 # max 10 for google api
        if (number_links < 10):
            items_per_page = number_links
        pages_nbr = (number_links / items_per_page) + 1
        from googleapiclient.discovery import build  # no need to import the package if the user didn't choose google in the list ??!
        links = []

        # get first page and store:
        print("Fetching images from google search...")
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
        self.images_links += links

    def fetch_from_flickr(self, keyword, api_key, api_secret, number_links=50):
        """ Fetch images from Flikr """
        from flickrapi import FlickrAPI # we import flikcr API only if needed

        # calculate number of pages:
        if (number_links < 200):
            items_per_page = number_links
        else:
            items_per_page = 200   # max 200 for flikr
        pages_nbr = (number_links / items_per_page) + 1
        links = []

        # get links from the first page:
        print("Fetching images from flickr...")
        flickr = FlickrAPI(api_key, api_secret)
        response = flickr.photos_search(api_key = api_key, text=keyword, per_page=items_per_page, media='photos', sort='relevance') 
        items = list(response.iter())
        images = [im for im in items if im.tag=='photo']
        for photo in images:
            photo_url = "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg". format( 
                     photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))
            links.append(photo_url)
        print(" >> ", len(links), " links extracted...", end="")

        # get next pages:
        for i in range(1, pages_nbr):
            response = flickr.photos_search(api_key = api_key, text=keyword, per_page=items_per_page, media='photos', sort='relevance') 
            items = list(response.iter())
            images = [im for im in items if im.tag=='photo']
            for photo in images:
                link = "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg". format( 
                        photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))
                links.append(link)
            print("\r >> ", len(links), " links extracted...", end="")

        # store and reduce the number of images if too much:
        self.images_links += links

    def save_urls(self, filename):
        """ Save links to disk """
        folder, basename = os.path.split(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        f = open(filename, 'w')
        for link in self.images_links:
            f.write(link + "\n")
        print("Links saved to '", filename, "'")

    def load_urls(self, filename):
        """ Load links from a file"""
        if not os.path.isfile(filename):
            self.error("Failed to load URLs, file '" + filename + "' does not exist")
        f = open(filename, 'r')
        for line in f:
            self.images_links.append(line)
        print("Links loaded from ", filename)

    def download_images(self, target_folder='./data'):
        """ Download images and store them in the specified folder """
        downloader = images_downloader.ImagesDownloader()
        if not target_folder:
            target_folder = self.keyword
        downloader.download(self.images_links, target_folder)
