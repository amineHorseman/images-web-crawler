# Web Image Crawler

This python package is intended to crawl various search engines (google, bing, yahoo, flikr) to collect large sets of images.

The actual version include only Google Search Engine and Flickr Search, throught the official APIs.

More search engines will be added later (e.g: Bing, Yahoo...)

## Dependencies
Please make sure the following python packages are installed before using the program:
*googleapiclient
*flickrapi
*scipy
*shutil
*urllib
```
pip install --upgrade google-api-python-client
pip install --upgrade flickrapi
pip install --upgrade scipy
pip install --upgrade shutil
pip install --upgraed urllib
```

## How to use?
### Crawl the web and download images
```
from web_crawler import WebCrawler

keywords = "cats"
api_keys = [('google', 'XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY'),
            ('flickr', 'XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY')] # replace XXX.. and YYY.. by your own keys
images_nbr = 50 # number of images to fetch
download_folder = "./data" # folder in which the images wil be stored

### Crawl and download images ###
from web_crawler import WebCrawler
crawler = WebCrawler(api_keys)

# Crawl the web and collect URLs:
crawler.collect_links_from_web(keywords, images_nbr, remove_duplicated_links=True)

# Save URLs to download them later (optional):
crawler.save_urls(download_folder + "/links.txt")

# Download the images:
crawler.download_images(keywords, target_folder=download_folder)
```
This program will crawl Google Search Images and Flikr to collect 50 images from each and save them to disk.

Note in this case that, the program will consume 5 queries from you Google Search Engine. That's because Google's API limits the number of images per querry to 10.

To test the program, make sure to replace the values of 'api_keys' variables by your own keys.

### Download images from existing list of URLs
```
from web_crawler import WebCrawler

keywords = "cats, dogs, birds"
api_keys = [('google', 'XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY'),
            ('flickr', 'XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY')]
images_nbr = 50 # number of images to get for each keyword
download_folder = "./data" # folder in which the images wil be stored

### Crawl and download images ###
from web_crawler import WebCrawler
crawler = WebCrawler(api_keys)

# Loads URLs from a file:
crawler.load_urls(download_folder + "/links.txt")

# Download the images:
crawler.download_images(keywords, target_folder=download_folder)
```

### Rename downloaded files
```
from dataset_builder import DatasetBuilder
source_folder = "./data"
target_folder = "./data_renamed"
dataset_builder = DatasetBuilder()
dataset_builder.rename_files(source_folder)
```
This program will read all .jpg, .jpeg and .png files from source_folder, copy them to target_folder, and rename them according to this pattern: 1.jpg, 2.jpg, 3.jpg...

You can also specify target_folder and accepted extensions by passing extra argument to the last command:
```
dataset_builder.rename_files(source_folder, target_folder, extensions=('.jpg', '.png', '.gif'))
``` 

### Resize the images
```
from dataset_builder import DatasetBuilder
source_folder = "./data_renamed"
target_folder = "./data_resized"
dataset_builder = DatasetBuilder()
dataset_builder.reshape_images(source_folder, target_folder)
```
This will resize the downloaded images to the default size of 128x128. To change the height and width to a custom size you can pass them as extra parameters:
```
dataset_builder.reshape_images(source_folder, target_folder, width=64, height=64)
```

## Note about API Limitations
This package is not intended to simulate a browser to bypass the **API limitations** of the search engines.
- Google Search API is limited to 100 queries per day, and 10 images per query (in the free version).
- Flikr API is limited to 3600 queries per hour, and 200 images per query. But return at most 4,000 results.
- Bing API is limited to 5000 queries per month
- Yahoo! API is limited to 50 images per query. But return at most 1000 results.