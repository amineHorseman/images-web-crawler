# Web Image Crawler

This python package is intended to crawl various search engines (google, bing, yahoo, flikr) to collect large sets of images.

The actual version include only Google Search Engine, through the official API.

More search engines will be added later (e.g: Bing, Yahoo and Flikr??)

## Dependencies
Please make sure the following python packages are installed before using the program:
*googleapiclient
```
pip install --upgrade google-api-python-client
```

## How to use?
```
import web_crawler

keyword = 'cats'
my_key = '1111111111111' # put here your google API Key
my_search_engine_id = '111111111111' # put here your Google Search API ID
images_nbr = 50 # number of images to get

api_keys = [('google', my_key, my_search_engine_id)]
crawler = web_crawler.WebCrawler(api_keys) # create the instance
crawler.fetch_links(keyword, images_nbr, remove_duplicated_links=True)
crawler.save_urls(keyword + "/links.txt")
crawler.download_images()
```
This program will crawl Google Images to collect 50 images and save them in `links.txt` file.

Note in this case that, the program will consume 5 querries from you Google Search Engine. That's because Google's API limits the number of images per querry to 10.

To test the program, make sure to replace the value of 'my_key' and 'my_serach_engine_id' variables by your own keys.

## Note about API Limitations
This package is not intended to simulate a browser to bypass the **API limitations** of the search engines.
- Flikr API is limited to 3600 queries per hour
- Google Search API is limited to 100 queries per day (in the free version).
- Bing API is limited to 5000 queries per month
