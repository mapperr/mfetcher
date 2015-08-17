#! /usr/bin/python
from bottle import route, run, template
import mfetcher

mfetcher.updateMangaDb()

@route('/i/<manga>')
@route('/i/<manga>/<chapter>')
@route('/i/<manga>/<chapter>/<page>')
def image(manga,chapter=1,page=0):
    nextPage = int(page) + 1
    nextChapter = int(chapter) + 1
    nextPageUrl = '/i/'+manga+'/'+str(chapter)+'/'+str(nextPage)
    nextChapterUrl = '/i/'+manga+'/'+str(nextChapter)+'/0'
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

run(host='0.0.0.0', port=8080)
