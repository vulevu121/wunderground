import csv
import time
import math
from parse_h import conv2utc, getZipcode
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, tzinfo
import os

pitchesfilename = 'WeatherCompTableRev_vu_temp.csv'

files = os.listdir('wunderground')

with open('wunderground_redo.csv', 'w', newline='') as ofile:
    fieldnames = ['file', 'entries']
    writer = csv.DictWriter(ofile, fieldnames=fieldnames)
    writer.writeheader()
    
    for each in files:
        htmlfilename = 'wunderground/' + each
        with open(htmlfilename) as htmlfile:
            soup = BeautifulSoup(htmlfile, "lxml")
            obsTable = soup.find(id='obsTable')
            result = obsTable.find_all("tr", attrs={"class": "no-metars"})

        entries = len(result)
        print('{} {}'.format(each, entries)) 

        if entries < 12:
            row = {'file' : each, 'entries': entries}
            writer.writerow(row)
            


