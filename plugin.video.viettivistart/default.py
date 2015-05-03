import os, xbmc
from viettivi import addon as viettv

cns = viettv.getChannels()
for cn in cns:
	if cn['label'] == 'VTV3 HD':
		xbmc.Player().play('http://s3.amazonaws.com/KA-youtube-converted/ANyVpMS3HL4.mp4/ANyVpMS3HL4.mp4')