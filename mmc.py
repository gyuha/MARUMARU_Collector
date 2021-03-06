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
import pathlib
import shutil


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

    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    pathlib.Path(temp_path).mkdir(parents=True, exist_ok=True)

    if not os.path.exists(download_path):
        pathlib.Path(download_path).mkdir(parents=True, exist_ok=True)


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


def writeCount(title, Comic_count):
    path = os.path.join(download_path, title, 'count.dat')
    f = open(path, "w")
    f.write(str(Comic_count))
    f.close()

def readCount(title):
    path = os.path.join(download_path, title)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    path = os.path.join(path, 'count.dat')
    if not os.path.exists(path):
        return 0
    try:
        f = open(path, "r")
        count = f.readline()
        return int(count)
    except ValueError:
        return 0
    finally:
        f.close()
        

def MultiCollect(driver):
    bs0bj = BeautifulSoup(driver.page_source, "html.parser")
    #bbsview > div.viewbox > div.subject > h1
    Allcomics = bs0bj.findAll("a", {"href": re.compile("http://www.shencomics.com/archives/.*")})\
        + bs0bj.findAll("a", {"href": re.compile("http://www.yuncomics.com/archives/.*")})\
        + bs0bj.findAll("a", {"href": re.compile("http://blog.yuncomics.com/archives/.*")})\
        + bs0bj.findAll("a", {"href": re.compile("http://wasabisyrup.com/archives/.*")})
    global Comics_title        
    Comics_title = bs0bj.find("h1").getText().strip()
    print("###################")
    print("> " + Comics_title)
    print("###################")
    Comic_count = 1
    Comic_total = len(Allcomics)

    download_count = readCount(Comics_title)
    for url in Allcomics:
        if download_count >= Comic_count:
            Comic_count += 1
            continue
        driver.get(url.attrs['href'])
        SingleCollect(driver, Comics_title, Comic_count, Comic_total)
        writeCount(Comics_title, Comic_count)
        Comic_count += 1

def SingleCollect(driver, Comics_title, Comic_count, Comic_total):
    print("[*] URL Parsing & Web Crawling...")
    bs0bj = BeautifulSoup(driver.page_source, "html.parser")
    sub_title = Collecting(driver.current_url, bs0bj,
                             Comic_count, Comic_total)

    if sub_title == "Protected":
        print("[*] This comic is Protected! Fail!")
    else:
        filelist = makeZIP(Comic_count, Comics_title, sub_title)
        Removing(filelist)


def Collecting(curl, bs0bj, Comic_count, Comic_total):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("< Current Progress >")
    print("Total: " + str(Comic_count) + " / " + str(Comic_total))
    # print("[ ] Web image filename Crawling...", end='\r')
    protect = bs0bj.find("h2")
    if protect != None:
        return protect.get_text()

    comic_title = bs0bj.find("div", {"class": "article-title"}).attrs['title']
    title_filter = '\\/<>:?!*"|'
    comic_title = comic_title.translate(
        {ord(x): y for (x, y) in zip(title_filter, "          ")})
    print("[" + comic_title + "]")
    gallery = bs0bj.find("div", {"id": "gallery_vertical"})
    comic_images = gallery.findAll("img")
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
    print("DOWNLOAD : " + imgurl + " => " + file_name)
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




def makeZIP(Comic_count, title, sub_title):
    sub_title = str(Comic_count).zfill(3) + "-" + sub_title
    zip_filepath = os.path.join(download_path, title, sub_title + ".zip")
    print("[ ] " + Comics_title + ".zip archive..", end="\r")
    if Comics_title != "":
        zip_filepath = os.path.join(download_path, Comics_title)
        if not os.path.exists(zip_filepath):
            os.mkdir(zip_filepath)
        zip_filepath = os.path.join(zip_filepath, sub_title + ".zip")
    
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
    Initializing()

    URL = input("[*] Please input URL(only MARUMARU): ")
    driver = URLparser(URL)

    MultiCollect(driver)

    print("[*] Closing Chrome..")
    driver.close()
    print("[*] Complete!")
