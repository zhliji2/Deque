#http://blog.abourget.net/2009/6/14/gstreamer-rtp-and-live-streaming/n

import libtorrent as lt
import time

ses = lt.session()

ses.add_extension(lt.create_ut_pex_plugin)
ses.start_dht()

params = {
    'save_path': './',
    'storage_mode': lt.storage_mode_t(1)
}
link = "magnet:?xt=urn:btih:c3b72f56e1ca81f16170b828e94fd0c0f2938707&dn=bleach+anime+all+episodes+movies+english+subs&tr=http%3A%2F%2Ftracker.ccc.de%2Fannounce"

handle = lt.add_magnet_uri(ses, link, params)

print "Downloading metadata..."
while (not handle.has_metadata()):
    time.sleep(1)
print "Done."

paths = [f.path for f in handle.get_torrent_info().files()]

files = {f.split('/')[-1]: f for f in paths}

for f in sorted(files):
    print f

priorities = [0] * len(paths)
priorities[paths.index('Bleach Anime/Bleach/Bleach 001.avi')] = 1

handle.prioritize_files(priorities)

#handle.set_sequential_download(true)
#print dict(zip(files, handle.file_priorities()))

while (handle.status().state != lt.torrent_status.finished):
    s = handle.status()

    fields = (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, s.state)

    print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % fields
    time.sleep(5)

print "Finished"

