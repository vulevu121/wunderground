import requests
import csv
import time
import json
from parse_h import getZipcode

start = time.time()

pitches_csv = 'WeatherCompTableRev_vu.csv'

bpjson = 'ballparks.json'

with open(bpjson, 'r') as f:
    bpdata = json.load(f)

print('Loading CSV file...')
with open(pitches_csv, newline='') as f1:
    reader = csv.DictReader(f1)
    print('Grabbing HTML files...')

    lastgameName = 'none'
    gameName = ''

    cur_row = 1
    percent = 5
    row_count = 704367
    row_mod = round(row_count / 20,0)
    #num_requests = 0

    startRow = 0
    
    for row in reader:

        if reader.line_num % row_mod == 0:
            print('Progress: {} % / Line: {}'.format(percent, reader.line_num))
            percent = percent + 5

        if reader.line_num >= startRow:
            gameName = row['gameName']
            sv_id = row['sv_id']
            venue = row['venue']
            lat = bpdata[venue]['lat']
            long = bpdata[venue]['long']

            closest_ap2_code = bpdata[venue]['closest_ap2_code']
            closest_ap3_code = bpdata[venue]['closest_ap3_code']

            gameNameSplit = gameName.split(sep='_')
            
            YEAR = gameNameSplit[1]
            MONTH = gameNameSplit[2]
            DAY = gameNameSplit[3]
            URL = 'https://www.wunderground.com/cgi-bin/findweather/getForecast'

            if gameName != lastgameName:
                params = {
                        'airportorwmo': 'query',
                        'historytype':  'DailyHistory',
                        'backurl':      '/history/index.html',
                        'code':         closest_ap2_code,
                        'day':          DAY,
                        'month':        MONTH,
                        'year':         YEAR,
                        }

                r = requests.get(URL, params=params)

                params['code'] = closest_ap3_code
                r2 = requests.get(URL, params=params)

                htmlfile = 'wunderground/{}_{}_{}_{}.html'.format(YEAR, MONTH, DAY, closest_ap2_code)
                htmlfile2 = 'wunderground/{}_{}_{}_{}.html'.format(YEAR, MONTH, DAY, closest_ap3_code)
                

                with open(htmlfile, 'w') as f:
                    f.write(r.text)

                with open(htmlfile2, 'w') as f2:
                    f2.write(r2.text)

                lastgameName = gameName
                #num_requests += 1

                time.sleep(1)

##                if num_requests > 500:
##                    print(cur_row)
##                    print('Pausing for 5 mins...')
##                    time.sleep(300)
##                    num_requests = 0
        cur_row += 1
print('Progress: DONE...')
elapsed = time.time() - start
print(elapsed)
