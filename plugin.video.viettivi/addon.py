#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xbmcswift2 import Plugin
import urlfetch
import re
from BeautifulSoup import BeautifulSoup

plugin = Plugin()

def toItems(rawitems):
    cns = []
    for rit in rawitems :
        cn = {
                'label': rit[0],
                'path': rit[1],
                'is_playable': True
            }
        cns.append(cn)
    return cns

def getChannels():
    channels_cached = plugin.get_storage('channels',TTL=24*60)

    if len(channels_cached.items()) > 0 :
        print('from cache')
        return toItems(channels_cached.items())

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
        path = plugin.url_for('plays',href = href)
        channels_cached.update({title : path})
    print('new data')
    return toItems(channels_cached.items())

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

@plugin.route('/')
def index():
    cns = getChannels()
    return cns
@plugin.route('/plays/<href>')
def plays(href):
    link = getLink(href)
    plugin.set_resolved_url(link)

getChannels()

if __name__ == '__main__':
    plugin.run()
