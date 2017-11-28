import crawl as cw
from datetime import *
import math


class Corp:
    slippage = 0.005
    tax = 0.003
    def __init__(self, _name, _code, start=date.fromordinal(date.today().toordinal()-365*5), end=date.today()):
        print('loading ' + _name + " " + _code)
        self.name = _name
        self.code = _code
        self.loading_success = False
        for i in range(10):
            try:
                self.prices = cw.get_stock(_code, start, end)
                self.loading_success = True
                break
            except Exception as e:
                print('error, trying again')
                pass

    def get_price(self, t):
        return self.prices.ix[t]

    def get_adjc(self, t):
        try:
            ret = self.prices.ix[t]['Adj Close']
            if math.isnan(ret):
                return None
            return ret
        except Exception as e:
            return None

    def get_buy_price(self, t):
        p = self.get_adjc(t)
        if math.isnan(p):
            print('debug nan1')
        if p:
            if math.isnan(p*(1+Corp.slippage)):
                print('debug nan2', p, 1+Corp.slippage)
            return p*(1+Corp.slippage)
        else:
            return None

    def get_sell_price(self, t):
        p = self.get_adjc(t)
        if p:
            return p*(1-Corp.slippage-Corp.tax)
        else:
            return None

    def get_recent_sell_price(self, t):
        for n in range(10): # look back at most 9 days
            p = self.get_sell_price(t - timedelta(n))
            if p:
                return p
        return None
        

    def get_name(self):
        return self.name

    def get_code(self):
        return self.code

    def can_trade(self, t):
        return (self.get_adjc(t) != None)

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return self.code == other.code

    def __ne__(self, other):
        return not(self == other)
