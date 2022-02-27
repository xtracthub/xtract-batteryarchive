
import os
import csv
import time
import pickle as pkl
from beep.structure.cli import auto_load

ba_file = "batteryarchive_files.csv"
base_ba_path = "/Users/tylerskluzacek/batteryarchive"
base_pkl_path = "beep_intermediates"

start_counter = 121

t0 = time.time()
with open(ba_file, 'r') as f:
    reader = csv.reader(f)
    next(reader)

    nan_count = 0
    for item in reader:
        id = item[0]
        filename = item[1]

        if int(id) < start_counter:
            continue

        if f"{id}.pkl" in os.listdir(base_pkl_path):
            print(f"ID {id} already a pkl. Continuing!")
            continue

        print(f"Filename: {filename}")
        print(f"ID: {id}")
        full_path = os.path.join(base_ba_path, filename)

        datapath = auto_load(full_path)
        is_valid, msg = datapath.validate()
        print("File is valid: ", is_valid)
        print(msg)
        try:
            datapath.structure()
        except NotImplementedError:
            nan_count += 1
            print(f"Nan count: {nan_count}")
            continue

        pkl_name = f"{id}.pkl"
        full_pkl_path = os.path.join(base_pkl_path, pkl_name)
        with open(full_pkl_path, 'wb') as g:
            pkl.dump(datapath, g)
