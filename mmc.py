"""	MARUMARU COLLECTOR	"""
"""	     	  BY IML  	"""
"""	shin10256|gmail.com   	"""	
"""	shino1025.blog.me    	"""
"""	github.com/iml1111   	"""	

from urllib.request import FancyURLopener, HTTPError
from bs4 import BeautifulSoup
from requests import get
import re
import sys
import os
import img2pdf

class AppURLopener(FancyURLopener):     			 
   	version = "Mozilla/5.0"

dirname = os.path.dirname(os.path.realpath('__file__'))
#dirname = os.path.dirname(os.path.realpath(sys.executable))

Comics_Page = "http://wasabisyrup.com"


def Initializing():
	
	os.system('cls')
	print("   |      |         |      |       ||||||")
	print("  | |    | |       ||     | |      |    |     ")
	print(" ||  |  |  ||     ||  |  |  ||     |              ")
	print(" ||   ||   ||     ||   ||   ||     |    |     ")
	print(" ||   ||   ||     ||   ||   ||     ||||||   Ver. 0.1 by IML")

	print("\n$ HI! THIS IS MARUAMRU COLLECTOR! $\n")
	mode = input("[*] MODE is All or Single ?(a/s) ")
	return mode


def URLparser(URL):
	try:
		html = AppURLopener().open(URL)
	except HTTPError as e:
		print(e)
		print("[*] HTTP ERROR!")
		sys.exit(1)

	return BeautifulSoup(html.read(), "html.parser")


def MultiCollect(bs0bj):
	Allcomics =bs0bj.findAll("a",{"href":re.compile("http://www.shencomics.com/archives/.*")})\
		     +bs0bj.findAll("a",{"href":re.compile("http://www.yuncomics.com/archives/.*")})\
		     +bs0bj.findAll("a",{"href":re.compile("http://wasabisyrup.com/archives/.*")})
	Comic_count = 1
	Comic_total = len(Allcomics)	     

	for url in Allcomics:
		bsbj = URLparser(url.attrs['href'])
		SingleCollect(bsbj,Comic_count,Comic_total)
		Comic_count += 1


def SingleCollect(bs0bj,Comic_count,Comic_total):
	comic_title = Collecting(bs0bj,Comic_count,Comic_total)
	if comic_title == "Protected":
		print("[*] This comic is Protected! Fail!")
	else:
		filelist = makePDF(comic_title)
		Removing(filelist)


def Collecting(bs0bj,Comic_count,Comic_total):
	os.system('cls')
	print("< Current Progress >")
	print("Total: " + str(Comic_count) + " / " + str(Comic_total))

	protect = bs0bj.find("h2")
	if protect != None :
		return protect.get_text()

	comic_title = bs0bj.find("div",{"class":"article-title"}).attrs['title']
	title_filter = '\\/<>:?!*"|'
	comic_title = comic_title.translate({ ord(x): y for (x, y) in zip(title_filter, "          ") })

	comic_images = bs0bj.findAll("img")
	count = 1

	for img in comic_images:
		imgurl = Comics_Page + img.attrs['data-src']
		imgfile = dirname + "\\" + comic_title + "_(" + "%04d" % count + ").jpg"
		count = count + 1
		print("\n# Link: " + imgurl)
		print("||\n||\n# Downloading to ->  " + imgfile)
		download(imgurl,imgfile)

		os.system('cls')
		print("< Current Progress >")
		print("# Total: " + str(Comic_count) + " / " + str(Comic_total))
		print("# Collecting " + comic_title + "\n# Progress:[", end='')
		for i in range(13):
			if (i / 13) <= (count / len(comic_images)):
				print("ㅁ", end ='')
			else:
				print("   ", end='')
		print(' ]')

	return comic_title


def download(url , file_name):
		with open(file_name, "wb") as file:
			response = get(url,stream = True)
			for chunk in response.iter_content(2000):
				file.write(chunk)


def makePDF(comic_title):
	try:
		with open(comic_title + ".pdf", "wb") as f:
			f.write(img2pdf.convert([i for i in os.listdir(dirname) if i.endswith(".jpg")]))
		print("[*] Combing to PDF file.")
	except:
		print("[*] PDF File Can't Make.")
		print("[*] Program Down!")
		sys.exit(1)

	return os.listdir(dirname)


def Removing(filelist):
	for file in filelist:
		path = os.path.join(dirname, file)
		if path.endswith(".jpg"):
			os.remove(path)
	print("[*] Removing image files.")



if __name__ == '__main__':

	mode = Initializing()

	if mode != 'a' and mode != 's':
		print("[*] plz right command.")
		sys.exit(1)

	URL = input("[*] Please input URL(only MARUMARU): ")
	bs0bj = URLparser(URL)
	print("[*] URL Parsing & Web Crawling...")

	if mode == 's':
		SingleCollect(bs0bj,1,1)
	else:
		MultiCollect(bs0bj)

	print("[*] Complete!")
