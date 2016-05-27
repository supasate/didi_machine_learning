def load_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if line[0] == '#':
                continue
            district_id, timeslot, day_of_week, weather, celsius, pm25, tf_lv1, tf_lv2, tf_lv3, tf_lv4, gap_t1, gap_t2, gap = line.strip().split()
            data.append([int(district_id), int(timeslot), int(day_of_week), int(weather), float(celsius), float(pm25), int(tf_lv1), int(tf_lv2), int(tf_lv3), int(tf_lv4), int(gap_t1), int(gap_t2), int(gap)])
    return data

def target_feature_split(data):
    target = []
    features = []
    for item in data:
        target.append(item[len(item) - 1])
        features.append(item[: -1])

    return target, features
