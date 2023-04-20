import requests
from pathlib import Path
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import csv
import shutil

down = 1
domain = ""
links = []
image_lst = []

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
                        im = url + im
                data = requests.get(im, headers=headers)
            except:
                if im:
                    print("no image to:"+ im)
                else:
                    print("fail to get image")
                continue
            if data.status_code == 403:
                print("Status for %s: %i"%(im, data.status_code))
                continue
        toPrint = (im[:size] + "..." + im[(len(im) - size):]) if len(im) > (size*2) else im
        print("image:{:<50}".format(toPrint),end="\t")
        ext = '.' + '.'.join(im.split('.')[-1:])
        if im and not im in image_lst and ext in extensions:
            name = path + str(down) + ext
            print("{}{}".format("Downloding as: ",name))
            f = open(name,'wb')
            f.write(data.content)
            f.close()
            image_lst.append(im)
            down += 1 
        else:
            print("{:<20}".format("not downloading."))

def get_src_image (url = "", count = 5):
    if url not in links:
        links.append(url)
    else:
        return
    try:
        r = requests.get(url, headers=headers)
    except:
        print("no valid link for: ",url)
        return
    content = bs(r.content, 'html.parser')
    l = content.select('a')
    print("\nchecking images lvl: %i in: %s\n"%(deep - count, url))
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
            print(origin)
            try:
                shutil.copy2(origin, dest)
            except:
                if i:
                    print("no image to:"+ i)
                else:
                    print("fail to get image")
                continue
            else:
                toPrint = (i[:size] + "..." + i[(len(i) - size):]) if len(i) > (size*2) else i
                print("image:{:<50}".format(toPrint),end="\t")
                print("{}{}{}".format("Downloding as: ",str(down),ext))
                down += 1

if __name__ == "__main__":
#    url = "https://www.geeksforgeeks.org/python-all-function"
#    url = "https://docs.python.org/es/3/library/random.html"
#    url = "https://www.42barcelona.com"
#    url = "https://www.filmaffinity.com/es/main.html"
#    url = "https://www.filmaffinity.com"
#    url = "https://www.colegiolosolivos.org/"
#    url = "https://www.colegiolosolivos.org/post/información-sobre-bachillerato"
#    url = "https://www.florzen.com/"
#    url = "htt://www.florzen.com/comprar/flores-en-botella/"
    url = "/Users/juan-aga/Documents/varios/www.42malaga.com.html"
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47', 'referer':'https://www.google.com/'}

    try:
        file = open(url)
        b = bs(file, "html.parser")
        file.close()
    except:
        domain = ('.'.join(urlparse(url).netloc.split('.')[-2:]))
        deep = 5
        for img in  get_src_image(url, deep):
            get_image(img, url)
    else:
        get_local_img(b)
    exit()
