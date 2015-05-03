import os, xbmc
import urlfetch
import re
from BeautifulSoup import BeautifulSoup

def getLink(url = None):
    if url == None :
        return None
    result = None
    result = urlfetch.fetch(url)
    if result.status_code != 200 :
        return None
    m = re.search(r'\"(http://.+\.cdnviet.com/.+\.m3u8\?.+)\"',result.content)
    if m == None :
        return None
    return m.group(1)

def playVtv3():
    url = 'http://hplus.com.vn/vi/categories/live-tv'
    result = None
    result = urlfetch.fetch(url)
    if result.status_code != 200 :
        return None
    soup = BeautifulSoup(result.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
    items = soup.findAll('div', {'class' : 'panel'})
    for item in items:
        ac = item.find('a', {'class' : 'tooltips'})
        href = 'http://hplus.com.vn/' + ac.get('href')
        title = ac.find('h3').string
        if title = 'VTV3 HD':
        	xbmc.Player().play(getLink(href))

playVtv3()