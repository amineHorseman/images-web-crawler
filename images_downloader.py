#!/usr/bin/env python
""" ImagesDownloader: get a list of links, download the images and order them in a folder"""

from __future__ import print_function
import urllib
import sys
from dataset_builder import DatasetBuilder

__author__ = "Amine BENDAHMANE (@AmineHorseman)"
__email__ = "bendahmane.amine@gmail.com"
__license__ = "GPL"
__date__ = "May 6nd, 2016"

class ImagesDownloader(object):
    """Download a list of images, rename them and save them to the specified folder"""

    images_links = []
    failed_links = []
    default_target_folder = 'images'

    def __init__(self):
        print("Preparing to download images...")

    def download(self, links, target_folder='./data'):
        """Download images from a lisk of links"""

        # check links and folder:
        if len(links) < 1:
            print("Error: Empty list, no links provided")
            exit()
        self.images_links = links
        DatasetBuilder.check_folder_existance(target_folder)
        if target_folder[-1] == '/':
            target_folder = target_folder[:-1]

        # start downloading:
        print("Downloading files...")
        progress = 0
        images_nbr = sum([len(self.images_links[key]) for key in self.images_links])
        for keyword, links in self.images_links.items():
            DatasetBuilder.check_folder_existance(target_folder + '/' + keyword, display_msg=False)
            for link in links:
                target_file = target_folder + '/' + keyword + '/' + link.split('/')[-1]
                try:
                    f = urllib.URLopener()
                    f.retrieve(link, target_file)
                except IOError:
                    self.failed_links.append(link)
                progress = progress + 1
                print("\r >> Download progress: ", (progress * 100 / images_nbr), "%...", end="")
                sys.stdout.flush()

        print("\r >> Download progress: ", (progress * 100 / images_nbr), "%")
        print(" >> ", (progress - len(self.failed_links)), " images downloaded")

        # save failed links:
        if len(self.failed_links):
            f2 = open(target_folder + "/failed_list.txt", 'w')
            for link in self.failed_links:
                f2.write(link + "\n")
            print(" >> Failed to download ", len(self.failed_links),
                  " images: access not granted ",
                  "(links saved to: '", target_folder, "/failed_list.txt')")
