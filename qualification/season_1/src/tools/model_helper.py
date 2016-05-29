import os
from datetime import datetime
from sklearn.externals import joblib

def save_model(model_object, save_folder, model_name):
    # Create folder if not exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Append timestamp to file name
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = model_name + '_' + current_time + '.pkl'
    file_path = os.path.join(save_folder, file_name)

    # Save model
    joblib.dump(model_object, file_path)

def load_model(file_path):
    return joblib.load(file_path)

# Usage:
# load_latest_model('./model', 'svm_model')
# will look for file name 'svm_model*.pkl' in ./model folder
def load_latest_model(lookup_folder, model_name):
    # Lookup for file name containing model_name
    files = []
    for file_name in os.listdir(lookup_folder):
        # file_name is not a folder
        # and has .pkl extension
        # and contains model_name as part of file name
        if (
            (os.path.isfile(os.path.join(lookup_folder,file_name))) and
            (file_name[-4:] == '.pkl') and
            (model_name in file_name)
            ):

            files.append(file_name)
    # No file matches
    if len(files) == 0:
        return None

    # Get lastest filename by timestamp
    files.sort()
    latest_file = files[-1]

    # Load model
    return load_model(os.path.join(lookup_folder, latest_file))
