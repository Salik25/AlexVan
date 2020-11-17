import requests
from constants import KEY
import time
import math
from tqdm import tqdm

def get_time():
    data = time.localtime()  # получить struct_time
    stroka = str(data.tm_year) + '-' + str(data.tm_mon) + '-' + str(data.tm_mday)
    stroka.split(' ')
    print(stroka + 'T00:00:00+0000')


def main():
    payload = {'symbols': 'AAPL', 'access_key': f'{KEY}', 'limit': 1}
    r = requests.get('http://api.marketstack.com/v1/eod', payload)
    print(r.text)


def price_close():
    close = {'symbols': 'AAPL', 'access_key': f'{KEY}', 'limit': 1}
    r = requests.get('http://api.marketstack.com/v1/eod', close)
    print(r.json()['data'][0]['close'])


def get_top_w():
    payload = {'access_key': f'{KEY}'}
    r = requests.get('http://api.marketstack.com/v1/tickers', payload)
    for i in r.json()['data']:
        print(i['symbol'])

"""
limit = a 
offset = b 
b, b+1, b+2, ... b+a-1 
limit = 3
надо набрать 10 акций
offset = 0, 3, 6, 9
акции = 0 1 2, 3 4 5, 6 7 8, 9 10 [11]
100
count_of_req = 34
34
i+3
"""
def get_symbols(count): 
    """
        count - кол-во акций которые надо получить 

        return - массив из symbols например ['APPL', 'MSFT', ....]
    """
    limit = 3
    offset = 0
    list_of_tickers = []
    count_of_requests = math.ceil(count/limit)
    for i in range(count_of_requests):
        payload = {'access_key': f'{KEY}', 'limit':limit, 'offset': offset}
        r = requests.get('http://api.marketstack.com/v1/tickers', payload)
        for j in r.json()['data']:
            list_of_tickers.append(j['symbol'])
        offset += limit
    list_of_tickers = list_of_tickers[:count]
    return list_of_tickers


def get_fullprice_of_top(count, date):
    fullpricetop = 0
    for ticker in tqdm(get_symbols(count)):
        payload = {'symbols': ticker, 'access_key': f'{KEY}', 'limit': 1, 'data': date}
        r = requests.get('http://api.marketstack.com/v1/eod', payload)
        fullpricetop += r.json()['data'][0]['close']           
    return fullpricetop


if __name__ == '__main__':
    count_of_tickers = int(input('Введите желаемое кол-во акций: '))
    print(get_fullprice_of_top(count_of_tickers, get_time()))
