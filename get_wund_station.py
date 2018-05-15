import csv
import requests
import math
from bs4 import BeautifulSoup

file = 'ballparks_closest_airports_vu_new.csv'

with open(file, 'r', newline='', encoding='utf-8') as ifile:
    reader = csv.DictReader(ifile)
    fieldnames = reader.fieldnames

    with open(file[0:-4] + '_new.csv', 'w', newline='', encoding='utf-8') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)
        
        for row in reader:
            lat = row['lat']
            long = row['long']
            
            CODE = '{},{}'.format(lat,long)
            
            YEAR = '2017'
            MONTH = '05'
            DAY = '09'

            
            URL = 'https://www.wunderground.com/cgi-bin/findweather/getForecast'

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

            soup = BeautifulSoup(r.text, "lxml")
            
            result = soup.find('div', attrs={'class': 'icao-input-field'})
            station = result.input['value']
            
            row['wund_station_code2'] = station

            writer.writerow(row)
            

            
