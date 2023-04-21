import requests
from pathlib import Path
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import shutil
import argparse

down = 1
domain = ""
links = []
image_lst = []

class colors:
    fail = '\033[91m'
    ok = '\033[92m'
    purple = '\033[95m'
    cyan = '\033[96m'
    yellow = '\033[93m'
    reset = '\033[0m'

def get_image(content, url):
    global image_lst
    global down
    extensions = [".jpg",".jpeg",".png",".gif",".bmp"]
    path = "des/"
    images = content.select('img')
    size = int(50 / 2)
    for image in images:
        try:
            im = image.get('src')
        except:
            continue
        try:
            if im[0] == '/':
                if im[1] == '/':
                    im = 'https:' + im
                else:
                    im = url + im
            data = requests.get(im)
        except:
            try:
                im = image.get('data-src')
                if im[0] == '/':
                    if im[1] == '/':
                        im = 'https:' + im
                    else:
                        if url[-1] == '/':
                            im = url[:-1] + im
                        else:
                            im = url + im
                data = requests.get(im, headers=headers)
            except:
                if im:
                    print(colors.fail + "no image to:"+ im + colors.reset)
                else:
                    print(colors.fail + "fail to get image" + colors.reset)
                continue
            if data.status_code == 403:
                print(colors.fail + "Status for %s: %i"%(im, data.status_code) + colors.reset)
                continue
        toPrint = (im[:size] + "..." + im[(len(im) - size):]) if len(im) > (size*2) else im
        print(colors.cyan + "image:{:<50}".format(toPrint),end="\t" + colors.reset)
        ext = '.' + '.'.join(im.split('.')[-1:])
        if im and not im in image_lst and ext in extensions:
            name = path + str(down) + ext
            print(colors.ok + "{}{}".format("Downloding as: ",name) + colors.reset)
            with open(name,'wb') as f:
                f.write(data.content)
            image_lst.append(im)
            down += 1 
        else:
            print(colors.fail + "{:<20}".format("not downloading.") + colors.reset)

def get_src_image (url, count):
    if url not in links:
        links.append(url)
    else:
        return
    try:
        r = requests.get(url, headers=headers)
    except:
        print(colors.fail + "no valid link for: ",url + colors.reset)
        return
    content = bs(r.content, 'html.parser')
    l = content.select('a')
    print(colors.yellow + "\nchecking images lvl: %i in: %s\n"%(deep - count, url) + colors.reset)
    for img in l:
       headers['referer'] = url
       yield img
    if count > 0:
        for ref in l:
            get = ref.get('href')
            if get and not get in links and domain in get:
                for img in get_src_image(get, count - 1):
                    get_image(img, get)

def get_local_img(l):
    global image_lst
    global down
    size = int(50 / 2)
    extensions = [".jpg",".jpeg",".png",".gif",".bmp"]
    path = "des/"
    b = l.find_all('img')
    for img in b:
        i = img.get('src')
        ext = '.' + '.'.join(i.split('.')[-1:])
        if i and not i in image_lst and ext in extensions:
            origin = '/'.join(url.split('/')[:-1]) + '/' +  i[2:]
            dest = path + str(down) + ext
            try:
                shutil.copy2(origin, dest)
            except:
                if i:
                    print(colors.fail + "no image to:"+ i + colors.reset)
                else:
                    print(colors.fail + "fail to get image" + colors.reset)
                continue
            else:
                toPrint = (i[:size] + "..." + i[(len(i) - size):]) if len(i) > (size*2) else i
                print(colors.cyan + "image:{:<50}".format(toPrint),end="\t" + colors.reset)
                print(colors.ok + "{}{}{}".format("Downloding as: ",str(down),ext) + colors.reset)
                down += 1

def parser():
    parser = argparse.ArgumentParser(
            prog='Spider',
            description='Simple web scraping',
            epilog='Is a simple web scraping')
    parser.add_argument('url', help="url to scrap")
    parser.add_argument('-r', '--recursive', help="recursively downloads the images in a URL received as a parameter", action='store_true')
    parser.add_argument('-l', '--level', help='indicates the maximum depth level of the recursive download.', default=5, type=int)
    parser.add_argument('-p', '--path', help=' indicates the path where the downloaded files will be saved.', default='./data/')
    arg = parser.parse_args()
    return arg

if __name__ == "__main__":
    arg = parser()
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47', 'referer':'https://www.google.com/'}

    try:
        url = arg.url
        file = open(url)
        b = bs(file, "html.parser")
        file.close()
    except:
        domain = ('.'.join(urlparse(arg.url).netloc.split('.')[-2:]))
        if arg.recursive:
            deep = int(arg.level)
        else:
            deep = 0
        for img in  get_src_image(arg.url, deep):
            get_image(img, arg.url)
    else:
        get_local_img(b)
    exit()
