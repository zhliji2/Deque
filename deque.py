import stream
import torrent

d = torrent.Downloader()
h = d.add_from_ml(r'magnet:?xt=urn:btih:c3b72f56e1ca81f16170b828e94fd0c0f2938707&dn=Bleach+Anime+-+All+Episodes+%26+Movies+-+English+Subs&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.ccc.de%3A80e')
d.mark_for_download(h, 'Bleach Anime/Bleach/Bleach 001.avi')
d.run_until_complete(h)