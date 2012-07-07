#!/usr/bin/python2
import metadata
import argparse

parser = argparse.ArgumentParser(description='Print metadata for a torrent')
parser.add_argument("action", help="ls")
parser.add_argument("torrent", help="path to torrent file or magnet uri")
args = parser.parse_args()

m = metadata.TorrentMetadata()

print m.fetch_metadata(args.torrent)
