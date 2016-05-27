import os

def load_weather_data(weather_folder_path):
    weathers_map = dict()

    for file_name in os.listdir(weather_folder_path):
        input_file = weather_folder_path + '/' + file_name

        with open(input_file, 'r') as f:
            for line in f.readlines():
                datetime_slot, weather, celsius, pm25 = line.strip().split()
                weathers_map[datetime_slot] = {
                    'weather': weather,
                    'celsius': celsius,
                    'pm25': pm25
                }

    return weathers_map

def load_traffic_data(traffic_folder_path):
    traffic_map = dict()

    for file_name in os.listdir(traffic_folder_path):
        input_file = traffic_folder_path + '/' + file_name

        with open(input_file, 'r') as f:
            for line in f.readlines():
                district_id, level1, level2, level3, level4, datetime_slot = line.strip().split()
                if datetime_slot not in traffic_map:
                    traffic_map[datetime_slot] = dict()
                traffic_map[datetime_slot][district_id] = {
                    'tf_lv1': level1.split(':')[1],
                    'tf_lv2': level2.split(':')[1],
                    'tf_lv3': level3.split(':')[1],
                    'tf_lv4': level4.split(':')[1]
                }

    return traffic_map

def load_gaps_data(gaps_folder_path):
    gaps_map = dict()

    for file_name in os.listdir(gaps_folder_path):
        input_file = gaps_folder_path + '/' + file_name

        with open(input_file, 'r') as f:
            for line in f.readlines():
                if line[0] == '#':
                    continue

                district_id, datetime_slot, day_of_week, gap = line.strip().split()
                if datetime_slot not in gaps_map:
                    gaps_map[datetime_slot] = dict()
                year, month, day, time_slot = datetime_slot.split('-')
                date = year + '-' + month + '-' + day
                gaps_map[datetime_slot][district_id] = {
                    'date': date,
                    'time_slot': time_slot,
                    'day_of_week': day_of_week,
                    'gap': gap
                }

    for datetime_slot, district_dict in gaps_map.items():
        for district_id, features in district_dict.items():
            year, month, day, time_slot = datetime_slot.split('-')
            previous_slot = '-'.join([year, month, day, str(int(time_slot) - 1)])
            previous_previous_slot = '-'.join([year, month, day, str(int(time_slot) - 2)])
            if (previous_slot in gaps_map) and (district_id in gaps_map[previous_slot]):
                gaps_map[datetime_slot][district_id]['gap_t-1'] = gaps_map[previous_slot][district_id]['gap']
            else:
                gaps_map[datetime_slot][district_id]['gap_t-1'] = '0'

            if (previous_previous_slot in gaps_map) and (district_id in gaps_map[previous_previous_slot]):
                gaps_map[datetime_slot][district_id]['gap_t-2'] = gaps_map[previous_previous_slot][district_id]['gap']
            else:
                gaps_map[datetime_slot][district_id]['gap_t-2'] = '0'

    return gaps_map

cleansed_folder = '../../cleansed_data'
processed_folder = '../../processed_data'

for dataset in ['training_data', 'test_set_1']:

    # Load weather data
    weathers_folder = cleansed_folder + '/' + dataset + '/weather_data'
    weathers_map = load_weather_data(weathers_folder)

    # Load traffic data
    traffic_folder = cleansed_folder + '/' + dataset + '/traffic_data'
    traffic_map = load_traffic_data(traffic_folder)

    # Load gaps data
    gaps_folder = processed_folder + '/gaps_data/' + dataset
    gaps_map = load_gaps_data(gaps_folder)

    # Output file and folder
    features_folder = processed_folder + '/features_data/' + dataset
    features_file = features_folder + '/features_ready'

    if not os.path.exists(features_folder):
        os.makedirs(features_folder)

    with open(features_file, 'w') as f:
        f.write('#district_id\ttimeslot\tday_of_week\tweather\tcelsius\tpm25\ttf_lv1\ttf_lv2\ttf_lv3\ttf_lv4\tgap_t-1\tgap_t-2\tgap\n')

        for datetime_slot, district_dict in gaps_map.items():
            for district_id, features in district_dict.items():
                if datetime_slot in weathers_map:
                    weather = weathers_map[datetime_slot]['weather']
                    celsius = weathers_map[datetime_slot]['celsius']
                    pm25 = weathers_map[datetime_slot]['pm25']
                else:
                    weather = 'NULL'
                    celsius = 'NULL'
                    pm25 = 'NULL'

                if (datetime_slot in traffic_map) and (district_id in traffic_map[datetime_slot]):
                    tf_lv1 = traffic_map[datetime_slot][district_id]['tf_lv1']
                    tf_lv2 = traffic_map[datetime_slot][district_id]['tf_lv2']
                    tf_lv3 = traffic_map[datetime_slot][district_id]['tf_lv3']
                    tf_lv4 = traffic_map[datetime_slot][district_id]['tf_lv4']
                else:
                    tf_lv1 = 'NULL'
                    tf_lv2 = 'NULL'
                    tf_lv3 = 'NULL'
                    tf_lv4 = 'NULL'

                f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                    district_id,
                    features['time_slot'],
                    features['day_of_week'],
                    weather,
                    celsius,
                    pm25,
                    tf_lv1,
                    tf_lv2,
                    tf_lv3,
                    tf_lv4,
                    features['gap_t-1'],
                    features['gap_t-2'],
                    features['gap']
                ))
