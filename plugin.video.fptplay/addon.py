#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xbmcswift2 import Plugin,xbmcaddon, xbmc
import urlfetch
import re
from BeautifulSoup import BeautifulSoup
import urllib
import json
import sys

plugin = Plugin()
__settings__ = xbmcaddon.Addon(id='plugin.video.fptplay')
crawurl = 'http://fptplay.net/livetv'

def getAllChannels():
    cns = []
    cns.extend(getChannels(crawurl))
    return cns

def getChannels(url):
    cns = []
    result = None
    result = urlfetch.fetch(
        url,
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'
            })
    if result.status_code != 200 :
        plugin.log.error('Something wrong when get list fpt play channel !')
        return None
    soup = BeautifulSoup(result.content, convertEntities=BeautifulSoup.HTML_ENTITIES)
    
    items = soup.findAll('div', {'class' : 'item_view'})
    for item in items:
            
        ac = item.find('a', {'class' : 'tv_channel '})
        
        if ac == None :
            ac = item.find('a', {'class' : 'tv_channel active'})
            if ac == None :
                continue
        
        lock = item.find('img', {'class' : 'lock'})
        
        if lock != None :
            continue
        
        dataref = ac.get('data-href')
        
        if dataref == None :
            continue
        
        img = ac.find('img', {'class' : 'img-responsive'})
        
        imgthumbnail = ''
        
        if img != None :
            imgthumbnail = img.get('data-original')
            
        if not dataref.startswith(crawurl) :
            continue
            
        channelid = dataref[26:]
        
        if not channelid :
            continue
            
        title = channelid
        cn = {
                'label': title,
                'path': plugin.url_for('plays', id = channelid),
                'thumbnail':imgthumbnail,
                'is_playable': True
            }
        cns.append(cn)
    return cns

def getLink(id = None):
    
    plugin.log.info('Get Link For Id ' + id)
    
    result = urlfetch.post(
        'http://fptplay.net/show/getlinklivetv',
        data={"id": id,
            "quality": "4",
            "mobile": "web"
            },
        headers={'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'
                }
        )
        
    if result.status_code != 200 :
        plugin.log.error("Can't get link for id " + id)
        return None
    info = json.loads(result.content)
    print info
    return info['stream']

@plugin.route('/')
def index():
    cns = getAllChannels()
    return cns

@plugin.route('/plays/<id>')
def plays(id):
    link = getLink(id)
    plugin.set_resolved_url(link)

def startChannel():
    channelid = __settings__.getSetting('start_channelid')
    link = getLink(channelid)
    xbmc.Player().play(link)
    
if __name__ == '__main__':
    plugin.run()
    
