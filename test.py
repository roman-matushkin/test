"""

This module displays information about flights from the site flyniki.com.
Python 3.6

"""
import requests
import sys
import re
from lxml import html


def enter_data():
    """Display message about entering data from the keyboard and read input data"""
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
    """Convert input data to dictionary"""
    dict_user_data = {keys_for_user_data[i]: data[i] for i in range(len(data))}
    dict_user_data['oneway'] = 0
    # Check oneway ticket
    if len(dict_user_data) == 4:
        dict_user_data['returnDate'] = dict_user_data['outboundDate']
        dict_user_data['oneway'] = 'on'
    return dict_user_data


def request(dict_user_data):
    """
    Send request to the site with input data

    Keyword arguments:
    dict_user_data -- dict containing IATA airport codes, outbound/return dates

    """
    my_url = 'http://www.flyniki.com/ru/booking/flight/vacancy.php'
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
    session = requests.Session()
    try:
        r = session.get(my_url, params=value)
        text_json = session.post(r.url, data=value_ajax)
    except requests.ConnectionError:
        print('Error web req!')
        print(sys.exc_info()[1])
        sys.exit()
    js = text_json.json()
    key_error = js.get('error')
    if key_error is not None:
        print('No flights found. Please check your search and try again.')
        sys.exit()
    return text_json


def parser(text_json, flag_oneway):
    """
    Extraction of information received from the site

    Keyword arguments:
    text_json - received html code
    flag_oneway - flag block return flight

    """
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
    return flights


def table_processing(table):
    """Record information in dictionary"""
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
    """Return price as a floating-point number"""
    # Check availability
    if len(price) > 0:
        p_text = price[0].text
        p_text = p_text.replace('.', '')
        p = p_text.replace(',', '.')
    else:
        p = 0
    return float(p)


def flights_combination(flights, flag_oneway):
    """Combines all flight options and prints considering the price"""
    if flag_oneway == 'on':
        print([['Time'], 'Duration', ['Time'], 'Duration', 'EconomyClassic',
               'EconomyFlex', 'BusinessFlex'])
        outbound = flights['outbound']
        for f in outbound.keys():
            outbound[f]['price_economy'] = str(outbound[f]['price_economy']) + flights['currency']
            outbound[f]['price_economflex'] = str(outbound[f]['price_economflex']) + flights['currency']
            outbound[f]['price_business'] = str(outbound[f]['price_business']) + flights['currency']
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
                         str(outbound[o]['price_economy'] + returnf[r]['price_economy'])+flights['currency'],
                         str(outbound[o]['price_economflex'] + returnf[r]['price_economflex'])+flights['currency'], '-'])
                else:
                    combination.append([outbound[o]['time'], outbound[o]['duration'], returnf[r]['time'],
                                        returnf[r]['duration'],
                                        str(outbound[o]['price_economy'] + returnf[r]['price_economy'])+flights['currency'],
                                        str(outbound[o]['price_economflex'] + returnf[r]['price_economflex'])+flights['currency'],
                                        str(outbound[o]['price_business'] + returnf[r]['price_business'])+flights['currency']])

        def sort_flights(f):
            return f[4]

        combination.sort(key=sort_flights)
        print([['Time'], 'Duration', ['Time'], 'Duration', 'EconomyClassic',
               'EconomyFlex', 'BusinessFlex'])
        for c in range(len(combination)):
            print(combination[c])


def main():
    """Main function"""
    user_data = enter_data()
    text_json = request(user_data)
    flights = parser(text_json.json(), user_data['oneway'])
    flights_combination(flights, user_data['oneway'])

if __name__ == "__main__":
    main()
