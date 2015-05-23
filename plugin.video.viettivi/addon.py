#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xbmcswift2 import Plugin
import urlfetch
import re
from BeautifulSoup import BeautifulSoup

plugin = Plugin()

def getAllChannels():
    cns = []
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/64/4'))
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/66/4'))
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/67/4'))
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/68/4'))
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/70/4'))
    cns.extend(getChannels('http://hplus.com.vn/vi/genre/index/71/4'))
    return cns

def getChannels(url):
    cns = []
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
        cn = {
                'label': title,
                'path': plugin.url_for('plays',href = href),
                'is_playable': True
            }
        cns.append(cn)
    return cns

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

@plugin.cached_route('/')
def index():
    cns = getAllChannels()
    return cns
@plugin.route('/plays/<href>')
def plays(href):
    link = getLink(href)
    plugin.set_resolved_url(link)

if __name__ == '__main__':
    plugin.run()
