import os, xbmc
import urlfetch
import re
from BeautifulSoup import BeautifulSoup
import urllib

def getLink(url = None, cookie = None):
    if url == None :
        return None
    if cookie == None :
        return None
    print cookie
    print url
    result = None
    result = urlfetch.fetch(
        url,
        headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
                'Cookie': cookie
                })
    if result.status_code != 200 :
        return None
    m = re.search(r'\"(http://.+\.cdnviet.com/.+\.m3u8\?.+)\"',result.content)
    if m == None :
        return None
    print m.group(1)
    return m.group(1)

def playVtv3():
    cookie = login()
    url = 'http://hplus.com.vn/vi/categories/live-tv'
    result = None
    result = urlfetch.fetch(url,
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
            'Cookie': cookie
            })
    if result.status_code != 200 :
        return None
    soup = BeautifulSoup(result.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
    items = soup.findAll('div', {'class' : 'panel'})
    for item in items:
        ac = item.find('a', {'class' : 'tooltips'})
        href = 'http://hplus.com.vn/' + ac.get('href')
        title = ac.find('h3').string
        if title == 'HTV9 HD' :
        	xbmc.Player().play(getLink(href,cookie))

def login():
    result = urlfetch.post(
        'http://hplus.com.vn/user/login/',
        data={"email": "mrcuxu@gmail.com",
            "passwd": "123456",
            "href": "http://hplus.com.vn/vi",
            "remember":"false",
            "linkNext":"",
            "proCode":""
            },
        headers={'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'
                }
        )
    if result.status_code != 200 :
        return None
    m = re.search(r'PHPSESSID=([^;]+);',result.headers['set-cookie'])
    if m == None :
        return None
    return m.group(0)

playVtv3()