import csv
import time
import math
from parse_h import conv2utc, getZipcode
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, tzinfo



pitchesfilename = 'WeatherCompTableRev_vu_svid_after.csv'

start = time.time()

print('Parsing file...')
with open(pitchesfilename, 'r', newline='') as ifile:
    reader = csv.DictReader(ifile)
    fieldnames = reader.fieldnames
    with open(pitchesfilename.rstrip('.csv') + '_vu.csv', 'w', newline='') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)
        writer.writeheader()
    
        lastCODE = 'none'
        lastgameName = 'none'
        CODE = ''
        gameName = ''

        cur_row = 1
        percent = 1
        row_count = 704367
        row_mod = round(row_count / 100, 0)
        
        buckets = 400
        min_bucket = [0]*buckets
        
        for row in reader:
            if cur_row % row_mod == 0:
                print('Progress: {}%'.format(percent))
                percent += 1

            gameName = row['gameName']
            sv_id = row['sv_id']
            
            forecast = row['forecast']
            starttime = row['Time']
            time_zone = row['time_zone']
            gameLength = row['gameLength']
            ampm = row['ampm']

            if sv_id[-2:] == '60':
                sv_id = sv_id[0:-2] + '59'
            dtsv_id = datetime.strptime(sv_id + ' UTC+0000', '%y%m%d_%H%M%S %Z%z')

            gameNameSplit = gameName.split(sep='_')
            gameLengthSplit = gameLength.split(sep=':')

            YEAR = gameNameSplit[1]
            MONTH = gameNameSplit[2]
            DAY = gameNameSplit[3]

            dtGameLength = timedelta(hours=int(gameLengthSplit[0]),
                                     minutes=int(gameLengthSplit[1]))
            dtStartTime = datetime.strptime(YEAR + MONTH + DAY + starttime + ampm + 'UTC-0400', '%Y%m%d%I:%M:%S%p%Z%z')
            dtEndTime = dtStartTime + dtGameLength

##            if (dtsv_id > dtEndTime):
##                writer.writerow(row)

##            if (dtsv_id > dtEndTime):
##                for i in range(0,buckets):
##                    if (dtsv_id - dtEndTime) > timedelta(minutes=i) and (dtsv_id - dtEndTime) < timedelta(minutes=i+1):
##                        min_bucket[i] += 1
            

##            if (dtsv_id < dtStartTime):
##                writer.writerow(row)
##                
##            if (dtsv_id < dtStartTime):
##                for i in range(0,buckets):
##                    if (dtStartTime - dtsv_id) > timedelta(minutes=i) and (dtStartTime - dtsv_id) < timedelta(minutes=i+1):
##                        min_bucket[i] += 1
            if (dtsv_id > dtEndTime):
                if (dtsv_id - dtEndTime) > timedelta(minutes=365):
                    writer.writerow(row)



            cur_row += 1
            


for i in range(0, buckets):
    print('{} min, {}'.format(i+1,min_bucket[i]))

print('Progres: 100%...DONE')
elapsed = time.time() - start
print(elapsed)
