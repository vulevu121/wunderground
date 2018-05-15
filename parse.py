import csv
import time
import math
import json
from parse_h import conv2utc, getZipcode, getAirDensity
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, tzinfo

start = time.time()
bpjson = 'ballparks.json'

pitchesfilename = 'WeatherCompTableRev_vu.csv'

with open(bpjson, 'r') as f:
    bpdata = json.load(f)

print('Parsing file...')
with open(pitchesfilename, 'r', newline='') as ifile:
    reader = csv.DictReader(ifile)
    fieldnames = reader.fieldnames
    #fieldnames.append('zip')
    fieldnames.append('temp')
    fieldnames.append('rel_hum')
    fieldnames.append('pressure')
    fieldnames.append('air_density')
    fieldnames.append('wund_abs_time_diff')
    fieldnames.append('sv_id_outside')

    startRow = 0

    if startRow > 0:
        permission = 'a'
    else:
        permission = 'w'
    
    with open(pitchesfilename[0:-4] + '_parsed.csv', permission, newline='') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)
        if startRow == 0:
            writer.writeheader()

        
        lastCODE = 'none'
        lastgameName = 'none'
        CODE = ''
        gameName = ''

        cur_row = 0
        percent = 5

        row_count = 704367
        row_mod = round(row_count / 100, 0)

        startRow = 0
        
        for row in reader:
            if reader.line_num % row_mod == 0:
                print('Progress: {} % / Line: {} / Time: {}'.format(percent, reader.line_num, (time.time() - start)))
                percent += 1
 
            if reader.line_num >= startRow:
                gameName = row['gameName']
                sv_id = row['sv_id']
                venue = row['venue']
                forecast = row['forecast']
                temperature = float(row['temperature'])
                starttime = row['Time']
                time_zone = row['time_zone']
                altitude = float(row['Altitude'])
                gameLength = row['gameLength']
                ampm = row['ampm']
                
                gameNameSplit = gameName.split(sep='_')
                gameLengthSplit = gameLength.split(sep=':')

                venueZip = getZipcode(venue)

                
                YEAR = gameNameSplit[1]
                MONTH = gameNameSplit[2]
                DAY = gameNameSplit[3]

                if sv_id[-2:] == '60':
                    sv_id = sv_id[0:-2] + '59'
                
                dtsv_id = datetime.strptime(sv_id + ' UTC+0000', '%y%m%d_%H%M%S %Z%z')
                dtGameLength = timedelta(hours=int(gameLengthSplit[0]),
                                     minutes=int(gameLengthSplit[1]))
                
                dtStartTime = datetime.strptime(YEAR + MONTH + DAY + starttime + ampm + 'UTC-0400', '%Y%m%d%I:%M:%S%p%Z%z')
                dtGameRange = dtStartTime + dtGameLength

                if (dtsv_id > dtGameRange):
                    row['sv_id_outside'] = abs(dtsv_id - dtGameRange)
                    
                    
                if (dtsv_id < dtStartTime):
                    row['sv_id_outside'] = '-{}'.format(abs(dtStartTime - dtsv_id))
                    
                
                if gameName != lastgameName:
                    try:
                        CODE = bpdata[venue]['wund_station_code']
                        htmlfilename = 'wunderground3/{0}_{1}_{2}_{3}.html'.format(YEAR, MONTH, DAY, CODE)
                        htmlfile = open(htmlfilename)
                    except:
                        try:
                            CODE = bpdata[venue]['closest_ap1_code']
                            htmlfilename = 'wunderground/{0}_{1}_{2}_{3}.html'.format(YEAR, MONTH, DAY, CODE)
                            htmlfile = open(htmlfilename)
                        except:
                            try:
                                CODE = bpdata[venue]['closest_ap2_code']
                                htmlfilename = 'wunderground/{0}_{1}_{2}_{3}.html'.format(YEAR, MONTH, DAY, CODE)
                                htmlfile = open(htmlfilename)
                            except:
                                try:
                                    CODE = bpdata[venue]['closest_ap3_code']
                                    htmlfilename = 'wunderground/{0}_{1}_{2}_{3}.html'.format(YEAR, MONTH, DAY, CODE)
                                    htmlfile = open(htmlfilename)
                                except:
                                    print(htmlfilename)
                                    print('no more html files to load')


                    soup = BeautifulSoup(htmlfile, "lxml")
                    obsTable = soup.find(id='obsTable')
                    result = obsTable.find_all("tr", attrs={"class": "no-metars"})
                    headings = obsTable.thead.find_all('th')
                    localTimezone = obsTable.thead.tr.th.span.next_element.strip('()')

                    htmlfile.close()


                    for i in range(0, len(headings)-1):
                        if 'Temp' in headings[i].text:
                            temp_idx = i
                        if 'Humidity' in headings[i].text:
                            humid_idx = i
                        if 'Pressure' in headings[i].text:
                            pressure_idx = i

                    lastCODE = CODE
                    lastgameName = gameName

                ## desired zulu time from sv_id


                desiredDateTime = datetime.strptime(sv_id + ' UTC+0000', '%y%m%d_%H%M%S %Z%z')

                minTimeDifference = timedelta(hours=6)

                minHumidity = 0.0
                minTemp = 0.0
                minPressure = 0.0

                ## compares with desired date/time and extract weather data
                
                for eachResult in result:
                    resultTime = eachResult.td.next_element
                    resultDateTimeStr = '{0} {1} {2} {3} {4}'.format(YEAR, MONTH, DAY, resultTime, conv2utc(localTimezone))
                    
                    resultDateTime = datetime.strptime(resultDateTimeStr, '%Y %m %d %I:%M %p %Z%z')
                  
                    tdResult = eachResult.find_all('td')

                    try:
                        temp = tdResult[temp_idx].span.span.next_element
                    except:
                        temp = '-'

                    try:
                        humidity = tdResult[humid_idx].next_element
                    except:
                        humidity = '-'

                    try:
                        pressure = tdResult[pressure_idx].span.span.next_element
                    except:
                        pressure = '-'

                    
                    if temp == '-' or humidity == 'N/A%' or pressure == '-':
                        continue

                    if not isinstance(temp, str) or not isinstance(humidity, str) or not isinstance(pressure, str):
                        continue

                    # choose closest time match
                    difference = resultDateTime - desiredDateTime

                    if abs(difference) < minTimeDifference:
                        minTimeDifference = abs(difference)
                        minHumidity = float(humidity.rstrip('%'))
                        minTemp = float(temp)
                        minPressure = float(pressure)
                #temp_diff = round(minTemp - float(temperature),2)
                #row['temp_diff'] = temp_diff
                #row['zip'] = venueZip
                row['pressure'] = minPressure
                row['sv_id'] = sv_id
                row['wund_abs_time_diff'] = minTimeDifference

                if forecast == 'dome' or forecast == 'roof closed':
                    row['temp'] = temperature
                    row['rel_hum'] = '50.0'
                    row['air_density'] = getAirDensity(temperature, 50.0, minPressure, altitude)
                else:
                    row['temp'] = minTemp
                    row['rel_hum'] = minHumidity
                    row['air_density'] = getAirDensity(minTemp, minHumidity, minPressure, altitude)

                writer.writerow(row)
            cur_row += 1

print('Progres: DONE...')
elapsed = time.time() - start
print(elapsed)
