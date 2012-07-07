#http://blog.abourget.net/2009/6/14/gstreamer-rtp-and-live-streaming/n

import libtorrent as lt
import time
import os

class Downloader(object):
    def __init__(self):
        self.ses = lt.session()
        self.ses.add_extension(lt.create_ut_pex_plugin)
        self.ses.start_dht()
        self.ses.add_dht_router("router.bittorrent.com", 6881)
        self.ses.add_dht_router("router.utorrent.com", 6881)
        pe = lt.pe_settings()
        pe.out_enc_policy = lt.enc_policy.forced
        pe.in_enc_policy = lt.enc_policy.forced
        self.ses.set_pe_settings(pe)

    def add_from_ml(self, link):
        params = {
            'save_path': 'queue/',
            'storage_mode': lt.storage_mode_t(1)
        }
        handle = lt.add_magnet_uri(self.ses, link, params)
        self.prepare_handle(handle)
        return handle
    
    def add_from_file(self, filename):
        params = {
            'save_path': 'queue/',
            'storage_mode': lt.storage_mode_t(1),
            'ti': lt.torrent_info(filename)
        }
        handle = self.ses.add_torrent(params)
        self.prepare_handle(handle)
        return handle
    def save_torrent(self, handle):
        pass
    
    def file_paths(self, handle):
    	return [f.path for f in handle.get_torrent_info().files()]

    def file_names(self, handle):
        return {f.split('/')[-1]: f for f in self.file_paths(handle)}

    def mark_for_download(self, handle, path):
    	paths = self.file_paths(handle)
        handle.file_priority(paths.index(path), 1)

    def prepare_handle(self, handle):
        while (not handle.has_metadata()):
            time.sleep(1)
        handle.prioritize_files([0] * len(handle.file_priorities()) )
        handle.pause()

    def run_until_complete(self, handle):
        s = handle.status()
        while (s.state != lt.torrent_status.finished):
            s = handle.status()
            if (s.num_peers > 0):
                break
                time.sleep(5)

        while (s.state != lt.torrent_status.finished):
            s = handle.status()
            fields = (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)

            print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % fields
            time.sleep(5)

        print "Finished"

