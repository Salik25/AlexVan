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


def get_top(date):
    payload = {'access_key': f'{KEY}'}
    r = requests.get('http://api.marketstack.com/v1/tickers', payload)
    fullpricetop = 0
    count = 4
    g = 0
    with tqdm(total=count) as pbar:
        for i in r.json()['data']:
            if g < count:
                payload = {'symbols': f'{i["symbol"]}', 'access_key': f'{KEY}', 'limit': 1, 'data': date}
                r = requests.get('http://api.marketstack.com/v1/eod', payload)
                fullpricetop += r.json()['data'][0]['close']
                pbar.update(1)
                g += 1
            else:
                print(fullpricetop)
                break


if __name__ == '__main__':
    get_top(get_time())
