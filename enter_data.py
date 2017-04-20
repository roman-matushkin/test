import requests
import sys

myUrl = 'http://www.flyniki.com/ru/booking/flight/vacancy.php?'
value = {'departure': 'DME', 'destination': 'PAR', 'outboundDate': '2017-04-24', 'returnDate': '2017-04-25',
         'oneway': 0, 'openDateOverview': 0, 'adultCount': 1, 'childCount': 0, 'infantCount': 0}

try:
    session = requests.Session()
    r = session.post(myUrl, params=value)
    print (r.url)
    print (r.text)

except Exception:
    print('Error web req!')
    print(sys.exc_info()[1])
