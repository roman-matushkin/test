import requests
import sys

myUrl = 'http://www.flyniki.com/{0}'
start = 'ru/start.php?'
vacancy = 'ru/booking/flight/vacancy.php?'
modernizr = 'site/javascript/require/vendor/custom.modernizr.js?v2'
loader = 'static/site/loader/nl,jslist:nzf.js'
datepicker = 'site/javascript/jquery/jquery.datepicker.js?v2'
datepicker_ru = 'site/javascript/jquery/ui/i18n/ui.datepicker-ru.js?v2'
cookie1 = 'site/javascript/jquery/jquery.1.2.6.cookie.js?v2'
bookingmask = 'site/javascript/bookingmask-widget.js?20160729&v2'
bookingmask_leg = 'site/javascript/bookingmask-multileg.js?20130913&v2'
vacancy_jquery = 'site/javascript/bookingprocess/vacancy-jquery.js?1424856737&v2'
stageoffer = 'site/css/screen/stageoffer.css?20130903'
vacancy_css = 'site/css/screen/vacancy.css?1424856798'
bookingprocess_css = 'site/css/screen/bookingprocess.css?20130703'
booking_chat = 'site/css/screen/booking-chat.css'
require = 'site/javascript/require/require/require-2.1.10.js'


value = {'departure': 'DME', 'destination': 'PAR', 'outboundDate': '2017-06-07', 'returnDate': '2017-06-08',
         'oneway': 0, 'openDateOverview': 0, 'adultCount': 1, 'childCount': 0, 'infantCount': 0}
param_for_start = {'market':'RU', 'language':'ru', 'bookingmask_widget_id':'bookingmask-widget-stageoffer',
                   'bookingmask_widget_dateformat':'dd.mm.yy', 'departure':'DME', 'destination':'PAR',
                   'outboundDate':'07.06.2017', 'returnDate':'08.06.2017', 'adultCount':1,'childCount':0, 'infantCount':0,
                   'submitSearch':''}
myHeader = {}
myHeader['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'

try:
    session = requests.Session()
    r = session.post(myUrl.format(start), params=param_for_start, headers=myHeader)
    print (r.url)
    myUrl1 = myUrl.format(vacancy)
    r = session.get(myUrl1, params=value)
    print(r.url)
    r = session.get(r.url)
    print(r.url)
    # r = session.get(myUrl.format(modernizr))
    # print(r.url)
    # r = session.get(myUrl.format(loader))
    # print(r.url)
    # r = session.get('https://www.google.com/recaptcha/api.js?onload=onloadRecaptchaCallback&render=explicit&hl=ru')
    # r = session.get(myUrl.format(datepicker))
    # r = session.get(myUrl.format(datepicker_ru))
    # r = session.get(myUrl.format((cookie1)))
    # r = session.get(myUrl.format((bookingmask)))
    # r = session.get(myUrl.format((bookingmask_leg)))
    # r = session.get(myUrl.format((vacancy_jquery)))
    # r = session.get(myUrl.format((stageoffer)))
    # r = session.get(myUrl.format((vacancy_css)))
    # r = session.get(myUrl.format((bookingprocess_css)))
    # r = session.get(myUrl.format((booking_chat)))
    # r = session.get(myUrl.format((require)))
    print (r.text)

except Exception:
    print('Error web req!')
    print(sys.exc_info()[1])
