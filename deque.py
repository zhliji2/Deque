import libtorrent as lt
import time

ses = lt.session()
params = { 'save_path': './'}
link = "magnet:?xt=urn:btih:3095CFD5EA94AC38074FF722E6682352AB187AAB&dn=Bleach&tr=http%3a//inferno.demonoid.me%3a3395/announce"

handle = lt.add_magnet_uri(ses, link, params)

while (not handle.has_metadata()):
    print "Nope."
    time.sleep(1)

while (handle.status().state != lt.torrent_status.seeding):
    s = handle.status()

    print s.progress, s.download_rate, s.upload_rate, s.num_peers, s.state, s.total_download
    time.sleep(5)