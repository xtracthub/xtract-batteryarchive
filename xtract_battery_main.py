from batdata.extractors.batteryarchive import BatteryArchiveExtractor
from batdata.extractors.arbin import ArbinExtractor

from beep.structure.cli import auto_load

from matplotlib import pyplot as plt

import time
import os

import pickle as pkl
import seaborn as sns

sns.color_palette('colorblind')

base_path = "/Users/tylerskluzacek/batteryarchive"

ts0 = 'CALCE_CX2-16_prism_LCO_25C_0-100_0.5-0.5C_a_timeseries.csv'
ts1 = 'HNEI_18650_NMC_LCO_25C_0-100_0.5-1.5C_a_timeseries.csv'
ts2 = 'OX_1-1_pouch_LCO_40C_0-100_2-1.84C_a_timeseries.csv'
ts3 = 'SNL_18650_NMC_25C_0-100_0.5-2C_a_timeseries.csv'
ts4 = 'UL-PUR_N10-EX9_18650_NCA_23C_0-100_0.5-0.5C_i_timeseries.csv'

ts_ls = [ts0, ts1, ts2, ts3, ts4]
# test_file = '/Users/tylerskluzacek/batteryarchive/SNL_18650_NMC_25C_0-100_0.5-2C_a_timeseries.csv'
# BATDATA WORKSPACE


# TYLER 02/20: UNCOMMENT THESE 5 LINES FOR TESTING CHARTS.
# datapath = auto_load(test_file)
# is_valid, msg = datapath.validate()
# print("File is valid: ", is_valid)
# print(msg)
# datapath.structure()

import psycopg2


conn = psycopg2.connect(host='xtractdb.c80kmwegdwta.us-east-1.rds.amazonaws.com',
                        user='xtract', dbname='xtractdb', port=5432, password='xtract123')


def parse_dataframe(filename):
    # TODO: right here, should put the total number of everything.
    pass


def parse_filename(filename):
    info_dict = dict()
    bits = filename.split('_')
    # print(bits)
    # Grab the group
    group = bits[0].split('/')[-1]
    info_dict['group'] = group

    # Get battery type (cylinder/pouch/prism)
    b_types = ['pouch', 'prism', '18650']
    b_type = None
    for possible_type in b_types:
        if possible_type in filename:
            b_type = possible_type
            break
    info_dict['structure'] = b_type

    # Get the chemistry
    chems = ['LCO', 'NMC_LCO', 'LFP', 'NCA', 'NMC']
    b_chem = None
    for possible_chem in chems:
        if possible_chem in filename:
            b_chem = possible_chem
            break
    info_dict['cathode'] = b_chem
    info_dict['anode'] = 'graphite'

    return info_dict

# Uncomment to test filenamea
# for ts in ts_ls:
#     full_path = os.path.join(base_path, ts)
#     mdata = parse_filename(full_path)
#     print(mdata)


