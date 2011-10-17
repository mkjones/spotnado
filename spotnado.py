import tornado.ioloop
import tornado.web
from spotify import Spotify
import subprocess

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        s = Spotify()
        verbs = ['skip']
        if s.isPlaying():
            verbs.append('pause')
        else:
            verbs.append('play')

        self.render('index.html',
                    verbs=verbs,
                    track_name=s.getTrackName(),
                    track_artist=s.getTrackArtist())

class DoHandler(tornado.web.RequestHandler):
    def post(self):
        verb = self.get_argument('verb')
        s = Spotify()
        s.tell(verb)

        self.redirect('/')

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/do", DoHandler),
    ])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

