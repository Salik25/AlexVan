import requests
from constants import KEY
import time
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


def get_top():
    payload = {'access_key': f'{KEY}'}
    r = requests.get('http://api.marketstack.com/v1/tickers', payload)
    for i in r.json()['data']:
        print(i['symbol'])


def get_top(count, date):
    payload = {'access_key': f'{KEY}'}
    r = requests.get('http://api.marketstack.com/v1/tickers', payload)
    fullpricetop = 0
    with tqdm(total=count) as pbar:
        tickers = r.json()['data']
        for i, ticker in enumerate(tickers):
            if i < count:
                payload = {'symbols': f'{ticker["symbol"]}', 'access_key': f'{KEY}', 'limit': 1, 'data': date}
                r = requests.get('http://api.marketstack.com/v1/eod', payload)
                fullpricetop += r.json()['data'][0]['close']
                pbar.update(1)
            else:
                break
    print(fullpricetop)


if __name__ == '__main__':
    count_of_tickers = int(input('Введите желаемое кол-во акций: '))
    get_top(count_of_tickers, get_time())
