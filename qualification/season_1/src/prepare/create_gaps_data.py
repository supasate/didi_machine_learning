import os
from time import time
from collections import defaultdict
from day_of_week import get_day_of_week

# Count supply, demand, gap from an order data file
def count_demand_supply_gap(input_path):
    # initialize counter of supply, demand, gap
    counter = {'gap': {}, 'demand': {}, 'supply': {}}
    for district_id in range(1, 67):
        counter['gap'][str(district_id)] = defaultdict(int)
        counter['demand'][str(district_id)] = defaultdict(int)
        counter['supply'][str(district_id)] = defaultdict(int)

    # Counting supply, demand, and gap
    with open(input_path, 'r') as f:
        for line in f.readlines():
            # Split each field from the file
            order_id, driver_id, passenger_id, start_district_id, dest_district_id, price, datetime_slot = line.strip().split()
            counter['demand'][start_district_id][datetime_slot] += 1

            if driver_id == 'NULL':
                counter['gap'][start_district_id][datetime_slot] += 1
            else:
                counter['supply'][start_district_id][datetime_slot] += 1
    return counter

# Save counting into a file sorted by district_id and datetime_slot
def save_couting(output_path, counter_dict):
    with open(output_path, 'w') as f:
        f.write("# district_id\tdatetime_slot\tday_of_week\tdemand\tsupply\tgap\n")

        # Sort gap count by district_id first
        sorted_gaps_count = sorted(counter_dict['gap'].items(), key = lambda x: x[0])
        for gap in sorted_gaps_count:
            district_id = gap[0]
            datetime_slot_gaps_count = gap[1]
            # Then, sort by slot (part of datetime_slot)
            sorted_datetime_slot_gaps_count = sorted(datetime_slot_gaps_count.items(), key = lambda x: int(x[0].split('-')[3]))
            for datetime_slot_gap in sorted_datetime_slot_gaps_count:
                datetime_slot = datetime_slot_gap[0]
                day_of_week = get_day_of_week(datetime_slot)
                gap_count = datetime_slot_gap[1]
                demand_count = counter_dict['demand'][district_id][datetime_slot]
                supply_count = counter_dict['supply'][district_id][datetime_slot]
                f.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (district_id, datetime_slot, day_of_week, demand_count, supply_count, gap_count))

if __name__ == "__main__":
    t0 = time()

    OUTPUT_FOLDER_PREFIX = '../../processed_data/gaps_data/'

    for dataset in ['training_data', 'test_set_1']:
        OUTPUT_FOLDER = OUTPUT_FOLDER_PREFIX + dataset

        # Create folder if not exist
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        # Each file represents orders in each da
        ORDER_DATA_FOLDER = '../../cleansed_data/' + dataset + '/order_data'

        for file_name in os.listdir(ORDER_DATA_FOLDER):
            # Get counter of supply, demand, gap
            input_path = ORDER_DATA_FOLDER + '/' + file_name
            counter = count_demand_supply_gap(input_path)

            # Save couting into a file
            output_path = OUTPUT_FOLDER + '/gaps_' + file_name
            save_couting(output_path, counter)
    print("Creating gaps data time:", round(time() - t0, 3), "s")
