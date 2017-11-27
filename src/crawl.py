import urllib.parse
import pandas as pd
from pandas_datareader import data as pdr
from pandas_datareader.google.daily import GoogleDailyReader
#import fix_yahoo_finance as yf
from tabulate import tabulate
from datetime import *
from yahoo_finance import Share

#yf.pdr_override()

MARKET_CODE_DICT = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt',
    'konex': 'konexMkt'
}

DOWNLOAD_URL = 'kind.krx.co.kr/corpgeneral/corpList.do'

def download_stock_codes(market=None, delisted=False):
    params = {'method': 'download'}

    if market.lower() in MARKET_CODE_DICT:
        params['marketType'] = MARKET_CODE_DICT[market]

    if not delisted:
        params['searchType'] = 13

    params_string = urllib.parse.urlencode(params)
    request_url = urllib.parse.urlunsplit(['http', DOWNLOAD_URL, '', params_string, ''])

    df = pd.read_html(request_url, header=0)[0]
    df.종목코드 = df.종목코드.map('{:06d}'.format)

    return df

def get_fund(code, fin_typ, freq_typ):
    url_tmp = 'http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=%s&fin_typ=%s&freq_typ=%s'
    url = url_tmp % (code, fin_typ, freq_typ) # 삼성전자, 4(IFRS 연결), Y:년 단위

    dfs = pd.read_html(url)
    df = dfs[0]
    df = df.set_index('주요재무정보')
    return df

def get_stock(code, start=date.fromordinal(date.today().toordinal()-365*5), end=date.today()):
    return pdr.DataReader(code, "yahoo", start, end)

def get_kospi(code, start=date.fromordinal(date.today().toordinal()-365*5), end=date.today()):
    return get_stock(code+".KS", start, end)

#Fix this. can't get kosdaq from both google and yahoo.
def get_kosdaq(code, start=date.fromordinal(date.today().toordinal()-365*5), end=date.today()):
    #return get_stock(code+".KQ", start, end)
    return pdr.DataReader("KOSDAQ:"+code, "google", start, end)


def pp(s):
    print(tabulate(s))

def main():
    ks_codes = download_stock_codes('kospi')

    results = {}

    for code in ks_codes.종목코드.head():
        try:
            results[code] = get_kospi(code)
        except Exception as e:
            pass

    df = pd.concat(results, axis=1)
    pp(df.loc[:,pd.IndexSlice[:, 'Adj Close']].tail()) 


if __name__ == "__main__":
    main()
