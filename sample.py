#!/usr/bin/env python

import web_crawler

keyword = 'cats'
my_key = '1111111111' # put here your google API Key
my_search_engine_id = '1111111111' # put here your Google Search API ID
images_nbr = 5 # number of images to get

api_keys = [('google', my_key, my_search_engine_id)]
crawler = web_crawler.WebCrawler(api_keys) # create the instance
crawler.fetch_links(keyword, images_nbr, remove_duplicated_links=True)
crawler.save_urls(keyword + "/links.txt")
crawler.download_images()
