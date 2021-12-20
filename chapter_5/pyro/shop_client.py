import Pyro4
from contextlib import contextmanager


@contextmanager
def auth(shop, name):
    shop.log_in(name)
    yield
    shop.log_out(name)


class Client:
    def __init__(self, name):
        self.name = name

    def add_cash(self, shop, cash):
        with auth(shop, self.name):
            shop.deposit(self.name, cash)

    def show_balance(self, shop):
        with auth(shop, self.name):
            print("{} balance = {}".format(self.name, shop.balance(self.name)))

    def buy_book(self, shop):
        with auth(shop, self.name):
            shop.buy(self.name, 32)


if __name__ == '__main__':
    shop = Pyro4.Proxy("PYRONAME:example.shop.Shop")
    radmir = Client("Radmir")
    radmir.add_cash(shop, 500)
    radmir.show_balance(shop)
    radmir.buy_book(shop)
    radmir.show_balance(shop)
