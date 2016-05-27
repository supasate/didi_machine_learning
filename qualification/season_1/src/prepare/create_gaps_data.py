import os
from collections import defaultdict
from day_of_week import get_day_of_week

processed_data_folder = '../../processed_data'

for dataset in ['training_data', 'test_set_1']:
    order_folder = '../../cleansed_data/' + dataset + '/order_data'
    gaps_folder = processed_data_folder + '/gaps_data/' + dataset

    if not os.path.exists(gaps_folder):
        os.makedirs(gaps_folder)

    for file_name in os.listdir(order_folder):
        gaps_count = dict()
        for district_id in range(1, 67):
            gaps_count[str(district_id)] = defaultdict(int)

        input_file = order_folder + '/' + file_name
        with open(input_file, 'r') as f:
            for line in f.readlines():
                order_id, driver_id, passenger_id, start_district_id, dest_district_id, price, timeslot = line.strip().split()
                if timeslot not in gaps_count[start_district_id]:
                    gaps_count[start_district_id][timeslot] = 0

                if driver_id == 'NULL':
                    gaps_count[start_district_id][timeslot] += 1

        sorted_gaps_count = sorted(gaps_count.items(), key = lambda x: x[0])
        output_file = gaps_folder + '/gaps_' + file_name
        with open(output_file, 'w') as f:
            f.write("#district_id\tdatetime_slot\tday_of_week\tgaps\n")
            for gap in sorted_gaps_count:
                district_id = gap[0]
                timeslot_gaps_count = gap[1]
                sorted_timeslot_gaps_count = sorted(timeslot_gaps_count.items(), key = lambda x: int(x[0].split('-')[3]))
                for timeslot_gap in sorted_timeslot_gaps_count:
                    timeslot = timeslot_gap[0]
                    day_of_week = get_day_of_week(timeslot)
                    count = timeslot_gap[1]
                    f.write("%s\t%s\t%s\t%s\n" % (district_id, timeslot, day_of_week, count))
