import os
import json
from district_mapping import district_map

district_cnt = max([int(i) for i in district_map.values()]) + 1
price_dict = [[0 for x in range(district_cnt)] for y in range(district_cnt)] 

for dataset in ['training_data']:
    order_folder = '../../' + dataset + '/order_data'
    for file_name in os.listdir(order_folder):
        input_file = order_folder + '/' + file_name
        with open(input_file, 'r') as f:
            for line in f.readlines():
                order_id, driver_id, passenger_id, start_district_id, dest_district_id, price, slot = line.strip().split()
                if dest_district_id.isdigit():
                    price_dict[int(start_district_id)][int(dest_district_id)] = price

price_map = json.dumps(price_dict)

output = 'price_map = ' + price_map
output += '\n'
output += """
def get_avg_price(start_district_id, dest_district_id):
    return price_map[start_district_id][dest_district_id]
"""

output_path = './order_data_avg_price_mapping.py'
with open(output_path, 'w') as f:
    f.write(output)

