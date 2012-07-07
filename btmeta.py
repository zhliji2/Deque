#!/usr/bin/python2
import argparse
import torrent

parser = argparse.ArgumentParser(description='Print metadata for a torrent')
parser.add_argument("torrent", help="path to torrent file or magnet uri")
args = parser.parse_args()

d = torrent.Downloader()
handle = d.add_from_file(args.torrent)
d.ses.set_alert_mask(16)
handle.scrape_tracker()
d.ses.wait_for_alert(20000)

print handle.status().num_complete, handle.status().num_incomplete
files = handle.get_torrent_info().files()
for f in files:
    print "%s, %s" % (f.path.split('/')[-1], f.size)
