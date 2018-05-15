import csv
import requests
import json
from parse_h import distance
from bs4 import BeautifulSoup
import time

file = 'ballparks_closest_airports_vu_new.csv'

with open(file, 'r', newline='', encoding='utf-8') as ifile:
    reader = csv.DictReader(ifile)
    fieldnames = reader.fieldnames

    with open(file[0:-4] + '_new.csv', 'a', newline='', encoding='utf-8') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            stadium = row['stadium']
            print(stadium)
            ADDRESS = row['address']
            lat = float(row['lat'])
            long = float(row['long'])

            url = 'http://airnav.com/cgi-bin/airport-search'

            payload = {
                'lat': lat,
                'lon':  long,
                'maxdistance': '40',
                'fieldtypes': 'a',
                'use': 'um'
                }


            r = requests.post(url, data = payload)
            soup = BeautifulSoup(r.text, "lxml")

            table = soup.findAll('table')
            tr = table[3].findAll('tr')

            near_ap = {}

            for i in range(1, 4):
                td = tr[i].findAll('td')

                code = td[0].text.strip()
                name = td[2].text.strip().title()

                url = 'http://airnav.com/airport/{}'.format(code)

                r = requests.get(url)

                soup2 = BeautifulSoup(r.text, "lxml")
                table = soup2.findAll('table')
                td = table[7].findAll('td')

                coord = td[3].br.next_sibling.next_sibling.next_sibling.split(' / ')
                lat2 = float(coord[0])
                long2 = float(coord[1])
                
                dist = round(distance(lat, long, lat2, long2), 4)

                near_ap[i-1] = {'name': name,
                                'code' : 'K{}'.format(code),
                                'lat': lat2,
                                'long': long2,
                                'distance': dist}
                time.sleep(1.0)

            row['closest_ap1_name']    = near_ap[0]['name']
            row['closest_ap1_code']    = near_ap[0]['code']
            row['closest_ap1_lat']     = near_ap[0]['lat']
            row['closest_ap1_long']    = near_ap[0]['long']
            row['closest_ap1_dist_km'] = near_ap[0]['distance']

            row['closest_ap2_name']    = near_ap[1]['name']
            row['closest_ap2_code']    = near_ap[1]['code']
            row['closest_ap2_lat']     = near_ap[1]['lat']
            row['closest_ap2_long']    = near_ap[1]['long']
            row['closest_ap2_dist_km'] = near_ap[1]['distance']

            row['closest_ap3_name']    = near_ap[2]['name']
            row['closest_ap3_code']    = near_ap[2]['code']
            row['closest_ap3_lat']     = near_ap[2]['lat']
            row['closest_ap3_long']    = near_ap[2]['long']
            row['closest_ap3_dist_km'] = near_ap[2]['distance']
            

            writer.writerow(row)

                   
