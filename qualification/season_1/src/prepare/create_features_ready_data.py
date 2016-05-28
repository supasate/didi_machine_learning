import os

# Return { datetime_slot: { 'weather': value, 'celsius': value, 'pm25': value } }
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

# Return { datetime_slot: { district_id: { 'tf_lv1': value, 'tf_lv2': value, 'tf_lv3': value, 'tf_lv4': value } } }
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

# Return previous datetime_slot in format yyyy-mm-dd-slot
def get_previous_datetime_slot(current_datetime_slot, num_previous_days):
    year, month, day, time_slot = current_datetime_slot.split('-')

    return '-'.join([year, month, day, str(int(time_slot) - num_previous_days)])

# Return { datetime_slot: { district_id: {
#   'date', 'time_slot', 'day_of_week',
#   'demand', 'demand_t-1', 'demand_t-2',
#   'supply', 'supply_t-1', 'supply_t-2',
#   'gap', 'gap_t-1', 'gap_t-2' } } }
def load_gap_data(gap_folder_path):
    gap_map = dict()

    # Retrive gap data from each input file
    for file_name in os.listdir(gap_folder_path):
        input_file = gap_folder_path + '/' + file_name

        with open(input_file, 'r') as f:
            for line in f.readlines():
                # Ignore comment lines
                if line[0] == '#':
                    continue

                district_id, datetime_slot, day_of_week, demand, supply, gap = line.strip().split()
                if datetime_slot not in gap_map:
                    gap_map[datetime_slot] = dict()
                year, month, day, time_slot = datetime_slot.split('-')
                date = year + '-' + month + '-' + day
                gap_map[datetime_slot][district_id] = {
                    'date': date,
                    'time_slot': time_slot,
                    'day_of_week': day_of_week,
                    'demand': demand,
                    'supply': supply,
                    'gap': gap
                }

    # Append data at previous time slot and previous of previous time slot
    for datetime_slot, district_dict in gap_map.items():
        for district_id, features in district_dict.items():
            previous_datetime_slot = get_previous_datetime_slot(datetime_slot, 1)
            previous_of_previous_datetime_slot = get_previous_datetime_slot(datetime_slot, 2)

            if (previous_datetime_slot in gap_map) and (district_id in gap_map[previous_datetime_slot]):
                gap_map[datetime_slot][district_id]['demand_t-1'] = gap_map[previous_datetime_slot][district_id]['demand']
                gap_map[datetime_slot][district_id]['supply_t-1'] = gap_map[previous_datetime_slot][district_id]['supply']
                gap_map[datetime_slot][district_id]['gap_t-1'] = gap_map[previous_datetime_slot][district_id]['gap']
            else:
                gap_map[datetime_slot][district_id]['demand_t-1'] = '0'
                gap_map[datetime_slot][district_id]['supply_t-1'] = '0'
                gap_map[datetime_slot][district_id]['gap_t-1'] = '0'

            if (previous_of_previous_datetime_slot in gap_map) and (district_id in gap_map[previous_of_previous_datetime_slot]):
                gap_map[datetime_slot][district_id]['demand_t-2'] = gap_map[previous_of_previous_datetime_slot][district_id]['demand']
                gap_map[datetime_slot][district_id]['supply_t-2'] = gap_map[previous_of_previous_datetime_slot][district_id]['supply']
                gap_map[datetime_slot][district_id]['gap_t-2'] = gap_map[previous_of_previous_datetime_slot][district_id]['gap']
            else:
                gap_map[datetime_slot][district_id]['demand_t-2'] = '0'
                gap_map[datetime_slot][district_id]['supply_t-2'] = '0'
                gap_map[datetime_slot][district_id]['gap_t-2'] = '0'

    return gap_map

def split_date_and_timeslot(datetime_slot):
    year, month, day, timeslot = datetime_slot.split('-')
    date = '-'.join([year, month, day])

    return date, timeslot

def get_nearest_weather(datetime_slot, weather_map, slot_distance_limit):
    date, timeslot = split_date_and_timeslot(datetime_slot)
    timeslot = int(timeslot)

    while timeslot >= 1 and slot_distance_limit >= 0:
        cur_datetime_slot = '-'.join([date, str(timeslot)])
        if cur_datetime_slot in weather_map:
            return weather_map[cur_datetime_slot]
        timeslot -= 1
        slot_distance_limit -= 1

    return None

def get_nearest_traffic_level(datetime_slot, district_id, traffic_map, slot_distance_limit):
    date, timeslot = split_date_and_timeslot(datetime_slot)
    timeslot = int(timeslot)

    while timeslot >= 1 and slot_distance_limit >= 0:
        cur_datetime_slot = '-'.join([date, str(timeslot)])
        if (cur_datetime_slot in traffic_map) and (district_id in traffic_map[cur_datetime_slot]):
            return traffic_map[cur_datetime_slot][district_id]
        timeslot -= 1
        slot_distance_limit -= 1

    return None

def get_nearest_demand_supply_gap(datetime_slot, district_id, gap_map, slot_distance_limit):
    date, timeslot = split_date_and_timeslot(datetime_slot)
    timeslot = int(timeslot)

    while timeslot >= 1 and slot_distance_limit >= 0:
        cur_datetime_slot = '-'.join([date, str(timeslot)])
        if (cur_datetime_slot in gap_map) and (district_id in gap_map[cur_datetime_slot]):
            return gap_map[cur_datetime_slot][district_id]
        timeslot -= 1
        slot_distance_limit -= 1

    return None

