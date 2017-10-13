# Web Image Crawler & Dataset Builder

This package is a complete tool for creating a large dataset of images (specially designed -but not only- for machine learning enthusiasts). With this package you can:
- Download a large number of images using a list of keywords, and organize the images in subfolders
- Rename and order the files automatically
- Resize the images to the desired dimensions
- Crop the images
- Convert images to the desired format
- Merge several subfolders of images into one single big folder
- Convert images to grayscale
- Encode the dataset in a single array file
- Generate labels automatically from subfolders names'
- Flat the images

The actual version can crawl and download images from Google Search Engine and Flickr Search, throught the official APIs. More search engines will be added later (e.g: Bing, Yahoo...)


## Dependencies
Please make sure the following python packages are installed before using the package:
```
pip install --upgrade google-api-python-client
pip install --upgrade flickrapi
pip install --upgrade scipy
pip install --upgrade shutil
pip install --upgrade urllib
pip install --upgrade json
```


## How to use?
This package can be used in different manners depending on what you want to do (a complete example can be found in sample.py file):
### 1. Crawl the web and download images
```
from web_crawler import WebCrawler

keywords = ["cats", "dogs", "birds"]
api_keys = {'google': ('XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY'),
            'flickr': ('XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY')} # replace XXX.. and YYY.. by your own keys
images_nbr = 20 # number of images to fetch
download_folder = "./data" # folder in which the images wil be stored

### Crawl and download images ###
from web_crawler import WebCrawler
crawler = WebCrawler(api_keys)

# Crawl the web and collect URLs:
crawler.collect_links_from_web(keywords, images_nbr, remove_duplicated_links=True)

# Save URLs to download them later (optional):
crawler.save_urls(download_folder + "/links.txt")
# crawler.save_urls_to_json(download_folder + "/links.json")

# Download the images:
crawler.download_images(keywords, target_folder=download_folder)
```
For each keyword, this program will crawl Google Search Images and Flikr to collect 20 images and save them in the download_folder.

Note in this case that, the program will consume 6 queries from you Google Search Engine.
That's because Google's API limits the number of images per querry to 10 (20 images * 3 keywords / 10 images_pre_query => 6 queries).

To test the program, make sure to replace the values of 'api_keys' variables by your own keys.

### 2. Download images from existing list of URLs
```
from web_crawler import WebCrawler

keywords = "cats, dogs, birds"
api_keys = {'google': ('XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY'),
            'flickr': ('XXXXXXXXXXXXXXXXXXXXXXXX', 'YYYYYYYYY')} # replace XXX.. and YYY.. by your own keys
images_nbr = 50 # number of images to get for each keyword
download_folder = "./data" # folder in which the images wil be stored

### Crawl and download images ###
from web_crawler import WebCrawler
crawler = WebCrawler(api_keys)

# Loads URLs from a file:
crawler.load_urls(download_folder + "/links.txt")
# crawler.load_urls_from_json(download_folder + "/links.json")

# Download the images:
crawler.download_images(keywords, target_folder=download_folder)
```

### 3. Rename the downloaded files
```
from dataset_builder import DatasetBuilder
source_folder = "./data"
target_folder = "./data_renamed"
dataset_builder = DatasetBuilder()
dataset_builder.rename_files(source_folder)
```
This program will read all .jpg, .jpeg and .png files from source_folder, copy them to target_folder, and rename them according to this pattern: 1.jpg, 2.jpg, 3.jpg...

You can also specify target_folder and accepted extensions by passing extra argument to the last command (default: .jpg, .jpeg and .png):
```
dataset_builder.rename_files(source_folder, target_folder, extensions=('.png', '.gif'))
```

If your files have no extensions (this can happens with images downloaded using a browser), you can simple send an empty string in 'extensions' argument

```
dataset_builder.rename_files(source_folder, target_folder, extensions=(''))
``` 

### 4. Resize the images
```
from dataset_builder import DatasetBuilder
source_folder = "./data"
target_folder = "./data_resized"
dataset_builder = DatasetBuilder()
dataset_builder.reshape_images(source_folder, target_folder)
```
This will resize the downloaded images to the default size of 128x128. To change the height and width to a custom size you can pass them as extra parameters:
```
dataset_builder.reshape_images(source_folder, target_folder, width=64, height=64)
```
You can also specify the images extensions' (default: .jpg, .jpeg and .png):
```
dataset_builder.reshape_images(source_folder, target_folder, width=64, height=64, extensions=('.png', '.gif'))
```

