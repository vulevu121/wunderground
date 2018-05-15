import csv
import time
import math
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, tzinfo
from parse_h import conv2utc, getZipcode



pitchesfilename = 'WeatherCompTableRev_vu_temp.csv'

start = time.time()

print('Parsing file...')
with open(pitchesfilename, 'r', newline='') as ifile:
    reader = csv.DictReader(ifile)

    fieldnames = ['Stadium','Count']

    with open(pitchesfilename[0:-4] + '_count_per_venue.csv', 'w', newline='') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)

        
        writer.writeheader()

        
        lastCODE = 'none'
        lastgameName = 'none'
        laststarttime = 'none'
        CODE = ''
        gameName = ''
        starttime = ''

        percent = 1
        row_count = 100
        row_mod = round(row_count / 100,0)

        buckets = 41

        temp_bucket = [0]*buckets

        
        duplist = {'Citi Field': 0, 'Coors Field': 0, 'Nationals Park': 0, 'Wrigley Field': 0, 'Yankee Stadium': 0, 'Progressive Field': 0, 'Busch Stadium': 0, 'Miller Park': 0, 'Angel Stadium of Anaheim': 0, 'AT&T Park': 0, 'Kauffman Stadium': 0, 'Fenway Park': 0, 'SunTrust Park': 0, 'Guaranteed Rate Field': 0, 'Rogers Centre': 0, 'PNC Park': 0, 'Great American Ball Park': 0, 'Dodger Stadium': 0, 'Oakland Coliseum': 0, 'Oriole Park at Camden Yards': 0, 'Safeco Field': 0, 'Globe Life Park in Arlington': 0, 'Comerica Park': 0, 'Citizens Bank Park': 0}
        
        for row in reader:
            venue = row['venue']
            duplist[venue] += 1

        
        
        for stadium, count in zip(duplist.keys(), duplist.values()):
            writer.writerow({'Stadium': stadium, 'Count': count})
           
        
##        for row in reader:
##            temp_diff = float(row['temp_diff'])
##
##            for i in range(-20, 20):
##                if (temp_diff > i) and (temp_diff <= i+1):
##                    temp_bucket[i+20] += 1
##                                            
##
##        for i in range(0, buckets):
##            writer.writerow({'Bucket':'{} degF'.format(i-20), 'Count': temp_bucket[i] })

##print('Progres: 100%...DONE')
elapsed = time.time() - start
print(elapsed)
