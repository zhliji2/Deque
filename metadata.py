from hachoir_core.error import HachoirError
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_core.tools import makePrintable
from hachoir_metadata import extractMetadata
from hachoir_core.i18n import getTerminalCharset
from sys import argv, stderr, exit

import requests
import json

class ShowMetadata(object):
    key = '1fa19d3aecbd7c51be3dd95a122b2ab7'

    def fetch_url(self, address):
            r = requests.get(address)
            return json.loads(r.text)

    def search_show(self, show):
        url = 'http://api.trakt.tv/search/shows.json/%s/%s'
        return fetch_url(url % (key, show))

    def episode_info(self, show, season, episode):
        url = 'http://api.trakt.tv/show/episode/summary.json/%s/%s/%i/%i'
        return fetch_url(url % (key, show, season, episode))

    def seasons_info(self, show):
        url = 'http://api.trakt.tv/show/seasons.json/%s/%s'
        return fetch_url(url % (key, show))

    def flat_to_season(self, show, number):
        seasons = {s['season']:s['episodes'] for s in seasons_info(show)}
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
