import tornado.ioloop
import tornado.web
import subprocess
import socket
import urllib2

from spotify import Spotify

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        s = Spotify()
        verbs = ['skip']
        if s.isPlaying():
            verbs.append('pause')
        else:
            verbs.append('play')

        volume_filled = int(s.getVolume()/10)

        self.render('index.html',
                    verbs=verbs,
                    track_name=s.getTrackName(),
                    track_artist=s.getTrackArtist(),
                    volume_filled = volume_filled,
                    volume_empty = 10 - volume_filled)

class DoHandler(tornado.web.RequestHandler):
    def post(self):
        verb = self.get_argument('verb')
        s = Spotify()
        if verb == '+':
            s.louder()
        elif verb == '-':
            s.quieter()
        else:
            s.tell(verb)

        self.redirect('/')

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/do", DoHandler),
    ])

if __name__ == "__main__":
    # note the local address and report it to the master so that iphone
    # clients can simply hit the master's URL, and it'll know where to
    # redirect them so they hit this server (whatever IP it happens to be on)
    local_addr = socket.gethostbyname(socket.gethostname())
    f = urllib2.urlopen("http://a.mkjon.es/register", "addr=%s" % (local_addr))
    print "Local address: %s, reported remote address; %s" % (
        local_addr,
        f.readline())

    # now start up the app itself
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

