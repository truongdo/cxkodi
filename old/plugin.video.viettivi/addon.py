#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xbmcswift2 import Plugin
import urlfetch
import re
from BeautifulSoup import BeautifulSoup
import urllib

plugin = Plugin()

def getAllChannels():
    cookie = login()
    print 'Login Success'
    print cookie
    cns = []
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/64/4',cookie))
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/66/4',cookie))
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/67/4',cookie))
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/68/4',cookie))
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/70/4',cookie))
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/71/4',cookie))
    return cns

def getChannels(url,cookie):
    cns = []
    result = None
    result = urlfetch.fetch(
        url,
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
        cn = {
                'label': title,
                'path': plugin.url_for('plays',href = href, cookie = cookie),
                'is_playable': True
            }
        cns.append(cn)
    return cns
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
    #print result.status_code
    #print result.content
    if result.status_code != 200 :
        return None
    m = re.search(r'\"(http://.+\.cdnviet.com/.+\.m3u8\?.+)\"',result.content)
    if m == None :
        return None
    print m.group(1)
    return m.group(1)

@plugin.route('/')
def index():
    session = login()
    cns = getAllChannels()
    return cns

@plugin.route('/plays/<cookie>/<href>')
def plays(cookie,href):
    link = getLink(href,cookie)
    plugin.set_resolved_url(link)

if __name__ == '__main__':
    plugin.run()
