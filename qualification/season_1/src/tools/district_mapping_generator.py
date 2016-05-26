cluster_map_path = '../../training_data/cluster_map/cluster_map'
dict_content = ""
with open(cluster_map_path, 'r') as f:
    for line in f.readlines():
        district_hash, district_id = line.strip().split()
        formatted_line = '    "' + district_hash + '" : "' + district_id + '",\n'
        dict_content += formatted_line
dict_content = dict_content[:-2]

output = 'district_map = {\n' + dict_content + '\n}\n'
output += """
def get_district_id(hash):
    return district_map[hash]
"""

output_path = './district_mapping.py'
with open(output_path, 'w') as f:
    f.write(output)