If your files have no extensions:

```
dataset_builder.reshape_images(source_folder, target_folder, width=64, height=64, extensions=(''))
``` 


### 5. Crop the images:

```
from dataset_builder import DatasetBuilder
source_folder = "./data"
target_folder = "./data_cropped"
dataset_builder = DatasetBuilder()
dataset_builder.crop_images(source_folder, target_folder, height=55, width=55)
dataset_builder.crop_images(source_folder, target_folder, height=55, width=55, extensions=('.jpg', '.jpeg', '.png', '.gif'))
```
Center crop the images. The new image dimenssions are height * width.

### 6. Merge images in one single folder

Sometimes it's interessting to have all the images in only one single folder (especially for non suppervised learning datasets).

The following code will copy all the images in source subfolders, and copy then to the target folder.

Note that the images will be renamed to avoid overwriting files having the same name, and also because most datasets have the follwing naming format : 1.jpg, 2.jpg, 3.jpg...

```
from dataset_builder import DatasetBuilder
source_folder = "./data"
target_folder = "./data_merged"
dataset_builder = DatasetBuilder()
dataset_builder.merge_folders(source_folder, target_folder, extensions=('.jpg', '.jpeg', '.png', '.gif'))
```

### 7. Convert images to grayscale

Some Machine Learning algorithms need grayscale images:

```
from dataset_builder import DatasetBuilder
source_folder = "./data"
target_folder = "./data_merged"
dataset_builder = DatasetBuilder()
dataset_builder.convert_to_grayscale(source_folder, target_folder, extensions=('.jpg', '.jpeg', '.png', '.gif'))
```

If your files have no extensions:

```
dataset_builder.convert_to_grayscale(source_folder, target_folder, extensions='')
```

### 8. Convert images' format

In case you want to change images to a specified format (eg: covert all images to PNG):

```
from dataset_builder import DatasetBuilder
source_folder = "./data"
target_folder = "./data_png_format"
dataset_builder = DatasetBuilder()
dataset_builder.convert_format(source_folder, target_folder, new_extension='.png', extensions=('.jpg', '.jpeg', '.png', '.gif'))
```

If your files have no extensions:

```
dataset_builder.convert_format(source_folder, target_folder, new_extension='.png', extensions='')
```

### 9. Convert dataset to a single file

Many datasets in Machine Learning are encoded in a single array file containing all data (e.g: Mnist, Cifar10...)

The following lines merge all the images into a single numpy variable stored in disk as "data.npy".

```
from dataset_builder import DatasetBuilder
source_folder = "./data"
target_folder = "./data_single_file"
dataset_builder = DatasetBuilder()
dataset_builder.convert_to_single_file(source_folder, target_folderr, flatten=False)
#dataset_builder.convert_to_single_file(source_folder, target_folder, flatten=False, extensions=('.jpg', '.jpeg', '.png', '.gif'))
```

If you want to generate automatically labels from images subfolders, set *create_labels_file* argument to *True*. In this case, two files will be generated: *data.npy* and *labels.npy*.:
```
source_folder = download_folder
target_folder = download_folder + "_single_file"
dataset_builder.convert_to_single_file(source_folder, target_folder, flatten=False, create_labels_file=True)
```

If you want the images to be flatten during the operation, set the optional argument *flatten* to *True*. In that case, the images will be grouped in a 2-D matrix, where each row contains a flatten image.
```
source_folder = download_folder
target_folder = download_folder + "_single_file"
dataset_builder.convert_to_single_file(source_folder, target_folder, flatten=True, create_labels_file=True)
```



## Note about APIs Limitations'

This package is not intended to simulate a browser in order to **bypass the API limitations** of the search engines.
- Google Search API is limited to 100 queries per day, with 10 images per query (in the free version).
- Flikr API is limited to 3600 queries per hour with 200 images per query, and returns at most 4,000 results for each keyword.
- Bing API is limited to 5000 queries per month.
- Yahoo! API is limited to 50 images per query, and return at most 1000 results for each keyword.

## TODO:

Feel free to contribute to this package, or propose your ideas:
- Add more search engines (Bing, Yahoo...)
- Test on python 3.x
- Change crawling and download method?
- Detect duplicated or very similar images?

Please report any [issue here](https://github.com/amineHorseman/images-web-crawler/issues).
