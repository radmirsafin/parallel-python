import Pyro4


class Account:
    def __init__(self):
        self._balance = 0.0

    def pay(self, price):
        self._balance -= price

    def deposit(self, cash):
        self._balance += cash

    def balance(self):
        return self._balance


@Pyro4.expose
class Shop:
    def __init__(self):
        self.name = "SUPER ANDY"
        self.accounts = {}

    def log_in(self, name):
        if name not in self.accounts.keys():
            self.accounts[name] = Account()
        print("{} log in".format(name))

    def log_out(self, name):
        print("{} log out".format(name))

    def deposit(self, name, amount):
        try:
            return self.accounts[name].deposit(amount)
        except KeyError:
            raise KeyError("Unknown username. Log in!")

    def balance(self, name):
        try:
            return self.accounts[name].balance()
        except KeyError:
            raise KeyError("Unknown username. Log in!")

    def all_accounts(self):
        accounts_balance = {}
        for k, v in self.accounts.items():
            accounts_balance[k] = v.balance()
        return accounts_balance

    def buy(self, name, price):
        self.accounts[name].pay(price)
