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
            stadium = row['stadium']
            print(stadium)
            ADDRESS = row['address']
            lat = float(row['lat'])
            long = float(row['long'])

            LOCATION = '{},{}'.format(lat,long)

            API_KEY = 'AIzaSyC04BPODsw3o22wk1WEHSwhELitdhr1Xbc'
            
            URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}&keyword=aiport&type=airport&radius=150000&key={}'.format(LOCATION, API_KEY)
            r = requests.get(URL)

            nearby_airports = r.json()

            ap_dist = {}

            for each in nearby_airports['results']:
                name = each['name']
                lat2 = each['geometry']['location']['lat']
                long2 = each['geometry']['location']['lng']
                dist = round(distance(lat, long, lat2, long2), 4)

                ap_dist[name] = {'distance' : dist,
                                 'lat' : lat2,
                                 'long' : long2}
                
                
            sorted_ap_dist = sorted(ap_dist.items(), key=lambda x: x[1]['distance'])

            row['closest_ap1_name']    = sorted_ap_dist[0][0]
            row['closest_ap1_lat']     = sorted_ap_dist[0][1]['lat']
            row['closest_ap1_long']    = sorted_ap_dist[0][1]['long']
            row['closest_ap1_dist_km'] = sorted_ap_dist[0][1]['distance']

            row['closest_ap2_name']    = sorted_ap_dist[1][0]
            row['closest_ap2_lat']     = sorted_ap_dist[1][1]['lat']
            row['closest_ap2_long']    = sorted_ap_dist[1][1]['long']
            row['closest_ap2_dist_km'] = sorted_ap_dist[1][1]['distance']


            row['closest_ap3_name']    = sorted_ap_dist[2][0]
            row['closest_ap3_lat']     = sorted_ap_dist[2][1]['lat']
            row['closest_ap3_long']    = sorted_ap_dist[2][1]['long']
            row['closest_ap3_dist_km'] = sorted_ap_dist[2][1]['distance']
            

            writer.writerow(row)

                   
