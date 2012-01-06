import Pyro.core
import torrent

class Controller(Pyro.core.ObjBase):
        def __init__(self):
                Pyro.core.ObjBase.__init__(self)
                self.d = torrent.Downloader()
        

Pyro.core.initServer()
daemon=Pyro.core.Daemon()
uri=daemon.connect(Controller(),"controller")

open('uri', 'w').write(str(uri))

daemon.requestLoop()