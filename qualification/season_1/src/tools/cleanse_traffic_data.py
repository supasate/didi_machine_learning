import os
from time_slot_mapping import get_datetime_slot
from district_mapping import get_district_id

for dataset in ['training_data', 'test_set_1']:
    traffic_folder = '../../' + dataset + '/traffic_data'
    cleansed_traffic_folder = '../../cleansed_data/' + dataset + '/traffic_data'

    if not os.path.exists(cleansed_traffic_folder):
        os.makedirs(cleansed_traffic_folder)

    for file_name in os.listdir(traffic_folder):
        output = ""
        input_file = traffic_folder + '/' + file_name
        with open(input_file, 'r') as f:
            for line in f.readlines():
                first_space_index = line.strip().find('\t')
                district_id = get_district_id(line[: first_space_index])

                second_space_index_from_last = line.strip().rfind('\t')
                datetime = line[second_space_index_from_last + 1:]
                datetimeslot = get_datetime_slot(datetime, 10)

                formatted_line = district_id + line[first_space_index: second_space_index_from_last + 1] + datetimeslot + '\n'
                output += formatted_line
        output = output[:-1]
        output_file = cleansed_traffic_folder + '/' + file_name
        with open(output_file, 'w') as f:
            f.write(output)
