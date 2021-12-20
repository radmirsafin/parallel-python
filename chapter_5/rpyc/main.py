import rpyc

c = rpyc.classic.connect("localhost")
c.execute("print('hello radmir')")
