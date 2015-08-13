#! /usr/bin/python

import sys
import mfetcher

try:
    usage = """
        update
        fetch <manga_alias> <chapter>
        url <manga_alias> <chapter> <page>
    """

    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        print usage
        sys.exit(2)

    if len(sys.argv) > 2:
        manga_name = sys.argv[2]

    if len(sys.argv) > 3:
        chapter = sys.argv[3]

    if len(sys.argv) > 4:
        page = sys.argv[4]

    if command == "update":
        mfetcher.updateMangaDb()
        sys.exit(0)


    if command == "fetch":
        mfetcher.fetch(manga_name, chapter)
        sys.exit(0)

    if command == "url":
        url = mfetcher.get_page_url_from_coordinates(manga_name, chapter, page)
        print url
        sys.exit(0)

#  r = requests.get(base_mangaeden_url + "/0?p=1")
#  for manga in r.json()["manga"]:
#    print manga["a"], "\t", manga["i"]

except SystemExit, e:
    sys.exit(e)

except:
    e = sys.exc_info()[1]
    print e
    sys.exit(1)
