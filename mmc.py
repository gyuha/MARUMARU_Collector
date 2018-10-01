#!/usr/bin/env python
"""	MARUMARU COLLECTOR	"""
"""	     	  BY IML  	"""
"""	shin10256|gmail.com   	"""
"""	shino1025.blog.me    	"""
"""	github.com/iml1111   	"""

from bs4 import BeautifulSoup
from multiprocessing import Pool, freeze_support
from os.path import basename
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import glob
import os
import re
import requests
import sys
import zipfile
import platform

temp_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'temp')
download_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'download')
Comics_Page = "http://wasabisyrup.com"
Comics_title = ""   # 전체 이름

def Initializing():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("   |      |         |      |       ||||||")
    print("  | |    | |       ||     | |      |    |     ")
    print(" ||  |  |  ||     ||  |  |  ||     |              ")
    print(" ||   ||   ||     ||   ||   ||     |    |     ")
    print(" ||   ||   ||     ||   ||   ||     ||||||   Ver. 0.2 by IML")

    print("\n$ HI! THIS IS MARUAMRU COLLECTOR! $\n")

    if not os.path.exists(temp_path):
        os.mkdir(temp_path)
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    mode = input("[*] MODE is All or Single ?(a/s) ")
    return mode


def URLparser(URL):
    print("[ ] Chrome Driver Starting...", end="\r")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % "1920,1080")
    dirver_file = './chromedriver.exe'
    if platform.system() == 'Linux':
        dirver_file = './chromedriver'

    driver = webdriver.Chrome(executable_path=dirver_file,
                              chrome_options=chrome_options)
    driver.set_window_size(600, 400)
    driver.implicitly_wait(1)
    driver.get(URL)
    print("[*] Chrome Driver Starting...")
    return driver


def MultiCollect(driver):
    bs0bj = BeautifulSoup(driver.page_source, "html.parser")
    #bbsview > div.viewbox > div.subject > h1
    Allcomics = bs0bj.findAll("a", {"href": re.compile("http://www.shencomics.com/archives/.*")})\
        + bs0bj.findAll("a", {"href": re.compile("http://www.yuncomics.com/archives/.*")})\
        + bs0bj.findAll("a", {"href": re.compile("http://wasabisyrup.com/archives/.*")})
    global Comics_title        
    Comics_title = bs0bj.find("h1").getText()
    print("###################")
    print("> " + Comics_title)
    print("###################")
    Comic_count = 1
    Comic_total = len(Allcomics)

    for url in Allcomics:
        drv = URLparser(url.attrs['href'])
        SingleCollect(drv, Comic_count, Comic_total)
        Comic_count += 1
        drv.close()


def SingleCollect(driver, Comic_count, Comic_total):
    print("[*] URL Parsing & Web Crawling...")
    bs0bj = BeautifulSoup(driver.page_source, "html.parser")
    comic_title = Collecting(driver.current_url, bs0bj,
                             Comic_count, Comic_total)

    if comic_title == "Protected":
        print("[*] This comic is Protected! Fail!")
    else:
        filelist = makeZIP(comic_title)
        Removing(filelist)


def Collecting(curl, bs0bj, Comic_count, Comic_total):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("< Current Progress >")
    print("Total: " + str(Comic_count) + " / " + str(Comic_total))
    print("[ ] Web image filename Crawling...", end='\r')
    protect = bs0bj.find("h2")
    if protect != None:
        return protect.get_text()

    comic_title = bs0bj.find("div", {"class": "article-title"}).attrs['title']
    title_filter = '\\/<>:?!*"|'
    comic_title = comic_title.translate(
        {ord(x): y for (x, y) in zip(title_filter, "          ")})

    comic_images = bs0bj.findAll("img")
    count = 1

    params = []

    for img in comic_images:
        if not img.has_attr('data-src'):
            continue
        imgurl = Comics_Page + img.attrs['data-src']
        imgfile = os.path.join(temp_path, comic_title + \
            "_(" + "%04d" % count + ").jpg")
        count = count + 1
        params.append([curl, imgurl, imgfile])

    pool = Pool(processes=4)
    pool.map(download, params)
    print("[*] Web image filename Crawling...")
    return comic_title


def download(p):
    # url, imgurl, file_name
    url = p[0]
    imgurl = p[1]
    file_name = p[2]

    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
			AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;\
			q=0.9,imgwebp,*/*;q=0.8",
        "Referer": url}

    session = requests.Session()
    req = session.get(imgurl, headers=header)

    with open(file_name, "wb") as file:
        file.write(req.content)



def makeZIP(comic_title):
    comic_title = re.sub(r'(\d+)화', lambda m : m.group(0).zfill(4), comic_title)
    zip_filepath = os.path.join(download_path, comic_title + ".zip")
    print("[ ] " + Comics_title + ".zip archive..", end="\r")
    if Comics_title != "":
        zip_filepath = os.path.join(download_path, Comics_title)
        if not os.path.exists(zip_filepath):
            os.mkdir(zip_filepath)
        zip_filepath = os.path.join(zip_filepath, comic_title + ".zip")
    
    try:
        zipf = zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED)
        for file in glob.glob(os.path.join("temp","*.jpg")):
            zipf.write(file, basename(file))
        zipf.close()
    except:
        print("[*] ZIP File Can't Make.")
        print("[*] Program Down!")
        sys.exit(1)
    print("[*] " + Comics_title + ".zip archive..")
    return os.listdir(temp_path)


def Removing(filelist):
    print("[ ] Removing image files.", end = '\r')
    for file in filelist:
        path = os.path.join(temp_path, file)
        if path.endswith(".jpg"):
            os.remove(path)
    print("[*] Removing image files.")


if __name__ == '__main__':
    freeze_support()
    
    mode = Initializing()

    if mode != 'a' and mode != 's':
        print("[*] plz right command.")
        sys.exit(1)

    URL = input("[*] Please input URL(only MARUMARU): ")
    driver = URLparser(URL)

    if mode == 's':
        SingleCollect(driver, 1, 1)
    else:
        MultiCollect(driver)

    print("[*] Closing Chrome..")
    driver.close()
    print("[*] Complete!")
