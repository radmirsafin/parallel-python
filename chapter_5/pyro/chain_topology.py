import Pyro4


@Pyro4.expose
class Chain:
    def __init__(self, current_server_name, next_server_name):
        self.current_server_name = current_server_name
        self.next_server_name = next_server_name
        self.next_server = None

    def process(self, message):
        if self.next_server is None:
            self.next_server = Pyro4.Proxy("PYRONAME:{}".format(self.next_server_name))

        if self.current_server_name in message:
            print("Back at {}; the chain is closed!".format(self.current_server_name))
            return ["complete at " + self.current_server_name]
        else:
            print("{} forwarding the message to the object {}".format(self.current_server_name, self.next_server_name))
            message.append(self.current_server_name)
            result = self.next_server.process(message)
            result.insert(0, "passed on from " + self.current_server_name)
            return result
