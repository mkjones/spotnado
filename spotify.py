import os
import subprocess
import binhex
import binascii


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

    def louder(self):
        current = self.getVolume()
        self.setVolume(current + 10)

    def quieter(self):
        current = self.getVolume()
        self.setVolume(current - 10)

    def getVolume(self):
        settings = self._exec('get volume settings')
        return int(settings.split(':')[1].split(',')[0])

    def setVolume(self, value):
        if (value > 100):
            raise Exception('invalid value %d' % (value))
        if (value < 0):
            raise Exception('too low value %d' % (value))

        self._exec('set volume output volume %d' % (value))

    def getArt(self):
        raw = self._get('artwork of current track')
        binary = binascii.a2b_hex(raw[11:-3])
        f = open('/tmp/whatever.tiff', 'w')
        f.write(binary)
        f.close()
        subprocess.Popen(('convert', '/tmp/whatever.tiff',
                          '/tmp/whatever.jpg')).wait()
        jpg = open('/tmp/whatever.jpg')
        ret = jpg.read(1000000)
        jpg.close()
        return ret

    def _get(self, thing):
        things = (
            'artwork of current track',
            'player state',
            'artist of current track',
            'name of current track',
            )
        return self._exec('tell application "Spotify" to set foo to %s' % (thing))

    def _tell(self, verb):
        self._exec('tell application "Spotify" to %s' % (verb))

    def _exec(self, script):
        args = ('osascript', '-e', script)
        sp = subprocess.Popen(args, stdout=subprocess.PIPE)
        return sp.stdout.readline()

