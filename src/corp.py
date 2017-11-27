import crawl as cw
from datetime import *


class Corp:
    slippage = 0.005
    tax = 0.003
    def __init__(self, _code, start=date.fromordinal(date.today().toordinal()-365*5), end=date.today()):
        print('loading ' + _code)
        self.code = _code
        self.prices = cw.get_stock(_code, start, end)

    def get_price(self, t):
        return self.prices.ix[t]

    def get_adjc(self, t):
        return self.prices.ix[t]['Adj Close']

    def get_buy_price(self, t):
        p = self.get_adjc(t)
        return p*(1+Corp.slippage)

    def get_sell_price(self, t):
        p = self.get_adjc(t)
        return p*(1-Corp.slippage-Corp.tax)

    def get_code(self):
        return self.code

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return self.code == other.code

    def __ne__(self, other):
        return not(self == other)
