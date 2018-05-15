import time
from datetime import datetime, timedelta, tzinfo

time1 = datetime.strptime('170604_205857', '%y%m%d_%H%M%S')
time2 = datetime.strptime('170604_210154', '%y%m%d_%H%M%S')

halftime = (time2 - time1)/2 + time1

halftimestr = halftime.strftime('%y%m%d_%H%M%S')

print(halftimestr)
