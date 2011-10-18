import tornado.ioloop
import tornado.web

# Runs on a master server somewhere outside the local network.
# Takes a POST request with a single param ('addr') and stores
# it in a map from from "remote address" (i.e. the address that
# makes requests to the internet) to reported "internal address"
# (i.e. the address to which phones on the local network should
# make a connection in order to control spotify).
# Props to Ben Newhouse for the idea:
# https://www.facebook.com/mkjones/posts/933567910263
class RegisterHandler(tornado.web.RequestHandler):

    addrs = {}

    def post(self):

        internal_addr = self.get_argument('addr')
        external_addr = self.request.remote_ip
        RegisterHandler.addrs[external_addr] = internal_addr
        self.write(external_addr)

# Takes a simple get request, and based on its remote address, redirects
# to the corresponding internal address that was registered when the local
# server started up.
class RedirectLocalHandler(tornado.web.RequestHandler):

    def get(self):
        remote_ip = self.request.remote_ip
        internal = RegisterHandler.addrs.get(remote_ip, '')
        if (internal):
            self.redirect('http://%s:8888/' % (internal))
        else:
            self.write('unknown address %s' % (remote_ip))

application = tornado.web.Application([
    (r"/register", RegisterHandler),
    (r"/", RedirectLocalHandler),
    ])

if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()

