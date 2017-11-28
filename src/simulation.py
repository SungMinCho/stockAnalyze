from crawl import *
from corp import *
from datetime import *
from collections import defaultdict
import random
import math

class Simulation:
    def __init__(self, universe_names_codes, _start, _end, _strategy, _wallet):
        self.universe = [Corp(name, code, _start, _end) for (name, code) in universe_names_codes]
        self.universe = [corp for corp in self.universe if corp.loading_success]
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
        assert(corp.can_trade(t))
        p = corp.get_buy_price(t)
        if math.isnan(self.cash / p):
            print('debug nan', self.cash, p)
        ret = int(self.cash / p)
        return ret

    def get_total(self, t):
        ret = self.cash    
        for key, value in self.stocks.items():
            sp = key.get_recent_sell_price(t)
            if sp:
                ret += sp * value
        return ret

    def buy(self, t, corp, amount):
        assert(amount <= self.can_buy(t, corp))
        assert(corp.can_trade(t))
        p = corp.get_buy_price(t)
        if not p:
            return
        self.cash -= p*amount
        self.stocks[corp] += amount

    def sell(self, t, corp, amount):
        assert(amount <= self.stocks[corp])
        assert(corp.can_trade(t))
        p = corp.get_sell_price(t)
        if not p:
            return
        self.cash += p*amount
        self.stocks[corp] -= amount    

    def liquidate(self, t):
        for key, value in self.stocks.items():
            if key.can_trade(t):
                self.sell(t, key, value)

    def log(self, t):
        tot = self.get_total(t)
        print(str(t) + " total : " + str(tot) + " gain/loss : " + str((tot-self.original_cash)/self.original_cash * 100) + "%")
        


def RandomStrategy(t, universe, wallet):
    random.shuffle(universe)
    wallet.liquidate(t)
    target = universe[0]
    if target.can_trade(t):
        wallet.buy(t, universe[0], wallet.can_buy(t, universe[0]))
    wallet.log(t)
    
    
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def main():
    start = date.fromordinal(date.today().toordinal()-365*5)
    end = date.today()
    wallet = Wallet(1000000)

    ks = download_stock_codes('kospi')
    ks_names_codes = ks[['회사명','종목코드']]
    universe_names_codes = [(name, code+".KS") for (name, code) in ks_names_codes.head(20).itertuples(index=False)]

    sim = Simulation(universe_names_codes, start, end, RandomStrategy, wallet)

    for t in daterange(start,end):
        sim.run(t)

if __name__ == "__main__":
    main()
