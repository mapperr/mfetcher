#! /usr/bin/python

import os
import urllib2
import argparse
from bs4 import BeautifulSoup
import urllib
import re

urlbase = "http://www.mangahere.com/manga/"

def fetchChapter(pageUrl,page=1):
	print "fetching page "+ str(page)
	pageHtml = urllib2.urlopen(pageUrl).read()
	soup = BeautifulSoup(pageHtml)
	linkImage = soup.find(id="image").get("src")
	formattedPage = str(page).zfill(3)
	pageUrl = pageUrl.replace(urlbase,"").replace("/","_")
	imageFilename = pageUrl + "_" + formattedPage + ".jpg"
	#imageFilename = args.manganame + "_v" + args.volume + "_c" + args.chapter + "_p" + formattedPage + ".jpg"
	if(not os.path.isfile(imageFilename)):
		print "fetching image: " + linkImage
		urllib.urlretrieve(linkImage, imageFilename)
	else:
			print "image "+imageFilename+" already exists"
	nexturl = soup.find(class_="next_page").get("href")
	if(nexturl.find("http") is not -1):
		fetchChapter(nexturl,(page+1))


parser = argparse.ArgumentParser()
parser.add_argument('manganame', type=str, help='manga name')
parser.add_argument('-v','--volume', help='volume number', required=False)
parser.add_argument('-c','--chapter', help='chapter number', required=False)
parser.add_argument('-l','--list', help='list chapters', required=False, action="store_true")
parser.add_argument('-f','--fetchall', help='fetch all the chapters', required=False, action="store_true")

args = parser.parse_args()

url = urlbase + args.manganame

print "fetching summary for " + args.manganame

result = urllib2.urlopen(url).read()

soup = BeautifulSoup(result)
detailNode = soup.find('div','detail_list')

chapterUrls = []
for liNode in detailNode.find('ul').find_all('li') :
	chapterUrls.append(liNode.find('a').get('href'))

if(args.chapter is not None or args.volume is not None) :
	volumeCompiledPattern = None
	chapterCompiledPattern = None
	mV = None
	mC = None
	if args.chapter is not None :
		chapterPattern = "c" + args.chapter
		chapterCompiledPattern = re.compile(chapterPattern)
	if args.volume is not None :
		volumePattern = "v" + args.volume
		volumeCompiledPattern = re.compile(volumePattern)
	for chapterUrl in reversed(chapterUrls) :
		if volumeCompiledPattern is not None:
			mV = volumeCompiledPattern.search(chapterUrl)
		if chapterCompiledPattern is not None:
			mC = chapterCompiledPattern.search(chapterUrl)
		if mV is not None or mC is not None :
			print "matched chapter: " + chapterUrl
			fetchChapter(chapterUrl)
else:
	if args.list :
		print "chapter list:"
		for chapterUrl in reversed(chapterUrls) :
			print chapterUrl
	elif args.fetchall :
		for chapterUrl in reversed(chapterUrls) :
			fetchChapter(chapterUrl)
	else:
		print "last chapter:" + chapterUrls[0]
