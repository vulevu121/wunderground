import requests
import csv
import time
import json
from parse_h import getZipcode

pitches_csv = 'WeatherCompTableRev.csv'

bpjson = 'ballparks.json'

with open(bpjson, 'r') as f:
    bpdata = json.load(f)
    
print('Loading CSV file...')
with open(pitches_csv, newline='') as f1:
    print('Grabbing HTML files...')
    lastCODE = 'none'
    lastgameName = 'none'
    CODE = ''
    gameName = ''

    cur_row = 1
    percent = 0
    row_count = 704367
    row_mod = round(row_count / 20,0)
    num_requests = 0

    startRow = 0
    
    reader = csv.DictReader(f1)
    
    for row in reader:
        if cur_row % row_mod == 0:
            print('Progress: {}%'.format(percent))
            percent = percent + 5
            
        if cur_row > startRow:
            gameName = row['gameName']
            sv_id = row['sv_id']
            venue = row['venue']
            
            gameNameSplit = gameName.split(sep='_')

            CODE = getZipcode(venue)
            YEAR = gameNameSplit[1]
            MONTH = gameNameSplit[2]
            DAY = gameNameSplit[3]
            URL = 'https://www.wunderground.com/cgi-bin/findweather/getForecast'

            if CODE != lastCODE and gameName != lastgameName:
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

                htmlfile = 'wunderground/{0}_{1}_{2}_{3}.html'.format(YEAR, MONTH, DAY, CODE)

                with open(htmlfile, 'w') as f:
                    f.write(r.text)

                lastCODE = CODE
                lastgameName = gameName
                num_requests += 1

                if num_requests > 500:
                    print('Exceeded maximum number of requests, pausing for 10 mins...')
                    time.sleep(600)
                    num_requests = 0
              
        cur_row += 1

print('Progress: 100%...DONE')
