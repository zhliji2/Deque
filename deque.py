#import stream
import torrent
import metadata
from guessit import guess_episode_info

links = open('links')

d = torrent.Downloader()
h = d.add_from_file('resume/((Demonoid.me))-[gg]_Puella_Magi_Madoka_Magica_1_12_[720p].torrent')
extensions = ["mkv"]
episodes = {}
for f in d.file_paths(h):
    if f.split('.')[-1] in extensions:
        episode = guess_episode_info(f.decode('utf8'), info = ['filename'])
        episodes[episode['episodeNumber']] = f

name = "Puella Magi Madoka Magica"
d.mark_for_download(h, episodes[1])
d.run_until_complete(d.torrents[0])
        
#d.generate_torrent(h)
#h = d.add_from_ml(links.read())
#d.generate_resume(h)
#d.mark_for_download(h, '')
#d.mark_for_download(h, '')
#d.run_until_complete(d.torrents[0])
