import os
import sys
from time import time
from day_of_week import get_day_of_week

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

                if district_id not in gap_map:
                    gap_map[district_id] = dict()

                year, month, day, time_slot = datetime_slot.split('-')
                date = year + '-' + month + '-' + day
                gap_map[district_id][datetime_slot] = {
                    'date': date,
                    'time_slot': time_slot,
                    'day_of_week': day_of_week,
                    'demand': demand,
                    'supply': supply,
                    'gap': gap
                }

    # Append data at previous time slot and previous of previous time slot
    for district_id, datetime_slot_dict in gap_map.items():
        for datetime_slot, features in datetime_slot_dict.items():
            previous_datetime_slot = get_previous_datetime_slot(datetime_slot, 1)
            previous_of_previous_datetime_slot = get_previous_datetime_slot(datetime_slot, 2)

            if (district_id in gap_map) and (previous_datetime_slot in gap_map[district_id]):
                gap_map[district_id][datetime_slot]['demand_t-1'] = gap_map[district_id][previous_datetime_slot]['demand']
                gap_map[district_id][datetime_slot]['supply_t-1'] = gap_map[district_id][previous_datetime_slot]['supply']
                gap_map[district_id][datetime_slot]['gap_t-1'] = gap_map[district_id][previous_datetime_slot]['gap']
            else:
                gap_map[district_id][datetime_slot]['demand_t-1'] = '0'
                gap_map[district_id][datetime_slot]['supply_t-1'] = '0'
                gap_map[district_id][datetime_slot]['gap_t-1'] = '0'

            if (district_id in gap_map) and (previous_of_previous_datetime_slot in gap_map[district_id]):
                gap_map[district_id][datetime_slot]['demand_t-2'] = gap_map[district_id][previous_of_previous_datetime_slot]['demand']
                gap_map[district_id][datetime_slot]['supply_t-2'] = gap_map[district_id][previous_of_previous_datetime_slot]['supply']
                gap_map[district_id][datetime_slot]['gap_t-2'] = gap_map[district_id][previous_of_previous_datetime_slot]['gap']
            else:
                gap_map[district_id][datetime_slot]['demand_t-2'] = '0'
                gap_map[district_id][datetime_slot]['supply_t-2'] = '0'
                gap_map[district_id][datetime_slot]['gap_t-2'] = '0'

    return gap_map

def split_date_and_timeslot(datetime_slot):
    year, month, day, timeslot = datetime_slot.split('-')
    date = '-'.join([year, month, day])

    return date, timeslot

def get_nearest_weather(datetime_slot, weather_map, slot_distance_limit):
    date, timeslot = split_date_and_timeslot(datetime_slot)
    timeslot_countdown = int(timeslot)
    timeslot_countup = int(timeslot)

    if slot_distance_limit == None:
        slot_distance_limit = sys.maxint

    while (timeslot_countdown >= 1 or timeslot_countup <= 144) and slot_distance_limit >= 0:
        cur_datetime_slot = '-'.join([date, str(timeslot_countdown)])
        if cur_datetime_slot in weather_map:
            return weather_map[cur_datetime_slot]

        cur_datetime_slot = '-'.join([date, str(timeslot_countup)])
        if cur_datetime_slot in weather_map:
            return weather_map[cur_datetime_slot]

        timeslot_countdown -= 1
        timeslot_countup += 1
        slot_distance_limit -= 1

    return None

def get_nearest_traffic_level(datetime_slot, district_id, traffic_map, slot_distance_limit):
    date, timeslot = split_date_and_timeslot(datetime_slot)
    timeslot = int(timeslot)

    if slot_distance_limit == None:
        slot_distance_limit = sys.maxint

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

    if slot_distance_limit == None:
        slot_distance_limit = sys.maxint

    while timeslot >= 1 and slot_distance_limit >= 0:
        cur_datetime_slot = '-'.join([date, str(timeslot)])
        if (district_id in gap_map) and (cur_datetime_slot in gap_map[district_id]):
            return gap_map[district_id][cur_datetime_slot]
        timeslot -= 1
        slot_distance_limit -= 1

    return None

def save_features(output_path, gap_map, weather_map, traffic_map):
    incomplete_data_count = 0

    with open(output_path, 'w') as f:
        f.write('# district_id\tdate\ttimeslot\tday_of_week\tweather_t-1\tcelsius_t-1\tpm25_t-1\tweather_t-2\tcelsius_t-2\tpm25_t-2\ttf_lv1_t-1\ttf_lv2_t-1\ttf_lv3_t-1\ttf_lv4_t-1\ttf_lv1_t-2\ttf_lv2_t-2\ttf_lv3_t-2\ttf_lv4_t-2\tdemand_t-1\tsupply_t-1\tgap_t-1\tdemand_t-2\tsupply_t-2\tgap_t-2\tgap\n')

        # Sort output by district_id first
        gap_map_sorted_by_district_id = sorted(gap_map.items(), key = lambda x: int(x[0]))

        for item in gap_map_sorted_by_district_id:
            district_id = item[0]
            datetime_slot_features_map = item[1]

            # Then, sort output by datetime, then by slot
            sorted_features_map_by_datetime_slot = sorted(datetime_slot_features_map.items(), key = lambda x: (x[0][: x[0].rfind('-')], int(x[0].split('-')[3])))
            for sub_item in sorted_features_map_by_datetime_slot:
                datetime_slot = sub_item[0]
                features = sub_item[1]

                # Ignore new year data
                if "2016-01-01" in datetime_slot:
                    continue

                # If slot is less than 3, it doesn't have 2 previous slots info, ignore it
                if datetime_slot[-2:] in ['-1', '-2']:
                    incomplete_data_count += 1
                    continue

                previous_datetime_slot = get_previous_datetime_slot(datetime_slot, 1)
                previous_of_previous_datetime_slot = get_previous_datetime_slot(datetime_slot, 2)

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
                if gap_t1 == None:
                    gap_t1 = {'demand': 0, 'supply': 0, 'gap': 0}
                if gap_t2 == None:
                    gap_t2 = {'demand': 0, 'supply': 0, 'gap': 0}

                # Ignore incomplete data point
                if gap == None or weather_t1 == None or tf_lv_t1 == None:
                    incomplete_data_count += 1
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
    print("number of incomplete data", incomplete_data_count)

