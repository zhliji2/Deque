#!/usr/bin/python2
import metadata
import argparse

parser = argparse.ArgumentParser(description='A management quere for watching shows with torrents.')
parser.add_argument("action", help="ls")
parser.add_argument("torrent", help="path to torrent file or magnet uri")
args = parser.parse_args()