def get_fade_curves(beep_file, graph_type, x_val):

    assert graph_type in ['charge', 'discharge'], "graph_type should be 'charge' or 'discharge'. "
    assert x_val in ['time', 'cycle'], "x_val should be of type 'cycle' or 'time'."

    reg_charge = beep_file.structured_data[beep_file.structured_data.step_type == graph_type]

    x_label = None
    cycles = beep_file.structured_summary.cycle_index

    # print(reg_charge.discharge_capacity[reg_charge.cycle_index == cycle].tolist())

    charge_holder = []
    discharge_holder = []
    time_holder = []
    last_discharge = 0
    last_charge = 0
    cycles_that_count = []
    times_that_count = []
    for cycle in cycles:
        # print(cycle)
        try:
            final_discharge = reg_charge.discharge_capacity[reg_charge.cycle_index == cycle].tolist()[-1]
            last_discharge = final_discharge
        except IndexError:
            final_discharge = last_discharge

        try:
            final_charge = reg_charge.charge_capacity[reg_charge.cycle_index == cycle].tolist()[-1]
            last_charge = final_charge
        except IndexError:
            final_charge = last_charge

        cycle_test_time = reg_charge.test_time[reg_charge.cycle_index == cycle].tolist()
        if len(cycle_test_time) == 0:
            continue
        else:
            cycles_that_count.append(cycle)
            time_holder.append(cycle_test_time[-1])


        # final_charge = reg_charge.charge_capacity[reg_charge.cycle_index == cycle].tolist()[-1]
        discharge_holder.append(final_discharge)
        charge_holder.append(final_charge)
        # print(charge_holder)

    # print(len(cycles))
    # print(len(discharge_holder))
    # plt.scatter(cycles_that_count, discharge_holder)
    # plt.scatter(cycles_that_count, charge_holder)

    plt.scatter(time_holder, discharge_holder)
    plt.scatter(time_holder, charge_holder)

    plt.ylabel("(Dis)charge capacity")
    plt.xlabel(x_val)
    plt.show()
    # exit()

    # cycles = [5, 10, 20]
    # for cycle in cycles:
    #
    #     cycle_test_time = reg_charge.test_time[reg_charge.cycle_index == cycle]
    #     cycle_test_time_2 = cycle_test_time - cycle_test_time.min()
    #
    #     x = None
    #     if x_val == 'time':
    #         x = cycle_test_time_2
    #         x_label = f'Time since {graph_type} cycle start (s)'
    #     elif x_val == 'cycle':
    #         #x = capacity_holder[reg_charge.cycle_index == cycle]
    #         x = beep_file.structured_summary.cycle_index
    #         x_label = f'Cycle Index'
    #
    #     print(len(x))
    #     print(len(reg_charge.discharge_capacity[reg_charge.cycle_index == cycle]))
    #
    #     print(dir(reg_charge))
    #     print(reg_charge.discharge_capacity)
    #     # print()
    #     import numpy as np
    #     y = np.arange(len(reg_charge.discharge_capacity))
    #     # y = []
    #
    #     plt.scatter(y, reg_charge.discharge_capacity)
    #
    #     # plt.scatter(x, reg_charge.discharge_capacity[reg_charge.cycle_index == cycle],
    #     #             # plt.scatter(capacity_holder[reg_charge.cycle_index == cycle], reg_charge.voltage[reg_charge.cycle_index == cycle],
    #     #             label=f'Cycle {cycle}',
    #     #             # color='green',
    #     #             s=20,
    #     #             alpha=0.5)
    #
    # plt.xlabel(x_label)
    #
    # plt.ylabel(f'{graph_type} capacity')
    # # plt.show()
    # # plt.plot(datapath.structured_summary.cycle_index, datapath.structured_summary.energy_efficiency)
    # plt.legend()
    # plt.show()


def get_charge_discharge_curves(beep_file, cycles, graph_type, x_val):

    assert graph_type in ['charge', 'discharge'], "graph_type should be 'charge' or 'discharge'. "
    assert x_val in ['time', 'capacity'], "x_val should be of type 'capacity' or 'time'."

    reg_charge = beep_file.structured_data[beep_file.structured_data.step_type == graph_type]

    # print("Mean current for cycle 25: ", reg_charge.current[reg_charge.cycle_index == 25].mean())
    # print("Number of cycles: ", reg_charge.cycle_index.max())
    # print("Max charge capacity at cycle 25: ", reg_charge.discharge_capacity[reg_charge.cycle_index == 25].max())

    capacity_holder = None
    if graph_type == 'charge':
        capacity_holder = reg_charge.charge_capacity
    elif graph_type == 'discharge':
        capacity_holder = reg_charge.discharge_capacity

    x_label = None
    for cycle in cycles:

        cycle_test_time = reg_charge.test_time[reg_charge.cycle_index == cycle]
        cycle_test_time_2 = cycle_test_time - cycle_test_time.min()

        x = None
        if x_val == 'time':
            x = cycle_test_time_2
            x_label = f'Time since {graph_type} cycle start (s)'
        elif x_val == 'capacity':
            x = capacity_holder[reg_charge.cycle_index == cycle]
            x_label = f'{graph_type}_capacity (Ah)'

        plt.scatter(x, reg_charge.voltage[reg_charge.cycle_index == cycle],
        # plt.scatter(capacity_holder[reg_charge.cycle_index == cycle], reg_charge.voltage[reg_charge.cycle_index == cycle],
                label=f'Cycle {cycle}',
                # color='green',
                s=20,
                alpha=0.5)
    """
    plt.scatter(capacity_holder[reg_charge.cycle_index == 10], reg_charge.voltage[reg_charge.cycle_index == 10], 
            color='red', 
            label='Cycle 10', 
            s=20, 
            alpha=0.5)

    plt.scatter(capacity_holder[reg_charge.cycle_index == 500], reg_charge.voltage[reg_charge.cycle_index == 500],
            color='orange',
            label='Cycle 500',
            s=20,
            alpha=0.5)
    """ 
    plt.xlabel(x_label)
    plt.ylabel('Voltage (V)')
    # plt.show()
    # plt.plot(datapath.structured_summary.cycle_index, datapath.structured_summary.energy_efficiency)
    plt.legend()
    plt.show()


