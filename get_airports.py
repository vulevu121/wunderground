import json
from parse_h import distance

with open('angel_airports.json', 'r', encoding='utf-8') as f:
    airports = json.load(f)


    ap_list = {}
        

    for each in airports['results']:
        name = each['name']
        lat2 = each['geometry']['location']['lat']
        long2 = each['geometry']['location']['lng']
        dist = round(distance(33.800308,-117.8827321, lat2, long2), 4)

        ap_list[name] = {'distance' : dist,
                         'lat' : lat2,
                         'long' : long2}
        
        
    sorted_airports = sorted(ap_list.items(), key=lambda x: x[1]['distance'])

    print(sorted_airports[0][0])
