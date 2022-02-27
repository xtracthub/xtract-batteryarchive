
import psycopg2
import beep
from matplotlib import pyplot as plt
import pickle as pkl
import pandas as pd


# class XtractBattery:
#     def __init__(self):
#         self.file_list = []
#         self.loaded_files = False
#         self.count_dict = dict()
#
#     def _load_beep_file(self, file_id):
#         with open(f'/home/ubuntu/beep_intermediates/{file_id}.pkl', 'rb') as f:
#             data = pkl.load(f)
#             self.loaded_file = True
#             return data
#
#     def get_energy_curve(self, beep_file, eff_type, x_val):
#         assert eff_type in ['coulombic', 'energy'], "eff_type (efficiency) must be of type 'coluombic' or 'energy"
#         assert x_val in ['time', 'cycle']
#         # print(datapath.structured_summary.columns)
#
#         import pandas as pd
#
#         print(beep_file.structured_summary.columns)
#         x = None
#         x_label = None
#         if x_val == 'time':
#             time_objs = pd.to_datetime(beep_file.structured_summary.date_time_iso)
#             # datetime.datetime.strptime(date_time_str, '%b %d %Y %I:%M%p')
#
#             min_x = time_objs.min()
#
#             x = (time_objs - min_x).dt.total_seconds()
#             print(x)
#             # TODO: maybe have 'time' converted from scientific notation "...e6"
#             x_label = f'Time since experiment start (s)'
#         elif x_val == 'cycle':
#             x = beep_file.structured_summary.cycle_index
#             x_label = "Cycle"
#
#         if eff_type == 'energy':
#             plt.plot(x, beep_file.structured_summary.energy_efficiency)
#         elif eff_type == 'coulombic':
#             coul_eff = beep_file.structured_summary.discharge_capacity / beep_file.structured_summary.charge_capacity
#             plt.plot(x, coul_eff)
#
#         plt.xlabel(x_label)
#         plt.ylabel(f"{eff_type} efficiency")
#         plt.show()
#
#     def count_and_collect(self, clauses=[], groupby=None):
#
#         self.file_list = []
#
#         assert type(clauses) == list, "Clauses must be list of triples (var, operator, value)"
#
#         conn = psycopg2.connect(host='xtractdb.c80kmwegdwta.us-east-1.rds.amazonaws.com',
#                                 user='xtract', dbname='xtractdb', port=5432, password='xtract123')
#
#         sql_conv = {
#             'n_cycles': 'num_cycles',
#             'n_days': 'elapsed_s',
#             'cathode': 'cathode',
#             'anode': 'anode',
#             'group': 'group_code',
#             'min_temp_c': 'min_temp_c',
#             'max_temp_c': 'max_temp_c',
#             'dvodt_start': 'dvodt_start',
#             'dvodt_end': 'dvodt_end'
#         }
#
#         sql_types = {
#             'n_cycles': [int, float],
#             'n_days': [int, float],
#             'cathode': [str],
#             'anode': [str],
#             'group': [str],
#             'min_temp_c': [float],
#             'max_temp_c': [float],
#             'dvodt_start': [float],
#             'dvodt_end': [float]
#         }
#
#         # TODO: check if op in allowed ops
#         allowed_ops = ['=', '<>', '<', '>', '>=', '<=', '!=']
#
#         select_clause = ''
#         groupby_clause = ''
#         if groupby:
#             groupby_clause = f"GROUP BY {sql_conv[groupby]}"
#             select_clause = f"{sql_conv[groupby]},"
#
#         where_clause = ''
#         if len(clauses) > 0:
#             where_clause = where_clause + "WHERE "
#             first = True
#             for clause in clauses:
#
#                 if not first:
#                     where_clause = where_clause + "AND "
#                 first = False
#
#                 var, op, val = clause
#                 sql_var = sql_conv[var]  # Convert to SQL version.
#
#                 assert type(val) in sql_types[var], f"{var} should be of types {sql_types[var]}"
#                 # TODO: Make sure operator is valid.
#
#                 where_clause = where_clause + sql_var + " "
#                 where_clause = where_clause + op + " "
#
#                 if type(val) is str:
#                     val = f"'{val}'"
#                 where_clause = where_clause + str(val) + " "
#
#         query = f"SELECT {select_clause} COUNT(*) FROM battery_data {where_clause} {groupby_clause};"
#         query2 = f"SELECT id FROM battery_data {where_clause};"
#         cur = conn.cursor()
#
#         cur.execute(query)
#
#         return_dict = {'groups': []}
#
#         total_count = 0
#         for item in cur.fetchall():
#             if len(item) == 1:
#                 total_count += item[0]
#             elif len(item) == 2:
#                 total_count += item[1]
#                 return_dict['groups'].append({item[0]: item[1]})
#
#         return_dict['count'] = total_count
#
#         cur.execute(query2)
#
#         file_ids = []
#         for item in cur.fetchall():
#             file_ids.append(item[0])
#
#         self.file_list = file_ids
#         print(self.file_list)
#         self.count_dict = return_dict
#
#         conn.close()
#         return return_dict
#
#     def list(self):
#         # Do a query to get everything in list
#         conn = psycopg2.connect(host='xtractdb.c80kmwegdwta.us-east-1.rds.amazonaws.com',
#                                 user='xtract', dbname='xtractdb', port=5432, password='xtract123')
#         cur = conn.cursor()
#
#         header_row = ['ID', 'Filename', 'Cathode', 'Anode', 'Cycles', 'Days', 'Group', 'Min Temp', 'Max Temp', 'DT/DV Start', 'DT/DV End']
#         base_query = "SELECT id, filename, cathode, anode, num_cycles, elapsed_s, group_code, min_temp_c, max_temp_c, dvodt_start, dvodt_end FROM battery_data WHERE "
#
#         first = True
#         for item in self.file_list:
#
#             if not first:
#                 base_query = base_query + "OR "
#             first = False
#
#             base_query = base_query + f"id={item} "
#
#         cur.execute(base_query)
#
#         master_ls = []
#         for item in cur.fetchall():
#             id, filename, cathode, anode, num_cycles, elapsed_s, group_code, \
#             min_temp_c, max_temp_c, dvodt_start, dvodt_end = item
#
#             master_ls.append([id, filename, cathode, anode, num_cycles, elapsed_s, group_code, min_temp_c, max_temp_c, dvodt_start, dvodt_end])
#
#         df = pd.DataFrame(master_ls, columns=header_row)
#         print(df)
#         return df

