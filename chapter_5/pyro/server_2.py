import Pyro4
import chain_topology

current_server_name = "example.second"
next_server_name = "example.third"

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()

chain = chain_topology.Chain(current_server_name, next_server_name)

uri = daemon.register(chain)
ns.register(current_server_name, uri)

print("server {} started".format(current_server_name))
daemon.requestLoop()
