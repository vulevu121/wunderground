import csv
import requests
import json
from parse_h import distance

file = 'ballparks_closest_airports_vu_new.csv'

with open(file, 'r', newline='', encoding='utf-8') as ifile:
    reader = csv.DictReader(ifile)
    fieldnames = reader.fieldnames
    

    with open(file[0:-4] + '_new.csv', 'w', newline='', encoding='utf-8') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            ADDRESS = row['address']
##            lat = row['lat']
##            long = row['long']
            
            #print(ADDRESS)
            API_KEY = 'AIzaSyC04BPODsw3o22wk1WEHSwhELitdhr1Xbc'
            URL = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(ADDRESS, API_KEY)
           
            r = requests.get(URL)

            jsondata = r.json()
            
            try:
                name = jsondata['results'][0]['address_components'][0]['long_name']
                latitude = jsondata['results'][0]['geometry']['location']['lat']
                longitude = jsondata['results'][0]['geometry']['location']['lng']
            except:
                name = 'NONE'
                latitude = 'NONE'
                longitude = 'NONE'
                dist_mi = 'NONE'
            print(jsondata['results'][0]['formatted_address'])

            
            row['lat'] = latitude
            row['long'] = longitude
            #row['closest_ap3_dist_km'] = 

            writer.writerow(row)
