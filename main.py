import requests
from constants import KEY
import datetime
import math
from tqdm import tqdm


def get_count_of_day(y, m): # функция для подсчета кол-ва дней в месяце
    day_in_months = datetime.date(2000, m + 1, 1) - datetime.timedelta(days=1)
    return day_in_months


def get_count_day_in_months(day_in_months, y, m): # создание словаря из дат в выбранном месяце
    count_of_day_in_months = {}
    work_week = set(range(5))
    for i in range(1, day_in_months.day + 1):
        if datetime.date.weekday(datetime.date(y, m, i)) in work_week:
            count_of_day_in_months[datetime.date(y, m, i)] = 0
    return count_of_day_in_months


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
    count_of_requests = math.ceil(count / limit)
    for i in range(count_of_requests):
        payload = {'access_key': f'{KEY}', 'limit': limit, 'offset': offset}
        r = requests.get('http://api.marketstack.com/v1/tickers', payload)
        for j in r.json()['data']:
            list_of_tickers.append(j['symbol'])
        offset += limit
    list_of_tickers = list_of_tickers[:count]
    return list_of_tickers


def get_fullprice_of_top(count, date):
    fullpricetop = 0
    for ticker in tqdm(get_symbols(count)):
        payload = {'symbols': ticker, 'access_key': f'{KEY}', 'limit': 1, 'date_to': date}
        r = requests.get('http://api.marketstack.com/v1/eod', payload)
        fullpricetop += r.json()['data'][0]['close']
    return fullpricetop


def get_all_price_in_month(count, data): # заполнение словаря данными о ценнах топовых компаний в каждый из дней
    mass_keys_data = []
    for i in data.keys():
        mass_keys_data.append(i)
    for day in range(len(data)):
        data.update({mass_keys_data[day]: get_fullprice_of_top(count, mass_keys_data[day])})
    return data


def good_and_bad_day(mass_price, count_g_d, count_b_d): # соортировка словаря и поиск хороших и плохих дней
    list_price = list(mass_price.items())
    list_price.sort(key=lambda i: i[1])
    good_day = []
    bad_day = []
    for i in range(count_g_d):
        good_day.append(list_price[i])
    for i in range(count_b_d):
        bad_day.append(list_price[len(mass_price) - (i + 1)])
    return good_day, bad_day


if __name__ == '__main__':
    count_of_tickers = int(input('Введите желаемое кол-во акций: '))
    print('Выберите дату.')
    y = int(input('Введите год: '))
    m = int(input('Введите месяц: '))
    mass_day = get_count_day_in_months(get_count_of_day(y, m), y, m)
    # print(get_all_price_in_month(count_of_tickers, mass_day))
    count_of_good_day = int(input('Сколько хороших дней вывести: '))
    count_of_bad_day = int(input('Сколько плохих дней вывести: '))
    print(good_and_bad_day(get_all_price_in_month(count_of_tickers, mass_day), count_of_good_day, count_of_bad_day))
