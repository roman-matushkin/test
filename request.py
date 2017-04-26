import requests
import sys

myUrl = 'http://www.flyniki.com/ru/booking/flight/vacancy.php?'
value = {'departure': 'DME', 'destination': 'PAR', 'outboundDate': '2017-06-07', 'returnDate': '2017-06-08',
         'oneway': 0, 'openDateOverview': 0, 'adultCount': 1, 'childCount': 0, 'infantCount': 0}
myHeader = {}
myHeader2 = {}
# myHeader['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
# myHeader['Cookie'] = {'PHPSESSID':'k9t4imacur3avqti6vpm1iqvm5', 'remember':'1%3Bru%3BRU', 'cookieconsent_dismissed':'yes', 'ABSESS':'12lf1tipefm2pi1olkjtcle8q4', '_gat':'1', '_gat_UA-35638432-3':1, 'startConnection':'DME%40PAR%402017-06-07%402017-06-08', '_ga':'GA1.2.1129290809.1492086949', 'lst':'1493032981'}
myHeader['Cookie'] = 'PHPSESSID=k9t4imacur3avqti6vpm1iqvm5; remember=1%3Bru%3BRU; cookieconsent_dismissed=yes;ABSESS=12lf1tipefm2pi1olkjtcle8q4; _gat=1; _gat_UA-35638432-3=1; startConnection=DME%40PAR%402017-06-07%402017-06-08; _ga=GA1.2.1129290809.1492086949; lst=1493032981'
# myHeader['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
myHeader2['Cookie'] = 'PHPSESSID=k9t4imacur3avqti6vpm1iqvm5; remember=1%3Bru%3BRU; cookieconsent_dismissed=yes; ABSESS=12lf1tipefm2pi1olkjtcle8q4; startConnection=DME%40PAR%402017-06-07%402017-06-08; _gat_UA-35638432-3=1; _gat=1; _ga=GA1.2.1129290809.1492086949; lst=1493182123'

# cookie = r'PHPSESSID=k9t4imacur3avqti6vpm1iqvm5; remember=1%3Bru%3BRU; cookieconsent_dismissed=yes; ' \
#          r'ABSESS=12lf1tipefm2pi1olkjtcle8q4; _gat=1; _gat_UA-35638432-3=1; ' \
#          r'startConnection=DME%40PAR%402017-06-07%402017-06-08; _ga=GA1.2.1129290809.1492086949; lst=1493032981 '
params2 = {'_ajax[templates][]':'main',
           '_ajax[templates][]':'priceoverview',
           '_ajax[templates][]':'infos',
           '_ajax[templates][]':'flightinfo',
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
try:
    session = requests.Session()
    r = session.get(myUrl, params=value, headers=myHeader)
    # r = session.get(myUrl, params=value, cookies='PHPSESSID=k9t4imacur3avqti6vpm1iqvm5; remember=1%3Bru%3BRU; cookieconsent_dismissed=yes;ABSESS=12lf1tipefm2pi1olkjtcle8q4; _gat=1; _gat_UA-35638432-3=1; startConnection=DME%40PAR%402017-06-07%402017-06-08; _ga=GA1.2.1129290809.1492086949; lst=1493032981')
    r = session.get('https://www.flyniki.com/site/javascript/ab/airportsuggestion/view.js?_=1493114488816')
    r1 = session.post(r.url, params=params2, headers=myHeader2)
    print (r1.request.headers)
    print (r1.url)
    print (r1.text)

except Exception:
    print('Error web req!')
    print(sys.exc_info()[1])