import os
from district_mapping import get_district_id

for dataset in ['training_data', 'test_set_1']:
    poi_folder = '../../' + dataset + '/poi_data'
    cleansed_poi_folder = '../../cleansed_data/' + dataset + '/poi_data'

    if not os.path.exists( cleansed_poi_folder):
        os.makedirs( cleansed_poi_folder)

    for file_name in os.listdir(poi_folder):
        output = ""
        input_file = poi_folder + '/' + file_name
        with open(input_file, 'r') as f:
            for line in f.readlines():
                first_space_index = line.strip().find('\t')
                district_id = get_district_id(line[: first_space_index])

                formatted_line = district_id + line[first_space_index: ]
                output += formatted_line
        output = output[:-1]
        output_file = cleansed_poi_folder + '/' + file_name
        with open(output_file, 'w') as f:
            f.write(output)
