# /usr/bin/python

import logging
import requests
import json
import os

logger = logging.getLogger("mfetcher")
logger.addHandler(logging.StreamHandler())
# logger.setLevel("DEBUG")

database_file = "mangadb.json"
base_mangaeden_url = "https://www.mangaeden.com/api"
base_images_url = "https://cdn.mangaeden.com/mangasimg"
loginUrl = "https://www.mangaeden.com/ajax/login"
# e.g.: https://www.mangaeden.com/ajax/login/?username=X&password=Y
logoutUrl = "https://www.mangaeden.com/ajax/logout/"
myMangaUrl = "https://www.mangaeden.com/api/mymanga"

def updateMangaDb():
    r = requests.get(base_mangaeden_url + "/list/0")
    f = open(database_file,"w")
    f.write(r.text)
    f.close()

def fetch(manga_name, chapter):
    with open(database_file) as dbfile:
        data = json.load(dbfile)

    manga_id = None

    for manga in data["manga"]:
        if manga["a"] == manga_name:
            manga_id = manga["i"]
            break

    if manga_id == None:
        print "[", manga_name, "] not found"
        return 1

    r = requests.get(base_mangaeden_url + "/manga/" + manga_id)
    manga_data = r.json()
    chapters_data = manga_data["chapters"]

    try:
        chapter
    except NameError:
        chapter = None

    if chapter != None:

        chapter_id = None
        for chapter_data in chapters_data:
            if chapter_data[0] == int(chapter):
                chapter_id = chapter_data[3]
                break

        if chapter_id == None:
            print "chapter [",chapter,"] not found"
            return 1

        r = requests.get(base_mangaeden_url + "/chapter/" + chapter_id)
        images_data = r.json()["images"]
        directory = manga_name + "__" + chapter
        if not os.path.exists(directory):
            os.makedirs(directory)
        for image_data in images_data:
            image_url = image_data[1]
            image_number = image_data[0]
            r = requests.get(base_images_url + "/" + image_url)
            f = open(directory+"/"+str(image_number)+".jpg", "w")
            f.write(r.content)
            f.close()
    else:
        print r.text


def getMangaId(mangaName):
    logger.info("getting manga_id of ["+mangaName+"] from local database")
    with open(database_file) as dbfile:
        data = json.load(dbfile)
    manga_id = None
    for manga in data["manga"]:
        if manga["a"] == mangaName:
            manga_id = manga["i"]
            logger.debug("found manga_id ["+manga_id+"]")
            return manga_id
    return None

def getChapterId(mangaId, chapterNumber):
    r = requests.get(base_mangaeden_url + "/manga/" + mangaId)
    manga_data = r.json()
    chapters_data = manga_data["chapters"]
    logger.info("getting chapter ["+str(chapterNumber)+"]")
    chapter_id = None
    for chapter_data in chapters_data:
        chapter_index = chapter_data[0]
        logger.debug("checking chapter_index ["+str(chapter_index)+"]")
        if chapter_index == int(chapterNumber):
            chapter_id = chapter_data[3]
            logger.debug("found chapter_id ["+str(chapter_id)+"]")
            return chapter_id
    return None

def getImageUrl(chapterId, pageNumber):
    logger.info("getting page ["+str(pageNumber)+"]")
    r = requests.get(base_mangaeden_url + "/chapter/" + chapterId)
    images_data = r.json()["images"]
    for image_data in images_data:
        image_number = image_data[0]
        logger.debug("checking image_number ["+str(image_number)+"]")
        if image_number == int(pageNumber):
            image_url = image_data[1]
            return base_images_url + "/" + image_url
    return None

def get_page_url_from_coordinates(manga_name, chapter_number, page_number):
    manga_id = getMangaId(manga_name)
    chapter_id = getChapterId(manga_id, chapter_number)
    return getImageUrl(chapter_id, page_number)
