import requests
from constants import KEY


def main():
    payload = {'symbols': 'AAPL', 'access_key': f'{KEY}', 'limit': 1}
    r = requests.get('http://api.marketstack.com/v1/eod', payload)
    print(r.text)


def price_close():
    close = {'symbols': 'AAPL', 'access_key': f'{KEY}', 'limit': 1}
    r = requests.get('http://api.marketstack.com/v1/eod', close)
    print(r.json()['data'][0]['close'])


def get_ticker():
    payload = {'access_key': f'{KEY}'}
    r = requests.get('http://api.marketstack.com/v1/tickers', payload)
    for i in r.json()['data']:
        print(i['name'], ' - ', i['symbol'])


if __name__ == '__main__':
    get_ticker()
