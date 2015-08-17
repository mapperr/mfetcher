#! /usr/bin/python
from bottle import route, run, template
import mfetcher

mfetcher.updateMangaDb()

@route('/')
def list():
    mfetcher.updateMangaDb()
    templatePage = '''
        <html>
            <head>
            </head>
            <body>
                % for manga in mfetcher.database["manga"]:
                    <a href="{{manga["a"]}}">{{manga["t"]}}</a><br />
                % end
                <br />
                <br />
                Powered by <a href="http://mangaeden.com">mangaeden.com</a>
            </body>
        </html>
    '''
    return template(templatePage)

@route('/<manga>')
@route('/<manga>/<chapter>')
@route('/<manga>/<chapter>/<page>')
def image(manga,chapter=1,page=0):
    nextPage = int(page) + 1
    nextChapter = int(chapter) + 1
    nextPageUrl = '/'+manga+'/'+str(chapter)+'/'+str(nextPage)
    nextChapterUrl = '/'+manga+'/'+str(nextChapter)+'/0'
    imgUrl = mfetcher.get_page_url_from_coordinates(manga,chapter,page)
    nextImgUrl = mfetcher.get_page_url_from_coordinates(manga,chapter,nextPage)

    templatePage = '''
        <html>
            <head>
            </head>
            <body>
                <a href="{{nextPageUrl}}">
                    <img style="width:100%" src="{{imgUrl}}" />
                </a>
                <br />
                <br />
                Powered by <a href="http://mangaeden.com">mangaeden.com</a>
            </body>
        </html>
    '''
    nextUrl = nextPageUrl
    if nextImgUrl == None:
        nextUrl = nextChapterUrl

    return template(templatePage,nextPageUrl=nextUrl, imgUrl=imgUrl)

run(host='0.0.0.0', port=80)
