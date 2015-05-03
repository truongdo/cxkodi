import os, xbmc, xbmcaddon

my_addon = xbmcaddon.Addon('plugin.video.viettivi')
addon_dir = xbmc.translatePath( my_addon.getAddonInfo('path') )

sys.path.append(os.path.join( addon_dir, 'resources', 'lib' ) )

from viettivi import addon as viettv

cns = viettv.getChannels()
for cn in cns:
	if cn['label'] == 'VTV3 HD':
		xbmc.Player().play('http://s3.amazonaws.com/KA-youtube-converted/ANyVpMS3HL4.mp4/ANyVpMS3HL4.mp4')