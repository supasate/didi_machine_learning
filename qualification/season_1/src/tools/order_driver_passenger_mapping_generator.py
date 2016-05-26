import os

cluster_map_path = '../../training_data/cluster_map/cluster_map'
dict_content = ""
with open(cluster_map_path, 'r') as f:
    for line in f.readlines():
        district_hash, district_id = line.strip().split()
        formatted_line = '    "' + district_hash + '" : "' + district_id + '",\n'
        dict_content += formatted_line
dict_content = dict_content[:-2]

driver_run_no = 1
passenger_run_no = 1
order_run_no = 1
driver_dict = dict()
passenger_dict = dict()
order_dict = dict()

for dataset in ['training_data', 'test_set_1']:
    order_folder = '../../' + dataset + '/order_data'
    for file_name in os.listdir(order_folder):
        input_file = order_folder + '/' + file_name
        with open(input_file, 'r') as f:
            for line in f.readlines():
                first_tab_idx = line.find('\t')
                second_tab_idx = line.find('\t', first_tab_idx + 1)
                third_tab_idx = line.find('\t', second_tab_idx + 1)
                order_hash = line[: first_tab_idx]
                driver_hash = line[first_tab_idx + 1: second_tab_idx]
                passenger_hash = line[second_tab_idx + 1: third_tab_idx]
                if order_hash != 'NULL' and order_hash not in order_dict:
                    order_dict[order_hash] = str(order_run_no)
                    order_run_no += 1
                if driver_hash != 'NULL' and driver_hash not in driver_dict:
                    driver_dict[driver_hash] = str(driver_run_no)
                    driver_run_no += 1
                if passenger_hash != 'NULL' and passenger_hash not in passenger_dict:
                    passenger_dict[passenger_hash] = str(passenger_run_no)
                    passenger_run_no += 1
order_dict_content = ""
for order_hash, order_id in order_dict.items():
    order_dict_content += '    "' + order_hash + '":"' +  order_id + '",\n'
order_dict_content = order_dict_content[: -2]

driver_dict_content = ""
for driver_hash, driver_id in driver_dict.items():
    driver_dict_content += '    "' + driver_hash + '":"' +  driver_id + '",\n'
driver_dict_content = driver_dict_content[: -2]

passenger_dict_content = ""
for passenger_hash, passenger_id in passenger_dict.items():
    passenger_dict_content += '    "' + passenger_hash + '":"' +  passenger_id + '",\n'
passenger_dict_content = passenger_dict_content[: -2]



output = 'order_map = {\n' + order_dict_content + '\n}\n\n'
output += 'driver_map = {\n' + driver_dict_content + '\n}\n\n'
output += 'passenger_map = {\n' + passenger_dict_content + '\n}\n'
output += """
def get_order_id(hash):
    return order_map[hash]

def get_driver_id(hash):
    return driver_map[hash]

def get_passenger_id(hash):
    return passenger_map[hash]
"""

output_path = './order_driver_passenger_mapping.py'
with open(output_path, 'w') as f:
    f.write(output)

print("a number of orders", order_run_no - 1)
print("a number of drivers", driver_run_no - 1)
print("a number of passengers", passenger_run_no - 1)
