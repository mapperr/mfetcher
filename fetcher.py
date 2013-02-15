#! /usr/bin/python

import os
import urllib2
import argparse
from bs4 import BeautifulSoup
import urllib
import re

def fetchChapter(pageUrl,args,page=1):
	print "fetching page "+ str(page)
	pageHtml = urllib2.urlopen(pageUrl).read()
	soup = BeautifulSoup(pageHtml)
	linkImage = soup.find(id="image").get("src")
	formattedPage = str(page).zfill(3)
	imageFilename = args['manganame']+"_v"+args['volume']+"_c"+args['chapter']+"_p"+formattedPage+".jpg"
	if(not os.path.isfile(imageFilename)):
		print "fetching image: " + linkImage
		urllib.urlretrieve(linkImage, imageFilename)
	else:
			print "image "+imageFilename+" already exists"
	nexturl = soup.find(class_="next_page").get("href")
	if(nexturl.find("http") is not -1):
		fetchChapter(nexturl,args,(page+1))


urlbase = "http://www.mangahere.com/manga/"

parser = argparse.ArgumentParser()
parser.add_argument('-m','--manganame', help='manga name', required=True)
parser.add_argument('-v','--volume', help='volume number', required=False)
parser.add_argument('-c','--chapter', help='chapter number', required=False)

args = vars(parser.parse_args())

url = urlbase + args['manganame']

print "fetching summary for " + args['manganame']

result = urllib2.urlopen(url).read()

soup = BeautifulSoup(result)
detailNode = soup.find('div','detail_list')

chapterUrls = []
for liNode in detailNode.find('ul').find_all('li') :
	chapterUrls.append(liNode.find('a').get('href'))

if(args['volume'] is not None and args['chapter'] is not None):
	p = re.compile("v"+args['volume']+"/c"+args['chapter'])
	for chapterUrl in chapterUrls :
		m = p.search(chapterUrl)
		if(m is not None):
			print "matched chapter: " + chapterUrl
			fetchChapter(chapterUrl,args)
else:
	print chapterUrls
