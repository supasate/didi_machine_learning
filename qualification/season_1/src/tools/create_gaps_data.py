import os
from collections import defaultdict
from day_of_week import get_day_of_week

processed_data_folder = '../../processed_data'

for dataset in ['training_data', 'test_set_1']:
    order_folder = '../../cleansed_data/' + dataset + '/order_data'
    gaps_folder = processed_data_folder + '/' + dataset + '/gaps_data'

    if not os.path.exists(gaps_folder):
        os.makedirs(gaps_folder)

    for file_name in os.listdir(order_folder):
        gaps_count = defaultdict(int)
        input_file = order_folder + '/' + file_name
        with open(input_file, 'r') as f:
            for line in f.readlines():
                order_id, driver_id, passenger_id, start_id, dest_id, price, timeslot = line.strip().split()
                if timeslot not in gaps_count:
                    gaps_count[timeslot] = 0

                if driver_id == 'NULL':
                    gaps_count[timeslot] += 1
        sorted_gaps_count = sorted(gaps_count.items(), key = lambda x: int(x[0].split('-')[3]))

        output_file = gaps_folder + '/' + file_name
        with open(output_file, 'w') as f:
            for gap in sorted_gaps_count:
                f.write("%s\t%s\t%s\t\n" % (gap[0], get_day_of_week(gap[0]), gap[1]))
