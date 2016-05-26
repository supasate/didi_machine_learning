import os
from time_slot_mapping import get_datetime_slot

for dataset in ['training_data', 'test_set_1']:
    weather_folder = '../../' + dataset + '/weather_data'
    cleansed_weather_folder = '../../cleansed_data/' + dataset + '/weather_data'

    if not os.path.exists(cleansed_weather_folder):
        os.makedirs(cleansed_weather_folder)

    for file_name in os.listdir(weather_folder):
        output = ""
        input_file = weather_folder + '/' + file_name
        with open(input_file, 'r') as f:
            for line in f.readlines():
                date, time, weather, temperature, pm = line.strip().split()
                formatted_line = "%s %s %s %s\n" % (get_datetime_slot(date + ' ' + time, 10), weather, temperature, pm)
                output += formatted_line
        output = output[:-1]
        output_file = cleansed_weather_folder + '/' + file_name
        with open(output_file, 'w') as f:
            f.write(output)
