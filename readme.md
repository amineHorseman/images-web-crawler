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
### Crawl the web and download images
```
import web_crawler

keyword = 'cats'
my_key = '1111111111111' # put here your google API Key
my_search_engine_id = '111111111111' # put here your Google Search API ID
images_nbr = 50 # number of images to get

# create the instance and fetch for images URLs in the web:
api_keys = [('google', my_key, my_search_engine_id)]
crawler = web_crawler.WebCrawler(api_keys)
crawler.fetch_links(keyword, images_nbr, remove_duplicated_links=True)

# save URLs in a file to download them later (optional):
urls_file_path = "./" + keyword + "/links.txt"
crawler.save_urls(urls_file_path)

# Download the images
images_folder_path = "./" + keyword
crawler.download_images(target_folder=folder_path)
```
This program will crawl Google Search Images to collect 50 images and save them in disk.

Note in this case that, the program will consume 5 querries from you Google Search Engine. That's because Google's API limits the number of images per querry to 10.

To test the program, make sure to replace the values of 'my_key' and 'my_serach_engine_id' variables by your own keys.

### Download images from existing list of URLs
```
import web_crawler

keyword = 'cats'
my_key = '1111111111111' # put here your google API Key
my_search_engine_id = '111111111111' # put here your Google Search API ID
images_nbr = 50 # number of images to get
urls_file_path = "./" + keyword + "/links.txt" # URLs previously saved using crawler.save_urls

# create the instance and load URLs:
api_keys = [('google', my_key, my_search_engine_id)]
crawler = web_crawler.WebCrawler(api_keys)
crawler.load_urls(urls_file_path) # using 'load_urls' instead of 'fetch_links'

# Download the images
images_folder_path = "./" + keyword
crawler.download_images(target_folder=folder_path)
```

### Rename downloaded files
```
import dataset_builder
folder_path = './cats'
dataset_builder = dataset_builder.DatasetBuilder()
dataset_builder.rename_files(folder_path)
```
This program will read all .jpg and .png files from folder_path, copy them to './cats/renamed' folder, and rename them according to this pattern: 1.jpg, 2.jpg, 3.jpg...

You can also specify target_folder and accepted extensions by passing extra argument to the last command:
```
dataset_builder.rename_files(folder_path, target_folder='./cats_renamed', extensions=('.jpg', '.png', '.gif'))
``` 

## Note about API Limitations
This package is not intended to simulate a browser to bypass the **API limitations** of the search engines.
- Flikr API is limited to 3600 queries per hour
- Google Search API is limited to 100 queries per day (in the free version).
- Bing API is limited to 5000 queries per month
