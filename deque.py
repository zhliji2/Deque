#import stream
import torrent

links = open('links')

d = torrent.Downloader()
h = d.add_from_ml(links.read())
d.mark_for_download(h, 'Bleach Anime/Bleach/Bleach 001.avi')
d.run_until_complete(h)

links.close()