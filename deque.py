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

while (not handle.has_metadata()):
    print "Nope."
    time.sleep(1)

files = [f.path for f in handle.get_torrent_info().files()]

priorities = [0] * len(files)
priorities[files.index('Bleach Anime/Bleach/Bleach 001.avi')] = 1

handle.prioritize_files(priorities)

print dict(zip(files, handle.file_priorities()))

while (handle.status().state != lt.torrent_status.finished):
    s = handle.status()

    print float(int(s.progress*10000)/100), s.download_rate, s.upload_rate, s.num_peers, s.state, s.total_download
    time.sleep(5)

print "Finished"