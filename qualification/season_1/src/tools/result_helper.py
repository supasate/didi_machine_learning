import os
from datetime import datetime

def save_result(save_folder, model_name, metadata_list, prediction_list):
    if len(metadata_list) != len(prediction_list):
        print("Size of metadata_list and predictions does not match")
        return False

    # Create folder if not exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Append timestamp to file name
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = 'result_' + model_name + '_' + current_time + '.csv'
    file_path = os.path.join(save_folder, file_name)

    with open(file_path, 'w') as f:
        for i in range(len(metadata_list)):
            f.write("%s,%s,%s\n" % (metadata_list[i][0], metadata_list[i][1], prediction_list[i]))
