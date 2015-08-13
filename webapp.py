#! /usr/bin/python
from bottle import route, run, template
import mfetcher

mfetcher.updateMangaDb()

@route('/i/<manga>/<chapter>/<page>')
def image(manga,chapter,page):
    nextPage = int(page) + 1
    nextPageUrl = '/i/'+manga+'/'+str(chapter)+'/'+str(nextPage)
    imgUrl = mfetcher.get_page_url_from_coordinates(manga,chapter,page)
    templatePage = '''
        <a href="{{nextPageUrl}}">
            <img style="width:100%" src="{{imgUrl}}" />
        </a>
        <br />
        <br />
        Powered by <a href="http://mangaeden.com">mangaeden.com</a>
    '''
    return template(templatePage,nextPageUrl=nextPageUrl, imgUrl=imgUrl)
    # return template('<b>Hello {{name}}</b>!', name=name)

run(host='0.0.0.0', port=8080)
