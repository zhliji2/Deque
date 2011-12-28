#http://blog.abourget.net/2009/6/14/gstreamer-rtp-and-live-streaming/n

import libtorrent as lt
import time

class Downloader:
    def __init__(self):
        self.ses = lt.session()

        self.ses.add_extension(lt.create_ut_pex_plugin)
        self.ses.start_dht()

        self.torrents = list()

    def add_from_ml(self, link):
        params = {
            'save_path': './',
            'storage_mode': lt.storage_mode_t(1)
        }
        handle = lt.add_magnet_uri(self.ses, link, params)

        print "Downloading metadata..."
        while (not handle.has_metadata()):
            time.sleep(1)
        print "Done."

        handle.prioritize_files([0] * len(handle.file_priorities()) )

        handle.pause()

        self.torrents.append(handle)

        return handle
    
    def file_paths(self, handle):
    	return [f.path for f in handle.get_torrent_info().files()]

    def file_names(self, handle):
        return {f.split('/')[-1]: f for f in file_paths(handle)}
    
    def mark_for_download(self, handle, path):
    	paths = self.file_paths(handle)
    	priorities = handle.file_priorities()
        priorities[paths.index(path)] = 1
        handle.prioritize_files(priorities)

    def run_until_complete(self, handle):
        handle.resume()
        while (handle.status().state != lt.torrent_status.finished):
            s = handle.status()

            fields = (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)

            print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % fields
            time.sleep(5)

        print "Finished"