# Uncomment to make/test charge curves. 
# charge_discharge_curves([10, 100, 500], graph_type='discharge', x_val='capacity')

def get_energy_curve(beep_file, eff_type, x_val):
    assert eff_type in ['coulombic', 'energy'], "eff_type (efficiency) must be of type 'coluombic' or 'energy"
    assert x_val in ['time', 'cycle']
    # print(datapath.structured_summary.columns)

    import pandas as pd

    print(beep_file.structured_summary.columns)
    x = None
    x_label = None
    if x_val == 'time':
        time_objs = pd.to_datetime(beep_file.structured_summary.date_time_iso)
        # datetime.datetime.strptime(date_time_str, '%b %d %Y %I:%M%p')

        min_x = time_objs.min()
        
        x = (time_objs - min_x).dt.total_seconds()
        print(x)
        # TODO: maybe have 'time' converted from scientific notation "...e6"
        x_label = f'Time since experiment start (s)'
    elif x_val == 'cycle':
        x = beep_file.structured_summary.cycle_index
        x_label = "Cycle"

    if eff_type == 'energy':
        plt.plot(x, beep_file.structured_summary.energy_efficiency)
    elif eff_type == 'coulombic':
        coul_eff = beep_file.structured_summary.discharge_capacity / beep_file.structured_summary.charge_capacity
        plt.plot(x, coul_eff)

    plt.xlabel(x_label)
    plt.ylabel(f"{eff_type} efficiency")
    plt.show()

# Uncomment to make/test energy curves
# energy_curve('energy', 'time')

# global start_zero
# global end_zero
# start_zero = 0
# end_zero = 0


