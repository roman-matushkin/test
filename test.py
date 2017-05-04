import requests
import sys
import re
from lxml import html


def enter_data():
    keys_for_user_data = ['departure', 'destination', 'outboundDate', 'returnDate']
    print('Hello! Please enter parameters of the desired flight separated by a comma')
    print('Departure(IATA airport code), destination(IATA airport code),'
          ' outbound date(yyyy-mm-dd), returnDate(optional)')
    data = input().split(',')
    # Check date format
    match_outbound = re.search(r'\d\d\d\d-\d\d-\d\d', data[2])
    if match_outbound:
        dict_user_data = gen_dict_from_enter_data(keys_for_user_data, data)
    else:
        print('Sorry, date entered incorrectly. Please try again')
        print('Departure(IATA airport code), destination(IATA airport code), outbound date(yyyy-mm-dd),'
              ' returnDate(optional)')
        dict_user_data = gen_dict_from_enter_data(keys_for_user_data, data)
    return dict_user_data


def gen_dict_from_enter_data(keys_for_user_data, data):
    dict_user_data = {keys_for_user_data[i]: data[i] for i in range(len(data))}
    dict_user_data['oneway'] = 0
    if 4 == len(dict_user_data):
        dict_user_data['returnDate'] = dict_user_data['outboundDate']
        dict_user_data['oneway'] = 'on'
    # flag oneway ticket
    return dict_user_data


def request(dict_user_data):
    my_url = 'http://www.flyniki.com/ru/booking/flight/vacancy.php?'
    value = {'departure': dict_user_data['departure'], 'destination': dict_user_data['destination'],
             'outboundDate': dict_user_data['outboundDate'], 'returnDate': dict_user_data['returnDate'],
             'oneway': dict_user_data['oneway'], 'openDateOverview': 0, 'adultCount': 1, 'childCount': 0,
             'infantCount': 0}
    value_ajax = {'_ajax[templates][]': 'main',
                  '_ajax[requestParams][departure]': dict_user_data['departure'],
                  '_ajax[requestParams][destination]': dict_user_data['destination'],
                  '_ajax[requestParams][returnDeparture]': '',
                  '_ajax[requestParams][returnDestination]': '',
                  '_ajax[requestParams][outboundDate]': dict_user_data['outboundDate'],
                  '_ajax[requestParams][returnDate]': dict_user_data['returnDate'],
                  '_ajax[requestParams][adultCount]': '1',
                  '_ajax[requestParams][childCount]': '0',
                  '_ajax[requestParams][infantCount]': '0',
                  '_ajax[requestParams][openDateOverview]': '',
                  '_ajax[requestParams][oneway]': dict_user_data['oneway']}
    try:
        session = requests.Session()
        r = session.get(my_url, params=value)
        text_json = session.post(r.url, data=value_ajax)
    except Exception:
        print('Error web req!')
        print(sys.exc_info()[1])
        sys.exit()
    return text_json


def parser(text_json, flag_oneway):
    try:
        flights = {}
        text = text_json['templates']['main']
        html_text = html.fromstring(text)
        outbound_table = html_text.xpath(
            './/*[@id="flighttables"]/*[@class="outbound block"]/*[@class="tablebackground"]/table/tbody')
        flights['outbound'] = table_processing(outbound_table[0])
        currency_html = html_text.xpath(
            './/*[@id="flighttables"]/*[@class="outbound block"]/*[@class="tablebackground"]/table/thead/tr[2]/*[@id]')
        flights['currency'] = currency_html[0].text
        if flag_oneway == 0:
            return_table = html_text.xpath(
                './/*[@id="flighttables"]/*[@class="return block"]/*[@class="tablebackground"]/table/tbody')
            flights['return'] = table_processing(return_table[0])
    except Exception:
        print('No flights found. Please check your search and try again.')
        sys.exit()
    return flights


def table_processing(table):
    info = {}
    num_tr = len(table)
    for num_tr in range(1, num_tr, 2):
        info_tr = {}
        tr = table.xpath(r'tr[' + str(num_tr) + ']')
        time_html = tr[0].xpath(r'td[2]/*[@id]/time')
        info_tr['time'] = [t.text for t in time_html]
        duration_html = tr[0].xpath(r'td[4]/*[@id]')
        info_tr['duration'] = duration_html[0].text
        price_economy_html = tr[0].xpath(r'td[5]/label/*[@class="lowest"]/*[@id]')
        info_tr['price_economy'] = check_price(price_economy_html)
        price_economflex_html = tr[0].xpath(r'td[6]/label/*[@class="lowest"]/*[@id]')
        info_tr['price_economflex'] = check_price(price_economflex_html)
        price_business_html = tr[0].xpath(r'td[7]/label/*[@class="lowest"]/*[@id]')
        info_tr['price_business'] = check_price(price_business_html)
        info[num_tr] = info_tr
    return info


def check_price(price):
    if len(price) > 0:
        p_text = price[0].text
        p = p_text[0:-3]
        p = p.split('.')
        p = p[0] + p[1]
    else:
        p = 0
    return int(p)


def flights_combination(flights, flag_oneway):
    print('Currency', flights['currency'])
    if flag_oneway == 'on':
        print([['Time'], 'Duration', ['Time'], 'Duration', 'EconomyClassic',
               'EconomyFlex', 'BusinessFlex'])
        outbound = flights['outbound']
        for f in outbound.keys():
            print(outbound[f])
    else:
        combination = []
        outbound = flights['outbound']
        returnf = flights['return']
        for o in outbound.keys():
            for r in returnf.keys():
                if outbound[o]['price_business'] == 0 or returnf[r]['price_business'] == 0:
                    combination.append(
                        [outbound[o]['time'], outbound[o]['duration'], returnf[r]['time'], returnf[r]['duration'],
                         outbound[o]['price_economy'] + returnf[r]['price_economy'],
                         outbound[o]['price_economflex'] + returnf[r]['price_economflex'], '-'])
                else:
                    combination.append([outbound[o]['time'], outbound[o]['duration'], returnf[r]['time'],
                                        returnf[r]['duration'],
                                        outbound[o]['price_economy'] + returnf[r]['price_economy'],
                                        outbound[o]['price_economflex'] + returnf[r]['price_economflex'],
                                        outbound[o]['price_business'] + returnf[r]['price_business']])

        def sort_flights(f):
            return f[4]

        combination.sort(key=sort_flights)
        print([['Time'], 'Duration', ['Time'], 'Duration', 'EconomyClassic',
               'EconomyFlex', 'BusinessFlex'])
        for c in range(len(combination)):
            print(combination[c])


def main():
    user_data = enter_data()
    text_json = request(user_data)
    flights = parser(text_json.json(), user_data['oneway'])
    flights_combination(flights, user_data['oneway'])

if __name__ == "__main__":
    main()
