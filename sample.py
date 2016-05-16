#!/usr/bin/env python

keywords = ["cats", "dogs", "birds"]
api_keys = {'google': ('XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY'),
            'flickr': ('XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY')}
images_nbr = 10 # number of images to fetch
download_folder = "./data" # folder in which the images will be stored

### Crawl and download images ###
from web_crawler import WebCrawler
crawler = WebCrawler(api_keys)

# 1. Crawl the web and collect URLs:
crawler.collect_links_from_web(keywords, images_nbr, remove_duplicated_links=True)

# 2. (alernative to the previous line) Load URLs from a file instead of the web:
#crawler.load_urls(download_folder + "/links.txt")

# 3. Save URLs to download them later (optional):
crawler.save_urls(download_folder + "/links.txt")

# 4. Download the images:
crawler.download_images(target_folder=download_folder)


### Build the dataset ###
from dataset_builder import DatasetBuilder
dataset_builder = DatasetBuilder()

# 1. rename the downloaded images:
source_folder = download_folder
target_folder = download_folder + "_renamed"
dataset_builder.rename_files(source_folder, target_folder)
#dataset_builder.rename_files(source_folder, target_folder, extensions=('.jpg', '.jpeg', '.png', '.gif'))

# 2. Resize the images:
source_folder = download_folder + "_renamed"
target_folder = download_folder + "_resized"
dataset_builder.reshape_images(source_folder, target_folder)
#dataset_builder.reshape_images(source_folder, target_folder, width=64, height=64)
