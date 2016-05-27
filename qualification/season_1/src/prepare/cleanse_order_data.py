import os
from order_driver_passenger_mapping import get_order_id
from order_driver_passenger_mapping import get_driver_id
from order_driver_passenger_mapping import get_passenger_id
from district_mapping import get_district_id
from time_slot_mapping import get_datetime_slot

for dataset in ['training_data', 'test_set_1']:
    order_folder = '../../' + dataset + '/order_data'
    cleansed_order_folder = '../../cleansed_data/' + dataset + '/order_data'

    if not os.path.exists(cleansed_order_folder):
        os.makedirs(cleansed_order_folder)

    for file_name in os.listdir(order_folder):
        output = ""
        input_file = order_folder + '/' + file_name
        with open(input_file, 'r') as f:
            for line in f.readlines():
                order_hash, driver_hash, passenger_hash, start_district_hash, dest_district_hash, price, date, time = line.strip().split()
                order_id = get_order_id(order_hash)
                driver_id = get_driver_id(driver_hash) if driver_hash != 'NULL' else 'NULL'
                passenger_id = get_passenger_id(passenger_hash) if passenger_hash != 'NULL' else 'NULL'
                start_district_id = get_district_id(start_district_hash)
                dest_district_id = get_district_id(dest_district_hash)
                datetime_slot = get_datetime_slot(date + ' ' + time, 10)

                formatted_line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (order_id, driver_id, passenger_id, start_district_id, dest_district_id, price, datetime_slot)
                output += formatted_line
        output = output[:-1]
        output_file = cleansed_order_folder + '/' + file_name
        with open(output_file, 'w') as f:
            f.write(output)
