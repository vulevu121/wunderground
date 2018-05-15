import json

bpjson = 'ballparks.json'

with open(bpjson, 'r') as f:
    bpdata = json.load(f)
print(bpdata['Angel Stadium']['address'])

##    for each in data:
##        print(each['stadium'])
