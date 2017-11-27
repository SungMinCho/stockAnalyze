import crawl as cw
from datetime import *


class Corp:
    slippage = 0.005
    tax = 0.003
    def __init__(self, _code, start=date.fromordinal(date.today().toordinal()-365*5), end=date.today()):
        print('loading ' + _code)
        self.code = _code
        while True:
            try:
                self.prices = cw.get_stock(_code, start, end)
                break
            except Exception as e:
                print('error, trying again')
                pass

    def get_price(self, t):
        return self.prices.ix[t]

    def get_adjc(self, t):
        try:
            return self.prices.ix[t]['Adj Close']
        except Exception as e:
            return None

    def get_buy_price(self, t):
        p = self.get_adjc(t)
        if p:
            return p*(1+Corp.slippage)
        else:
            return None

    def get_sell_price(self, t):
        p = self.get_adjc(t)
        if p:
            return p*(1-Corp.slippage-Corp.tax)
        else:
            return None

    def get_code(self):
        return self.code

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return self.code == other.code

    def __ne__(self, other):
        return not(self == other)