def load_datetime_slot_to_predict(file_path):
    datetime_slot_list = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            datetime_slot_list.append(line.strip())
    return datetime_slot_list

def save_features_to_predict(output_path, datetime_slot_to_predict_file_path, gap_map, weather_map, traffic_map):

    incomplete_data_count = 0
    datetime_slot_to_predict_list = load_datetime_slot_to_predict(datetime_slot_to_predict_file_path)

    with open(output_path, 'w') as f:
        f.write('# district_id\tdate\ttimeslot\tday_of_week\tweather_t-1\tcelsius_t-1\tpm25_t-1\tweather_t-2\tcelsius_t-2\tpm25_t-2\ttf_lv1_t-1\ttf_lv2_t-1\ttf_lv3_t-1\ttf_lv4_t-1\ttf_lv1_t-2\ttf_lv2_t-2\ttf_lv3_t-2\ttf_lv4_t-2\tdemand_t-1\tsupply_t-1\tgap_t-1\tdemand_t-2\tsupply_t-2\tgap_t-2\tgap\n')

        for district_id_int in range(1, 67):
            for datetime_slot in datetime_slot_to_predict_list:
                district_id = str(district_id_int)

                year, month, day, time_slot = datetime_slot.split('-')
                date = '-'.join([year, month, day])
                day_of_week = get_day_of_week(datetime_slot)

                previous_datetime_slot = get_previous_datetime_slot(datetime_slot, 1)
                previous_of_previous_datetime_slot = get_previous_datetime_slot(datetime_slot, 2)

                # Get weather of 2 previous slots (or nearest if there is no data)
                WEATHER_SLOT_DISTANCE_LIMIT = None # 90 minutes
                weather_t1 = get_nearest_weather(previous_datetime_slot, weather_map, WEATHER_SLOT_DISTANCE_LIMIT)
                weather_t2 = get_nearest_weather(previous_of_previous_datetime_slot, weather_map, WEATHER_SLOT_DISTANCE_LIMIT)
                if weather_t2 == None:
                    weather_t2 = weather_t1

                # Get traffic of 2 previous slots (or nearest if there is no data)
                TRAFFIC_SLOT_DISTANCE_LIMIT = None # 30 minutes
                tf_lv_t1 = get_nearest_traffic_level(previous_datetime_slot, district_id, traffic_map, TRAFFIC_SLOT_DISTANCE_LIMIT)
                tf_lv_t2 = get_nearest_traffic_level(previous_of_previous_datetime_slot, district_id, traffic_map, TRAFFIC_SLOT_DISTANCE_LIMIT)
                if tf_lv_t2 == None:
                    tf_lv_t2 = tf_lv_t1

                # Get demand, supply, gap of 2 previous slots (or nearest if there is no data)
                DEMAND_SUPPLY_GAP_DISTANCE_LIMIT = None # 30 minutes
                gap_t1 = get_nearest_demand_supply_gap(previous_datetime_slot, district_id, gap_map, DEMAND_SUPPLY_GAP_DISTANCE_LIMIT)
                gap_t2 = get_nearest_demand_supply_gap(previous_of_previous_datetime_slot, district_id, gap_map, DEMAND_SUPPLY_GAP_DISTANCE_LIMIT)
                if gap_t1 == None:
                    gap_t1 = {'demand': 0, 'supply': 0, 'gap': 0}
                if gap_t2 == None:
                    gap_t2 = {'demand': 0, 'supply': 0, 'gap': 0}

                gap = 'PREDICT'

                # Ignore incomplete data point
                if weather_t1 == None or tf_lv_t1 == None:
                    incomplete_data_count += 1
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
    print("features_to_predict: incomplete_data_count", incomplete_data_count)

if __name__ == '__main__':
    # Show processing time
    start_time = time()

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

        if dataset == 'test_set_1':
            PREDICTION_DATA_FOLDER = '../../processed_data/prediction_data'
            features_to_predict_file = PREDICTION_DATA_FOLDER + '/to_predict_features'
            datetime_slot_for_prediction_file = PREDICTION_DATA_FOLDER + '/datetime_for_prediction.txt'

            save_features_to_predict(features_to_predict_file, datetime_slot_for_prediction_file, gap_map, weather_map, traffic_map)
    print("Creating features data time", round(time() - start_time, 3), "s")
