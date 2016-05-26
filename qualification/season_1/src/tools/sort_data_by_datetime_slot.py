import os

processed_data_folder = '../../processed_data'

for dataset in ['training_data', 'test_set_1']:
    order_folder = '../../cleansed_data/' + dataset + '/order_data'
    processed_order_folder = processed_data_folder + '/' + dataset + '/order_data'

    if not os.path.exists(processed_order_folder):
        os.makedirs(processed_order_folder)

    for file_name in os.listdir(order_folder):
        rows = []
        input_file = order_folder + '/' + file_name
        with open(input_file, 'r') as f:
            for line in f.readlines():
                rows.append(line.strip().split())
        rows.sort(key = lambda x: x[6]) # column 6 is datetime_slot
        output_file = processed_order_folder + '/sorted_' + file_name
        with open(output_file, 'w') as f:
            for row in rows:
                formatted_line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                f.write(formatted_line)