#
# # xb = XtractBattery()
# # xb.count_and_collect(clauses=[('n_cycles', '>', 100), ('cathode', '=', 'NCA')], groupby='group')
#
# # Logan: answer for #1
# # TODO.
#
# # Logan: answer for #2.
# xb.count_and_collect(clauses=[('n_cycles', '>=', 100), ('n_cycles', '<=', 300), ], groupby='group')
#
# # Logan: answer for #3.


import psycopg2
import beep
from matplotlib import pyplot as plt
import pickle as pkl
import pandas as pd


class XtractBattery:
    def __init__(self):
        self.file_list = []
        self.loaded_files = False
        self.count_dict = dict()

    def _load_beep_file(self, file_id):
        with open(f'/home/ubuntu/beep_intermediates/{file_id}.pkl', 'rb') as f:
            data = pkl.load(f)
            self.loaded_file = True
            return data

    def count_and_collect(self, clauses=[], groupby=None):

        self.file_list = []

        assert type(clauses) == list, "Clauses must be list of triples (var, operator, value)"

        conn = psycopg2.connect(host='xtractdb.c80kmwegdwta.us-east-1.rds.amazonaws.com',
                                user='xtract', dbname='xtractdb', port=5432, password='xtract123')

        sql_conv = {
            'n_cycles': 'num_cycles',
            'n_days': 'elapsed_s',
            'cathode': 'cathode',
            'anode': 'anode',
            'group': 'group_code',
            'min_temp_c': 'min_temp_c',
            'max_temp_c': 'max_temp_c',
            'dtodv_start': 'dvodt_start',
            'dtodv_end': 'dvodt_end'
        }

        sql_types = {
            'n_cycles': [int, float],
            'n_days': [int, float],
            'cathode': [str],
            'anode': [str],
            'group': [str],
            'min_temp_c': [float],
            'max_temp_c': [float],
            'dtodv_start': [float],
            'dtodv_end': [float]
        }

        # TODO: check if op in allowed ops
        allowed_ops = ['=', '<>', '<', '>', '>=', '<=', '!=']

        select_clause = ''
        groupby_clause = ''
        if groupby:
            groupby_clause = f"GROUP BY {sql_conv[groupby]}"
            select_clause = f"{sql_conv[groupby]},"

        where_clause = ''
        if len(clauses) > 0:
            where_clause = where_clause + "WHERE "
            first = True
            for clause in clauses:

                if not first:
                    where_clause = where_clause + "AND "
                first = False

                var, op, val = clause
                sql_var = sql_conv[var]  # Convert to SQL version.

                assert type(val) in sql_types[var], f"{var} should be of types {sql_types[var]}"
                # TODO: Make sure operator is valid.

                where_clause = where_clause + sql_var + " "
                where_clause = where_clause + op + " "

                if type(val) is str:
                    val = f"'{val}'"
                where_clause = where_clause + str(val) + " "

        query = f"SELECT {select_clause} COUNT(*) FROM battery_data {where_clause} {groupby_clause};"
        query2 = f"SELECT id FROM battery_data {where_clause};"
        cur = conn.cursor()

        cur.execute(query)

        return_dict = {'groups': []}

        total_count = 0
        for item in cur.fetchall():
            if len(item) == 1:
                total_count += item[0]
            elif len(item) == 2:
                total_count += item[1]
                return_dict['groups'].append({item[0]: item[1]})

        return_dict['count'] = total_count

        cur.execute(query2)

        file_ids = []
        for item in cur.fetchall():
            file_ids.append(item[0])

        self.file_list = file_ids
        # print(self.file_list)
        self.count_dict = return_dict

        conn.close()
        return return_dict


    def get_charge_discharge_curves(self, fid, cycles, graph_type, x_val):

        assert graph_type in ['charge', 'discharge'], "graph_type should be 'charge' or 'discharge'. "
        assert x_val in ['time', 'capacity'], "x_val should be of type 'capacity' or 'time'."

        with open(f'/home/ubuntu/beep_intermediates/{fid}.pkl', 'rb') as f:
            beep_file = pkl.load(f)

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

    def get_fade_curves(self, fid, x_val):
        # assert graph_type in ['charge', 'discharge'], "graph_type should be 'charge' or 'discharge'. "
        assert x_val in ['time', 'cycle'], "x_val should be of type 'cycle' or 'time'."

        with open(f'/home/ubuntu/beep_intermediates/{fid}.pkl', 'rb') as f:
            beep_file = pkl.load(f)

        

        reg_charge = beep_file.structured_data[beep_file.structured_data.step_type == 'discharge']

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

    def get_efficiency_curve(self, fid, eff_type, x_val):
        assert eff_type in ['coulombic', 'energy'], "eff_type (efficiency) must be of type 'coluombic' or 'energy"
        assert x_val in ['time', 'cycle']
        # print(datapath.structured_summary.columns)


        with open(f'/home/ubuntu/beep_intermediates/{fid}.pkl', 'rb') as f:
            beep_file = pkl.load(f)
            # self.loaded_file = True
            # return data


        import pandas as pd

        # print(beep_file.structured_summary.columns)
        x = None
        x_label = None
        if x_val == 'time':
            time_objs = pd.to_datetime(beep_file.structured_summary.date_time_iso)
            # datetime.datetime.strptime(date_time_str, '%b %d %Y %I:%M%p')

            min_x = time_objs.min()

            x = (time_objs - min_x).dt.total_seconds()
            # print(x)
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

    def df_dump(self):
        # Do a query to get everything in list
        conn = psycopg2.connect(host='xtractdb.c80kmwegdwta.us-east-1.rds.amazonaws.com',
                                user='xtract', dbname='xtractdb', port=5432, password='xtract123')
        cur = conn.cursor()

        header_row = ['id', 'filename', 'cathode', 'anode', 'n_cycles', 'n_days', 'group', 'min_temp_c', 'max_temp_c', 'dtodv_start', 'dtodv_end']
        base_query = "SELECT id, filename, cathode, anode, num_cycles, elapsed_s, group_code, min_temp_c, max_temp_c, dvodt_start, dvodt_end FROM battery_data WHERE "

        first = True
        for item in self.file_list:

            if not first:
                base_query = base_query + "OR "
            first = False

            base_query = base_query + f"id={item} "

        cur.execute(base_query)

        master_ls = []
        for item in cur.fetchall():
            id, filename, cathode, anode, num_cycles, elapsed_s, group_code, \
            min_temp_c, max_temp_c, dvodt_start, dvodt_end = item

            filename = filename.replace('/Users/tylerskluzacek/batteryarchive', '') 

            master_ls.append([id, filename, cathode, anode, num_cycles, elapsed_s, group_code, min_temp_c, max_temp_c, dvodt_start, dvodt_end])

        df = pd.DataFrame(master_ls, columns=header_row)
        # print(df)
        return df


# xb = XtractBattery()
# # xb.count_and_collect(clauses=[('n_cycles', '>', 100), ('cathode', '=', 'NCA')], groupby='group')
#
# # Logan: answer for #1
# # TODO.
#
# # Logan: answer for #2.
# xb.count_and_collect(clauses=[('n_cycles', '>=', 100), ('n_cycles', '<=', 300), ], groupby='group')
#
# # Logan: answer for #3.
# # 17.1
#
#
# print(len(xb.file_list))
# print(xb.count_dict)
# xb.get_energy_curve()
