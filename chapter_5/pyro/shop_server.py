import Pyro4
import shop

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(shop.Shop())
ns.register("example.shop.Shop", uri)
print("Shop started")
daemon.requestLoop()
