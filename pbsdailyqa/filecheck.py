# from tzlocal import get_localzone
# import datetime
import re

dtformat = "%Y%m%d"

# testdate = META["work_started"].astimezone(
#             get_localzone()).strftime(dtformat)
# testdate = datetime.datetime.now().astimezone(
#             get_localzone()).strftime(dtformat)

filename = "O:\\temp\\Adit\\dailyQAfiles\\position_20150818.opg"

with open(filename, 'r') as f:
    for i, line in enumerate(f):
        if i == 5:
            date = line
            break

print date
print date.split('\\')[-1].split('.')[0].split('_')[0]#.rstrip('.opw')
print re.findall('\d{8}', date)[0]

# spot_position_file_date = 1 if (testdate == date) else 0
