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
import web_crawler

keyword = 'cats'
api_keys = [('google', 'XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY'),
            ('flickr', 'XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY')] # replace XXX.. and YYY.. by your own keys
images_nbr = 50 # number of images to get

# create the instance and fetch for images URLs in the web:
crawler = web_crawler.WebCrawler(api_keys)
crawler.fetch_links(keyword, images_nbr, remove_duplicated_links=True)

# save URLs in a file to download them later (optional):
urls_file_path = "./" + keyword + "/links.txt"
crawler.save_urls(urls_file_path)

# Download the images
images_folder_path = "./" + keyword
crawler.download_images(target_folder=folder_path)
```
This program will crawl Google Search Images and Flikr to collect 50 images from each and save them to disk.

Note in this case that, the program will consume 5 queries from you Google Search Engine. That's because Google's API limits the number of images per querry to 10.

To test the program, make sure to replace the values of 'api_keys' variables by your own keys.

### Download images from existing list of URLs
```
import web_crawler

keyword = 'cats'
api_keys = [('google', 'XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY'),
            ('flickr', 'XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY')]
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
This program will read all .jpg, .jpeg and .png files from folder_path, copy them to './cats/renamed' folder, and rename them according to this pattern: 1.jpg, 2.jpg, 3.jpg...

You can also specify target_folder and accepted extensions by passing extra argument to the last command:
```
dataset_builder.rename_files(folder_path, target_folder='./cats_renamed', extensions=('.jpg', '.png', '.gif'))
``` 

### Resize the images
```
import dataset_builder
folder_path = './cats'
dataset_builder = dataset_builder.DatasetBuilder()
dataset_builder.reshape_images(folder_path, target_folder=folder_path + "_reshaped")
```
This will resize the downloaded images to the default size of 128x128. To change the height and width to a custom size you can pass them as extra parameters:
```
dataset_builder.reshape_images(folder_path, target_folder=folder_path + "_reshaped", width=64, height=64)
```

## Note about API Limitations
This package is not intended to simulate a browser to bypass the **API limitations** of the search engines.
- Google Search API is limited to 100 queries per day, and 10 images per query (in the free version).
- Flikr API is limited to 3600 queries per hour, and 200 images per query. But return at most the first 4,000 results for any given search query.
- Bing API is limited to 5000 queries per month
