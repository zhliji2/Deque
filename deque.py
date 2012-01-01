#import stream
import torrent

links = open('links')

d = torrent.Downloader()
#h = d.add_from_ml(links.read())
h = d.add_from_file('resume/Justice_-_Audio__Video__Disco_(2011)_[FLAC]_(CUE___LOG).6760385.TPB.torrent')
#d.generate_torrent(h)
#d.generate_resume(h)
#d.mark_for_download(h, 'Bleach Anime/Bleach/Bleach 001.avi')
d.mark_for_download(h, 'Justice - Audio, Video, Disco (2011) [FLAC]/Audio, Video, Disco.log')
d.run_until_complete(d.torrents[0])
