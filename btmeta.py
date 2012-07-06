#!/usr/bin/python
import argparse
import libtorrent as lt

parser = argparse.ArgumentParser(description='Print metadata for a torrent')
parser.add_argument("torrent", help="path to torrent file or magnet uri")
args = parser.parse_args()
session = lt.session()
handle = session.add_torrent({
    'save_path': 'queue/',
    'storage_mode': lt.storage_mode_t(1),
    'ti': lt.torrent_info(args.torrent)
    })
handle.pause()
handle.prioritize_files([0] * len(handle.file_priorities()) )
handle.scrape_tracker()
while handle.status().state != lt.torrent_status.downloading:
    pass
print session.wait_for_alert(20000)
print session.pop_alert()
print handle.status().num_complete, handle.status().num_incomplete()
