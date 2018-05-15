import csv
import requests
import json
from bs4 import BeautifulSoup

file = 'ballparks_closest_airports_vu_new_new.csv'

with open(file, 'r', newline='', encoding='utf-8') as ifile:
    reader = csv.DictReader(ifile)
    fieldnames = reader.fieldnames
    

    with open(file[0:-4] + '_new.csv', 'w', newline='', encoding='utf-8') as ofile:
        writer = csv.DictWriter(ofile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            print(row['python_code'])
            latitude = row['latitude']
            longitude = row['longitude']

            URL = 'https://airport.globefeed.com/US_Nearest_Airport_Result.asp?lat={}&lng={}'.format(latitude, longitude)

            r = requests.get(URL)

            soup = BeautifulSoup(r.text, "lxml")
            ap1 = soup.table.tr.next_sibling.td.next_sibling
            ap1_name = ap1.next_element
            ap1_code = ap1.next_sibling.next_sibling.next_sibling.next_element
            ap1_dist = ap1.next_sibling.next_sibling.next_sibling.next_sibling.next_element

            
            ap2 = soup.table.tr.next_sibling.next_sibling.td.next_sibling
            ap2_name = ap2.next_element
            ap2_code = ap2.next_sibling.next_sibling.next_sibling.next_element
            ap2_dist = ap2.next_sibling.next_sibling.next_sibling.next_sibling.next_element


            ap3 = soup.table.tr.next_sibling.next_sibling.next_sibling.td.next_sibling
            ap3_name = ap3.next_element
            ap3_code = ap3.next_sibling.next_sibling.next_sibling.next_element
            ap3_dist = ap3.next_sibling.next_sibling.next_sibling.next_sibling.next_element

            
##            print('1: {}, {}, {}'.format(ap1_name, ap1_code, ap1_dist))
##            print('2: {}, {}, {}'.format(ap2_name, ap2_code, ap2_dist))
##            print('3: {}, {}, {}'.format(ap3_name, ap3_code, ap3_dist))

            row['closest_ap1_name'] = ap1_name
            row['closest_ap1_code'] = ap1_code
            row['closest_ap1_dist_km'] = ap1_dist.rstrip(' km')
            
            row['closest_ap2_name'] = ap2_name
            row['closest_ap2_code'] = ap2_code
            row['closest_ap2_dist_km'] = ap2_dist.rstrip(' km')

            row['closest_ap3_name'] = ap3_name
            row['closest_ap3_code'] = ap3_code
            row['closest_ap3_dist_km'] = ap3_dist.rstrip(' km')
            writer.writerow(row)





