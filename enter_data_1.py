import requests
import sys

myUrl = 'http://www.flyniki.com/ru/booking/flight/vacancy.php?'
value = {'departure': 'DME', 'destination': 'PAR', 'outboundDate': '2017-06-07', 'returnDate': '2017-06-08',
         'oneway': 0, 'openDateOverview': 0, 'adultCount': 1, 'childCount': 0, 'infantCount': 0}
myHeader = {}
# myHeader['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
# myHeader['Cookie'] = {'PHPSESSID':'k9t4imacur3avqti6vpm1iqvm5', 'remember':'1%3Bru%3BRU', 'cookieconsent_dismissed':'yes', 'ABSESS':'12lf1tipefm2pi1olkjtcle8q4', '_gat':'1', '_gat_UA-35638432-3':1, 'startConnection':'DME%40PAR%402017-06-07%402017-06-08', '_ga':'GA1.2.1129290809.1492086949', 'lst':'1493032981'}
myHeader['Cookie'] = 'PHPSESSID=k9t4imacur3avqti6vpm1iqvm5; remember=1%3Bru%3BRU; cookieconsent_dismissed=yes;ABSESS=12lf1tipefm2pi1olkjtcle8q4; _gat=1; _gat_UA-35638432-3=1; startConnection=DME%40PAR%402017-06-07%402017-06-08; _ga=GA1.2.1129290809.1492086949; lst=1493032981'
# myHeader['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'

# cookie = r'PHPSESSID=k9t4imacur3avqti6vpm1iqvm5; remember=1%3Bru%3BRU; cookieconsent_dismissed=yes; ' \
#          r'ABSESS=12lf1tipefm2pi1olkjtcle8q4; _gat=1; _gat_UA-35638432-3=1; ' \
#          r'startConnection=DME%40PAR%402017-06-07%402017-06-08; _ga=GA1.2.1129290809.1492086949; lst=1493032981 '
try:
    session = requests.Session()
    r = session.get(myUrl, params=value, headers=myHeader)
    # r = session.get(myUrl, params=value, cookies=myHeader)
    print (r.request.headers)
    print (r.url)
    print (r.text)

except Exception:
    print('Error web req!')
    print(sys.exc_info()[1])