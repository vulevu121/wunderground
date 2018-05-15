import csv
import json
import requests
from parse_h import distance
from bs4 import BeautifulSoup


url = 'http://airnav.com/cgi-bin/airport-search'

lat = 33.800308
long = -117.8827321

payload = {
    'lat': lat,
    'lon':  long,
    'maxdistance': '20',
    'fieldtypes': 'a',
    'use': 'um'
    }


r = requests.post(url, data = payload)
soup = BeautifulSoup(r.text, "lxml")

table = soup.findAll('table')
tr = table[3].findAll('tr')

near_ap = {}

for i in range(1, 3):
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
    
    
