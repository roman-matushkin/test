import requests
import sys

myUrl = 'http://www.flyniki.com/ru/booking/flight/vacancy.php?'
value = {'departure': 'DME', 'destination': 'PAR', 'outboundDate': '2017-06-07', 'returnDate': '2017-06-08',
         'oneway': 0, 'openDateOverview': 0, 'adultCount': 1, 'childCount': 0, 'infantCount': 0}

value_ajax = {'_ajax[templates][]':'main',
           '_ajax[requestParams][departure]':'Москва - Домодедово',
           '_ajax[requestParams][destination]':'Париж',
           '_ajax[requestParams][returnDeparture]':'',
           '_ajax[requestParams][returnDestination]':'',
           '_ajax[requestParams][outboundDate]':'2017-06-07',
           '_ajax[requestParams][returnDate]':'2017-06-08',
           '_ajax[requestParams][adultCount]':'1',
           '_ajax[requestParams][childCount]':'0',
           '_ajax[requestParams][infantCount]':'0',
           '_ajax[requestParams][openDateOverview]':'',
           '_ajax[requestParams][oneway]':''}

myHeader = {}
myHeader['Cookie'] = 'PHPSESSID=k9t4imacur3avqti6vpm1iqvm5; remember=1%3Bru%3BRU; cookieconsent_dismissed=yes;ABSESS=12lf1tipefm2pi1olkjtcle8q4; _gat=1; _gat_UA-35638432-3=1; startConnection=DME%40PAR%402017-06-07%402017-06-08; _ga=GA1.2.1129290809.1492086949; lst=1493032981'

try:
    session = requests.Session()
    r = session.get(myUrl, params=value, headers=myHeader)
    r1 = session.post(r.url,  data=value_ajax)
    print(r1.json())

except Exception:
    print('Error web req!')
    print(sys.exc_info()[1])