def save_features(output_path, gap_map, weather_map, traffic_map):
    with open(output_path, 'w') as f:
        f.write('# district_id\tdate\ttimeslot\tday_of_week\tweather_t-1\tcelsius_t-1\tpm25_t-1\tweather_t-2\tcelsius_t-2\tpm25_t-2\ttf_lv1_t-1\ttf_lv2_t-1\ttf_lv3_t-1\ttf_lv4_t-1\ttf_lv1_t-2\ttf_lv2_t-2\ttf_lv3_t-2\ttf_lv4_t-2\tdemand_t-1\tsupply_t-1\tgap_t-1\tdemand_t-2\tsupply_t-2\tgap_t-2\tgap\n')

        for datetime_slot, district_dict in gap_map.items():
            # There is no previous 2 slots for slot 1 and 2
            if datetime_slot[-2:] in ['-1', '-2']:
                continue

            previous_datetime_slot = get_previous_datetime_slot(datetime_slot, 1)
            previous_of_previous_datetime_slot = get_previous_datetime_slot(datetime_slot, 2)

            for district_id, features in district_dict.items():

                date = features['date']
                time_slot = features['time_slot']
                day_of_week = features['day_of_week']
                gap = features['gap'] if features['gap'] != 'NULL' else None

                # Get weather of 2 previous slots (or nearest if there is no data)
                WEATHER_SLOT_DISTANCE_LIMIT = 9 # 90 minutes
                weather_t1 = get_nearest_weather(previous_datetime_slot, weather_map, WEATHER_SLOT_DISTANCE_LIMIT)
                weather_t2 = get_nearest_weather(previous_of_previous_datetime_slot, weather_map, WEATHER_SLOT_DISTANCE_LIMIT)
                if weather_t2 == None:
                    weather_t2 = weather_t1


                # Get traffic of 2 previous slots (or nearest if there is no data)
                TRAFFIC_SLOT_DISTANCE_LIMIT = 3 # 30 minutes
                tf_lv_t1 = get_nearest_traffic_level(previous_datetime_slot, district_id, traffic_map, TRAFFIC_SLOT_DISTANCE_LIMIT)
                tf_lv_t2 = get_nearest_traffic_level(previous_of_previous_datetime_slot, district_id, traffic_map, TRAFFIC_SLOT_DISTANCE_LIMIT)
                if tf_lv_t2 == None:
                    tf_lv_t2 = tf_lv_t1

                # Get demand, supply, gap of 2 previous slots (or nearest if there is no data)
                DEMAND_SUPPLY_GAP_DISTANCE_LIMIT = 3 # 30 minutes
                gap_t1 = get_nearest_demand_supply_gap(previous_datetime_slot, district_id, gap_map, DEMAND_SUPPLY_GAP_DISTANCE_LIMIT)
                gap_t2 = get_nearest_demand_supply_gap(previous_of_previous_datetime_slot, district_id, gap_map, DEMAND_SUPPLY_GAP_DISTANCE_LIMIT)
                if gap_t2 == None:
                    gap_t2 = gap_t1

                # Ignore incomplete data point
                if gap == None or weather_t1 == None or tf_lv_t1 == None or gap_t1 == None:
                    continue

                f.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                    district_id,
                    date, time_slot, day_of_week,
                    weather_t1['weather'], weather_t1['celsius'], weather_t1['pm25'],
                    weather_t2['weather'], weather_t2['celsius'], weather_t2['pm25'],
                    tf_lv_t1['tf_lv1'], tf_lv_t1['tf_lv2'], tf_lv_t1['tf_lv3'], tf_lv_t1['tf_lv4'],
                    tf_lv_t2['tf_lv1'], tf_lv_t2['tf_lv2'], tf_lv_t2['tf_lv3'], tf_lv_t2['tf_lv4'],
                    gap_t1['demand'], gap_t1['supply'], gap_t1['gap'],
                    gap_t2['demand'], gap_t2['supply'], gap_t2['gap'],
                    gap
                ))

if __name__ == '__main__':
    OUTPUT_FOLDER_PREFIX = '../../processed_data/features_data/'
    CLEANSED_DATA_FOLDER = '../../cleansed_data'
    PROCESSED_DATA_FOLDER = '../../processed_data'

    for dataset in ['training_data', 'test_set_1']:
        # Load weather data
        weather_folder = CLEANSED_DATA_FOLDER + '/' + dataset + '/weather_data'
        weather_map = load_weather_data(weather_folder)

        # Load traffic data
        traffic_folder = CLEANSED_DATA_FOLDER + '/' + dataset + '/traffic_data'
        traffic_map = load_traffic_data(traffic_folder)

        # Load gaps data
        gap_folder = PROCESSED_DATA_FOLDER + '/gaps_data/' + dataset
        gap_map = load_gap_data(gap_folder)

        # Output file and folder
        features_folder = OUTPUT_FOLDER_PREFIX + dataset
        features_file = features_folder + '/features_ready'

        # Create output folder if it doesn't exist
        if not os.path.exists(features_folder):
            os.makedirs(features_folder)

        save_features(features_file, gap_map, weather_map, traffic_map)
