from hachoir_core.error import HachoirError
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_core.tools import makePrintable
from hachoir_metadata import extractMetadata
from hachoir_core.i18n import getTerminalCharset
from sys import argv, stderr, exit

import requests
import json

import torrent

from guessit import guess_episode_info

class TorrentMetadata(object):
    def fetch_metadata(self, filename):
        d = torrent.Downloader()
        handle = d.add_from_file(filename)
        d.ses.set_alert_mask(16)
        handle.scrape_tracker()
        d.ses.wait_for_alert(20000)

        return {
            'seeds': handle.status().num_complete,
            'leeches': handle.status().num_incomplete,
            'files': handle.get_torrent_info().files()
        }

class ShowMetadata(object):
    key = '1fa19d3aecbd7c51be3dd95a122b2ab7'

    def fetch_url(self, address):
            r = requests.get(address)
            return json.loads(r.text)

    def search_show(self, show):
        url = 'http://api.trakt.tv/search/shows.json/%s/%s'
        return self.fetch_url(url % (self.key, show.replace(" ", "+")))

    def episode_info(self, show, season, episode):
        url = 'http://api.trakt.tv/show/episode/summary.json/%s/%s/%i/%i'
        return self.fetch_url(url % (self.key, show.replace(" ", "+"), season, episode))

    def seasons_info(self, show):
        url = 'http://api.trakt.tv/show/seasons.json/%s/%s'
        return self.fetch_url(url % (self.key, show.replace(" ", "+")))

    def flat_to_season(self, show, numer):
        seasons = {s['season']:s['episodes'] for s in self.seasons_info(show)}
        if 0 in seasons:
            del seasons[0]
        for s in seasons:
            if number - seasons[s] > 0:
                number -= seasons[s]
            else:
                return (s, number)


class VideoMetadata(object):
    def getMetadata(self, filename):
        filename, realname = unicodeFilename(filename), filename
        parser = createParser(filename, realname)
        if not parser:
            print >>stderr, "Unable to parse file"
            exit(1)
        try:
            metadata = extractMetadata(parser)
        except HachoirError, err:
            print "Metadata extraction error: %s" % unicode(err)
            metadata = None
        if not metadata:
            print "Unable to extract metadata"
            exit(1)

        return metadata.exportPlaintext()

    def parseMetadata(self, metadata):
        parts = []
        next = {}
        for line in metadata:
            if line.startswith('- '):
                kv = line.split(':')
                next[kv[0][2:]] = kv[1][1:]
            else:
                parts.append(next)
                next = {}
                next['tag'] = line[:-1]
        
        del parts[0]
        return parts
    
    def extractUseful(self, filename):
        metadata = self.getMetadata(filename)
        parsed = self.parseMetadata(metadata)
        useful = {}
        for section in parsed:
            tag = section['tag'].lower()
            if 'common' in tag:
                duration = section['Duration']
                fr = section['Frame rate'] if 'Frame rate' in section else ''
                print "General: %s %s" % (duration, fr)
            if 'video' in tag:
                height = section['Image height'][:3]+'p'
                compression = section['Compression']
                print 'video: %s (%s)' % (height, compression)
            elif 'audio' in tag:
                language = section['Language'] if 'Language' in section else ''
                print 'audio: %s' % (language)
            elif 'subtitle' in tag:
                print 'subtitle: %s' % (section['Language'])
