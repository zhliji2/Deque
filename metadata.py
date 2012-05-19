from hachoir_core.error import HachoirError
from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser
from hachoir_core.tools import makePrintable
from hachoir_metadata import extractMetadata
from hachoir_core.i18n import getTerminalCharset
from sys import argv, stderr, exit

class Metadata(object):
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
    
    def extractUseful(self, metadata):
        for section in metadata:
            tag = section['tag'].lower()
            if 'common' in tag:
                duration = section['Duration']
                fr = section['Frame rate'] if 'Frame rate' in section else ''
                print "General: %s %s" % (duration, fr)
            if 'video' in tag:
                height = section['Image height'][:3]+'p'
                print 'video: %s' % (height)
            elif 'audio' in tag:
                language = section['Language'] if 'Language' in section else ''
                print 'audio: %s' % (language)
            elif 'subtitle' in tag:
                print 'subtitle: %s' % (section['Language'])
            
videos = [
    "/Volumes/Shared/Shows/Black Lagoon/Season 1/01 The Black Lagoon.mkv",
    "/Volumes/Shared/Shows/Rurouni Kenshin/Season 1/[a4e]Rurouni_Kenshin_TV_01[divx5].ogm",
    "/Volumes/Shared/Shows/Adventure Time/Season 1/Adventure Time - 112a - Rainy Day Daydream [fudog].avi",
    "/Volumes/Shared/Shows/Avatar - The Last Airbende/Season 1/Ep. 01 - The Boy in the Iceberg-[720p].mkv",
    "/Volumes/Shared/Shows/Bleach/Season - 1 (ep.001-020)/Bleach - 01.avi",
    "/Volumes/Shared/Shows/Brainiac Science Abuse/Season 2/Brainiac.Science.Abuse.S02E01.mp4",
    "/Volumes/Shared/Shows/Chowder/Season 1/Chowder - S01E01 - The Froggy Apple.mp4",
    "/Volumes/Shared/Shows/Code Geass/Season 1/Code Geass 01.mkv",
]

#print Metadata().parseMetadata(b)

#for v in videos:
#    print '---'
#    m = Metadata().parseMetadata(Metadata().getMetadata(v))
#    Metadata().extractUseful(m)
