# Load and split into metadata, features, target lists
def load_and_split_data(file_path):
    metadata_list = []
    features_list = []
    target_list = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if line[0] == '#':
                continue
            district_id, date, timeslot, day_of_week, weather_t1, celsius_t1, pm25_t1, weather_t2, celsius_t2, pm25_t2, tf_lv1_t1, tf_lv2_t1, tf_lv3_t1, tf_lv4_t1, tf_lv1_t2, tf_lv2_t2, tf_lv3_t2, tf_lv4_t2, demand_t1, supply_t1, gap_t1, demand_t2, supply_t2, gap_t2, poi1, poi2, poi3, poi4, poi5, poi6, poi7, poi8, poi9, poi10, poi11, poi12, poi13, poi14, poi15, poi16, poi17, poi18, poi19, poi20, poi21, poi22, poi23, poi24, poi25, gap = line.strip().split()
            metadata_list.append([district_id, date + '-' + timeslot])
            features_list.append([
                int(district_id), int(timeslot), int(day_of_week),
                int(weather_t1), float(celsius_t1), float(pm25_t1),
                int(weather_t2), float(celsius_t2), float(pm25_t2),
                int(tf_lv1_t1), int(tf_lv2_t1), int(tf_lv3_t1), int(tf_lv4_t1),
                int(tf_lv1_t2), int(tf_lv2_t2), int(tf_lv3_t2), int(tf_lv4_t2),
                int(demand_t1), int(supply_t1), int(gap_t1),
                int(demand_t2), int(supply_t2), int(gap_t2),
                int(poi1), int(poi2), int(poi3), int(poi4), int(poi5),
                int(poi6), int(poi7), int(poi8), int(poi9), int(poi10),
                int(poi11), int(poi12), int(poi13), int(poi14), int(poi15),
                int(poi16), int(poi17), int(poi18), int(poi19), int(poi20),
                int(poi21), int(poi22), int(poi23), int(poi24), int(poi25)])
            if gap == 'PREDICT':
                gap = 0
            target_list.append(int(gap))
    return metadata_list, features_list, target_list
