import requests

URL = 'https://www.wunderground.com/cgi-bin/findweather/getForecast'
CODE = '90012'
MONTH = 11
DAY = 1
YEAR = 2017

params = {
    'airportorwmo': 'query',
    'historytype':  'DailyHistory',
    'backurl':      '/history/index.html',
    'code':         CODE,
    'day':          DAY,
    'month':        MONTH,
    'year':         YEAR,
    }

r = requests.get(URL, params=params)

with open('index.html', 'w') as f:
    f.write(r.text)
