import Pyro4

server = Pyro4.Proxy("PYRONAME:example.first")
print("Result={}".format(server.process(["hello"])))
