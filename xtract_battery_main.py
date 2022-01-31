from batdata.extractors.batteryarchive import BatteryArchiveExtractor
from batdata.extractors.arbin import ArbinExtractor

from beep.structure.cli import auto_load

from matplotlib import pyplot as plt

import seaborn as sns

sns.color_palette('colorblind')


test_file = '/Users/tylerskluzacek/batteryarchive/UL-PUR_N10-EX9_18650_NCA_23C_0-100_0.5-0.5C_i_timeseries.csv'
test_file = '/Users/tylerskluzacek/batteryarchive/SNL_18650_NMC_25C_0-100_0.5-2C_a_timeseries.csv'

# BATDATA WORKSPACE

datapath = auto_load(test_file)
is_valid, msg = datapath.validate()
print("File is valid: ", is_valid)
print(msg)

datapath.structure()

def charge_discharge_curves(cycles, graph_type, x_val):

    assert graph_type in ['charge', 'discharge'], "graph_type should be 'charge' or 'discharge'. "
    assert x_val in ['time', 'capacity'], "x_val should be of type 'capacity' or 'time'."

    reg_charge = datapath.structured_data[datapath.structured_data.step_type == graph_type]

    # print("Mean current for cycle 25: ", reg_charge.current[reg_charge.cycle_index == 25].mean())
    # print("Number of cycles: ", reg_charge.cycle_index.max())
    # print("Max charge capacity at cycle 25: ", reg_charge.discharge_capacity[reg_charge.cycle_index == 25].max())
    
    if graph_type == 'charge':
        capacity_holder = reg_charge.charge_capacity
    elif graph_type == 'discharge':
        capacity_holder = reg_charge.discharge_capacity

    for cycle in cycles:

       cycle_test_time = reg_charge.test_time[reg_charge.cycle_index == cycle]
       cycle_test_time_2 = cycle_test_time - cycle_test_time.min()

       if x_val == 'time':
           x = cycle_test_time_2
           xlabel = f'Time since {graph_type} cycle start (s)'
       elif x_val == 'capacity':
           x = capacity_holder[reg_charge.cycle_index == cycle]
           xlabel = f'{graph_type}_capacity (Ah)'

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
    plt.xlabel(xlabel)
    plt.ylabel('Voltage (V)')
    # plt.show()
    # plt.plot(datapath.structured_summary.cycle_index, datapath.structured_summary.energy_efficiency)
    plt.legend()
    plt.show()


# Uncomment to make/test charge curves. 
# charge_discharge_curves([10, 100, 500], graph_type='discharge', x_val='capacity')

def energy_curve(eff_type, x_val):
    assert eff_type in ['coulombic', 'energy'], "eff_type (efficiency) must be of type 'coluombic' or 'energy"
    assert x_val in ['time', 'cycle']
    # print(datapath.structured_summary.columns)

    import pandas as pd

    print(datapath.structured_summary.columns)
    if x_val == 'time':
        time_objs = pd.to_datetime(datapath.structured_summary.date_time_iso)
        # datetime.datetime.strptime(date_time_str, '%b %d %Y %I:%M%p')

        min_x = time_objs.min()
        
        x = (time_objs - min_x).dt.total_seconds()
        print(x)
        # TODO: maybe have 'time' converted from scientific notation "...e6"
        xlabel = f'Time since experiment start (s)'
    elif x_val == 'cycle':
        x = datapath.structured_summary.cycle_index
        xlabel = "Cycle"

    if eff_type == 'energy':
        plt.plot(x, datapath.structured_summary.energy_efficiency)
    elif eff_type == 'coulombic':
        coul_eff = datapath.structured_summary.discharge_capacity / datapath.structured_summary.charge_capacity 
        plt.plot(x, coul_eff)

    plt.xlabel(xlabel)
    plt.ylabel("Energy efficiency")
    plt.show()

# Uncomment to make/test energy curves
energy_curve('energy', 'time')

def execute_extractor():
    ex = BatteryArchiveExtractor()
    
    data = ex.parse_timeseries_to_dataframe(test_file)
    
    num_cycles = ex.get_number_of_cycles(data)
    calendar_days = ex.get_calendar_aging(data)
    temp_min_max = ex.get_temp_min_max(data)
    
    delta_v_over_delta_t = ex.get_delta_v_over_delta_t(data)
    
    # print(delta_v_over_delta_t)
    # filename_info = get_info_from_filename(test_file)

    # beep_data = ex.get_beep_data(test_file)
    # print(beep_data)

        
    datapath = auto_load(test_file)
    is_valid, msg = datapath.validate()
    print("File is valid: ", is_valid)
    print(msg)

    datapath.structure()

    plt.plot(data['voltage'])
    plt.show()

    return data



# if __name__ == "__main__":
#     mdata = execute_extractor()
