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

        self.torrents = list()

    def add_from_ml(self, link):
        params = {
            'save_path': 'queue/',
            'storage_mode': lt.storage_mode_t(2)
        }
        handle = lt.add_magnet_uri(self.ses, link, params)
        self.prepare_handle(handle)
        return handle
    
    def add_from_file(self, filename):
        params = {
            'save_path': 'queue/',
            'storage_mode': lt.storage_mode_t(2),
            'ti': lt.torrent_info(filename)
        }
        handle = self.ses.add_torrent(params)
        self.prepare_handle(handle)
        return handle
    
    def file_paths(self, handle):
    	return [f.path for f in handle.get_torrent_info().files()]

    def file_names(self, handle):
        return {f.split('/')[-1]: f for f in self.file_paths(handle)}

    def generate_resume(self, handle):
        handle.pause()
        m = open('resume/'+handle.name()+'.metadata', "wb")
        m.write(handle.get_torrent_info().metadata())
        handle.save_resume_data()
        self.ses.wait_for_alert(10)
        alert = self.ses.pop_alert()
        while (type(alert)!=lt.save_resume_data_alert):
            self.ses.wait_for_alert(10)
            alert = self.ses.pop_alert()
        r = open('resume/'+handle.name()+'.resume', "wb")
        r.write(lt.bencode(alert.resume_data))
    
    def generate_torrent(self, handle):
        fs = lt.file_storage()
        lt.add_files(fs, handle.get_torrent_info().orig_files())
        t = lt.create_torrent(fs)
        for tracker in handle.get_torrent_info().trackers():
            t.add_tracker(tracker.url, tracker.tier)
        t.set_creator("Deque")
        t.set_comment("")
        t.set_priv(True)
        #lt.set_piece_hashes(t, "C:\\", lambda x: sys.stderr.write('.'))
        f = open('resume/'+handle.name()+'.torrent', "wb")
        f.write(lt.bencode(t.generate()))

    def load_resume(self):
        resumes = filter(lambda x: x.find('.resume')!=-1 ,os.listdir('resume'))
        metadatas = filter(lambda x: x.find('.metadata')!=-1 ,os.listdir('resume'))

        for f in zip(resumes, metadatas):
            r = {
            'save_path': 'queue/',
            'storage_mode': lt.storage_mode_t(1),
            "resume_data": open('resume/'+f[0],'rb').read(),
            }
            h = self.ses.add_torrent(r)
            h.get_torrent_info().set_metadata(open('resume/'+f[1],'rb').read())
            self.torrents.append(h)
            print h.status().state
    
    def mark_for_download(self, handle, path):
    	paths = self.file_paths(handle)
    	priorities = handle.file_priorities()
        priorities[paths.index(path)] = 1
        handle.prioritize_files(priorities)

    def prepare_handle(self, handle):
        print "Downloading metadata..."
        while (not handle.has_metadata()):
            time.sleep(1)
        print "Done."

        handle.prioritize_files([0] * len(handle.file_priorities()) )

        handle.pause()

        self.torrents.append(handle)

    def run_until_complete(self, handle):
        while (handle.status().state != lt.torrent_status.finished):
            s = handle.status()

            fields = (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)

            print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % fields
            time.sleep(5)

        print "Finished"

