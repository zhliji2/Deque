#!/usr/bin/python2
import metadata
import torrent
import argparse
from collections import Counter

parser = argparse.ArgumentParser(description='A management quere for watching shows with torrents.')
parser.add_argument("action", help="ls")
parser.add_argument("torrent", help="path to torrent file or magnet uri")
args = parser.parse_args()

#d = torrent.Downloader()
#d.add_from_ml(args.torrent)

tm = metadata.TorrentMetadata()
md = tm.fetch_metadata(args.torrent)
show_name = Counter([f[0]['series'] for f in md['files']]).most_common(1)[0][0]

sm = metadata.ShowMetadata()
md2 = sm.search_show(show_name)

def episode_name_from_number(blob, number):
    numberings = {f[0]['episodeNumber']: f[1] for f in blob if ('episodeNumber' in f[0])}
    return numberings[number]

d = torrent.Downloader()
handle = d.add_from_file(args.torrent)
def episode_path_from_name(paths, name):
    return [p for p in paths if p.endswith(name)][0]

name = episode_name_from_number(md['files'], 10)
path = episode_path_from_name(d.file_paths(handle), name)
d.mark_for_download(handle, path)
