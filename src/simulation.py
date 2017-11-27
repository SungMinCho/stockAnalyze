from crawl import *
from corp import *
from datetime import *
from collections import defaultdict
import random

class Simulation:
    def __init__(self, universe_codes, _start, _end, _strategy, _wallet):
        self.universe = [Corp(x, _start, _end) for x in universe_codes]
        self.start = _start
        self.end = _end
        self.strategy = _strategy
        self.wallet = _wallet

    def run(self, t):
        self.strategy(t, self.universe, self.wallet)

class Wallet:
    def __init__(self, _cash):
        self.original_cash = _cash
        self.cash = _cash
        self.stocks = defaultdict(lambda:0)  # dictionary from corp to amount of stocks

    def can_buy(self, t, corp):
        p = corp.get_buy_price(t)
        ret = int(self.cash / p)
        return ret

    def get_total(self, t):
        ret = self.cash    
        for key, value in self.stocks.items():
            ret += key.get_sell_price(t) * value
        return ret

    def buy(self, t, corp, amount):
        assert(amount <= self.can_buy(t, corp))
        p = corp.get_buy_price(t)
        self.cash -= p*amount
        self.stocks[corp] += amount

    def sell(self, t, corp, amount):
        assert(amount <= self.stocks[corp])
        p = corp.get_sell_price(t)
        self.cash += p*amount
        self.stocks[corp] -= amount    

    def liquidate(self, t):
        for key, value in self.stocks.items():
            self.sell(t, key, value)

    def log(self, t):
        tot = self.get_total(t)
        print(str(t) + " total : " + str(tot) + " gain/loss : " + str((tot-self.original_cash)/self.original_cash * 100) + "%")
        


def RandomStrategy(t, universe, wallet):
    random.shuffle(universe)
    wallet.liquidate(t)
    wallet.buy(t, universe[0], wallet.can_buy(t, universe[0]))
    wallet.log(t)
    
    
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def main():
    start = date.fromordinal(date.today().toordinal()-365*5)
    end = date.today()
    wallet = Wallet(1000000)

    ks_codes = download_stock_codes('kospi')
    universe_codes = [code+".KS" for code in ks_codes.종목코드.head()]

    sim = Simulation(universe_codes, start, end, RandomStrategy, wallet)

    for t in daterange(start,end):
        sim.run(t)

if __name__ == "__main__":
	main()
