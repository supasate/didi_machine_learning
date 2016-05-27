import os

district_dict = dict()

for dataset in ['training_data', 'test_set_1']:
    cluster_folder = '../../' + dataset + '/cluster_map'
    for file_name in os.listdir(cluster_folder):
        input_file = cluster_folder + '/' + file_name
        with open(input_file, 'r') as f:
            for line in f.readlines():
                district_hash, district_id = line.strip().split()
                if district_hash not in district_dict:
                    district_dict[district_hash] = district_id

district_dict_content = ''
for district_hash, district_id in district_dict.items():
    district_dict_content += '    "' + district_hash + '":"' +  district_id + '",\n'
district_dict_content = district_dict_content[:-2]

output = 'district_map = {\n' + district_dict_content + '\n}\n'
output += """
def get_district_id(hash):
    return district_map[hash] if hash in district_map else hash
"""

output_path = './district_mapping.py'
with open(output_path, 'w') as f:
    f.write(output)
