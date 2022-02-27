
import os
import csv
from xtract_battery_main import parse_filename

i = 0
base_path = '/Users/tylerskluzacek/batteryarchive'


writer = csv.writer(open('batteryarchive_files.csv', 'w'))
writer.writerow(['id', 'path', 'group', 'cathode', 'anode'])

for item in os.listdir(base_path):

    if 'timeseries' in item:
        full_path = os.path.join(base_path, item)
        finfo = parse_filename(full_path)

        writable = [i,
                    item,
                    finfo['group'],
                    finfo['structure'],
                    finfo['cathode'],
                    finfo['anode']]

        writer.writerow(writable)

        # TODO: add things from outside filename.

        i += 1