import libtorrent as lt
import time

ses = lt.session()
ses.listen_on(6881, 6891)

link = "magnet:?xt=urn:btih:04C0FBA9E272E086C47C225A416A06C85FC70810&dn=Bleach%20Season%201-11%20%2b%20movies&tr=http%3a//tracker.thepiratebay.org/announce"


