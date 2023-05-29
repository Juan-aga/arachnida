# Arachnida     [![juan-aga's 42 arachnida Score](https://badge42.vercel.app/api/v2/cli8xz75i005408mh2tn5hewj/project/3065320)](https://github.com/JaeSeoKim/badge42)

This project consists of two programs, **Spider** and **Scorpion**, designed to work with image files.

**Note:** The use of external functions or libraries like wget or scrapy is not allowed. The logic of each program should be developed by yourself.

## Spider

### Description
The Spider program allows you to extract all the images from a website recursively. Simply provide a URL as a parameter, and the program will download the images.



### Usage
```
./spider [-h] [-r] [-l LEVEL] [-p PATH] url
```

### Options
```
positional arguments:
  url                   url to scrap

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       recursively downloads the images in a URL received as
                        a parameter
  -l LEVEL, --level LEVEL
                        indicates the maximum depth level of the recursive
                        download.
  -p PATH, --path PATH  indicates the path where the downloaded files will be
                        saved.
```



## Scorpion

### Description
The Scorpion program is designed to parse image files for EXIF and other metadata, and display them on the screen. It supports the same extensions handled by the Spider program.

### Usage
```
./scorpion [-h] images [images ...]
```
### Options
```
positional arguments:
  images      Images files to check

optional arguments:
  -h, --help  show this help message and exit
```
