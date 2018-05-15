import csv
import requests
import json
from bs4 import BeautifulSoup
from parse_h import distance

file = 'ballparks_closest_airports_vu_new.csv'

with open(file, 'r', newline='', encoding='utf-8') as ifile:
    reader = csv.DictReader(ifile)
    fieldnames = reader.fieldnames
    

    with open(file[0:-4] + '_new.csv', 'w', newline='', encoding='utf-8') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            stadium = row['stadium']
            print(stadium)
            lat1  = float(row['lat'])
            long1 = float(row['long'])

            lat2  = float(row['closest_ap1_lat'])
            long2 = float(row['closest_ap1_long'])
       
            dist = distance(lat1, long1, lat2, long2)
            row['closest_ap1_dist_km'] = round(dist, 4)


            lat2  = float(row['closest_ap2_lat'])
            long2 = float(row['closest_ap2_long'])
       
            dist = distance(lat1, long1, lat2, long2)
            row['closest_ap2_dist_km'] = round(dist, 4)

            lat2  = float(row['closest_ap3_lat'])
            long2 = float(row['closest_ap3_long'])
       
            dist = distance(lat1, long1, lat2, long2)
            row['closest_ap3_dist_km'] = round(dist, 4)


            writer.writerow(row)
