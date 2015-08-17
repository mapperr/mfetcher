# /usr/bin/python

import logging
import requests
import json
import os

database = None
mangasInfo = {}
chaptersInfo = {}

logger = logging.getLogger("mfetcher")
logger.addHandler(logging.StreamHandler())
# logger.setLevel("DEBUG")

base_mangaeden_url = "https://www.mangaeden.com/api"
base_images_url = "https://cdn.mangaeden.com/mangasimg"
loginUrl = "https://www.mangaeden.com/ajax/login"
# e.g.: https://www.mangaeden.com/ajax/login/?username=X&password=Y
logoutUrl = "https://www.mangaeden.com/ajax/logout/"
myMangaUrl = "https://www.mangaeden.com/api/mymanga"

def updateMangaDb():
    r = requests.get(base_mangaeden_url + "/list/0")
    global database
    database = r.json()

def fetch(manga_name, chapter):
    manga_id = None

    for manga in database["manga"]:
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
    manga_id = None
    for manga in database["manga"]:
        if manga["a"] == mangaName:
            manga_id = manga["i"]
            logger.debug("found manga_id ["+manga_id+"]")
            return manga_id
    return None

def getChapterId(mangaId, chapterNumber):
    global mangasInfo
    if mangaId not in mangasInfo:
        logger.debug("updating cache with manga infos")
        r = requests.get(base_mangaeden_url + "/manga/" + mangaId)
        manga_data = r.json()
        mangasInfo[mangaId] = manga_data
    manga_data = mangasInfo[mangaId]
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
    global chaptersInfo
    if chapterId not in chaptersInfo:
        logger.debug("updating cache with chapter info")
        r = requests.get(base_mangaeden_url + "/chapter/" + chapterId)
        chapter_data = r.json()
        chaptersInfo[chapterId] = chapter_data
    images_data = chaptersInfo[chapterId]["images"]
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
