"""

This module displays information about flights from the site flyniki.com.
Python 3.6

"""
import requests
import sys
import re
from lxml import html
import datetime
import random


def enter_data():
    """Display message about entering data from the keyboard and read input data"""
    keys_for_user_data = ['departure', 'destination', 'outboundDate', 'returnDate']
    print('Hello! Please enter parameters of the desired flight separated by a comma')
    print('Departure(IATA airport code), destination(IATA airport code),'
          ' outbound date(yyyy-mm-dd), returnDate(optional)')
    data = input().replace(' ', '').split(',')
    if len(data) < 3:
        print('How is it possible to forget enter date? Try again ;)')
        print('Departure(IATA airport code), destination(IATA airport code),'
              'outbound date(yyyy-mm-dd), returnDate(optional)')
        data = input().split(',')
    # Check date format
    match_outbound = re.search(r'\d\d\d\d-\d\d-\d\d\b', data[2])
    if match_outbound:
        dict_user_data = gen_dict_from_enter_data(keys_for_user_data, data)
    else:
        print('Sorry, date entered incorrectly. Please try again')
        print('Departure(IATA airport code), destination(IATA airport code),'
              ' outbound date(yyyy-mm-dd), returnDate(optional)')
        data = input().split(',')
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
        error_processing(js.get('errorRAW'), value)
        sys.exit()
    return text_json


def error_processing(errorraw, value):
    """Handle the error response"""
    error = errorraw[0]['code']
    if error == 'departure' or error == 'destination':
        error_iata_code(value, error)
    else:
        error_date(value)
    return


def error_iata_code(value, error):
    """Handles error response when invalid IATA code input"""
    if error == 'departure':
        print('The choice of the departure airport is not valid. Correct the entered data, please.'
              'You entered a non-existent IATA airport code. '
              'Maybe you mean:')
        find_iata_code(value['departure'][0])
    elif error == 'destination':
        print('The choice of the destination airport is not valid. Correct the entered data, please.'
              'You entered a non-existent IATA airport code. '
              'Maybe you mean:')
        find_iata_code(value['destination'][0])
    else:
        print('The choice of the airport is not valid. Correct, please, the entered data.'
              '(IATA airport code  is a THREE(!!!)-letter code)')
    return


def find_iata_code(first_symb):
    """Select the existing IATA code considering first entered letter entered in request"""
    url_iata_code = r'https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_{}'
    session = requests.Session()
    r = session.get(url_iata_code.format(first_symb.upper()))
    html_text = html.fromstring(r.text)
    three_rand_num_tr = [random.randint(2, 20) for i in range(3)]
    rand_iata_code = []
    for n in three_rand_num_tr:
        a = html_text.xpath('/html/body/div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"]'
                            '/table/tr[{}]/td[1]'.format(n))
        rand_iata_code.append(a[0].text)
    print(rand_iata_code)
    return


def error_date(value):
    """Handles error response when invalid date input"""
    flag_oneway = value['oneway']
    enter_year_outbound = int(value['outboundDate'][0:4])
    enter_month_outbound = int(value['outboundDate'][5:7])
    enter_day_outbound = int(value['outboundDate'][8:10])
    current_date = datetime.datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    current_day = current_date.day
    too_far_future_outbound = (enter_year_outbound > current_year and enter_month_outbound > current_month and
                               enter_day_outbound > current_day)
    past_date_outbound = ((enter_year_outbound < current_year or enter_month_outbound <= current_month) or
                          (enter_year_outbound == current_year and enter_month_outbound == current_month and
                          enter_day_outbound < current_day))
    check_date_format(enter_year_outbound, enter_month_outbound, enter_day_outbound, 'outbound')
    if too_far_future_outbound:
        print("Don't think so far. There are no available tickets for the dates you have selected (outbound).")
    elif past_date_outbound:
        print("Sorry, you're late. This day has already passed (outbound).")

    if flag_oneway == 0:
        enter_year_return = int(value['returnDate'][0:4])
        enter_month_return = int(value['returnDate'][5:7])
        enter_day_return = int(value['returnDate'][8:10])
        too_far_future_return = (enter_year_return > current_year and enter_month_return > current_month and
                                 enter_day_return > current_day)
        past_date_return = ((enter_year_return < current_year or enter_month_return <= current_month) or
                            (enter_year_return == current_year and enter_month_return == current_month and
                             enter_day_return < current_day))
        check_date_format(enter_year_return, enter_month_return, enter_day_return, 'return')
        if too_far_future_return:
            print("Don't think so far. There are no available tickets for the dates you have selected (return).")
        elif past_date_return:
            print("Sorry, you're late. This day has already passed (return).")
        elif (enter_year_outbound > enter_year_return or enter_month_outbound > enter_month_return) or \
             (enter_year_outbound == enter_year_return and enter_month_outbound == enter_month_return
              and enter_day_outbound > enter_day_return):
            print("You can't fly back without flying. In entered information the departure date after the return date")
    return


def check_date_format(enter_year, enter_month, enter_day, type_way):
    """Search error in the entered date"""
    current_date = datetime.datetime.now()
    current_year = current_date.year
    current_month = current_date.month
    # Leap year
    leap_year = ((enter_year % 4) == 0 and (enter_year % 100) != 0) or (enter_year % 400) == 0
    # If entered date is too far in the future
    if enter_year > current_year and enter_month > current_month:
        print("Don't think so far. There are no available tickets for the dates"
              " you have selected. ({})".format(type_way))
    # If entered date has already passed
    elif enter_year < current_year and enter_month < current_month:
        print("Sorry, you're late. This day has already passed ({})".format(type_way))
    # Invalid month entered
    elif enter_month > 12 or enter_month < 0:
        print('You have chosen a non-existent month.'
              ' This year there are only such options ({}):'.format(type_way) + '\n' +
              '01 - January, 02 - February, 03 - March, 04 - April, 05 - May, 06 - June,' + '\n' +
              '07 - July, 08 - August, 09 - September, 10 - October, 11 - November, 12 - December')
    # Invalid day entered
    elif enter_day > 31 or enter_day < 1 and enter_month == any([1, 3, 5, 7, 8, 10, 12]):
        print('There are not so many numbers in a month ({}).'.format(type_way))
    elif enter_day > 30 or enter_day < 1 and enter_month == any([4, 6, 9, 11]):
        print('There are not so many numbers in a month ({}).'.format(type_way))
    # Invalid day entered in February
    elif enter_day > 29 or enter_day < 1 and enter_month == 2 and leap_year:
        print('There are not so many numbers in a month ({}).'.format(type_way))
    elif enter_day > 28 or enter_day < 1 and enter_month == 2 and not leap_year:
        print('There are not so many numbers in a month ({}).'.format(type_way))
    return


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
                         str(outbound[o]['price_economflex'] + returnf[r]['price_economflex']) +
                         flights['currency'], '-'])
                else:
                    combination.append([outbound[o]['time'], outbound[o]['duration'], returnf[r]['time'],
                                        returnf[r]['duration'],
                                        str(outbound[o]['price_economy'] + returnf[r]['price_economy']) +
                                        flights['currency'],
                                        str(outbound[o]['price_economflex'] + returnf[r]['price_economflex']) +
                                        flights['currency'],
                                        str(outbound[o]['price_business'] + returnf[r]['price_business']) +
                                        flights['currency']])

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
