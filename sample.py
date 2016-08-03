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
#crawler.load_urls_from_json(download_folder + "/links.json")

# 3. Save URLs to download them later (optional):
crawler.save_urls(download_folder + "/links.txt")
#crawler.save_urls_to_json(download_folder + "/links.json")

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
source_folder = download_folder
target_folder = download_folder + "_resized"
dataset_builder.reshape_images(source_folder, target_folder)
#dataset_builder.reshape_images(source_folder, target_folder, width=64, height=64)

# 3. Crop the images:
source_folder = download_folder
target_folder = download_folder + "_cropped"
dataset_builder.crop_images(source_folder, target_folder, height=55, width=55)

# 4. Merge the folders:
source_folder = download_folder
target_folder = download_folder + "_merged"
dataset_builder.merge_folders(source_folder, target_folder, extensions=('.jpg', '.jpeg', '.png', '.gif'))

# 5. Convert to grayscale:
source_folder = download_folder
target_folder = download_folder + "_grayscale"
dataset_builder.convert_to_grayscale(source_folder, target_folder, extensions=('.jpg', '.jpeg', '.png', '.gif'))

# 6. Change format to .png:
source_folder = download_folder
target_folder = download_folder + "_png_format"
dataset_builder.convert_format(source_folder, target_folder, new_extension='.png')
#dataset_builder.convert_format(source_folder, target_folder, extensions=('.jpg', '.jpeg', '.png', '.gif'), new_extension='.png')

# 7. Convert dataset to sigle file:
source_folder = download_folder
target_folder = download_folder + "_single_file"
dataset_builder.convert_to_single_file(source_folder, target_folder, flatten=False, create_labels_file=True)
#dataset_builder.convert_to_single_file(source_folder, target_folder, flatten=False, create_labels_file=True, extensions=('.jpg', '.jpeg', '.png', '.gif')) 