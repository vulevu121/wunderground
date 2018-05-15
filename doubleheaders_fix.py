import csv
import time
import math
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, tzinfo

def game2fix(x):
    return {
        'gid_2017_05_14_houmlb_nyamlb_2':'07:39:00', #7:39pm Yankee Stadium EDT
        'gid_2017_05_21_kcamlb_minmlb_2':'06:07:00', #5:07pm Target Field CDT
        'gid_2017_05_27_detmlb_chamlb_2':'05:49:00', #4:49pm Guaranteed Rate Field CDT
        'gid_2017_06_10_oakmlb_tbamlb_2':'06:54:00', #6:54pm Tropicana Field EDT
        'gid_2017_08_06_seamlb_kcamlb_2':'05:54:00', #4:54pm Kauffman Stadium CDT
        'gid_2017_08_21_minmlb_chamlb_2':'09:22:00', #8:22pm Guaranteed Rate Field CDT
        'gid_2017_08_22_miamlb_phimlb_2':'07:53:00', #7:53pm Citizens Bank Park EDT
        'gid_2017_08_30_atlmlb_phimlb_2':'03:35:00', #3:35pm Citizens Bank Park EDT
        'gid_2017_08_30_clemlb_nyamlb_2':'05:01:00', #5:01pm Yankee Stadium EDT
        'gid_2017_09_09_houmlb_oakmlb_2':'08:27:00', #5:27pm Oakland-Alameda County Coliseum PDT
        'gid_2017_09_25_atlmlb_nynmlb_2':'07:46:00', #7:46pm Citi Field EDT
    }[x]

def conv2utc(x):
    return {
        'PDT': 'UTC-0700',
        'MDT': 'UTC-0600',
        'CDT': 'UTC-0500',
        'EDT': 'UTC-0400',
        'PST': 'UTC-0800',
        'MST': 'UTC-0700',
        'CST': 'UTC-0600',
        'EST': 'UTC-0500',
    }[x]

def getZipcode(stadium_name):
    return {
        'Angel Stadium':'92806',
        'Angel Stadium of Anaheim':'92806', #alias
        'AT&T Park':'94107',
        'Busch Stadium':'63102',
        'Chase Field':'85004',
        'Citi Field':'11368',
        'Citizens Bank Park':'19148',
        'Comerica Park':'48201',
        'Coors Field':'80205',
        'Dodger Stadium':'90012',
        'Fenway Park':'02215',
        'Globe Life Park in Arlington':'76011',
        'Great American Ball Park':'45202',
        'Guaranteed Rate Field':'60616',
        'Kauffman Stadium':'64129',
        'Marlins Park':'33125',
        'Miller Park':'53214',
        'Minute Maid Park':'77002',
        'Nationals Park':'20003',
        'Oakland-Alameda County Coliseum':'94621',
        'Oakland Coliseum':'94621', #alias
        'Oriole Park at Camden Yards':'21201',
        'Petco Park':'92101',
        'PNC Park':'15212',
        'Progressive Field':'44115',
        'Rogers Centre':'M5V 1J1',
        'Safeco Field':'98134',
        'SunTrust Park':'30339',
        'Target Field':'55403',
        'Tropicana Field':'33705',
        'Wrigley Field':'60613',
        'Yankee Stadium':'10451'
    }[stadium_name]


def getAirDensity(tempf, rh, baropresin, elevft):
	temp = (tempf - 32.0)*(5.0/9.0)   # convert temperature to degrees Celsius 
	baropres = 25.4*baropresin   # convert barometric presure to mm of mercury 
	elev = 0.3048*elevft     # convert elevation to meters 
	g = 9.80665       # earth's gravitational acceleration 
	M = 0.0289644     # molecular mass of air 
	R = 8.31447       # universal gas constant 
	airpres = baropres*math.exp( (-g*M*elev) / (R*(temp+273.15)))  # absolute atmospheric air pressure 
	svp = 4.5841*math.exp( ((18.687 - temp/234.5)*temp)/(257.14+temp))   # Buck approximation to saturation vapor pressure 
	airdensity = 1.2929*(273.0/(temp+273.0))*((airpres - svp*rh/100.0)/760.0)  # air density in kg/m^3 
	
	return round(airdensity, 4);

pitchesfilename = 'WeatherCompTableRev.csv'

start = time.time()

print('Parsing file...')
with open(pitchesfilename, newline='') as ifile:
    reader = csv.DictReader(ifile)
    fieldnames = reader.fieldnames

    
    with open(pitchesfilename[0:-4] + '_vu.csv', 'w', newline='') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)
        writer.writeheader()
        
        lastCODE = 'none'
        lastgameName = 'none'
        CODE = ''
        gameName = ''

        cur_row = 1
        percent = 1
        row_count = 704367
        row_mod = round(row_count / 100,0)

        doubleheaders = ['gid_2017_05_14_houmlb_nyamlb_2',
                         'gid_2017_05_21_kcamlb_minmlb_2',
                         'gid_2017_05_27_detmlb_chamlb_2',
                         'gid_2017_06_10_oakmlb_tbamlb_2',
                         'gid_2017_08_06_seamlb_kcamlb_2',
                         'gid_2017_08_21_minmlb_chamlb_2',
                         'gid_2017_08_22_miamlb_phimlb_2',
                         'gid_2017_08_30_atlmlb_phimlb_2',
                         'gid_2017_08_30_clemlb_nyamlb_2',
                         'gid_2017_09_09_houmlb_oakmlb_2',
                         'gid_2017_09_25_atlmlb_nynmlb_2']

        for row in reader:
            if cur_row % row_mod == 0:
                print('Progress: {}%'.format(percent))
                percent += 1

                
            gameName = row['gameName']
            
            if gameName in doubleheaders:
                row['Time'] = game2fix(gameName)
                row['ampm'] = 'PM'

            
            writer.writerow(row)
            cur_row += 1

print('Progres: 100%...DONE')
elapsed = time.time() - start
print(elapsed)
