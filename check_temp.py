import csv
import time
import math
from parse_h import conv2utc, getZipcode
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, tzinfo

pitchesfilename = 'WeatherCompTableRev_vu.csv'

start = time.time()

print('Parsing file...')
with open(pitchesfilename, 'r', newline='') as ifile:
    reader = csv.DictReader(ifile)
    fieldnames = reader.fieldnames
    fieldnames.append('zip')
    fieldnames.append('start_temp')
    fieldnames.append('temp_diff')

    with open(pitchesfilename[0:-4] + '_temp.csv', 'w', newline='') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)
        writer.writeheader()

        
        lastCODE = 'none'
        lastgameName = 'none'
        laststarttime = 'none'
        CODE = ''
        gameName = ''
        starttime = ''

        percent = 1
        row_count = 704367
        row_mod = round(row_count / 100,0)
        
        
        for row in reader:
            if reader.line_num % row_mod == 0:
                print('Progress: {}%'.format(percent))
                percent += 1

            gameName = row['gameName']


            sv_id = row['sv_id']
            venue = row['venue']
            forecast = row['forecast']
            starttime = row['Time']
            time_zone = row['time_zone']
            gameLength = row['gameLength']
            ampm = row['ampm']
            temperature = float(row['temperature'])



            if sv_id[-2:] == '60':
                sv_id = sv_id[0:-2] + '59'

            gameNameSplit = gameName.split(sep='_')
            gameLengthSplit = gameLength.split(sep=':')

            venueZip = getZipcode(venue)

            CODE = venueZip
            YEAR = gameNameSplit[1]
            MONTH = gameNameSplit[2]
            DAY = gameNameSplit[3]


            dtStartTime = datetime.strptime(YEAR + MONTH + DAY + starttime + ampm + 'UTC-0400', '%Y%m%d%I:%M:%S%p%Z%z')

            if gameName != lastgameName:
                htmlfilename = 'wunderground/{0}_{1}_{2}_{3}.html'.format(YEAR, MONTH, DAY, CODE)


                with open(htmlfilename) as htmlfile:
                    soup = BeautifulSoup(htmlfile, "lxml")
                    obsTable = soup.find(id='obsTable')
                    result = obsTable.find_all("tr", attrs={"class": "no-metars"})
                    headings = obsTable.thead.find_all('th')
                    localTimezone = obsTable.thead.tr.th.span.next_element.strip('()')

                    for i in range(0, len(headings)-1):
                        if 'Temp' in headings[i].text:
                            temp_idx = i
                        if 'Humidity' in headings[i].text:
                            humid_idx = i
                        if 'Pressure' in headings[i].text:
                            pressure_idx = i

                lastCODE = CODE
                lastgameName = gameName

                minTimeDifference = timedelta(hours=6)
                minTemp = 0.0


                for eachResult in result:
                    resultTime = eachResult.td.next_element
                    resultDateTimeStr = '{0} {1} {2} {3} {4}'.format(YEAR, MONTH, DAY, resultTime, conv2utc(localTimezone))
                    
                    resultDateTime = datetime.strptime(resultDateTimeStr, '%Y %m %d %I:%M %p %Z%z')
                  
                    tdResult = eachResult.find_all('td')

                    try:
                        temp = tdResult[temp_idx].span.span.next_element
                    except:
                        temp = '-'

                    if temp == '-':
                        continue

                    difference = resultDateTime - dtStartTime

                    if abs(difference) < minTimeDifference:
                        minTimeDifference = abs(difference)
                        minTemp = float(temp)

            temp_diff = round(minTemp - float(temperature),2)
            if forecast != 'dome' and forecast != 'roof closed':
                row['start_temp'] = minTemp
                row['temp_diff'] = temp_diff
            row['zip'] = venueZip    
            writer.writerow(row)
             
print('Progres: 100%...DONE')
elapsed = time.time() - start
print(elapsed)
