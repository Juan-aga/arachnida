import requests
from pathlib import Path
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import csv

down = 1
domain = ""
links = []
image_lst = []

def get_image(content):
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
                    im = 'https:/' + im
            data = requests.get(im)
        except:
            try:
                im = image.get('data-src')
                if im[0] == '/':
                    if im[1] == '/':
                        im = 'https:' + im
                    else:
                        im = 'https://' + im
                data = requests.get(im)
            except:
                if im:
                    print("no image to:"+ im,end="")
                else:
                    print("fail to get image",end="")
                continue
        toPrint = (im[:size] + "..." + im[(len(im) - size):]) if len(im) > (size*2) else im
        print("\r\r\rimage:\n{:<50}".format(toPrint),end="\t")
        if im and not im in image_lst and '.' + '.'.join(im.split('.')[-1:]) in extensions:
            name = path + str(down) + '.' + '.'.join(im.split('.')[-1:])
            print("{}{}".format("Downloding as: ",name),end="")
            f = open(name,'wb')
            f.write(data.content)
            f.close()
            image_lst.append(im)
            down += 1 
        else:
            print("{:<20}".format("not downloading                     "),end="")
#        print(headers)

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
#                print(headers)
                for img in get_src_image(get, count - 1):
#                    headers['referer'] = get
                    get_image(img)

if __name__ == "__main__":
#    url = "https://www.geeksforgeeks.org/python-all-function"
#    url = "https://docs.python.org/es/3/library/random.html"
#    url = "https://www.42barcelona.com"
#    url = "https://www.filmaffinity.com/es/main.html"
#    url = "https://www.filmaffinity.com"
#    url = "https://www.colegiolosolivos.org/"
#    url = "https://www.colegiolosolivos.org/post/información-sobre-bachillerato"
#    url = "https://www.florzen.com/"
    url = "https://www.florzen.com/comprar/flores-en-botella/"
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47', 'referer':'https://www.google.com/'}
    r = requests.get(url, headers=headers)
    print(r.status_code)

    domain = ('.'.join(urlparse(url).netloc.split('.')[-2:]))
    
    deep = 5
    for img in  get_src_image(url, deep):
        get_image(img)
    print(links)