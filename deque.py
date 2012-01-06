#import stream
import torrent
import metadata

links = open('links')

d = torrent.Downloader()
h = d.add_from_ml(links.read())
#h = d.add_from_file('resume/-_Demonoid.me_-Bleach_All_Episodes_(1_328)_Highest_Quality_Eng_Subbed_6678995.2574.torrent')
#d.generate_torrent(h)
#d.generate_resume(h)
d.mark_for_download(h, 'Bleach Anime/Bleach/Bleach 001.avi')
#d.mark_for_download(h, 'Justice - Audio, Video, Disco (2011) [FLAC]/Audio, Video, Disco.log')
d.run_until_complete(d.torrents[0])
