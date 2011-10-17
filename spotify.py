import os
import subprocess
import binhex


class Spotify:
    def tell(self, verb):
        verbs = ('play', 'pause', 'skip')
        if not verb in verbs:
            raise Exception('Invalid verb %s' % verb)
        if verb == 'skip':
            verb = 'next track'
        self._tell(verb)

    def isPlaying(self):
        out = self._get('player state').strip()
        print out
        return out == 'playing'

    def getTrackName(self):
        return self._get('name of current track')

    def getTrackArtist(self):
        return self._get('artist of current track')

    def getArt(self):
        raw = self._get('artwork of current track')
        data = raw[10:-1]
        f = open('/tmp/whatever', 'w')
        f.write(data)
        f.close
        binhex.hexbin(open('/tmp/whatever', 'r'),
                      open('/tmp/whatever.out', 'w'))


    def _get(self, thing):
        things = (
            'artwork of current track',
            'player state',
            'artist of current track',
            'name of current track',
            )
        print thing
        args = (
            'osascript',
            '-e',
            'tell application "Spotify" to set foo to %s' % (thing),
            )
        print args
        sp = subprocess.Popen(args, stdout=subprocess.PIPE)
        return sp.stdout.readline()

    def _tell(self, verb):
        args = ('osascript', '-e', 'tell application "Spotify" to %s' % (verb))
        print args
        subprocess.Popen(args)
