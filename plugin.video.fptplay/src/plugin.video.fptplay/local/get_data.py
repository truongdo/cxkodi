#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 truong-d <truong-d@truongd-ThinkPad-X1-Carbon-3rd>
#
# Distributed under terms of the MIT license.

"""

"""

import urlfetch
import fptplay
from BeautifulSoup import BeautifulSoup
import json
crawurl = "https://fptplay.net/livetv"
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



    items = soup.findAll('div', {'class' : 'hover01'})

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
        channelid = dataref[27:]
        if not channelid :
            continue
        title = channelid
        cn = {
                'label': title,
                'path': fptplay.getLinkById(title),
                'thumbnail':imgthumbnail,
                'is_playable': True
            }

        cns.append(cn)

    return json.dumps(cns)

print getChannels("https://fptplay.net/livetv")