def execute_extractor(id, filename):
    ex = BatteryArchiveExtractor()

    # Gives us GROUP, STRUCTURE, CATHODE, ANODE
    filename_mdata = parse_filename(filename)

    # Convert time series to dataframe (using Logan's code)
    data = ex.parse_timeseries_to_dataframe(filename)

    # Get DT/DV information
    volt = data['voltage'].to_list()
    temp = data['temperature'].to_list()

    first_20_v = volt[0:20]
    first_20_t = temp[0:20]

    second_20_v = volt[21:40]
    second_20_t = temp[21:40]

    last_20_v = volt[-20:]
    last_20_t = temp[-20:]
    secondlast_20_v = volt[-40:-21]
    secondlast_20_t = temp[-40:-21]

    print(id)
    can_attempt = True
    try:
        first_dv = sum(first_20_v)/len(first_20_v)
        first_dt = sum(first_20_t)/len(first_20_t)
        second_dv = sum(second_20_v)/len(second_20_v)
        second_dt = sum(second_20_t)/len(second_20_t)

        last_dv = sum(last_20_v)/len(last_20_v)
        last_dt = sum(last_20_t)/len(last_20_t)
        secondlast_dv = sum(secondlast_20_v)/len(secondlast_20_v)
        secondlast_dt = sum(secondlast_20_t)/len(secondlast_20_t)

    except ZeroDivisionError:
        can_attempt = False

    if can_attempt:
        try:
            dt_over_dv_start = (second_dt - first_dt) / (second_dv - first_dv)
        except ZeroDivisionError:
            dt_over_dv_start = None

        try:
            dt_over_dv_end = (last_dt - secondlast_dt) / (last_dv - secondlast_dv)
        except ZeroDivisionError:
            dt_over_dv_end = None

    else:
        dt_over_dv_start = None
        dt_over_dv_end = None

    # Gives us CYCLES, DAYS, TEMP (min and max).
    num_cycles = ex.get_number_of_cycles(data)
    calendar_days = ex.get_calendar_aging(data)
    temp_min_max = ex.get_temp_min_max(data)
    # print(temp_min_max)

    interpolation_nans = False
    if f"{id}.pkl" not in os.listdir('beep_intermediates'):
        interpolation_nans = True

    print(f"ID: {id}")
    print(f"Filanme: {filename}")
    print(f"Cathode: {filename_mdata['cathode']}")
    print(f"Anode: {filename_mdata['anode']}")
    print(f"Structure: {filename_mdata['structure']}")
    print(f"Num Cycles: {num_cycles}")
    print(f"Calendar Aging: {calendar_days}")
    print(f"Group Code: {filename_mdata['group']}")
    print(f"Interp. Nans: {interpolation_nans}")
    print(f"DT/DV Start: {dt_over_dv_start}")
    print(f"DT/DV End: {dt_over_dv_end}")
    print(f"Min temp: {temp_min_max[0]}")
    print(f"Max temp: {temp_min_max[1]}")
    # TODO: ADD STRUCTURE.

    temp_min = temp_min_max[0]
    temp_max = temp_min_max[1]
    import math

    if math.isnan(temp_min):
        temp_min = 'NULL'
    if math.isnan(temp_max):
        temp_max = 'NULL'

    if dt_over_dv_start is None or math.isnan(dt_over_dv_start):
        dt_over_dv_start = 'NULL'
    if dt_over_dv_end is None or math.isnan(dt_over_dv_end):
        dt_over_dv_end = 'NULL'

    if math.isnan(num_cycles):
        num_cycles = 'NULL'

    if math.isnan(calendar_days):
        calendar_days = 'NULL'

    print(f"Pushing to DB...")
    query = f"""INSERT INTO battery_data (id, filename, cathode, anode, num_cycles, elapsed_s, group_code, min_temp_c, max_temp_c, dvodt_start, dvodt_end) 
    VALUES ({id}, '{filename}', '{filename_mdata['cathode']}', '{filename_mdata['anode']}', {num_cycles}, 
    {calendar_days}, '{filename_mdata['group']}', {temp_min}, {temp_max}, {dt_over_dv_start}, {dt_over_dv_end});"""

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

    # Don't forget to skip the nan files.
    # with open(f'beep_intermediates/{id}.pkl', 'rb') as a:
    #     datapath = pkl.load(a)


    # GRAPHS: the following should be commented out and moved to query-time processing.

    # Charge and discharge curves
    # get_charge_discharge_curves(beep_file=datapath,
    #                             cycles=[10, 100, 500, 1000],
    #                             graph_type='discharge',
    #                             x_val='capacity')

    # import time
    # t0 = time.time()
    # with open('beep_intermediates/98.pkl', 'rb') as g:
    #     datapath = pkl.load(g)
    # print(f"Time to load: {time.time() - t0}")

    # Energy
    # get_energy_curve(datapath, eff_type='coulombic', x_val='time')

    # Fade
    # get_fade_curves(beep_file=datapath,
    #                             graph_type='discharge',
    #                             x_val='cycle')

    # TYLER: 02/20 -- uncomment for voltage curve
    # plt.plot(data['voltage'])
    # plt.show()

    # with open('thick_pickle.pkl', 'wb') as f:
    #     pkl.dump(datapath, f)

    return data


# if __name__ == "__main__":
# for ts in ts_ls:
#     full_path = os.path.join(base_path, ts)
#     execute_extractor(full_path)

import csv
with open('batteryarchive_files.csv', 'r') as f1:
    reader = csv.reader(f1)
    next(reader)

    for item in reader:
        id = item[0]
        path = item[1]
        print(path)
        full_path = os.path.join(base_path, path)
        execute_extractor(id, full_path)
        # time.sleep(0.5)
