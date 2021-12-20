# first run pyro4-ns

import Pyro4


@Pyro4.expose
class GreetingMaker:
    def __init__(self, message):
        self.message = message

    def get_message(self):
        return "It's message: {}".format(self.message)


daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
oo = GreetingMaker('olala')
uri = daemon.register(oo)
ns.register("example.greeting", uri)
print("Ready.")
daemon.requestLoop()
